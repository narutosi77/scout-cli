# generate_docs.py
import subprocess
import os
import re

# --- CONFIGURACIÓN ---
# Ruta al ejecutable de tu docker-scout CLI dentro del contenedor.
# Para pruebas locales en Windows, si lo copiaste a la raíz del repo, puedes usar "docker-scout.exe"
# Pero para el Dockerfile, la ruta dentro del contenedor es "/usr/local/bin/docker-scout"
SCOUT_CLI_EXEC = ["./docker-scout.exe"] # ¡IMPORTANTE para pruebas LOCALES en Windows!

# Directorio donde se guardarán los archivos Markdown generados.
OUTPUT_DIR = "docs" # Usaremos la carpeta 'docs' que ya existe en tu repo

# Define los comandos principales que deseas documentar.
# ¡DEBES REVISAR Y AJUSTAR ESTA LISTA BASÁNDOTE EN LA SALIDA REAL DE TU CLI!
# Esta lista se ha ajustado para reflejar los nombres de archivo que ya tienes en tus 'docs'.
COMMAND_CONFIG = {
    "scout": [], # Ayuda general de 'docker-scout --help'

    "scout_attestation": ["attestation"],
    "scout_attestation_add": ["attestation", "add"],
    
    "scout_cache": ["cache"],
    "scout_cache_df": ["cache", "df"],
    "scout_cache_prune": ["cache", "prune"],

    "scout_compare": ["compare"],
    "scout_config": ["config"],
    "scout_cves": ["cves"],
    
    "scout_docker-cli-plugin-hooks": ["docker-cli-plugin-hooks"],
    "scout_enroll": ["enroll"],
    "scout_environment": ["environment"],
    "scout_help": ["help"], # Comando 'help' del propio CLI

    "scout_integration": ["integration"],
    "scout_integration_configure": ["integration", "configure"],
    "scout_integration_delete": ["integration", "delete"],
    "scout_integration_list": ["integration", "list"],

    "scout_policy": ["policy"],
    "scout_push": ["push"],
    "scout_quickview": ["quickview"],
    "scout_recommendations": ["recommendations"],

    "scout_repo": ["repo"],
    "scout_repo_disable": ["repo", "disable"],
    "scout_repo_enable": ["repo", "enable"],
    "scout_repo_list": ["repo", "list"],
    
    "scout_sbom": ["sbom"],
    "scout_stream": ["stream"],
    "scout_version": ["version"],
    "scout_watch": ["watch"],
}

# --- FUNCIONES DE AYUDA ---

def run_scout_command(command_args):
    """Ejecuta un comando de docker-scout CLI y retorna su salida estándar."""
    try:
        full_command = SCOUT_CLI_EXEC + command_args + ["--help"]
        print(f"Ejecutando: {' '.join(full_command)}")
        result = subprocess.run(
            full_command,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8',
            errors='replace'
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Falló el comando: {' '.join(e.cmd)}")
        print(f"STDOUT: {e.stdout}")
        print(f"STDERR: {e.stderr}")
        return None
    except FileNotFoundError:
        print(f"ERROR: El ejecutable de docker-scout CLI no fue encontrado en '{SCOUT_CLI_EXEC[0]}'.")
        print("Asegúrate de que 'docker-scout.exe' esté en la misma carpeta que este script para pruebas locales,")
        print("o que la ruta en 'SCOUT_CLI_EXEC' sea correcta dentro del contenedor Docker.")
        return None

def clean_and_format_output(output, command_name):
    """
    Limpia y formatea la salida de --help en un Markdown más legible.
    **DEBES PERSONALIZAR ESTA FUNCIÓN** para que se adapte al formato de la salida de tu CLI.
    """
    if not output:
        return ""

    lines = output.splitlines()
    markdown_lines = []
    
    # El título del manual puede ser el mismo, pero el texto de "comando" cambia a "docker-scout"
    title_display_name = command_name.replace('scout_', '').replace('_', ' ')
    if title_display_name == "": # Para el caso de 'scout' general
        title_display_name = "General"
    
    markdown_lines.append(f"# Manual de `docker-scout` {title_display_name.title()}\n")
    markdown_lines.append(f"Este documento provee un manual detallado para el comando `{command_name.replace('scout_', '').replace('_', ' ')}` de Docker Scout CLI.\n")

    current_section = None
    for line in lines:
        line = line.strip()

        if re.match(r"^(Usage|Available Commands|Available Commands and Flags|Flags|Global Flags|Examples|See Also|Description):?\s*$", line, re.IGNORECASE):
            section_title = line.strip(':').title()
            markdown_lines.append(f"\n## {section_title}\n")
            current_section = section_title
        elif not line:
            markdown_lines.append("\n")
        else:
            if current_section:
                # Aquí ajustamos para el nombre del CLI: "docker scout"
                if "Usage" in current_section and (line.startswith("docker scout") or line.startswith("scout")):
                    markdown_lines.append(f"```bash\n{line}\n```\n")
                elif "Flags" in current_section or "Commands" in current_section or "Available Commands" in current_section:
                    # Intenta formatear como lista si parece una opción/subcomando
                    if re.match(r"^\s*(--[\w-]+|-[\w]),?\s*.*", line) or re.match(r"^\s*([\w-]+)\s+.*", line):
                        markdown_lines.append(f"- `{line.strip()}`\n")
                    else:
                        markdown_lines.append(f"{line}\n")
                else: # Para otras secciones, solo el texto
                    markdown_lines.append(f"{line}\n")
            else: # Contenido antes de cualquier sección conocida (ej. descripción principal)
                markdown_lines.append(f"{line}\n")
    
    final_markdown = []
    for i, line in enumerate(markdown_lines):
        if line.strip() == "" and i > 0 and final_markdown and final_markdown[-1].strip() == "":
            continue
        final_markdown.append(line)

    return "".join(final_markdown).strip()

# --- FUNCIÓN PRINCIPAL ---

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"Iniciando la generación de documentación en Markdown en: {OUTPUT_DIR}")

    for file_name_prefix, command_args_list in COMMAND_CONFIG.items():
        output = run_scout_command(command_args_list)

        if output:
            markdown_content = clean_and_format_output(output, file_name_prefix)
            output_file_path = os.path.join(OUTPUT_DIR, f"{file_name_prefix}.md")
            
            with open(output_file_path, "w", encoding='utf-8') as f:
                f.write(markdown_content)
            print(f"  Documento generado: {output_file_path}")
        else:
            print(f"  ADVERTENCIA: No se pudo generar el contenido para '{file_name_prefix}.md'.")

    print("\n¡Generación de documentación Markdown finalizada!")