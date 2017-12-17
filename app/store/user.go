package store

import (
	"golang.org/x/crypto/bcrypt"

	"github.com/factlist/factlist/app/model"
	"github.com/factlist/factlist/db"
)

// GetUserList is func for all users
func GetUserList() ([]*model.User, error) {
	db := db.GetDB()
	users := []*model.User{}
	err := db.Find(&users).Error
	return users, err

}

// GetUser is func for  user detail
func GetUser(id uint) (*model.User, error) {
	db := db.GetDB()
	user := new(model.User)
	err := db.First(&user, id).Error
	return user, err
}

// GetUserByLogin is email and password verification
func GetUserByLogin(email, password string) (*model.User, error) {
	db := db.GetDB()
	user := new(model.User)

	if err := db.Where(&model.User{Email: email}).First(&user).Error; err != nil {
		return nil, err
	}

	if err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(password)); err != nil {
		return nil, err
	}
	return user, nil
}

//CreateUser is user create method
func CreateUser(user *model.User) (*model.User, error) {
	db := db.GetDB()
	err := db.Create(user).Error

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)

	if err != nil {
		return nil, err
	}

	user.Password = string(hashedPassword)

	return user, err
}

//UpdateUser is user update method
func UpdateUser(user *model.User, id uint) (*model.User, error) {
	newUser := new(model.User)
	db := db.GetDB()

	err := db.Model(&newUser).Updates(user).Error

	hashedPassword, err := bcrypt.GenerateFromPassword([]byte(user.Password), bcrypt.DefaultCost)

	if err != nil {
		return nil, err
	}

	user.Password = string(hashedPassword)

	return user, err
}

// DeleteUser is delete func
func DeleteUser(id uint) error {
	db := db.GetDB()
	user := new(model.User)
	if err := db.Find(&user, id).Error; err != nil {
		return err
	}
	var err = db.Delete(&user).Error

	return err
}
