package model

import (
	validation "github.com/go-ozzo/ozzo-validation"
	"github.com/jinzhu/gorm"
)

//Evidence Model
type Evidence struct {
	gorm.Model
	UserID int    `json:"user_id"`
	Status string `json:"status" gorm:"type:enum('true','false','complicated'); default:'true'"`
	Text   string `json:"text"`
	Files  []File `gorm:"many2many:evidence_files"`
	Links  []Link `gorm:"many2many:evidence_links"`
	User   User
}

//EvidenceFile Model
type EvidenceFile struct {
	EvidenceID int `json:"evidence_id"`
	FileID     int `json:"file_id"`
}

//EvidenceLink model
type EvidenceLink struct {
	EvidenceID int `json:"evidence_id"`
	LinkID     int `json:"link_id"`
}

//Validate for user model
func (e Evidence) Validate() error {
	return validation.ValidateStruct(&e,
		validation.Field(&e.UserID, validation.Required),
		validation.Field(&e.Status, validation.Required),
		validation.Field(&e.Text, validation.Required),
	)
}
