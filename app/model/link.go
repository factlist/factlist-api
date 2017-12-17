package model

import (
	validation "github.com/go-ozzo/ozzo-validation"
	"github.com/go-ozzo/ozzo-validation/is"
	"github.com/jinzhu/gorm"
)

//Link Model
type Link struct {
	gorm.Model
	URL        string `json:"url"`
	ArchiveURL string `json:"archive_url"`
	UserID     int    `json:"user_Id"`
}

//Validate for user model
func (l Link) Validate() error {
	return validation.ValidateStruct(&l,
		validation.Field(&l.URL, validation.Required, is.URL),
		validation.Field(&l.ArchiveURL, validation.Required, is.URL),
		validation.Field(&l.UserID, validation.Required),
	)
}
