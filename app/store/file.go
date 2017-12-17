package store

import (
	"github.com/factlist/factlist/app/model"
	"github.com/factlist/factlist/db"
)

// GetFileList is func for all files
func GetFileList() ([]*model.File, error) {
	db := db.GetDB()
	files := []*model.File{}
	err := db.Find(&files).Error
	return files, err

}

// GetFile is func for  file detail
func GetFile(id uint) (*model.File, error) {
	db := db.GetDB()
	file := new(model.File)
	err := db.First(&file, id).Error
	return file, err
}

//CreateFile is file create method
func CreateFile(file *model.File) (*model.File, error) {
	db := db.GetDB()
	err := db.Create(file).Error

	return file, err
}

//UpdateFile is file update method
func UpdateFile(file *model.File, id uint) (*model.File, error) {
	newFile := new(model.File)
	db := db.GetDB()
	err := db.Model(&newFile).Updates(file).Error

	return file, err
}

// DeleteFile is delete func
func DeleteFile(id uint) error {
	db := db.GetDB()
	file := new(model.File)
	if err := db.Find(&file, id).Error; err != nil {
		return err
	}
	var err = db.Delete(&file).Error

	return err
}
