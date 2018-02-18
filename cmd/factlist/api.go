package main

import (
	"os"

	"github.com/factlist/factlist-api/api/router"
	"github.com/factlist/factlist-api/db"
)

func main() {

	//Initialize DB
	db.Init()

	// //Initialize Router
	r := router.Init()

	// //Close DB
	defer db.GetClose()

	r.Start(":" + os.Getenv("PORT"))
}
