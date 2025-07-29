# Dockerfile para el Plugin de Docker Scout
FROM alpine:latest

# Instalar certificados CA
RUN apk --no-cache add ca-certificates

WORKDIR /app

# Copiar el binario compilado del plugin
COPY scout-plugin-binary /usr/local/bin/scout-plugin

# Copiar el archivo de configuración del plugin
COPY config.json /etc/docker/plugins/scout-plugin.json

# Hacer el binario ejecutable
RUN chmod +x /usr/local/bin/scout-plugin

# Punto de entrada del plugin
ENTRYPOINT ["/usr/local/bin/scout-plugin"]