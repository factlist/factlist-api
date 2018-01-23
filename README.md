# factlist (In development)


## Quick Run

If you are using Docker, you can use the following command to easily try Factlist. Only external dependency is MySQL.


```
docker run factlist/factlist-api:latest \
	-e DB_HOST=localhost \ # Defaults to localhost
	-e DB_NAME =... \
	-e DB_USERNAME =... \
	-e DB_PASSWORD =... \
	-e DB_PORT=3306 \ # Defaults to 3306
	-e HOST=... \
	-e PORT=... \
	-e JWT_SIGNING_KEY=... \
	-e ACCESS_KEY_ID=... \
	-e SECRET_KEY=... \
	-e S3_REGION=... \
	-e S3_BUCKET=... \
	-e S3_ROOT_PATH=...
```