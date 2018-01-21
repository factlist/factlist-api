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
	UserID, _ := strconv.Atoi(c.FormValue("user_id"))

	evidenceModel := model.Evidence{}

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

	evidenceModel.Text = c.FormValue("text")
	evidenceModel.Status = c.FormValue("status")
	evidenceModel.UserID = UserID

	evidence, err := store.CreateEvidence(&evidenceModel, modelFiles, modelLinks)

	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}

	return c.JSON(http.StatusOK, evidence)

}

//UpdateEvidence is func
func UpdateEvidence(c echo.Context) error {

	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	UserID, _ := strconv.Atoi(c.FormValue("user_id"))

	evidenceModel := model.Evidence{}

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

	evidenceModel.Text = c.FormValue("text")
	evidenceModel.Status = c.FormValue("status")
	evidenceModel.UserID = UserID

	evidence, err := store.UpdateEvidence(&evidenceModel, modelFiles, modelLinks, uint(id))

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
