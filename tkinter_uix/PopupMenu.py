import tkinter
from tkinter_uix import Theme

theme = Theme()


class PopupMenu(tkinter.Menu):
    def __init__(self, master, bg=theme.app_color['background'], *args, **kwargs):
        tkinter.Menu.__init__(self, master, bg=bg, tearoff=0, *args, **kwargs)

        self.sub_menus = dict()

    def add_item(self, name='', command=None, args=tuple()):
        if command and args:
            self.add_command(label=name, command=lambda: command(args))
        else:
            self.add_command(label=name, command=command)

    def add_sub_menu(self, label='', name='', command=None, args=tuple()):
        sub_menu = PopupMenu(self)
        if label in self.sub_menus:
            pass
        else:
            self.sub_menus[label] = sub_menu
        self.add_cascade(label=label, menu=sub_menu)
        if command and args:
            sub_menu.add_command(label=name, command=lambda: command(args))
        else:
            sub_menu.add_command(label=name, command=command)

    def add_sub_menu_item(self, label='', name='', command=None, args=tuple()):
        sub_menu = self.sub_menus.get(label)
        if sub_menu:
            if command and args:
                sub_menu.add_command(label=name, command=lambda: command(args))
            else:
                sub_menu.add_command(label=name, command=command)
        else:
            raise ValueError(f'Sub menu "{label}" was not found!')

    def trigger(self, widget):
        widget.bind('<Button-3>', self.show)

    def show(self, event):
        self.post(event.x_root, event.y_root)


if __name__ == '__main__':
    pass
