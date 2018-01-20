package store

import (
	"github.com/factlist/factlist/app/model"
	"github.com/factlist/factlist/db"
)

// GetReportList is func for all questions
func GetReportList() ([]*model.Report, error) {
	db := db.GetDB()
	reports := []*model.Report{}
	err := db.Find(&reports).Error
	return reports, err

}

// GetReport is func for  question detail
func GetReport(id uint) (*model.Report, error) {
	db := db.GetDB()
	report := new(model.Report)
	db.Model(&report).Association("files").Find(&report.Files)
	db.Model(&report).Association("links").Find(&report.Links)
	err := db.First(&report, id).Error
	return report, err
}

//CreateReport is question create method
func CreateReport(report *model.Report) (*model.Report, error) {
	db := db.GetDB()
	err := db.Create(report).Error

	return report, err
}

//UpdateReport is question update method
func UpdateReport(report *model.Report, id uint) (*model.Report, error) {
	newReport := new(model.Report)
	db := db.GetDB()

	err := db.Model(&newReport).Updates(report).Error

	return report, err
}

// DeleteReport is delete func
func DeleteReport(id uint) error {
	db := db.GetDB()
	report := new(model.Report)
	if err := db.Find(&report, id).Error; err != nil {
		return err
	}
	var err = db.Delete(&report).Error

	return err
}
