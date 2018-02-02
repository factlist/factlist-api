package store

import (
	"github.com/factlist/factlist-api/api/model"
	"github.com/factlist/factlist-api/db"
)

// GetReportList is func for all reports
func GetReportList() ([]*model.Report, error) {
	db := db.GetDB()
	reports := []*model.Report{}
	err := db.Preload("User").Preload("Files").Preload("Links").Find(&reports).Error
	return reports, err

}

// GetReport is func for  report detail
func GetReport(id uint) (*model.Report, error) {
	db := db.GetDB()
	report := new(model.Report)
	db.Model(&report).Association("files").Find(&report.Files)
	db.Model(&report).Association("links").Find(&report.Links)
	err := db.Preload("User").First(&report, id).Error
	return report, err
}

//CreateReport is report create method
func CreateReport(report *model.Report, files []model.File, links []model.Link) (*model.Report, error) {
	db := db.GetDB()
	err := db.Create(report).Error
	db.Model(&report).Association("files").Append(files)
	db.Model(&report).Association("links").Append(links)
	return report, err
}

//UpdateReport is report update method
func UpdateReport(report *model.Report, evidences *model.Evidence, files []model.File, links []model.Link,
	evidenceFiles []model.File, evidenceLinks []model.Link, id uint) (*model.Report, error) {
	db := db.GetDB()
	newReport := new(model.Report)
	// newEvidence := new(model.Evidence)

	db.First(&newReport, id)

	err := db.Model(&newReport).Updates(report).Error

	db.Model(&newReport).Association("evidences").Replace(evidences)
	db.Model(&newReport).Association("files").Replace(files)
	db.Model(&newReport).Association("links").Replace(links)
	db.Model(&newReport.Evidences[0]).Association("links").Replace(evidenceLinks)
	db.Model(&newReport.Evidences[0]).Association("files").Replace(evidenceFiles)

	// db.First(&newEvidence, newReport.Evidences[0].ID)

	// db.Model(&newEvidence).Association("files").Replace(evidenceFiles)
	// db.Model(&newEvidence).Association("links").Replace(evidenceLinks)

	return newReport, err
}

// DeleteReport is delete func
func DeleteReport(id uint) error {
	db := db.GetDB()
	report := new(model.Report)
	if err := db.Find(&report, id).Error; err != nil {
		return err
	}
	var err = db.Delete(&report).Error
	db.Model(&report).Association("files").Clear()
	db.Model(&report).Association("links").Clear()
	return err
}
