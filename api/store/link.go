package store

import (
	"github.com/factlist/factlist/api/model"
	"github.com/factlist/factlist/db"
)

// GetLinkList is func for all links
func GetLinkList() ([]*model.Link, error) {
	db := db.GetDB()
	links := []*model.Link{}
	err := db.Find(&links).Error
	return links, err

}

// GetLink is func for  link detail
func GetLink(id uint) (*model.Link, error) {
	db := db.GetDB()
	link := new(model.Link)
	err := db.First(&link, id).Error
	return link, err
}

//CreateLink is link create method
func CreateLink(link *model.Link) (*model.Link, error) {
	db := db.GetDB()
	err := db.Create(link).Error

	return link, err
}

//UpdateLink is link update method
func UpdateLink(link *model.Link, id uint) (*model.Link, error) {
	newLink := new(model.Link)
	db := db.GetDB()

	err := db.Model(&newLink).Updates(link).Error

	return link, err
}

// DeleteLink is delete func
func DeleteLink(id uint) error {
	db := db.GetDB()
	link := new(model.Link)
	if err := db.Find(&link, id).Error; err != nil {
		return err
	}
	var err = db.Delete(&link).Error

	return err
}
