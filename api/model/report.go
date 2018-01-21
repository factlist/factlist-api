package model

import (
	validation "github.com/go-ozzo/ozzo-validation"
	"github.com/jinzhu/gorm"
)

//Report Model
type Report struct {
	gorm.Model
	UserID    int    `json:"user_id"`
	Text      string `json:"text"`
	Files     []File
	Links     []Link
	Evidences []Evidence `gorm:"many2many:report_evidences"`
}

//ReportEvidence Model
type ReportEvidence struct {
	ReportID   int `json:"report_id"`
	EvidenceID int `json:"evidence_id"`
}

//ReportFile Model
type ReportFile struct {
	ReportID int `json:"report_id"`
	FileID   int `json:"file_id"`
}

//ReportLink Model
type ReportLink struct {
	ReportID int `json:"report_id"`
	LinkID   int `json:"link_id"`
}

//Validate for user model
func (q Report) Validate() error {
	return validation.ValidateStruct(&q,
		validation.Field(&q.UserID, validation.Required),
		validation.Field(&q.Text, validation.Required),
	)
}
