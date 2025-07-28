#!/bin/bash
set -euo pipefail

CLI_NAME="scout-cli"
REPO_OWNER="narutosi77" # ¡IMPORTANTE! Reemplaza con tu nombre de usuario de GitHub
REPO_NAME="scout-cli" # ¡IMPORTANTE! Reemplaza con el nombre de tu repositorio
DOWNLOAD_DIR="/usr/local/bin" # Directorio donde instalar el binario. Requiere 'sudo' si no es un directorio de usuario.

echo "Descargando la última versión de ${CLI_NAME} desde ${REPO_OWNER}/${REPO_NAME}..."

# Obtener la última versión del release
LATEST_VERSION=$(curl -sL "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases/latest" | grep -oP '"tag_name": "\K(.*)(?=")')

if [ -z "$LATEST_VERSION" ]; then
    echo "Error: No se pudo encontrar la última versión del CLI. Asegúrate de que haya releases publicados."
    exit 1
fi

DOWNLOAD_URL_BASE="https://github.com/${REPO_OWNER}/${REPO_NAME}/releases/download/${LATEST_VERSION}"

echo "Última versión encontrada: ${LATEST_VERSION}"

case "$(uname -s)" in
    Linux*)
        echo "Detectado Linux..."
        ARCH=$(uname -m)
        if [ "$ARCH" == "x86_64" ]; then
            FILE_NAME="${CLI_NAME}-linux-amd64"
        elif [ "$ARCH" == "arm64" ] || [ "$ARCH" == "aarch64" ]; then
            FILE_NAME="${CLI_NAME}-linux-arm64" # Si también compilas para ARM
        else
            echo "Arquitectura de Linux no soportada: $ARCH"
            exit 1
        fi
        ;;
    Darwin*)
        echo "Detectado macOS..."
        ARCH=$(uname -m)
        if [ "$ARCH" == "x86_64" ]; then
            FILE_NAME="${CLI_NAME}-darwin-amd64"
        elif [ "$ARCH" == "arm64" ]; then
            FILE_NAME="${CLI_NAME}-darwin-arm64" # Si también compilas para Apple Silicon
        else
            echo "Arquitectura de macOS no soportada: $ARCH"
            exit 1
        fi
        ;;
    # Para Windows, la instalación es diferente (descargar .exe y añadir a PATH).
    # Este script no lo cubre directamente para instalación automática.
    CYGWIN*|MINGW32*|MSYS*|MINGW64*)
        echo "Detectado Windows. Por favor, descarga el archivo .exe manualmente:"
        echo "${DOWNLOAD_URL_BASE}/${CLI_NAME}-windows-amd64.exe"
        exit 0
        ;;
    *)
        echo "Sistema operativo no soportado para instalación automática: $(uname -s)"
        echo "Por favor, descarga el binario manualmente desde: ${DOWNLOAD_URL_BASE}"
        exit 1
        ;;
esac

FULL_DOWNLOAD_URL="${DOWNLOAD_URL_BASE}/${FILE_NAME}"
echo "Descargando binario desde: ${FULL_DOWNLOAD_URL}"

# Descargar el binario. Usar 'sudo' si DOWNLOAD_DIR requiere permisos.
# Considera descargar a un directorio temporal y luego moverlo si quieres evitar permisos de escritura en root de inicio.
if [ -w "$DOWNLOAD_DIR" ]; then
    curl -L -o "${DOWNLOAD_DIR}/${CLI_NAME}" "${FULL_DOWNLOAD_URL}"
else
    echo "Necesita permisos de sudo para instalar en ${DOWNLOAD_DIR}. Solicitando..."
    sudo curl -L -o "${DOWNLOAD_DIR}/${CLI_NAME}" "${FULL_DOWNLOAD_URL}"
fi

# Hacerlo ejecutable
chmod +x "${DOWNLOAD_DIR}/${CLI_NAME}"

echo "----------------------------------------------------"
echo "${CLI_NAME} versión ${LATEST_VERSION} instalado en ${DOWNLOAD_DIR}/${CLI_NAME}"
echo "----------------------------------------------------"
echo "Verificando la instalación:"
"${DOWNLOAD_DIR}/${CLI_NAME}" --version # Intenta ejecutar el CLI para verificar

echo "¡Instalación completada!"
echo "Asegúrate de que ${DOWNLOAD_DIR} esté en tu PATH para ejecutar '${CLI_NAME}' directamente."