package handler

import (
	"fmt"
	"io"
	"net/http"
	"os"
	"strconv"

	"github.com/factlist/factlist-api/api/helper"
	"github.com/factlist/factlist-api/api/model"
	"github.com/factlist/factlist-api/api/store"
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
	evidenceModel := model.Evidence{}

	var modelFiles []model.File
	var modelLinks []model.Link
	var modelEvidenceFiles []model.File
	var modelEvidenceLinks []model.Link

	m, _ := c.MultipartForm()

	for _, link := range m.Value["links[]"] {
		l := model.Link{URL: string(link)}
		modelEvidenceLinks = append(modelEvidenceLinks, l)
	}

	for _, link := range m.Value["evidence_links[]"] {
		l := model.Link{URL: string(link)}
		modelLinks = append(modelLinks, l)
	}

	files := m.File["files[]"]
	evidenceFiles := m.File["evidence_files[]"]

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

	for i := range evidenceFiles {
		file, err := files[i].Open()
		defer file.Close()
		if err != nil {
			fmt.Println(err)
			return c.JSON(http.StatusInternalServerError, err)
		}

		dst, err := os.Create(evidenceFiles[i].Filename)
		defer dst.Close()
		if err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}

		if _, err := io.Copy(dst, file); err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}

		location, err := helper.AddFileToS3("uploads", "./"+evidenceFiles[i].Filename, evidenceFiles[i])

		f := model.File{Type: files[i].Header["Content-Type"][0], Source: location, UserID: UserID}

		modelEvidenceFiles = append(modelEvidenceFiles, f)

		if err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}
	}

	reportModel.Text = c.FormValue("report_text")
	reportModel.UserID = UserID

	evidenceModel.Text = c.FormValue("evidence_text")
	evidenceModel.UserID = UserID
	evidenceModel.Status = c.FormValue("evidence_status")

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
