package model

import (
	validation "github.com/go-ozzo/ozzo-validation"
	"github.com/jinzhu/gorm"
)

//Question Model
type Question struct {
	gorm.Model
	UserID int    `json:"user_id"`
	Text   string `json:"text"`
}

//Validate for user model
func (q Question) Validate() error {
	return validation.ValidateStruct(&q,
		validation.Field(&q.UserID, validation.Required),
		validation.Field(&q.Text, validation.Required),
	)
}
