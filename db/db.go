package db

import (
	"os"

	"github.com/Sirupsen/logrus"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
)

var (
	db  *gorm.DB
	err error
)

// Init function for DB connection
func Init() {
	db, err = gorm.Open("mysql", os.Getenv("db_username")+":"+os.Getenv("db_password")+"@tcp("+os.Getenv("db_host")+":"+os.Getenv("db_port")+")/"+os.Getenv("db_name")+"?charset=utf8&parseTime=True&loc=Local")
	if err != nil {
		logrus.Errorln(err)
		logrus.Fatalln("database connection failed")

	}
}

// GetDB is db instance
func GetDB() *gorm.DB {
	return db
}

// GetClose is db closing func
func GetClose() error {
	return db.Close()
}
