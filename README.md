# WHS2기 웹 퍼저 프로젝트

## 프로젝트 목표
- WHS2기 프로젝트임을 명확히 알립니다.
- CTF 등에서 자동화된 초기 정찰과 빠른 취약점 탐색을 수행하는 웹 퍼저를 구현합니다.
- 탐지 최소화를 지향하면서도 고수준 크롤링으로 커버리지를 극대화합니다.
- 각 취약점 탐지 로직을 고도화해 사용자의 초기 접근을 더 편리하게 만듭니다.

## 현재 구현 요약
- 크롤러: `scrapy-playwright` 기반, URL 정규화·도메인 스코프·중복 필터 일원화. 결과는 `output.txt`와 로컬 SQLite(`data/crawl.db`)에 기록합니다.
- 프록시: 기본 미사용, UI/인자/환경변수로 지정 가능.
- UI: Vite + React로 제작, Flask가 API(`/api/crawl`, `/api/status`)와 정적 파일을 제공합니다.
- 계획 문서: `docs/plans.md`

## 실행 방법
1. 백엔드 의존성 설치  
   ```
   pip install -r crawler/spiders/Requirement.txt
   python -m playwright install chromium
   ```
2. 프론트엔드 빌드  
   ```
   cd ui
   npm install
   npm run build
   cd ..
   ```
3. 웹 UI 실행 (권장)  
   ```
   python main.py
   ```
   - 기본 포트: 5000 (`PORT` 환경변수로 변경 가능)
   - 브라우저에서 `http://localhost:5000` 접속 → URL/프록시/깊이/쿠키 입력 후 “크롤 시작”

4. 크롤러 단독 실행 예시 (프록시/쿠키 선택)  
   ```
   scrapy runspider crawler/spiders/crawler.py \
     -a start_url=https://example.com \
     -a proxy_url=http://127.0.0.1:8080 \
     -a cookies_file=cookie_header.txt \
     -a max_depth=3 \
     -s LOG_LEVEL=INFO
   ```
   - 프록시를 쓰지 않으려면 `proxy_url`을 생략하거나 `none`으로 지정하세요.
   - `cookie_header.txt`는 `name=value` 한 줄씩 저장합니다.

## DB 설정 (로컬 SQLite 기본값)
- 기본 파일: `data/crawl.db`
- 경로 변경: 환경변수 `SQLITE_PATH`로 지정
- 크롤링 시 수집 URL이 자동으로 `collected_urls` 테이블에 적재됩니다.

## 브라우저 스모크 테스트
- `scrapy runspider crawler/spiders/crawler.py -a start_url=https://example.com -s LOG_LEVEL=INFO`
- 실행 후 `output.txt`에 `https://example.com/` 등 렌더링된 결과가 기록되는지 확인합니다.
