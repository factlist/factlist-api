package handler

import (
	"net/http"
	"strconv"

	"github.com/factlist/factlist/app/model"
	"github.com/factlist/factlist/app/store"
	"github.com/labstack/echo"
)

//GetReportList is func
func GetReportList(c echo.Context) error {
	reports, err := store.GetReportList()
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, reports)
}

//GetReport is func
func GetReport(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	report, err := store.GetReport(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, report)
}

//CreateReport is func
func CreateReport(c echo.Context) error {
	reportModel := model.Report{}

	err := c.Bind(&reportModel)

	if err := reportModel.Validate(); err != nil {
		c.JSON(http.StatusUnprocessableEntity, err)
		return nil
	}

	report, err := store.CreateReport(&reportModel)

	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, report)
}

//UpdateReport is func
func UpdateReport(c echo.Context) error {
	ReportModel := model.Report{}

	err := c.Bind(&ReportModel)

	if err != nil {
		c.String(http.StatusBadRequest, err.Error())
		return nil
	}
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)

	report, err := store.UpdateReport(&ReportModel, uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, err)

	}
	return c.JSON(http.StatusOK, report)
}

//DeleteReport is func
func DeleteReport(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	if err := store.DeleteReport(uint(id)); err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return nil
	}
	return c.JSON(http.StatusOK, id)
}
