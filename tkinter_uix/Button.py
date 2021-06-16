from tkinter import Label
from tkinter import FLAT
from typing import NoReturn, Any, Callable
from tkinter_uix import Theme

theme = Theme()


class Button(Label):
    """The Button is a custom button created using a Label widget but has the same functionality as a regular button.
All the Label methods, arguments and keyword arguments are supported as the Button is an actual Label widget"""
    def __init__(self, master: Any, text: str = '', command: (Callable, None) = None, color: str = 'default',
                 disabled: bool = False, *args: Any, **kwargs: Any):
        """

        :param Any master: The parent Window where the widget will be placed on.
        :param str text: The text of the button.
        :param command: A function to be trigger when the button is pressed.
        :type command: Callable or None
        :param str color: The available colors are - cloud, info, primary, danger, warning, success, elegant and default
        :param bool disabled: If the button is disabled it does not respond to click and it must be a bool value.
        :param Any args: Any extra arguments.
        :param Any kwargs: Any extra keyword arguments.
        """
        Label.__init__(self, master, text=text, padx=14, pady=6, font=('Verdana', 12), relief=FLAT, *args, **kwargs)
        self.disabled = disabled
        self.colors = theme.btn_color

        if color not in self.colors:
            color = 'default'

        self.on_hover_color = self.colors[color]['on_hover']
        if not disabled:
            self.background_color = self.colors[color]['background']
            self.foreground_color = self.colors[color]['foreground']
            self.bind('<Enter>', self.on_hover)
            self.bind('<Leave>', self.off_hover)
            self.bind('<Button-1>', lambda event: self.on_click(command))
        elif disabled:
            self.background_color = self.colors[color]['disabled_bg']
            self.foreground_color = self.colors[color]['disabled_fg']

        self.off_hover()

    def on_hover(self, *args) -> NoReturn:
        """When mouse hover over the button it changes color and display a hand pointer."""
        if not self.disabled:
            self.configure(bg=self.on_hover_color, cursor="hand2")

    def off_hover(self, *args) -> NoReturn:
        """when mouse move away from the button it revert back to main color and default mouse pointer."""
        self.configure(bg=self.background_color, fg=self.foreground_color)

    def on_click(self, command: callable) -> NoReturn:
        """When button is clicked it triggers the function passed on the command argument."""
        if not self.disabled:
            if command:
                command()

    @property
    def text(self) -> str:
        """Return button text"""
        return self.cget('text')

    @text.setter
    def text(self, text='') -> NoReturn:
        """Set the button text to the given value"""
        self.configure(text=text)


if __name__ == '__main__':
    pass
