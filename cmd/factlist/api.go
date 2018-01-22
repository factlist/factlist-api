package main

import (
	"strconv"

	"github.com/factlist/factlist-api/api/helper"
	"github.com/factlist/factlist-api/api/model"
	"github.com/factlist/factlist-api/api/router"
	"github.com/factlist/factlist-api/db"
)

func main() {

	config := helper.SetConfig(".")

	//Initialize DB
	db.Init(config)

	//Migrate DB

	db.GetDB().AutoMigrate(&model.User{})
	db.GetDB().AutoMigrate(&model.Evidence{})
	db.GetDB().AutoMigrate(&model.EvidenceFile{})
	db.GetDB().AutoMigrate(&model.EvidenceLink{})
	db.GetDB().AutoMigrate(&model.Report{})
	db.GetDB().AutoMigrate(&model.Link{})
	db.GetDB().AutoMigrate(&model.File{})
	db.GetDB().AutoMigrate(&model.ReportEvidence{})
	db.GetDB().AutoMigrate(&model.ReportFile{})
	db.GetDB().AutoMigrate(&model.ReportLink{})

	// //Initialize Router
	r := router.Init()

	// r.POST("/upload", func(c echo.Context) error {

	// 	file, handler, err := c.Request().FormFile("file")

	// 	if err != nil {
	// 		fmt.Println(err)
	// 	}

	// 	f, _ := os.OpenFile(handler.Filename, os.O_WRONLY|os.O_CREATE, 0777)

	// 	defer f.Close()

	// 	io.Copy(f, file)

	// 	location, err := helper.AddFileToS3("uploads", "./"+handler.Filename, handler)

	// 	if err != nil {
	// 		fmt.Println(err)
	// 	}
	// 	fmt.Println(location)

	// 	return nil
	// })

	// //Close DB
	defer db.GetClose()

	r.Start(":" + strconv.Itoa(config.GetInt("server.port")))

}
