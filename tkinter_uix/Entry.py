from tkinter import Entry as _Entry
from tkinter import Frame as _Frame
from tkinter import YES, FLAT, END, X
from tkinter_uix import Theme

theme = Theme()


class Entry(_Frame):
    def __init__(self, master, bg=theme.entry_color['background'], show=None, width=30, on_return=None,
                 fg=theme.entry_color['foreground'],
                 placeholder='', *args, **kwargs):
        _Frame.__init__(self, master, bg=bg, *args, **kwargs)

        self.show = show
        self.width = width
        self.fg = fg
        self.placeholder = placeholder

        self.entry_frame = _Frame(self, borderwidth=2, bg=theme.entry_color['border'])
        self.entry_frame.pack(fill=X, expand=YES)

        self.entry = _Entry(self.entry_frame, borderwidth=6, relief=FLAT, bg=theme.entry_color['background'],
                            fg=theme.entry_color['foreground'], font=('Verdana', 12),
                            show=show, width=width)
        self.entry.pack(fill=X, expand=YES)
        self.on_focus_out()

        if on_return:
            self.entry.bind('<Return>', lambda event: on_return(*args, **kwargs))

        # Default bindings to control boder on focus and placeholder.
        self.entry.bind('<FocusIn>', self.on_focus_in)
        self.entry.bind('<FocusOut>', self.on_focus_out)

    def on_focus_in(self, *args, **kwargs):
        text = self.entry.get()
        self.configure(borderwidth=2, bg=theme.entry_color['outline'])
        if text and text == self.placeholder:
            self.entry.delete(0, END)

        self.entry.configure(fg=self.fg)
        self.entry.icursor(END)
        self.entry.configure(show=self.show)

    def on_focus_out(self, *args, **kwargs):
        text = self.entry.get()
        if text:
            if text == self.placeholder:
                self.entry.configure(fg=theme.entry_color['placeholder'])
                self.entry.configure(show='')
            else:
                self.entry.configure(fg=self.fg)
                self.entry.configure(show=self.show)
        else:
            self.entry.insert(0, self.placeholder)
            self.entry.configure(fg=theme.entry_color['placeholder'])
            self.entry.configure(show='')

        self.configure(borderwidth=0)

    def get(self, *args, **kwargs):
        text = self.entry.get()
        if text:
            if text == self.placeholder:
                return ''
            else:
                return self.entry.get()
        else:
            return ''

    def focus(self, *args, **kwargs):
        self.entry.focus_force()

    def delete(self, *args, **kwargs):
        self.entry.delete(0, END)

    def insert(self, value='', *args, **kwargs):
        text = self.entry.get()
        if text:
            if text == self.placeholder:
                self.entry.delete(0, END)
                self.entry.insert(0, value)
                self.on_focus_out()
            else:
                self.entry.insert(END, value)
                self.on_focus_out()
        else:
            self.entry.insert(0, value)
            self.on_focus_out()


if __name__ == '__main__':
    pass
