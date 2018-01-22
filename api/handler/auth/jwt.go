package auth

import (
	"net/http"
	"time"

	"github.com/labstack/echo"

	jwt "gopkg.in/dgrijalva/jwt-go.v3"

	"github.com/factlist/factlist/api/helper"
	"github.com/factlist/factlist/api/model"
	"github.com/factlist/factlist/api/store"
)

// PostLogin is jwt token handler
func PostLogin(c echo.Context) error {

	userModel := model.User{}
	if c.Bind(&userModel) != nil {
		return c.JSON(http.StatusBadRequest, "Missing Email or Password")
	}

	u, err := store.GetUserByLogin(userModel.Email, userModel.Password)

	if err != nil {
		return c.JSON(http.StatusUnauthorized, "Incorrect Email or Password")

	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": u.ID,
		"iat": time.Now().UTC().Unix(),
		"exp": time.Now().UTC().Unix() + (500 * 1000),
		"nbf": time.Now().UTC().Unix() + (500 * 1000),
	})

	config := helper.SetConfig(".")
	tokenString, err := token.SignedString([]byte(config.GetString("jwt_signing_key")))

	if err != nil {
		return c.JSON(http.StatusInternalServerError, err)
	}

	data := map[string]string{
		"token": tokenString,
	}

	return c.JSON(http.StatusOK, data)

}

// PostRegister is user register handler
func PostRegister(c echo.Context) error {
	userModel := model.User{}
	err := c.Bind(&userModel)

	if err != nil {
		c.JSON(http.StatusBadRequest, err)
		return nil
	}

	if err != nil {
		c.JSON(http.StatusBadRequest, err)
		return nil
	}

	user, err := store.CreateUser(&userModel)

	if err != nil {
		c.JSON(http.StatusInternalServerError, err)
		return nil
	}

	return c.JSON(http.StatusOK, user)
}
