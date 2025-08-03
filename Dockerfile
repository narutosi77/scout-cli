# ---- Etapa 1: El Constructor (Builder) ----
# Usamos una imagen oficial de Go para construir la aplicación.
FROM golang:1.24-alpine AS builder

# Establecemos el directorio de trabajo dentro del contenedor.
WORKDIR /app

# Copiamos los archivos de módulos de Go primero para aprovechar la caché de Docker.
COPY go.mod go.sum ./

# Descargamos las dependencias. Si no hay, este comando no hace nada pero no falla.
# Esto es más robusto que el vendoring para un proyecto simple.
RUN go mod download

# Ahora, copiamos TODO el resto del código fuente y otros archivos.
# El punto '.' significa "todo en el directorio actual del proyecto".
COPY . .

# Compilamos la aplicación de Go, creando un binario estático para Linux.
RUN CGO_ENABLED=0 GOOS=linux go build -o /app/scout-cli .


# ---- Etapa 2: La Imagen Final (Mucho más pequeña) ----
# Empezamos desde una imagen base mínima.
FROM alpine:latest

# (Buena práctica) Instalar certificados para conexiones HTTPS.
RUN apk --no-cache add ca-certificates

# Copiamos ÚNICAMENTE el programa ya compilado desde la etapa del constructor.
# Lo ponemos en un directorio estándar para binarios.
COPY --from=builder /app/scout-cli /usr/local/bin/scout-cli

# Establecemos el comando que se ejecutará cuando el contenedor se inicie.
ENTRYPOINT ["/usr/local/bin/scout-cli"]