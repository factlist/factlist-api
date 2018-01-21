package handler

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/factlist/factlist/app/router"
	"github.com/gavv/httpexpect"
)

func testRouter(e *httpexpect.Expect) {
	e.GET("/api/users").
		Expect().
		Status(http.StatusOK)
}

func testRouterClient(t *testing.T) {

	handler := router.Init()

	server := httptest.NewServer(handler)
	defer server.Close()

	e := httpexpect.WithConfig(httpexpect.Config{
		BaseURL:  server.URL,
		Reporter: httpexpect.NewAssertReporter(t),
		Printers: []httpexpect.Printer{
			httpexpect.NewDebugPrinter(t, true),
		},
	})

	testRouter(e)

}

func TestRouteHandler(t *testing.T) {
	handler := router.Init()

	e := httpexpect.WithConfig(httpexpect.Config{
		Client: &http.Client{
			Transport: httpexpect.NewBinder(handler),
			Jar:       httpexpect.NewJar(),
		},
		Reporter: httpexpect.NewAssertReporter(t),
		Printers: []httpexpect.Printer{
			httpexpect.NewDebugPrinter(t, true),
		},
	})

	testRouter(e)

}
