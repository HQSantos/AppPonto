import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appponto.settings")
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
