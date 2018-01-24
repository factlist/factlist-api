package helper

import (
	"fmt"
	"log"
	"mime/multipart"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3/s3manager"
	"github.com/spf13/viper"
)

//SetConfig is file configuration
func SetConfig(path string) *viper.Viper {
	v := viper.New()
	v.AutomaticEnv()
	v.SetConfigName("config")
	v.SetConfigType("toml")

	v.AddConfigPath(path)

	err := v.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("Invalid application configuration: %s", err))
	}
	return v
}

// AddFileToS3 will upload a single file to S3, it will require a pre-built aws session
// and will set file info like content type and encryption on the uploaded file.
func AddFileToS3(bucketPath, path string, file *multipart.FileHeader) (string, error) {
	var s3Bucket = os.Getenv("S3_BUCKET")
	sess := session.Must(session.NewSession(&aws.Config{
		Region:      aws.String(os.Getenv("S3_REGION")),
		Credentials: credentials.NewStaticCredentials(os.Getenv("ACCESS_KEY_ID"), os.Getenv("SECRET_KEY"), ""),
	}))

	osFile, err := os.Open(path)
	if err != nil {
		log.Fatalln("Error when opening", path, err)
	}

	filename := bucketPath + "/" + file.Filename

	upparams := &s3manager.UploadInput{
		Bucket:      &s3Bucket,
		Key:         &filename,
		Body:        osFile,
		ContentType: aws.String(file.Header["Content-Type"][0]),
		ACL:         aws.String("public-read"),
	}

	uploader := s3manager.NewUploader(sess)

	_, err = uploader.Upload(upparams)
	if err != nil {
		log.Fatalln("Error when uploading to S3", err)
		return "", err
	}

	os.Remove(osFile.Name())

	s3path := os.Getenv("S3_ROOT_PATH") + "/" + os.Getenv("S3_BUCKET") + "/" + filename

	return s3path, nil
}
