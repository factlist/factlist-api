package store

import (
	"fmt"

	"github.com/factlist/factlist/app/model"
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

	fmt.Println(evidence.User.ID)
	return evidence, err
}

//CreateEvidence is evidence create method
func CreateEvidence(evidence *model.Evidence, files []model.File) (*model.Evidence, error) {
	db := db.GetDB()
	err := db.Create(evidence).Error

	db.Model(&evidence).Association("files").Append(files)

	return evidence, err
}

//UpdateEvidence is evidence update method
func UpdateEvidence(evidence *model.Evidence, id uint) (*model.Evidence, error) {
	newEvidence := new(model.Evidence)
	db := db.GetDB()

	err := db.Model(&newEvidence).Updates(evidence).Error

	return evidence, err
}

// DeleteEvidence is delete func
func DeleteEvidence(id uint) error {
	db := db.GetDB()
	evidence := new(model.Evidence)
	if err := db.Find(&evidence, id).Error; err != nil {
		return err
	}
	err := db.Delete(&evidence).Error

	return err
}
