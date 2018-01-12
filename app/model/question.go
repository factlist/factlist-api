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
	Files  []File
	Links  []Link
}

//QuestionEvidence Model
type QuestionEvidence struct {
	QuestionID int `json:"question_id"`
	EvidenceID int `json:"evidence_id"`
}

//QuestionFile Model
type QuestionFile struct {
	QuestionID int `json:"question_id"`
	FileID     int `json:"file_id"`
}

//QuestionLink Model
type QuestionLink struct {
	QuestionID int `json:"question_id"`
	LinkID     int `json:"link_id"`
}

//Validate for user model
func (q Question) Validate() error {
	return validation.ValidateStruct(&q,
		validation.Field(&q.UserID, validation.Required),
		validation.Field(&q.Text, validation.Required),
	)
}
