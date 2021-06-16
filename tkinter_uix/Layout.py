import tkinter
from tkinter_uix import Theme

theme = Theme()


class BoxLayout(tkinter.Frame):
    def __init__(self, master, bg=theme.app_color['background'], *args, **kwargs):
        tkinter.Frame.__init__(self, master, bg=bg, *args, **kwargs)
        self.show()

    def show(self):
        self.pack(fill=tkinter.BOTH, expand=tkinter.YES)

    def hide(self):
        self.pack_forget()


class AnchorLayout(tkinter.Frame):
    def __init__(self, master, bg=theme.app_color['background'], anchor=None, anchor_x='LEFT', anchor_y='TOP',
                 *args, **kwargs):
        tkinter.Frame.__init__(self, master, bg=bg, *args, **kwargs)
        self.anchor = anchor
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.show()

    def show(self):
        anchors = {'LEFT': 'w', 'RIGHT': 'e'}

        if self.anchor == 'CENTER':
            self.pack(side=tkinter.TOP, expand=tkinter.YES, anchor=tkinter.CENTER)
        else:
            x = anchors.get(self.anchor_x)
            y = self.anchor_y
            if x and y in ['TOP', 'BOTTOM']:
                self.pack(side=y.lower(), anchor=x)
            else:
                raise TypeError('Invalid anchor!')

    def hide(self):
        self.pack_forget()


if __name__ == '__main__':
    pass
