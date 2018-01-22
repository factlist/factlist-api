package handler

import (
	"net/http"
	"strconv"

	"github.com/factlist/factlist-api/api/model"
	"github.com/factlist/factlist-api/api/store"
	"github.com/labstack/echo"
)

//GetLinkList is func
func GetLinkList(c echo.Context) error {
	links, err := store.GetLinkList()
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, links)
}

//GetLink is func
func GetLink(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	link, err := store.GetLink(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, link)
}

//CreateLink is func
func CreateLink(c echo.Context) error {
	linkModel := model.Link{}

	err := c.Bind(&linkModel)

	if err := linkModel.Validate(); err != nil {
		c.JSON(http.StatusUnprocessableEntity, err)
		return nil
	}

	link, err := store.CreateLink(&linkModel)

	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, link)
}

//UpdateLink is func
func UpdateLink(c echo.Context) error {
	linkModel := model.Link{}

	err := c.Bind(&linkModel)

	if err != nil {
		c.String(http.StatusBadRequest, err.Error())
		return nil
	}
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)

	link, err := store.UpdateLink(&linkModel, uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, err)

	}
	return c.JSON(http.StatusOK, link)
}

//DeleteLink is func
func DeleteLink(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	if err := store.DeleteLink(uint(id)); err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return nil
	}
	return c.JSON(http.StatusOK, id)
}
