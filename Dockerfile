FROM golang:1.9 AS builder
RUN go get -u github.com/golang/dep/cmd/dep
RUN mkdir -p /go/src/github.com/factlist/factlist-api
WORKDIR /go/src/github.com/factlist/factlist-api
COPY . .
RUN dep ensure
RUN go build -o factlistapp ./cmd/factlist/api.go
EXPOSE 8884
ENTRYPOINT ["./factlistapp"]
