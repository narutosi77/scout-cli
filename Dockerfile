# Dockerfile para generar documentación
# Este Dockerfile es para crear una imagen que ejecuta generate_docs.py
# y guarda los archivos Markdown generados.

# Usamos una imagen base de Python ligera.
FROM python:3.9-slim

WORKDIR /app

# Copiar el script de Python que generará la documentación Markdown
# Asume que generate_docs.py no necesita un binario de docker-scout funcionando
COPY generate_docs.py /app/generate_docs.py

# Si generate_docs.py tiene dependencias de Python (ej. click, markdown), instálalas
# COPY requirements.txt /app/requirements.txt
# RUN pip install --no-cache-dir -r /app/requirements.txt

# Crear el directorio para almacenar los archivos Markdown generados.
RUN mkdir -p /app/docs_output_path # Nombre más genérico para la salida

# Ejecuta el script de generación de documentación durante la construcción de la imagen.
# Los archivos generados estarán en /app/docs_output_path dentro del contenedor.
RUN python /app/generate_docs.py

# Este Dockerfile no necesita un ENTRYPOINT/CMD si su único propósito es generar docs durante el build.
# Si la intención es que el contenedor sea útil para algo más después, se puede definir.