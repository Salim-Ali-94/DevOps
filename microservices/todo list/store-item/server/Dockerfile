FROM golang:1.20

WORKDIR /app

COPY . .

RUN go get

EXPOSE 8081

CMD ["go", "run", "api.go", "constants.go", "todo.go"]
