package middleware

import (
	"net/http"

	"github.com/onerciller/thor"
)

const (
	options           string = "OPTIONS"
	allow_origin      string = "Access-Control-Allow-Origin"
	allow_methods     string = "Access-Control-Allow-Methods"
	allow_headers     string = "Access-Control-Allow-Headers"
	allow_credentials string = "Access-Control-Allow-Credentials"
	expose_headers    string = "Access-Control-Expose-Headers"
	credentials       string = "true"
	origin            string = "Origin"
	methods           string = "POST, GET, OPTIONS, PUT, DELETE, HEAD, PATCH"

	// If you want to expose some other headers add it here
	headers string = "Access-Control-Allow-Origin, Accept, Accept-Encoding, Authorization, Content-Length, Content-Type, X-CSRF-Token"
)

//Cors is middleware
func Cors() *thor.HandlerFunc {

	return func(c *thor.Context) error {

		if o := c.GetHeader(origin); o != "" {
			w.Header().Set(allow_origin, o)
		} else {
			w.Header().Set(allow_origin, "*")
		}

		c.SetHeader(allow_headers, headers)
		c.SetHeader(allow_methods, methods)
		c.SetHeader(allow_credentials, credentials)
		c.SetHeader(expose_headers, headers)

		if c.Request.Method == options {
			c.Response.WriteHeader(http.StatusOK)
			c.Response.Write(nil)
			return
		}

		c.Next()
	}
}
