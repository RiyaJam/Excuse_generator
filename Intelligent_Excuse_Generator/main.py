# main.py — Entry point for the Intelligent Excuse Generator

import tkinter as tk
from app import ExcuseGeneratorApp

if __name__ == "__main__":
    root = tk.Tk()
    app = ExcuseGeneratorApp(root)
    root.mainloop()
