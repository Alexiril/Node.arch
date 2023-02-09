from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image

from frontend.AppState import AppState
from frontend.ExtendedWidget import ExtendedWidget


class TexturePanel(ExtendedWidget):
    texture: Image
    color: tuple[int, int, int, int]
    texture_multiplier: float

    def __init__(self, appState: AppState, **kwargs) -> None:
        self.texture = Image()
        self.color = (1, 1, 1, 1)
        self.texture_multiplier = 1
        super().__init__(appState, **kwargs)

    def draw(self) -> None:
        tx = self.texture.texture
        if self.canvas is not None and tx is not None:
            self.canvas.after.clear()
            with self.canvas.after:
                Color(self.color[0], self.color[1],
                      self.color[2], self.color[3], mode="rgba")
                tx.uvsize = (                                                   # type: ignore
                    -(self.size[0] / tx.size[0] * self.texture_multiplier),     # type: ignore
                    -(self.size[1] / tx.size[1] * self.texture_multiplier)      # type: ignore
                )
                Rectangle(pos=(0, 0), size=self.size,
                          texture=tx)
        return super().draw()
