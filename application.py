import json
from os import path, scandir
from random import random

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window

from backend.core.errors import LibError, SettingsError, ThemeError
from backend.core.libs import parseLib
from frontend.nodesWidget import NodesWidget

Config.set('input', 'mouse', 'mouse, disable_multitouch')


class Application:
    """ Main program class. Isn't it obvious?... """

    class ApplicationGraphics(App):
        """ Class for application graphics. Why do you even read that?..."""

        nodesWidget: NodesWidget

        def __init__(self, uiSize: float, nodesLibs: dict, theme: dict, **kwargs):
            super().__init__(**kwargs)
            self.nodesWidget = NodesWidget(uiSize, nodesLibs, theme, **kwargs)

        def build(self):
            self.title = "Application. I love My Little Pony" if random() > 0.95 else "Application"
            Window.size = (1280, 720)
            Window.minimum_width, Window.minimum_height = Window.size
            return self.nodesWidget

    graphics: ApplicationGraphics
    nodesLibs: dict[str, dict]
    globalSettings: dict
    theme: dict

    def __init__(self) -> None:

        try:
            with open(path.join("settings", "global.json"), "r") as settings:
                self.globalSettings = json.loads(
                    settings.read().replace("\n", ""))
        except FileNotFoundError:
            SettingsError("The file with global settings was not found.")
            exit(1001)
        except json.JSONDecodeError:
            SettingsError(
                "The file with global settings probably was corrupted.")
        except:
            SettingsError(
                "Unexpected error has occured while working with the global settings file.")

        self.nodesLibs = dict()
        for lib in scandir(path.join("backend", "libs")):
            if lib.is_dir():
                self.nodesLibs[lib.name] = parseLib(lib)
            else:
                LibError(
                    "Not correct node library folder. Check the file out.", lib.path)

        try:
            with open(path.join("frontend", "themes", self.globalSettings.get("theme file", "theme.json")), "r") as themeFile:
                self.theme = json.loads(themeFile.read().replace("\n", ""))
        except FileNotFoundError:
            ThemeError("Please, check the name of the theme. The file wasn't found.",
                       self.globalSettings["theme file"])
            exit(998)
        except json.JSONDecodeError:
            ThemeError("Sorry, the theme file is not correct.",
                       self.globalSettings["theme file"])
            exit(997)
        except:
            ThemeError("Sorry, unexpected behavior has happened while working with the theme file",
                       self.globalSettings["theme file"])
            exit(996)

        self.graphics = self.ApplicationGraphics(
            self.globalSettings.get("ui size", 0.7), self.nodesLibs, self.theme)

        self.graphics.run()


if __name__ == "__main__":
    Application()
