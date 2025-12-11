package crawler

import (
	"errors"
	"fmt"
	"net/url"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"

	"github.com/gocolly/colly/v2"
)

// Request는 크롤 시작 시 전달되는 파라미터 집합입니다.
type Request struct {
	StartURL   string `json:"startUrl"`
	ProxyURL   string `json:"proxyUrl"`
	MaxDepth   int    `json:"depth"`
	CookiesFile string `json:"cookiesFile"`
}

// String은 상태 표시용 명령 문자열을 생성합니다.
func (r Request) String() string {
	return fmt.Sprintf("start_url=%s proxy_url=%s max_depth=%d", r.StartURL, r.ProxyURL, r.MaxDepth)
}

// Run은 colly 기반 크롤을 수행하고 결과를 output.txt에 기록합니다.
func Run(req Request) error {
	if req.MaxDepth <= 0 {
		req.MaxDepth = 3
	}

	outputPath := filepath.Join(".", "output.txt")
	if err := os.WriteFile(outputPath, []byte{}, 0644); err != nil {
		return fmt.Errorf("output 파일 생성 실패: %w", err)
	}

	u, err := url.Parse(req.StartURL)
	if err != nil {
		return fmt.Errorf("URL 파싱 실패: %w", err)
	}
	baseHost := u.Hostname()       // ex) localhost
	hostWithPort := u.Host         // ex) localhost:30102
	if baseHost == "" {
		return errors.New("호스트를 판별할 수 없습니다")
	}

	c := colly.NewCollector(
		colly.AllowedDomains(baseHost, hostWithPort),
		colly.MaxDepth(req.MaxDepth),
		colly.Async(true),
	)
	c.SetRequestTimeout(30 * time.Second)
	c.UserAgent = "Fuzzingzzingi-GoCrawler/0.1"

	if req.ProxyURL != "" && strings.ToLower(req.ProxyURL) != "none" {
		if err := c.SetProxy(req.ProxyURL); err != nil {
			return fmt.Errorf("프록시 설정 실패: %w", err)
		}
	}

	seen := sync.Map{}
	mu := &sync.Mutex{}

	writeURL := func(u string) {
		mu.Lock()
		defer mu.Unlock()
		f, err := os.OpenFile(outputPath, os.O_APPEND|os.O_WRONLY, 0644)
		if err != nil {
			return
		}
		defer f.Close()
		_, _ = f.WriteString(u + "\n")
	}

	c.OnRequest(func(r *colly.Request) {
		norm := normalize(r.URL.String())
		if _, loaded := seen.LoadOrStore(norm, true); loaded {
			r.Abort()
		}
	})

	c.OnResponse(func(r *colly.Response) {
		norm := normalize(r.Request.URL.String())
		writeURL(norm)
	})

	c.OnHTML("a[href]", func(e *colly.HTMLElement) {
		link := e.Attr("href")
		abs := e.Request.AbsoluteURL(link)
		norm := normalize(abs)
		host := hostOf(norm)
		if host != baseHost {
			return
		}
		if _, loaded := seen.LoadOrStore(norm, true); loaded {
			return
		}
		_ = e.Request.Visit(norm)
	})

	c.OnError(func(r *colly.Response, err error) {
		fmt.Fprintf(os.Stderr, "크롤 오류 %s: %v\n", r.Request.URL, err)
	})

	if err := c.Visit(req.StartURL); err != nil {
		return fmt.Errorf("초기 방문 실패: %w", err)
	}
	c.Wait()
	return nil
}

func normalize(raw string) string {
	u, err := url.Parse(raw)
	if err != nil {
		return raw
	}
	q := u.Query()
	for _, k := range []string{"random", "session", "timestamp"} {
		q.Del(k)
	}
	u.RawQuery = q.Encode()
	u.Fragment = ""
	return u.String()
}

func hostOf(raw string) string {
	u, err := url.Parse(raw)
	if err != nil {
		return ""
	}
	return u.Hostname()
}
