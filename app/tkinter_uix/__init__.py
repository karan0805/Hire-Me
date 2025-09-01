import yaml
from utils.variables import APP_FOLDER

THEMES_FOLDER = APP_FOLDER / "tkinter_uix/themes"


class Theme:
    def __init__(self, name="default"):
        with open(
            str(THEMES_FOLDER / f"{name}.yaml"), "r", encoding="UTF-8"
        ) as file:
            self.theme = yaml.load(file, Loader=yaml.FullLoader)

        self.app_color = self.theme["App"]
        self.btn_color = self.theme["Button"]
        self.entry_color = self.theme["Entry"]
        self.navbar_color = self.theme["Navbar"]
