package handler

import (
	"net/http"
	"strconv"

	"github.com/labstack/echo"
	"github.com/onerciller/factlist/app/model"
	"github.com/onerciller/factlist/app/store"
)

//GetQuestionList is func
func GetQuestionList(c echo.Context) error {
	questions, err := store.GetQuestionList()
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, questions)
}

//GetQuestion is func
func GetQuestion(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	question, err := store.GetQuestion(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, question)
}

//CreateQuestion is func
func CreateQuestion(c echo.Context) error {
	questionModel := model.Question{}

	err := c.Bind(&questionModel)

	if err := questionModel.Validate(); err != nil {
		c.JSON(http.StatusUnprocessableEntity, err)
		return nil
	}

	question, err := store.CreateQuestion(&questionModel)

	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, question)
}

//UpdateQuestion is func
func UpdateQuestion(c echo.Context) error {
	QuestionModel := model.Question{}

	err := c.Bind(&QuestionModel)

	if err != nil {
		c.String(http.StatusBadRequest, err.Error())
		return nil
	}
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)

	question, err := store.UpdateQuestion(&QuestionModel, uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, err)

	}
	return c.JSON(http.StatusOK, question)
}

//DeleteQuestion is func
func DeleteQuestion(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	if err := store.DeleteQuestion(uint(id)); err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return nil
	}
	return c.JSON(http.StatusOK, id)
}
