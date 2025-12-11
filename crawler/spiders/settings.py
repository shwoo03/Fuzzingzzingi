# Scrapy 설정 (크롤러 실행 시 프로젝트 단위 설정이 필요한 경우 사용)

BOT_NAME = "fuzzingzzingi"

SPIDER_MODULES = ["crawler.spiders"]
NEWSPIDER_MODULE = "crawler.spiders"

USER_AGENT = "FuzzingzzingiCrawler/0.1 (+https://example.com)"
ROBOTSTXT_OBEY = False
LOG_LEVEL = "INFO"

DOWNLOAD_TIMEOUT = 30
CONCURRENT_REQUESTS = 16
DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS_PER_IP = 8

# 기본 프록시 (스파이더 인자에서 덮어쓸 수 있습니다)
PROXY = "http://127.0.0.1:8080"

# DOWNLOADER_MIDDLEWARES에 Selenium을 넣지 않았습니다.
# 현재는 스파이더 내부 BrowserSession을 사용하므로 중복 제어를 피하기 위함입니다.
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 1,
}

# MySQL 설정 (현재 파이프라인 비활성화)
MYSQL_HOST = "13.209.63.65"
MYSQL_DATABASE = "Fuzzingzzingi"
MYSQL_USER = "zzingzzingi"
MYSQL_PASSWORD = "!Ru7eP@ssw0rD!12"

# ITEM_PIPELINES는 기본적으로 꺼 둡니다. (DB 연동 필요 시 활성화)
ITEM_PIPELINES = {
    # "crawler.spiders.pipelines.DuplicateURLPipeline": 100,
}

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
