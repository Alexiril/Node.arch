from typing import Callable

from frontend.AppState import AppState
from frontend.ExtendedWidget import ExtendedWidget

class AppButton(ExtendedWidget):
    state: int
    touched: bool
    on_click: Callable | None

    def __init__(self, appState: AppState, **kwargs) -> None:
        super().__init__(appState, **kwargs)
        self.state = 0
        self.touched = False
        self.on_click = None

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and (touch.button == "right" or touch.button == "left"):
            self.touched = True
            self.state = 2
            if self.on_click:
                self.on_click()
            self.draw()
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.state = 3
            self.draw()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos) and self.touched:
            self.touched = False
            self.state = 0
            self.draw()
        return super().on_touch_up(touch)
