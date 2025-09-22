# PD Reader - Installation Guide

## 📦 Installation
1. Download and run `pdreadersetup.exe` from releases
2. Launch from Start Menu > PD Reader

## Usage

# For Uploading Milwaukee Setup Files
- Open PD Reader, go to the 3rd tab
- Before import, make sure the setup file headers are correct. The first row should be header.
- Drag and drop the setup file to the UI
- Select File, Select File Type and hit Upload to Database.

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