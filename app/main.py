from tkinter import Tk

from modules.login import log
from utils.variables import ELEMENTS_FOLDER

if __name__ == "__main__":
    root = Tk()
    root.geometry("1050x700")
    root.title("Hire ME")
    root.resizable(0, 0)
    root.iconbitmap(str(ELEMENTS_FOLDER / "favicon.ico"))
    log(root)
    root.mainloop()
