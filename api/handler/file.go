package handler

import (
	"net/http"
	"strconv"

	"github.com/labstack/echo"

	"github.com/factlist/factlist/api/model"
	"github.com/factlist/factlist/api/store"
)

//GetFileList is func
func GetFileList(c echo.Context) error {
	files, err := store.GetFileList()
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, files)
}

//GetFile is func
func GetFile(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	file, err := store.GetFile(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, file)
}

//CreateFile is func
func CreateFile(c echo.Context) error {
	fileModel := model.File{}

	err := c.Bind(&fileModel)

	if err := fileModel.Validate(); err != nil {
		c.JSON(http.StatusUnprocessableEntity, err)
		return nil
	}

	file, err := store.CreateFile(&fileModel)

	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, file)
}

//UpdateFile is func
func UpdateFile(c echo.Context) error {
	FileModel := model.File{}

	err := c.Bind(&FileModel)

	if err != nil {
		c.JSON(http.StatusBadRequest, err)
		return nil
	}
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)

	file, err := store.UpdateFile(&FileModel, uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, err)

	}
	return c.JSON(http.StatusOK, file)
}

//DeleteFile is func
func DeleteFile(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	if err := store.DeleteFile(uint(id)); err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return nil
	}
	return c.JSON(http.StatusOK, id)
}
