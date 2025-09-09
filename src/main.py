import os
import sys
from src.PDUI import App
import customtkinter

def get_app_base_path():
    # Works for both dev mode and PyInstaller .exe
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

BASE_DIR = get_app_base_path()

REQUIRED_DIRS = ["Logs", "Uploaded Files", "Stage 2", "Matrixify"]

def ensure_directories():
    for folder in REQUIRED_DIRS:
        path = os.path.join(BASE_DIR, folder)
        os.makedirs(path, exist_ok=True)

def main():
    ensure_directories()
    print("PD Reader App Started")
    app = App()
    app.mainloop()
        
    
if __name__ == "__main__":
    main()
