package handler

// import (
// 	"bytes"
// 	"fmt"
// 	"io/ioutil"
// 	"net/http"
// )

// func testGetMockUserCredentials() {
// 	client := &http.Client{
// 		CheckRedirect: redirectPolicyFunc,
// 	}

// 	var jsonString = []byte(`{"username": "enis", "email": "enis@bobmail.com", "password": "123456"}`)

// 	req, err := http.NewRequest("POST", "/api/register", bytes.NewBuffer(jsonString))
// 	req.Header.Set("Content-Type", "application/json")

// 	resp, err := client.Do(req)
// 	if err != nil {
// 		fmt.Print(err)
// 	}

// 	defer resp.Body.Close()

// 	fmt.Println("response Status:", resp.Status)
// 	fmt.Println("response Headers:", resp.Header)
// 	body, _ := ioutil.ReadAll(resp.Body)
// 	fmt.Println("response Body:", string(body))
// }

// func getClaimList() {
// 	client := &http.Client{
// 		CheckRedirect: redirectPolicyFunc,
// 	}

// 	req, err := http.NewRequest("GET", "/api/claims", nil)
// 	req.Header.Add("Authorization", "Bearer TOKEN")
// }
