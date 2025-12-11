# WHS2기 웹 퍼저 프로젝트

## 프로젝트 목표
- WHS2기 프로젝트임을 명확히 알립니다.
- CTF 등에서 자동화된 초기 정찰과 빠른 취약점 탐색을 수행하는 웹 퍼저를 구현합니다.
- 탐지 최소화를 지향하면서도 고수준 크롤링으로 커버리지를 극대화합니다.
- 각 취약점 탐지 로직을 고도화해 사용자의 초기 접근을 더 편리하게 만듭니다.

## 현재 구현 요약
- 크롤러: Go(colly) 기반, 도메인 스코프/정규화/중복 필터 일원화. 결과는 `output.txt`에 기록합니다.
- 서버: Go Gin API(`/api/crawl`, `/api/status`)가 React 빌드 결과(`ui/dist`)를 정적 서빙합니다.
- 프론트: Vite + React UI로 URL/프록시/깊이/쿠키 입력 후 크롤링 실행.
- 계획 문서: `docs/plans.md`

## 실행 방법 (Go)
1. 프론트엔드 빌드  
   ```
   cd ui
   npm install
   npm run build
   cd ..
   ```
2. Go 서버 실행  
   ```
   go run ./cmd/server           # 기본 포트 5000 사용
   # 5000이 이미 사용 중이면
   PORT=5001 go run ./cmd/server # Windows PowerShell: $env:PORT=5001; go run ./cmd/server
   ```
   - 기본 포트: 5000 (`PORT` 환경변수로 변경 가능)
   - 브라우저에서 `http://localhost:5000` 접속 → URL/프록시/깊이/쿠키 입력 후 “크롤 시작”

3. Go 크롤러 단독 실행 예시  
   ```
   go run ./cmd/server  # 서버 구동 후 /api/crawl 로 JSON POST
   ```
   예시 요청 바디:
   ```json
   {
     "startUrl": "https://example.com",
     "proxyUrl": "none",
     "depth": 3,
     "cookiesFile": ""
   }
   ```
   - 프록시를 쓰지 않으려면 `proxyUrl`에 `none` 또는 빈 문자열을 지정하세요.
   - 크롤링 결과는 `output.txt`에 기록됩니다.

## 참고
- 기존 Python Scrapy/Playwright 스택은 유지돼 있지만, 기본 경로는 Go 서버+colly 크롤러입니다.
- 타깃이 기동돼야 크롤이 성공합니다(`http://localhost:30102` 등). 대상이 죽어 있으면 연결 거부 오류가 발생합니다.

## 브라우저 스모크 테스트
- `scrapy runspider crawler/spiders/crawler.py -a start_url=https://example.com -s LOG_LEVEL=INFO`
- 실행 후 `output.txt`에 `https://example.com/` 등 렌더링된 결과가 기록되는지 확인합니다.
