FROM golang:latest
RUN mkdir /factlist
ADD . /factlist/
WORKDIR /app
RUN make build
CMD ["./factlist"]
