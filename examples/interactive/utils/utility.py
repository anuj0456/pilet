import tkinter as tk
from tkinter import filedialog


class Utility:
    @staticmethod
    def select_folder():
        root = tk.Tk()
        root.withdraw()
        folder_path = filedialog.askdirectory()
        root.destroy()
        return folder_path
