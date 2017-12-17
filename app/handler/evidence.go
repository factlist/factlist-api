package handler

import (
	"net/http"
	"strconv"

	"github.com/labstack/echo"
	"github.com/onerciller/factlist/app/model"
	"github.com/onerciller/factlist/app/store"
)

//GetEvidenceList is func
func GetEvidenceList(c echo.Context) error {
	evidences, err := store.GetEvidenceList()
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, evidences)
}

//GetEvidence is func
func GetEvidence(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	evidence, err := store.GetEvidence(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, evidence)
}

//CreateEvidence is func
func CreateEvidence(c echo.Context) error {
	evidenceModel := model.Evidence{}

	c.Bind(&evidenceModel)

	if err := evidenceModel.Validate(); err != nil {
		c.JSON(http.StatusUnprocessableEntity, err)
		return nil
	}

	evidence, err := store.CreateEvidence(&evidenceModel)

	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}

	return c.JSON(http.StatusOK, evidence)
}

//UpdateEvidence is func
func UpdateEvidence(c echo.Context) error {
	evidenceModel := model.Evidence{}

	err := c.Bind(&evidenceModel)

	if err != nil {
		c.String(http.StatusBadRequest, err.Error())
		return nil
	}
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)

	evidence, err := store.UpdateEvidence(&evidenceModel, uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, err)

	}
	return c.JSON(http.StatusOK, evidence)
}

//DeleteEvidence is func
func DeleteEvidence(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	if err := store.DeleteEvidence(uint(id)); err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return nil
	}
	return c.JSON(http.StatusOK, id)
}
