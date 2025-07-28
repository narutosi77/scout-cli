# generate_docs.py
import os
import subprocess
import shutil

# Esta función se encarga de generar la documentación.
# Asume que MkDocs y sus dependencias ya están instaladas en el entorno del contenedor
# (gracias al Dockerfile.docs y requirements.txt).
def generate_documentation():
    print("Starting documentation generation process...")

    # Asegurarse de que el directorio de salida de MkDocs ('site') esté limpio
    # MkDocs por defecto crea la carpeta 'site' en el WORKDIR.
    output_dir = "site"
    if os.path.exists(output_dir):
        print(f"Cleaning existing output directory: {output_dir}")
        shutil.rmtree(output_dir)

    print("Running mkdocs build command...")
    try:
        # Ejecuta el comando 'mkdocs build'.
        # MkDocs buscará 'mkdocs.yml' y la carpeta 'docs/' en el WORKDIR (/app).
        # La salida HTML se generará en el directorio 'site' dentro del WORKDIR (/app/site).
        subprocess.run(["mkdocs", "build"], check=True, capture_output=True, text=True)
        print("MkDocs build completed successfully.")
        # Imprime la salida y errores de mkdocs para depuración
        # print("MkDocs stdout:\n", result.stdout)
        # print("MkDocs stderr:\n", result.stderr)

    except subprocess.CalledProcessError as e:
        print(f"Error during MkDocs build: {e}")
        print(f"MkDocs stdout:\n{e.stdout}")
        print(f"MkDocs stderr:\n{e.stderr}")
        # Re-raise la excepción para que el paso del workflow falle si mkdocs falla
        raise

    print("Documentation generation process finished.")

if __name__ == "__main__":
    # Este bloque asegura que la función generate_documentation se ejecute
    # cuando el script es llamado por el Dockerfile.
    generate_documentation()