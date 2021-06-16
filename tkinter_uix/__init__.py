import yaml


class Theme:
    def __init__(self, name='default'):
        with open(f'tkinter_uix/themes/{name}.yaml', 'r') as file:
            self.theme = yaml.load(file, Loader=yaml.FullLoader)

        self.app_color = self.theme['App']
        self.btn_color = self.theme['Button']
        self.entry_color = self.theme['Entry']
        self.navbar_color = self.theme['Navbar']
