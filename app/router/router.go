package router

import (
	"github.com/factlist/factlist/app/handler"
	"github.com/factlist/factlist/app/handler/auth"
	"github.com/labstack/echo"
	echoMiddleware "github.com/labstack/echo/middleware"
)

//Init Router
func Init() *echo.Echo {
	e := echo.New()

	/*
		|--------------------------------------------------------------------------
		| Global Middlewares
		|--------------------------------------------------------------------------
		|
	*/

	e.Use(echoMiddleware.Logger())
	e.Use(echoMiddleware.Recover())
	e.Use(echoMiddleware.CORSWithConfig(echoMiddleware.CORSConfig{
		AllowOrigins: []string{"*"},
		AllowMethods: []string{echo.GET, echo.HEAD, echo.PUT, echo.PATCH, echo.POST, echo.DELETE},
	}))

	api := e.Group("/api")
	/*
		|--------------------------------------------------------------------------
		| Authenticate Handler Routes
		|--------------------------------------------------------------------------
		|
		| Endpoint: /api/login-register
		|
	*/

	api.POST("/login", auth.PostLogin)
	api.POST("/register", auth.PostRegister)

	/*
		|--------------------------------------------------------------------------
		| User Handler Routes
		|--------------------------------------------------------------------------
		|
		| Endpoint: /api/routes
		|
	*/

	api.GET("/users", handler.GetUserList)
	api.GET("/users/:id", handler.GetUser)
	api.POST("/users", handler.CreateUser)
	api.DELETE("/users/:id", handler.DeleteUser)
	api.PATCH("/users/:id", handler.UpdateUser)

	/*
		|--------------------------------------------------------------------------
		| Evidence Handler Routes
		|--------------------------------------------------------------------------
		|
		| Endpoint: /api/evidences
		|
	*/

	api.GET("/evidences", handler.GetEvidenceList)
	api.GET("/evidences/:id", handler.GetEvidence)
	api.POST("/evidences", handler.CreateEvidence)
	api.DELETE("/evidences/:id", handler.DeleteEvidence)
	api.PATCH("/evidences/:id", handler.UpdateEvidence)

	/*
		|--------------------------------------------------------------------------
		| Questions Handler Routes
		|--------------------------------------------------------------------------
		|
		| Endpoint: /api/questions
		|
	*/

	api.GET("/questions", handler.GetQuestionList)
	api.GET("/questions/:id", handler.GetQuestion)
	api.POST("/questions", handler.CreateQuestion)
	api.DELETE("/questions/:id", handler.DeleteQuestion)
	api.PATCH("/questions/:id", handler.UpdateQuestion)

	/*
		|--------------------------------------------------------------------------
		| Files Handler Routes
		|--------------------------------------------------------------------------
		|
		| Endpoint: /api/files
		|
	*/

	api.GET("/files", handler.GetFileList)
	api.GET("/files/:id", handler.GetFile)
	api.POST("/files", handler.CreateFile)
	api.DELETE("/files/:id", handler.DeleteFile)
	api.PATCH("/files/:id", handler.UpdateFile)

	/*
		|--------------------------------------------------------------------------
		| Links Handler Routes
		|--------------------------------------------------------------------------
		|
		| Endpoint: /api/links
		|
	*/

	api.GET("/links", handler.GetLinkList)
	api.GET("/links/:id", handler.GetLink)
	api.POST("/links", handler.CreateLink)
	api.DELETE("/links/:id", handler.DeleteLink)
	api.PATCH("/links/:id", handler.UpdateLink)

	return e
}
