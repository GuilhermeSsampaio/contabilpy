import subprocess
import os

def main():
    # Define o diretório raiz do projeto
    project_root = os.path.dirname(os.path.abspath(__file__))
    subprocess.run(["streamlit", "run", "interface/app.py"], shell=True, cwd=project_root)

if __name__ == "__main__":
    main()