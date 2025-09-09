# PD Reader - Installation Guide

## 📦 Installation
1. Download and run `pdreadersetup.exe`
    -   Install to a location with read/write permissions
2. Launch from Start Menu > PD Reader

## 📁 Output Folders
The following folders are used:
- `Logs`: Contains logs of operations
- `Uploaded Files`: Files uploaded to Product Data Database are saved here
- `Stage 2`: Stage 2 Files are saved here
- `Matrixify`: Final data formatted for Matrixify

## Dev
- Clone this repo
- pip install -r requirements.txt
- Activate venv
- Run via `python -m src.main` or `./App.bat`
- Build .exe file with `pyinstaller --clean -F -n PDReaderApp src/main.py`
- Build installer setup by compiling "pdreaderinnosetup.iss"