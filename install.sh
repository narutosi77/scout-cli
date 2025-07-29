#!/bin/bash
set -euo pipefail

CLI_NAME="scout-cli"
REPO_OWNER="narutosi77"
REPO_NAME="scout-cli"
INSTALL_DIR="/usr/local/bin"

echo "🚀 Instalando $CLI_NAME desde $REPO_OWNER/$REPO_NAME..."

# Obtener la última versión del release
LATEST_VERSION=$(curl -sL "https://api.github.com/repos/$REPO_OWNER/$REPO_NAME/releases/latest" | grep -oP '"tag_name": "\K(.*)(?=")')

if [ -z "$LATEST_VERSION" ]; then
    echo "❌ Error: No se pudo encontrar la última versión del CLI."
    exit 1
fi

DOWNLOAD_URL_BASE="https://github.com/$REPO_OWNER/$REPO_NAME/releases/download/$LATEST_VERSION"
echo "✅ Última versión encontrada: $LATEST_VERSION"

# Detectar sistema operativo y arquitectura
OS=$(uname -s)
ARCH=$(uname -m)
echo "🖥️  Sistema detectado: $OS $ARCH"

case "$OS" in
    Linux*)
        case "$ARCH" in
            x86_64)
                FILE_NAME="$CLI_NAME-linux-amd64"
                ;;
            arm64|aarch64)
                FILE_NAME="$CLI_NAME-linux-arm64"
                ;;
            *)
                echo "❌ Arquitectura de Linux no soportada: $ARCH"
                exit 1
                ;;
        esac
        ;;
    Darwin*)
        case "$ARCH" in
            x86_64)
                FILE_NAME="$CLI_NAME-darwin-amd64"
                ;;
            arm64)
                FILE_NAME="$CLI_NAME-darwin-arm64"
                ;;
            *)
                echo "❌ Arquitectura de macOS no soportada: $ARCH"
                exit 1
                ;;
        esac
        ;;
    CYGWIN*|MINGW32*|MSYS*|MINGW64*)
        echo "🪟 Detectado Windows."
        echo "   Descarga manual desde: $DOWNLOAD_URL_BASE/$CLI_NAME-windows-amd64.exe"
        exit 0
        ;;
    *)
        echo "❌ Sistema operativo no soportado: $OS"
        exit 1
        ;;
esac

FULL_DOWNLOAD_URL="$DOWNLOAD_URL_BASE/$FILE_NAME"
echo "📥 Descargando binario desde: $FULL_DOWNLOAD_URL"

# Crear directorio temporal
TEMP_DIR=$(mktemp -d)
TEMP_BINARY="$TEMP_DIR/$CLI_NAME"

# Descargar el binario
if ! curl -L -o "$TEMP_BINARY" "$FULL_DOWNLOAD_URL"; then
    echo "❌ Error al descargar el binario"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Verificar descarga
if [ ! -f "$TEMP_BINARY" ] || [ ! -s "$TEMP_BINARY" ]; then
    echo "❌ Error: El binario descargado está vacío"
    rm -rf "$TEMP_DIR"
    exit 1
fi

# Hacer ejecutable
chmod +x "$TEMP_BINARY"

# Instalar
echo "📦 Instalando en $INSTALL_DIR/$CLI_NAME..."
if [ -w "$INSTALL_DIR" ]; then
    cp "$TEMP_BINARY" "$INSTALL_DIR/$CLI_NAME"
else
    sudo cp "$TEMP_BINARY" "$INSTALL_DIR/$CLI_NAME"
fi

# Limpiar
rm -rf "$TEMP_DIR"

echo "🎉 ¡Instalación completada!"
echo "📍 $CLI_NAME versión $LATEST_VERSION instalado"

# Verificar
if command -v "$CLI_NAME" >/dev/null 2>&1; then
    "$CLI_NAME" --version
    echo "✅ $CLI_NAME está listo para usar!"
else
    echo "⚠️  Añade $INSTALL_DIR a tu PATH"
fi