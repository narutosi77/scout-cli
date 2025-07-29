# generate_docs.py
import os
import subprocess
import shutil

def generate_documentation():
    print("Starting documentation generation process...")
    output_dir = "site"
    if os.path.exists(output_dir):
        print(f"Cleaning existing output directory: {output_dir}")
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    print("Running mkdocs build command...")
    try:
        result = subprocess.run(["mkdocs", "build"], check=True, capture_output=True, text=True)
        print("MkDocs build completed successfully.")
        if result.stdout:
            print("MkDocs stdout:\n", result.stdout)
        if result.stderr:
            print("MkDocs stderr:\n", result.stderr)
    except subprocess.CalledProcessError as e:
        print(f"Error during MkDocs build: {e}")
        print(f"MkDocs stdout:\n{e.stdout}")
        print(f"MkDocs stderr:\n{e.stderr}")
        raise

    print("Documentation generation process finished.")

if __name__ == "__main__":
    generate_documentation()