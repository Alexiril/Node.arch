from typing import Callable
from kivy.uix.widget import Widget
from kivy.graphics import Color

class ComputedSpriteButton(Widget):
    state: int
    touches: int
    click: Callable
    needToRedraw: bool

    baseColor: Color | tuple[int, int, int, int]
    pressedColor: Color | tuple[int, int, int, int]
    additionalColor: Color | tuple[int, int, int, int]

    def __init__(self, uiScale: float, **kwargs):
        super(ComputedSpriteButton, self).__init__(**kwargs)
        self.uiScale: float = uiScale
        self.needToRedraw = True
        self.state = 0
        self.touches = 0
        self.click = lambda: print
        self.bind(size=self.rescale, pos=self.move)  # type: ignore
    
    def post_init(self) -> None:
        self.baseColor = self.parent.theme["computedSpriteButton"]["base_color"]
        self.pressedColor = self.parent.theme["computedSpriteButton"]["pressed_color"]
        self.additionalColor = self.parent.theme["computedSpriteButton"]["additional_color"]

    def getColorFromColor(self, color: Color) -> Color:
        return Color(color.r, color.g, color.b, color.a, mode="rgba")
    
    def getColor(self, color: tuple[float, float, float, float]) -> Color:
        return Color(color[0], color[1], color[2], color[3], mode="rgba")

    def draw(self) -> None:
        self.needToRedraw = False
        return

    def rescale(self, *args):
        self.needToRedraw = True
        self.draw()

    def move(self, *args):
        pass

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and (touch.button == "right" or touch.button == "left"):
            self.touches += 1
            self.state = 2
            if self.click:
                self.click()
            self.draw()
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.collide_point(*touch.pos):
            self.state = 3
            self.needToRedraw = True
            self.draw()
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.collide_point(*touch.pos):
            self.touches -= 1
            if self.touches <= 0:
                self.state = 0
                self.needToRedraw = True
                self.draw()
            return True
        return super().on_touch_up(touch)
