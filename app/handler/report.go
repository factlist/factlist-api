package handler

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"

	"github.com/factlist/factlist/app/helper"
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

	UserID, _ := strconv.Atoi(c.FormValue("user_id"))

	reportModel := model.Report{}

	var modelFiles []model.File
	var modelLinks []model.Link

	m, _ := c.MultipartForm()

	for _, link := range m.Value["links[]"] {
		l := model.Link{URL: string(link)}
		modelLinks = append(modelLinks, l)
	}

	files := m.File["files[]"]

	for i := range files {
		file, err := files[i].Open()
		defer file.Close()
		if err != nil {
			fmt.Println(err)
			return c.JSON(http.StatusInternalServerError, err)
		}

		dst, err := os.Create(files[i].Filename)
		defer dst.Close()
		if err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}

		if _, err := io.Copy(dst, file); err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}

		location, err := helper.AddFileToS3("uploads", "./"+files[i].Filename, files[i])

		f := model.File{Type: files[i].Header["Content-Type"][0], Source: location, UserID: UserID}

		modelFiles = append(modelFiles, f)

		if err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}
	}

	reportModel.Text = c.FormValue("text")
	reportModel.UserID = UserID

	report, err := store.CreateReport(&reportModel, modelFiles, modelLinks)

	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}

	return c.JSON(http.StatusOK, report)
}

//UpdateReport is func
func UpdateReport(c echo.Context) error {

	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	UserID, _ := strconv.Atoi(c.FormValue("user_id"))

	reportModel := model.Report{}

	var modelFiles []model.File
	var modelLinks []model.Link

	// if err := evidenceModel.Validate(); err != nil {
	// 	c.JSON(http.StatusUnprocessableEntity, err)
	// 	return nil
	// }

	m, _ := c.MultipartForm()

	for _, link := range m.Value["links[]"] {
		l := model.Link{URL: string(link)}
		modelLinks = append(modelLinks, l)
	}

	files := m.File["files[]"]

	for i := range files {
		file, err := files[i].Open()
		defer file.Close()
		if err != nil {
			fmt.Println(err)
			return c.JSON(http.StatusInternalServerError, err)
		}

		dst, err := os.Create(files[i].Filename)
		defer dst.Close()
		if err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}

		if _, err := io.Copy(dst, file); err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}

		location, err := helper.AddFileToS3("uploads", "./"+files[i].Filename, files[i])

		f := model.File{Type: files[i].Header["Content-Type"][0], Source: location, UserID: UserID}

		modelFiles = append(modelFiles, f)

		if err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}
	}

	reportModel.Text = c.FormValue("text")
	reportModel.UserID = UserID

	report, err := store.UpdateReport(&reportModel, modelFiles, modelLinks, uint(id))

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
