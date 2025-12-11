import scrapy
import logging
import tldextract
from scrapy.http import HtmlResponse
from seleniumwire import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs, urlunparse, urlencode
from webdriver_manager.chrome import ChromeDriverManager
import time

class MySpider(scrapy.Spider):
    name = 'crawler'
    
    custom_settings = {
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',  # 또는 'sha1'
    }

    def __init__(self, start_url=None, proxy_url=None, cookies_file='cookie_header.txt', *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)

        if start_url:
            self.start_urls = [start_url]
        else:
            raise ValueError("No start URL provided")

        self.proxy_url = proxy_url if proxy_url else 'http://127.0.0.1:8080'
        self.domain_origin = tldextract.extract(self.start_urls[0]).domain
        self.output_file = 'output.txt'
        self.seen_urls = set()

        # Load cookies from file
        self.cookies = self.load_cookies(cookies_file)

        chrome_options = Options()
        chrome_options.add_argument(f'--proxy-server={self.proxy_url}')
        logging.info(f'Using proxy: {self.proxy_url}')
        
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        capabilities['proxy'] = {
            "proxyType": ProxyType.MANUAL,
            "httpProxy": self.proxy_url,
            "sslProxy": self.proxy_url,
        }

        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=chrome_options)

# cookie_header.txt에서 쿠키 읽어옴
    def load_cookies(self, cookies_file):
        cookies = {}
        with open(cookies_file, 'r') as f:
            for line in f:
                if '=' in line:
                    name, value = line.strip().split('=', 1)
                    cookies[name] = value
        return cookies

# scrapy.Request 객체 생성 시 cookies 매개변수를 사용하여 쿠키를 포함시킴. 이 쿠키는 요청 헤더에 포함되어 서버가 틀라이언트를 인증하고 로그인 세션 유지할 수 있게 함
    def start_requests(self):
        # Use cookies to start requests
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookies)

    def parse(self, response):
        try:
            content_type = response.headers.get('Content-Type', b'').decode('utf-8')
            logging.debug(f'Content-Type for {response.url}: {content_type}')

            if not content_type.startswith('text'):
                logging.debug(f'Skipped non-text content: {response.url}')
                return

            normalized_url = self.normalize_url(response.url)

            if normalized_url in self.seen_urls:
                logging.debug(f'Skipping already seen URL: {normalized_url}')
                return

            self.seen_urls.add(normalized_url)
            with open(self.output_file, 'a') as f:
                f.write(f'{normalized_url}\n')
                f.flush()  # Flush the buffer to ensure data is written immediately

            logging.debug(f'Collected URL: {normalized_url}')

            a_links = response.xpath('//a/@href').extract()
            logging.debug(f'Found {len(a_links)} links on {response.url}')

            for link in a_links:
                link = response.urljoin(link)
                link = self.normalize_url(link)
                link_domain = urlparse(link).netloc

                if self.domain_origin in link_domain and link not in self.seen_urls and not link.endswith('logout.php'):
                    logging.debug(f'Yielding request for: {link}')
                    yield scrapy.Request(url=link, callback=self.parse, cookies=self.cookies)

            logging.debug(f'Processing with Selenium for URL: {response.url}')
            self.driver.get(response.url)
            self.trigger_js_events()

            # Wait for JavaScript to execute and page to fully load
            time.sleep(5)  # Adjust the wait time as needed

            updated_body = self.driver.page_source
            updated_response = HtmlResponse(
                url=response.url, 
                body=updated_body, 
                encoding='utf-8',
                headers={'Content-Type': 'text/html'}
            )
            logging.debug(f'Updated body length: {len(updated_body)}')

            # Yield the updated response as a request
            yield scrapy.Request(url=response.url, body=updated_body, encoding='utf-8', callback=self.parse, cookies=self.cookies)

        except Exception as e:
            logging.error(f'Error detected in Function parse: {e}')

    def normalize_url(self, url):
        parsed_url = urlparse(url)
        query = parse_qs(parsed_url.query)
        filtered_query = {k: v for k, v in query.items() if k not in ['random', 'session', 'timestamp']}
        normalized_query = urlencode(filtered_query, doseq=True)

        normalized_url = urlunparse((
            parsed_url.scheme,
            parsed_url.netloc,
            parsed_url.path,
            parsed_url.params,
            normalized_query,
            parsed_url.fragment
        ))
        logging.debug(f'Normalized URL: {normalized_url}')
        return normalized_url

    def trigger_js_events(self):
        try:
            initial_url = self.driver.current_url
            self.driver.execute_script("""
                var elements = document.querySelectorAll('*');
                elements.forEach(function(element) {
                    var href = element.getAttribute('href');
                    if (typeof element.onclick == 'function' && href !== 'reset.php' && href !== 'logout.php') {
                        element.click();
                    }
                });
            """)

            try:
                WebDriverWait(self.driver, 10).until(EC.url_changes(initial_url))
                self.driver.back()
            except Exception as e:
                logging.error(f'Error during WebDriverWait or driver.back(): {e}')

        except Exception as e:
            logging.error(f'Error during trigger_js_events: {e}')

    def closed(self, reason):
        self.driver.quit()

        
  # scrapy runspider crawler.py -a start_url=http://localhost/DVWA/