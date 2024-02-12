import subprocess
import sys

def install_package(package_name):
    try:
        subprocess.check_call(['pip', 'install', package_name])
        print(f"Successfully installed {package_name}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package_name}. Error: {e}")

def install_package_var():
    try:
        subprocess.check_call(['python3' '-m' 'spacy' 'download' 'en_core_web_sm'])
        print(f"Successfully installed")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install. Error: {e}")

