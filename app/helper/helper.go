package helper

import (
	"fmt"

	"github.com/spf13/viper"
)

// import (
// 	"bytes"
// 	"fmt"
// 	"net/http"
// 	"os"

// 	"github.com/aws/aws-sdk-go/aws"
// 	"github.com/aws/aws-sdk-go/aws/session"
// 	"github.com/aws/aws-sdk-go/service/s3"
// 	"github.com/spf13/viper"
// )

// TODO fill these in!
// const (
// 	S3_REGION = ""
// 	S3_BUCKET = ""
// )

//SetConfig is file configuration
func SetConfig(path string) *viper.Viper {
	v := viper.New()
	v.SetConfigName("config")
	v.SetConfigType("toml")
	v.AutomaticEnv()

	v.AddConfigPath(path)

	err := v.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("Invalid application configuration: %s", err))
	}
	return v
}

// // AddFileToS3 will upload a single file to S3, it will require a pre-built aws session
// // and will set file info like content type and encryption on the uploaded file.
// func AddFileToS3(s *session.Session, fileDir string) error {

// 	// Open the file for use
// 	file, err := os.Open(fileDir)
// 	if err != nil {
// 		return err
// 	}
// 	defer file.Close()

// 	// Get file size and read the file content into a buffer
// 	fileInfo, _ := file.Stat()
// 	var size int64 = fileInfo.Size()
// 	buffer := make([]byte, size)
// 	file.Read(buffer)

// 	// Config settings: this is where you choose the bucket, filename, content-type etc.
// 	// of the file you're uploading.
// 	_, err = s3.New(s).PutObject(&s3.PutObjectInput{
// 		Bucket:               aws.String(S3_BUCKET),
// 		Key:                  aws.String(fileDir),
// 		ACL:                  aws.String("private"),
// 		Body:                 bytes.NewReader(buffer),
// 		ContentLength:        aws.Int64(size),
// 		ContentType:          aws.String(http.DetectContentType(buffer)),
// 		ContentDisposition:   aws.String("attachment"),
// 		ServerSideEncryption: aws.String("AES256"),
// 	})
// 	return err
// }
