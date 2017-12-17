package store

import (
	"github.com/factlist/factlist/app/model"
	"github.com/factlist/factlist/db"
)

// GetQuestionList is func for all questions
func GetQuestionList() ([]*model.Question, error) {
	db := db.GetDB()
	questions := []*model.Question{}
	err := db.Find(&questions).Error
	return questions, err

}

// GetQuestion is func for  question detail
func GetQuestion(id uint) (*model.Question, error) {
	db := db.GetDB()
	question := new(model.Question)
	err := db.First(&question, id).Error
	return question, err
}

//CreateQuestion is question create method
func CreateQuestion(question *model.Question) (*model.Question, error) {
	db := db.GetDB()
	err := db.Create(question).Error

	return question, err
}

//UpdateQuestion is question update method
func UpdateQuestion(question *model.Question, id uint) (*model.Question, error) {
	newQuestion := new(model.Question)
	db := db.GetDB()

	err := db.Model(&newQuestion).Updates(question).Error

	return question, err
}

// DeleteQuestion is delete func
func DeleteQuestion(id uint) error {
	db := db.GetDB()
	question := new(model.Question)
	if err := db.Find(&question, id).Error; err != nil {
		return err
	}
	var err = db.Delete(&question).Error

	return err
}
