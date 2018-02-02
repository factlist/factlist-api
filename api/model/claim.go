package model

import (
	validation "github.com/go-ozzo/ozzo-validation"
	"github.com/jinzhu/gorm"
)

//Claim Model
type Claim struct {
	gorm.Model
	UserID    int        `json:"user_id"`
	Text      string     `json:"text"`
	Files     []File     `gorm:"many2many:claim_files"`
	Links     []Link     `gorm:"many2many:claim_links"`
	Evidences []Evidence `gorm:"many2many:claim_evidences"`
	User      User
}

//ClaimEvidence Model
type ClaimEvidence struct {
	ClaimID    int `json:"claim_id"`
	EvidenceID int `json:"evidence_id"`
}

//ClaimFile Model
type ClaimFile struct {
	ClaimID int `json:"claim_id"`
	FileID  int `json:"file_id"`
}

//ClaimLink Model
type ClaimLink struct {
	ClaimID int `json:"claim_id"`
	LinkID  int `json:"link_id"`
}

//Validate for user model
func (q Claim) Validate() error {
	return validation.ValidateStruct(&q,
		validation.Field(&q.UserID, validation.Required),
		validation.Field(&q.Text, validation.Required),
	)
}
