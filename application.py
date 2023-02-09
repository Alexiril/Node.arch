from importlib import util
from json import JSONDecodeError, loads
from os import DirEntry, path, scandir
from random import random
from typing import Any
from types import ModuleType

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.metrics import Metrics

from backend.errors import LibError, SettingsError, ThemeError
from frontend.AppState import AppState
from frontend.app.root import AppRootWidget


def parseLib(lib: DirEntry) -> ModuleType | None:
    modulePath = path.join(lib, "__init__.py")
    moduleSpec = util.spec_from_file_location(
        lib.name, modulePath
    )
    if moduleSpec is None:
        LibError(
            "Not correct module spec. Please, check module path, if it's possible.", lib.path)
        return
    module = util.module_from_spec(moduleSpec)
    if moduleSpec.loader is None:
        LibError(
            "Have no idea how that had happen. Sorry. Module spec loader was None. Whaaat?..", lib.path)
        return
    moduleSpec.loader.exec_module(module)
    return module


class Application(App):
    appState: AppState

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.appState = AppState()

        try:
            with open(path.join("settings", "global.json"), "r") as settings:
                self.appState.globalSettings = loads(
                    settings.read().replace("\n", ""))
        except FileNotFoundError:
            SettingsError("The file with global settings was not found.")
            exit(1001)
        except JSONDecodeError:
            SettingsError(
                "The file with global settings probably was corrupted.")
            exit(1000)
        except:
            SettingsError(
                "Unexpected error has occured while working with the global settings file.")
            exit(999)

        for lib in scandir("libs"):
            if lib.is_dir():
                self.appState.nodesLibs[lib.name] = parseLib(lib)
            else:
                LibError(
                    "Not correct node library folder. Check the file out.", lib.path)

        try:
            with open(path.join("themes", self.appState.globalSettings.get("theme file", "theme.json")), "r") as themeFile:
                self.appState.theme = loads(themeFile.read().replace("\n", ""))
        except FileNotFoundError:
            ThemeError("Please, check the name of the theme. The file wasn't found.",
                       self.appState.globalSettings.get("theme file", "theme.json"))
            exit(998)
        except JSONDecodeError:
            ThemeError("Sorry, the theme file is not correct.",
                       self.appState.globalSettings.get("theme file", "theme.json"))
            exit(997)
        except:
            ThemeError("Sorry, unexpected behavior has happened while working with the theme file",
                       self.appState.globalSettings.get("theme file", "theme.json"))
            exit(996)

        self.appState.uiScale = Metrics.dpi * \
            self.appState.globalSettings.get("ui size", 0.7)

    def build(self):
        self.title = "Application. I love My Little Pony" if random() > 0.95 else "Application"
        Window.size = (1280, 720)
        Window.minimum_width, Window.minimum_height = Window.size
        return AppRootWidget(self.appState)


if __name__ == "__main__":
    Config.set('input', 'mouse', 'mouse, disable_multitouch')
    Application().run()
