# Dockerfile para Docker Scout CLI (desde la raíz)
FROM golang:1.22-alpine AS builder

WORKDIR /app

# Copiar archivos de Go
COPY go.mod go.sum ./
RUN go mod download

# Copiar código fuente (desde la raíz)
COPY main.go ./

# Compilar el CLI principal
RUN CGO_ENABLED=0 GOOS=linux go build -o scout-cli .

# Imagen final
FROM alpine:latest

# Instalar certificados CA
RUN apk --no-cache add ca-certificates

WORKDIR /root/

# Copiar el binario compilado
COPY --from=builder /app/scout-cli .

# Hacer ejecutable
RUN chmod +x ./scout-cli

# Punto de entrada
ENTRYPOINT ["./scout-cli"]