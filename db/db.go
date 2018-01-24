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
	db, err = gorm.Open("mysql", os.Getenv("DB_USERNAME")+":"+os.Getenv("DB_PASSWORD")+"@tcp("+os.Getenv("DB_HOST")+":"+os.Getenv("DB_PORT")+")/"+os.Getenv("DB_NAME")+"?charset=utf8&parseTime=True&loc=Local")
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
