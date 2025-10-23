FROM golang:1.22-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./go.mod go.sum
RUN go mod download

COPY . .

RUN go build -o /app/server ./cmd/api

FROM alpine:latest

WORKDIR /root/

COPY --from=builder /app/server .

EXPOSE 8080

CMD ["./server"]
