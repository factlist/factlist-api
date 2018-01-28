package handler

import (
	"net/http"
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
		err := helper.SaveUploadedFile(files[i], files[i].Filename)

		location, err := helper.AddFileToS3("uploads", "./"+files[i].Filename, files[i])

		f := model.File{Type: files[i].Header["Content-Type"][0], Source: location, UserID: UserID}

		modelFiles = append(modelFiles, f)

		if err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}
	}

	reportModel.Text = c.FormValue("text")
	reportModel.UserID = UserID

	report, _ := store.CreateReport(&reportModel, modelFiles, modelLinks)

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

	for _, link := range m.Value["report_links[]"] {
		l := model.Link{URL: string(link)}
		modelLinks = append(modelEvidenceLinks, l)
	}

	for _, link := range m.Value["evidence_links[]"] {
		l := model.Link{URL: string(link)}
		modelEvidenceLinks = append(modelLinks, l)
	}

	reportfiles := m.File["report_files[]"]
	evidenceFiles := m.File["evidence_files[]"]

	if len(reportfiles) != 0 {
		for i := range reportfiles {
			err := helper.SaveUploadedFile(reportfiles[i], reportfiles[i].Filename)

			if err != nil {
				return c.JSON(http.StatusInternalServerError, err)
			}

			location, err := helper.AddFileToS3("uploads", "./"+reportfiles[i].Filename, reportfiles[i])

			f := model.File{Type: reportfiles[i].Header["Content-Type"][0], Source: location, UserID: UserID}

			modelFiles = append(modelFiles, f)

			if err != nil {
				return c.JSON(http.StatusInternalServerError, err)
			}
		}
	}

	if len(evidenceFiles) != 0 {
		for i := range evidenceFiles {
			err := helper.SaveUploadedFile(evidenceFiles[i], evidenceFiles[i].Filename)

			if err != nil {
				return c.JSON(http.StatusInternalServerError, err)
			}

			location, err := helper.AddFileToS3("uploads", "./"+evidenceFiles[i].Filename, evidenceFiles[i])

			f := model.File{Type: evidenceFiles[i].Header["Content-Type"][0], Source: location, UserID: UserID}

			modelEvidenceFiles = append(modelEvidenceFiles, f)

			if err != nil {
				return c.JSON(http.StatusInternalServerError, err)
			}
		}

	}

	reportModel.Text = c.FormValue("report_text")
	reportModel.UserID = UserID

	evidenceModel.Text = c.FormValue("evidence_text")
	evidenceModel.UserID = UserID
	evidenceModel.Status = c.FormValue("evidence_status")

	report, err := store.UpdateReport(&reportModel, &evidenceModel, modelFiles, modelLinks, modelEvidenceFiles, modelEvidenceLinks, uint(id))

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
