package main

import (
	"os"

	"github.com/factlist/factlist-api/api/model"
	"github.com/factlist/factlist-api/api/router"
	"github.com/factlist/factlist-api/db"
)

func main() {

	//Initialize DB
	db.Init()

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

	// //Close DB
	defer db.GetClose()

	r.Start(":" + os.Getenv("SERVER_PORT"))
}
