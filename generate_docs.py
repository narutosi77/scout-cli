# .github/workflows/generate_docs.yaml
name: Build and Deploy Docs

on:
  push:
    branches:
      - main # Desplegar cuando se haga push a la rama principal
  workflow_dispatch: # Permite ejecutar el workflow manualmente desde la UI de GitHub

jobs:
  generate-and-deploy-docs:
    runs-on: ubuntu-latest
    permissions:
      contents: write # Necesario para actions/checkout
      pages: write # Permiso necesario para desplegar en GitHub Pages
      id-token: write # Permiso para autenticación OIDC, requerido por actions/deploy-pages

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      # --- Paso 1: Generar los archivos Markdown usando tu Dockerfile.docs y generate_docs.py ---
      - name: Build Docker Image for Markdown Generator
        run: docker build -t markdown-generator -f Dockerfile.docs .
        # Este paso ejecuta generate_docs.py DENTRO de la imagen y genera los .md

      - name: Create temporary container to extract Markdown files
        # Asumiendo que generate_docs.py guarda los Markdown en /app/docs_output_path dentro del contenedor
        # Si tu generate_docs.py guarda en otra ruta, ajusta '/app/docs_output_path'
        run: docker create --name md_container markdown-generator

      - name: Copy generated Markdown files from container
        run: docker cp md_container:/app/docs_output_path/. ./generated_markdown_docs
        # Esto copia los .md generados a una carpeta local 'generated_markdown_docs'

      - name: Remove temporary container
        run: docker rm md_container

      # --- Paso 2: Construir el sitio HTML usando MkDocs a partir de los archivos Markdown generados ---
      # Aquí, necesitamos una imagen diferente que tenga MkDocs instalado.
      # Podemos construirla al vuelo o usar una imagen pre-existente con MkDocs.
      # Crearemos un Dockerfile específico para MkDocs para claridad.

      - name: Create Dockerfile for MkDocs Site Builder
        run: |
          echo "FROM python:3.10-slim-buster" > Dockerfile.mkdocs
          echo "WORKDIR /app" >> Dockerfile.mkdocs
          echo "RUN pip install mkdocs mkdocs-material" >> Dockerfile.mkdocs
          echo "COPY mkdocs.yml ." >> Dockerfile.mkdocs
          echo "COPY generated_markdown_docs/ ./docs/" >> Dockerfile.mkdocs # Copiar los .md generados
          echo "CMD mkdocs build" >> Dockerfile.mkdocs

      - name: Build MkDocs Site Builder Image
        run: docker build -t mkdocs-site-builder -f Dockerfile.mkdocs .

      - name: Create temporary container to extract HTML site
        run: docker create --name site_container mkdocs-site-builder

      - name: Copy generated HTML site from container
        run: docker cp site_container:/app/site/. ./docs_output_for_pages
        # MkDocs genera el sitio en la carpeta 'site' por defecto

      - name: Remove temporary container
        run: docker rm site_container

      # --- Paso 3: Desplegar en GitHub Pages ---
      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload artifact for GitHub Pages
        uses: actions/upload-pages-artifact@v3
        with:
          path: './docs_output_for_pages' # La carpeta que contiene los archivos HTML estáticos

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4