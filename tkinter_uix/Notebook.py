from tkinter.ttk import Notebook as NB
from tkinter import ttk
from tkinter_uix import Theme

theme = Theme()


class Notebook(ttk.Notebook):
    def __init__(self, master, **kwargs):
        ttk.Notebook.__init__(self, master, **kwargs)

        s = ttk.Style()
        s.configure('TNotebook.Tab', font=('Verdana', '12'), padding=(14, 6), foreground=theme.app_color['foreground'])
        s.configure('TNotebook', background=theme.app_color['background'])
        s.map('TNotebook.Tab', foreground=[('selected', theme.entry_color['outline'])])


if __name__ == '__main__':
    pass
