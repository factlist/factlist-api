package model

import (
	validation "github.com/go-ozzo/ozzo-validation"
)

// User model
type User struct {
	BaseModel
	Username string `json:"username"`
	Email    string `json:"email"`
	Password string `json:"password"`
}

//Validate for user model
func (u User) Validate() error {
	return validation.ValidateStruct(&u,
		validation.Field(&u.Email, validation.Required),
		validation.Field(&u.Password, validation.Required),
	)
}
