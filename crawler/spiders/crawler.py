import contextlib
import logging
import os
from typing import Optional
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse

import scrapy
import tldextract
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class BrowserSession:
    """Selenium 제어를 캡슐화해 스파이더가 단순히 HTML만 요청하도록 돕습니다."""

    def __init__(self, proxy_url: Optional[str] = None, wait_seconds: int = 10):
        self.proxy_url = proxy_url
        self.wait_seconds = wait_seconds
        self.driver = self._init_driver()
        self.wait = WebDriverWait(self.driver, self.wait_seconds)

    def _init_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        if self.proxy_url:
            chrome_options.add_argument(f"--proxy-server={self.proxy_url}")
            logging.info(f"Using proxy: {self.proxy_url}")

        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)

    def render(self, url: str) -> Optional[str]:
        """URL을 렌더링하고 동적 요소 클릭을 시도한 뒤 HTML을 반환합니다."""
        try:
            self.driver.get(url)
            self._trigger_js_events()
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            return self.driver.page_source
        except WebDriverException as exc:
            logging.error(f"Browser rendering error for {url}: {exc}")
            return None
        except Exception as exc:  # pylint: disable=broad-except
            logging.error(f"Unexpected error while rendering {url}: {exc}")
            return None

    def _trigger_js_events(self):
        """onclick 요소를 순회하며 간단한 사용자 상호작용을 시뮬레이션합니다."""
        self.driver.execute_script(
            """
            document.querySelectorAll('[onclick]').forEach((element) => {
                const href = element.getAttribute('href') || '';
                if (href.includes('logout.php')) { return; }
                try { element.click(); } catch (e) { /* ignore */ }
            });
            """
        )

    def close(self):
        with contextlib.suppress(Exception):
            self.driver.quit()


class MySpider(scrapy.Spider):
    name = "crawler"

    custom_settings = {
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": "2.7",
    }

    def __init__(self, start_url=None, proxy_url=None, cookies_file="cookie_header.txt", *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)

        if start_url:
            self.start_urls = [start_url]
        else:
            raise ValueError("No start URL provided")

        self.proxy_url = proxy_url if proxy_url else "http://127.0.0.1:8080"
        self.domain_origin = tldextract.extract(self.start_urls[0]).registered_domain
        self.output_file = "output.txt"
        self.seen_urls = set()

        self.cookies = self.load_cookies(cookies_file)
        self.browser = BrowserSession(self.proxy_url)

    def load_cookies(self, cookies_file):
        cookies = {}
        if not os.path.exists(cookies_file):
            logging.warning(f"Cookie file not found: {cookies_file}")
            return cookies

        with open(cookies_file, "r", encoding="utf-8") as f:
            for line in f:
                if "=" in line:
                    name, value = line.strip().split("=", 1)
                    cookies[name] = value
        logging.info(f"Loaded {len(cookies)} cookies from {cookies_file}")
        return cookies

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookies)

    def parse(self, response):
        try:
            normalized_url = self.normalize_url(response.url)

            if self._should_skip_response(response, normalized_url):
                return

            self._remember_url(normalized_url)

            for link in self.extract_links(response):
                yield scrapy.Request(url=link, callback=self.parse, cookies=self.cookies)

            # 동적 렌더링 결과 기반으로 추가 링크 확보
            logging.debug(f"Processing with Selenium for URL: {response.url}")
            updated_body = self.browser.render(response.url)
            if not updated_body:
                return

            updated_response = HtmlResponse(
                url=response.url,
                body=updated_body,
                encoding="utf-8",
                headers={"Content-Type": "text/html"},
            )

            for link in self.extract_links(updated_response):
                yield scrapy.Request(url=link, callback=self.parse, cookies=self.cookies)

        except Exception as e:  # pylint: disable=broad-except
            logging.error(f"Error detected in Function parse: {e}")

    def _should_skip_response(self, response, normalized_url):
        content_type = response.headers.get("Content-Type", b"").decode("utf-8", errors="ignore")
        logging.debug(f"Content-Type for {response.url}: {content_type}")

        if content_type and not content_type.startswith("text"):
            logging.debug(f"Skipped non-text content: {response.url}")
            return True

        if normalized_url in self.seen_urls:
            logging.debug(f"Skipping already seen URL: {normalized_url}")
            return True

        return False

    def _remember_url(self, normalized_url):
        self.seen_urls.add(normalized_url)
        with open(self.output_file, "a", encoding="utf-8") as f:
            f.write(f"{normalized_url}\n")
            f.flush()

    def extract_links(self, response):
        a_links = response.xpath("//a/@href").getall()
        logging.debug(f"Found {len(a_links)} links on {response.url}")

        for link in a_links:
            absolute = response.urljoin(link)
            normalized = self.normalize_url(absolute)

            if self._is_in_scope(normalized):
                logging.debug(f"Yielding request for: {normalized}")
                yield normalized

    def _is_in_scope(self, url):
        if url.endswith("logout.php"):
            return False

        domain = tldextract.extract(url).registered_domain
        if domain != self.domain_origin:
            return False

        if url in self.seen_urls:
            return False

        return True

    def normalize_url(self, url):
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        filtered_query = {k: v for k, v in query.items() if k not in ["random", "session", "timestamp"]}
        normalized_query = urlencode(filtered_query, doseq=True)

        normalized_url = urlunparse(
            (
                parsed_url.scheme,
                parsed_url.netloc,
                parsed_url.path,
                parsed_url.params,
                normalized_query,
                parsed_url.fragment,
            )
        )
        logging.debug(f"Normalized URL: {normalized_url}")
        return normalized_url

    def closed(self, reason):
        self.browser.close()


# scrapy runspider crawler.py -a start_url=http://localhost/DVWA/
