FROM scratch
ADD factlist-api /
EXPOSE 8884
ENTRYPOINT ["./factlist-api"]
