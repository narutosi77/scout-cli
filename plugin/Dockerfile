# C:\Users\cever\Documents\scout-cli\plugin\Dockerfile
# Imagen base para tu plugin. alpine es ligera.
FROM alpine:latest

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el binario compilado de tu plugin al contenedor
# Asume que 'scout-plugin-binary' existe en la raíz de la carpeta 'plugin/'
COPY ./scout-plugin-binary /usr/local/bin/scout-plugin

# Copia el archivo de configuración del plugin
# El nombre del archivo aquí es importante para que Docker lo detecte
COPY config.json /etc/docker/plugins/scout-plugin.json

# Define el punto de entrada de tu plugin
# Este comando se ejecutará cuando el contenedor del plugin se inicie
ENTRYPOINT ["/usr/local/bin/scout-plugin"]