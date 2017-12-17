package db

import (
	"strconv"

	"github.com/spf13/viper"

	"github.com/Sirupsen/logrus"
	"github.com/jinzhu/gorm"
	_ "github.com/jinzhu/gorm/dialects/mysql"
)

var (
	db  *gorm.DB
	err error
)

// Init function for DB connection
func Init(config *viper.Viper) {
	db, err = gorm.Open("mysql", config.GetString("database.username")+":"+config.GetString("database.password")+"@tcp("+config.GetString("database.host")+":"+strconv.Itoa(config.GetInt("database.port"))+")/"+config.GetString("database.name")+"?charset=utf8&parseTime=True&loc=Local")
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
