import subprocess

def main():
    # Define o diretório raiz do projeto
    subprocess.run(["streamlit", "run", "app.py"], shell=True)

if __name__ == "__main__":
    main()