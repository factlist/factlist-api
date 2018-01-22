package store

import (
	"github.com/factlist/factlist/api/model"
	"github.com/factlist/factlist/db"
)

// GetEvidenceList is func for all users
func GetEvidenceList() ([]*model.Evidence, error) {
	db := db.GetDB()
	evidences := []*model.Evidence{}
	err := db.Preload("User").Preload("Files").Preload("Links").Find(&evidences).Error
	return evidences, err

}

// GetEvidence is func for  evidence detail
func GetEvidence(id uint) (*model.Evidence, error) {
	db := db.GetDB()
	evidence := new(model.Evidence)
	err := db.Preload("User").First(&evidence, id).Error
	db.Model(&evidence).Association("files").Find(&evidence.Files)
	db.Model(&evidence).Association("links").Find(&evidence.Links)

	return evidence, err
}

//CreateEvidence is evidence create method
func CreateEvidence(evidence *model.Evidence, files []model.File, links []model.Link) (*model.Evidence, error) {
	db := db.GetDB()
	err := db.Create(evidence).Error

	db.Model(&evidence).Association("files").Append(files)
	db.Model(&evidence).Association("links").Append(links)
	return evidence, err
}

//UpdateEvidence is evidence update method
func UpdateEvidence(evidence *model.Evidence, files []model.File, links []model.Link, id uint) (*model.Evidence, error) {
	db := db.GetDB()
	newEvidence := new(model.Evidence)
	db.First(&newEvidence, id)
	err := db.Model(&newEvidence).Updates(evidence).Error
	db.Model(&newEvidence).Association("files").Replace(files)
	db.Model(&newEvidence).Association("links").Replace(links)

	return newEvidence, err
}

// DeleteEvidence is delete func
func DeleteEvidence(id uint) error {
	db := db.GetDB()
	evidence := new(model.Evidence)
	if err := db.Find(&evidence, id).Error; err != nil {
		return err
	}

	err := db.Delete(&evidence).Error
	db.Model(&evidence).Association("files").Clear()
	db.Model(&evidence).Association("links").Clear()

	return err
}
