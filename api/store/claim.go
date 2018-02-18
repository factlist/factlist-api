package store

import (
	"github.com/factlist/factlist-api/api/model"
	"github.com/factlist/factlist-api/db"
)

// GetClaimList is func for all claims
func GetClaimList() ([]*model.Claim, error) {
	db := db.GetDB()
	claims := []*model.Claim{}
	err := db.Preload("Evidences").Preload("Evidences.Files").Preload("Evidences.Links").Preload("User").Preload("Files").Preload("Links").Find(&claims).Error
	return claims, err

}

// GetClaim is func for  claim detail
func GetClaim(id uint) (*model.Claim, error) {
	db := db.GetDB()
	claim := new(model.Claim)
	err := db.Preload("User").First(&claim, id).Error
	db.Model(&claim).Association("files").Find(&claim.Files)
	db.Model(&claim).Association("links").Find(&claim.Links)
	db.Model(&claim).Association("evidences").Find(&claim.Evidences)
	db.Model(&claim.Evidences[0]).Association("files").Find(&claim.Evidences[0].Files)
	db.Model(&claim.Evidences[0]).Association("links").Find(&claim.Evidences[0].Links)
	return claim, err
}

//CreateClaim is claim create method
func CreateClaim(claim *model.Claim, files []model.File, links []model.Link) (*model.Claim, error) {
	db := db.GetDB()
	err := db.Create(claim).Error
	db.Model(&claim).Association("files").Append(files)
	db.Model(&claim).Association("links").Append(links)
	return claim, err
}

//UpdateClaim is claim update method
func UpdateClaim(claim *model.Claim, evidences *model.Evidence, files []model.File, links []model.Link,
	evidenceFiles []model.File, evidenceLinks []model.Link, id uint) (*model.Claim, error) {
	db := db.GetDB()
	newClaim := new(model.Claim)
	db.First(&newClaim, id)

	err := db.Model(&newClaim).Updates(claim).Error

	db.Model(&newClaim).Association("evidences").Replace(evidences)

	if len(files) > 0 {
		db.Model(&newClaim).Association("files").Replace(files)
	}

	if len(links) > 0 {
		db.Model(&newClaim).Association("links").Replace(links)
	}

	if len(evidenceLinks) > 0 {
		db.Model(&newClaim.Evidences[0]).Association("links").Replace(evidenceLinks)
	}

	if len(evidenceFiles) > 0 {
		db.Model(&newClaim.Evidences[0]).Association("files").Replace(evidenceFiles)
	}

	return newClaim, err
}

// DeleteClaim is delete func
func DeleteClaim(id uint) error {
	db := db.GetDB()
	claim := new(model.Claim)
	if err := db.Find(&claim, id).Error; err != nil {
		return err
	}
	var err = db.Delete(&claim).Error
	db.Model(&claim).Association("evidences").Clear()
	db.Model(&claim).Association("files").Clear()
	db.Model(&claim).Association("links").Clear()
	return err
}
