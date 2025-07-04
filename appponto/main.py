import importlib
import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, 'frozen', False) else __file__))
sys.path.append(BASE_DIR)

DB_PATH = os.path.join(BASE_DIR, 'db.sqlite3')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

settings_module = importlib.import_module("settings")
settings_module.DATABASES['default']['NAME'] = DB_PATH

django.setup()

from tkinter import Tk
from screens import RegistroPontoScreen

class RegistroPontoApp:
    def __init__(self):
        self.root = Tk()
        self.root.title("Registro de Ponto")
        self.screen = RegistroPontoScreen(self.root)
        self.root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        RegistroPontoApp()
