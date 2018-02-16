package handler

import (
	"net/http"
	"strconv"

	"github.com/factlist/factlist-api/api/helper"
	"github.com/factlist/factlist-api/api/model"
	"github.com/factlist/factlist-api/api/store"
	"github.com/labstack/echo"
)

//GetClaimList is func
func GetClaimList(c echo.Context) error {
	claims, err := store.GetClaimList()
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, claims)
}

//GetClaim is func
func GetClaim(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	claim, err := store.GetClaim(uint(id))
	if err != nil {
		c.JSON(http.StatusNotFound, err)
	}
	return c.JSON(http.StatusOK, claim)
}

//CreateClaim is func
func CreateClaim(c echo.Context) error {

	UserID, _ := strconv.Atoi(c.FormValue("user_id"))

	claimModel := model.Claim{}

	var modelFiles []model.File
	var modelLinks []model.Link

	m, _ := c.MultipartForm()

	for _, link := range m.Value["claim_links[]"] {
		l := model.Link{URL: string(link), UserID: UserID}
		modelLinks = append(modelLinks, l)
	}

	files := m.File["claim_files[]"]

	for i := range files {
		err := helper.SaveUploadedFile(files[i], files[i].Filename)

		location, err := helper.AddFileToS3("uploads", "./"+files[i].Filename, files[i])

		f := model.File{Type: files[i].Header["Content-Type"][0], Source: location, UserID: UserID}

		modelFiles = append(modelFiles, f)

		if err != nil {
			return c.JSON(http.StatusInternalServerError, err)
		}
	}

	claimModel.Text = c.FormValue("claim_text")
	claimModel.UserID = UserID

	claim, _ := store.CreateClaim(&claimModel, modelFiles, modelLinks)

	return c.JSON(http.StatusOK, claim)
}

//UpdateClaim is func
func UpdateClaim(c echo.Context) error {

	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	UserID, _ := strconv.Atoi(c.FormValue("user_id"))

	claimModel := model.Claim{}
	evidenceModel := model.Evidence{}

	var modelFiles []model.File
	var modelLinks []model.Link
	var modelEvidenceFiles []model.File
	var modelEvidenceLinks []model.Link

	m, _ := c.MultipartForm()

	for _, link := range m.Value["claim_links[]"] {
		l := model.Link{URL: string(link)}
		modelLinks = append(modelEvidenceLinks, l)
	}

	for _, link := range m.Value["evidence_links[]"] {
		l := model.Link{URL: string(link), UserID: UserID}
		modelEvidenceLinks = append(modelLinks, l)
	}

	claimfiles := m.File["claim_files[]"]
	evidenceFiles := m.File["evidence_files[]"]

	if len(claimfiles) != 0 {
		for i := range claimfiles {
			err := helper.SaveUploadedFile(claimfiles[i], claimfiles[i].Filename)

			if err != nil {
				return c.JSON(http.StatusInternalServerError, err)
			}

			location, err := helper.AddFileToS3("uploads", "./"+claimfiles[i].Filename, claimfiles[i])

			f := model.File{Type: claimfiles[i].Header["Content-Type"][0], Source: location, UserID: UserID}

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

	claimModel.Text = c.FormValue("claim_text")
	claimModel.UserID = UserID

	evidenceModel.Text = c.FormValue("evidence_text")
	evidenceModel.UserID = UserID
	evidenceModel.Status = c.FormValue("evidence_status")

	claim, err := store.UpdateClaim(&claimModel, &evidenceModel, modelFiles, modelLinks, modelEvidenceFiles, modelEvidenceLinks, uint(id))

	if err != nil {
		c.JSON(http.StatusNotFound, err)

	}

	return c.JSON(http.StatusOK, claim)
}

//DeleteClaim is func
func DeleteClaim(c echo.Context) error {
	id, _ := strconv.ParseUint(c.Param("id"), 10, 32)
	if err := store.DeleteClaim(uint(id)); err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return nil
	}
	return c.JSON(http.StatusOK, id)
}
