package handler

import (
	"net/http"
	"strconv"

	"github.com/labstack/echo"

	"github.com/factlist/factlist/api/model"
	"github.com/factlist/factlist/api/store"
)

//GetUserList is func
func GetUserList(c echo.Context) error {
	users, err := store.GetUserList()
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, users)
}

//GetUser is func
func GetUser(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	users, err := store.GetUser(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, users)
}

//CreateUser is func
func CreateUser(c echo.Context) error {
	userModel := model.User{}

	c.Bind(&userModel)

	if err := userModel.Validate(); err != nil {
		c.JSON(http.StatusUnprocessableEntity, err)
		return nil
	}

	user, err := store.CreateUser(&userModel)

	if err != nil {
		if err != nil {
			c.JSON(http.StatusNotFound, err)
		}

	}
	return c.JSON(http.StatusOK, user)
}

//UpdateUser is func
func UpdateUser(c echo.Context) error {
	userModel := model.User{}

	err := c.Bind(&userModel)

	if err != nil {
		c.JSON(http.StatusBadRequest, err.Error())
		return nil
	}
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)

	user, err := store.UpdateUser(&userModel, uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, err)

	}
	return c.JSON(http.StatusOK, user)
}

//DeleteUser is func
func DeleteUser(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	if err := store.DeleteUser(uint(id)); err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return nil
	}
	return c.JSON(http.StatusOK, id)
}
