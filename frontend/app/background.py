from kivy.graphics import Color, Rectangle

from frontend.AppState import AppState
from frontend.TexturePanel import TexturePanel


class AppBackground(TexturePanel):
    color_background: tuple[int, int, int, int]

    def __init__(self, appState: AppState, **kwargs) -> None:
        self.color_background = (0, 0, 0, 0)
        super().__init__(appState, **kwargs)
        if self.texture.texture is not None:
            self.texture.texture.wrap = 'repeat' # type: ignore

    def draw(self) -> None:
        self.size = self.appState.windowSize
        if self.texture is not None:
            self.texture.texture.uvpos = ( # type: ignore
                self.appState.appNodeRootPoint.pos[0] * 0.0078,
                self.appState.appNodeRootPoint.pos[1] * 0.0078
            )
        if self.canvas is not None:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(self.color_background[0], self.color_background[1],
                      self.color_background[2], self.color_background[3], mode="rgba")
                Rectangle(pos=(0, 0), size=self.appState.windowSize)
        return super().draw()

    def on_rescale(self, *args) -> None:
        return