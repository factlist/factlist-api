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
}

//Validate for user model
func (e Evidence) Validate() error {
	return validation.ValidateStruct(&e,
		validation.Field(&e.UserID, validation.Required),
		validation.Field(&e.Status, validation.Required),
		validation.Field(&e.Text, validation.Required),
	)
}
