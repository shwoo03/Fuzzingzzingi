# 스마트 퍼저 (React UI 포함) 계획 및 진행상태

## 목표
- 크롤러는 `scrapy-playwright` 기반으로 유지하되, 프록시 기본값은 무사용, DB는 로컬 SQLite로 단순화.
- React(프론트) + Flask(백엔드)로 웹 UI를 제공해 사용자가 URL/프록시/깊이를 입력하면 즉시 크롤을 시작할 수 있도록 한다.
- 성능: Vite 기반 번들, 적은 렌더링 비용, 상태 폴링 최소화. 디자인: 대비 강한 색상, 카드형 레이아웃, 명확한 CTA.
- 테스트: 로컬 크롤 대상 `http://localhost:30102`로 스모크 테스트 시도, 프론트는 `npm run build`로 검증.

## 진행 체크리스트
- [x] Playwright 크롤러 유지 및 SQLite 기본 기록 구조 정비.
- [x] 프록시 기본값 무사용, 환경변수/입력으로 덮어쓰기 가능.
- [x] React + Vite UI 생성, API 연동 설계.
- [x] Flask 백엔드에 JSON API(`/api/crawl`, `/api/status`) 추가 및 정적 파일 서빙.
- [x] React UI에서 크롤 파라미터 입력/상태 조회/로그 안내 UX 구현.
- [x] README 및 의존성/실행 가이드 최신화.
- [ ] 테스트: `npm run build`, `scrapy runspider ... -a start_url=http://localhost:30102` (서비스 기동 필요) 결과 기록.

## 구현 방향
1) **UI/백엔드 분리**: `ui/`에 Vite-React 앱을 두고, 빌드 결과(`ui/dist`)를 Flask가 정적으로 서빙.  
2) **API 설계**: POST `/api/crawl`(url, proxy, depth, cookies_file) → 백그라운드 크롤 시작. GET `/api/status` → 진행 여부/마지막 명령/에러/출력 파일 경로 제공.  
3) **크롤 범위 보호**: 기존 `registered_domain` 스코프 필터 그대로 유지.  
4) **테스트**: 프론트 `npm run build`, 백엔드 `scrapy runspider ...` 스모크. 타깃 서비스가 없으면 에러 로그를 문서화.

## 테스트 계획
- 프론트: `cd ui && npm install && npm run build`. (완료)
- 백엔드: `scrapy runspider crawler/spiders/crawler.py -a start_url=http://localhost:30102 -a proxy_url=none -s LOG_LEVEL=INFO` (서비스 실행 전제). 현재 대상 서비스 미기동 시 `ERR_CONNECTION_REFUSED` 가능.
