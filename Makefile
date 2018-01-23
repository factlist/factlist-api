all:  # run
	echo "MAKEFILE"
dep:
	go get -u github.com/golang/dep/cmd/dep
	dep ensure
build: dep
	CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o factlist-api ./cmd/factlist/api.go
dockerbuild: build
	docker build -t factlist/factlist-api .
dockerrun:
	docker run factlist/factlist-api:latest #ENV

test:
	echo "TEST"
run:
	./factlist-api #ENV
