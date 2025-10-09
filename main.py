
import subprocess


def main():
    subprocess.run(["streamlit", "run", "interface/app.py"], shell=True)
if __name__ == "__main__":
    main()