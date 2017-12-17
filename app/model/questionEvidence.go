package model

// Question_Evidences
// question_id
// evidence_id

//QuestionEvidence Model
type QuestionEvidence struct {
	QuestionID int `json:"question_id"`
	EvidenceID int `json:"evidence_id"`
}
