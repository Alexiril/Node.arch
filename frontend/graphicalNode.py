from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import (
    RoundedRectangle,
    Color
)
from random import random
from typing import Any


class GraphicalNodeSock(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GraphicalNode(Widget):
    # Core part
    kind: int
    name: str
    Id: int
    coreSockets: dict[str, Any]
    work: bool

    # Graphical part
    needToRedraw: bool
    touched: bool
    touchedPos: tuple[int, int]
    touchedLocalPos: tuple[int, int]
    relativePosition: tuple[int, int]
    header: RoundedRectangle
    body: RoundedRectangle
    headerColor: Color
    moveSpeed: float
    sockets: list[GraphicalNodeSock]
    label: Label

    def __init__(self, uiScale: float, work: bool = True, kind: int = -1, moveSpeed: float = 1, **kwargs) -> None:
        super(GraphicalNode, self).__init__(**kwargs)
        self.uiScale = uiScale
        self.needToRedraw = True
        self.touched = False
        self.headerColor = Color(random(), random(), random(), mode="rgb")
        self.relativePosition = (0, 0)
        self.moveSpeed = moveSpeed
        self.sockets = list()
        self.kind = kind
        self.Id = id(self)
        self.coreSockets = dict()
        self.name = "Heya here"
        self.label = Label(text=self.name, font_size=uiScale * 0.4)
        self.add_widget(self.label)
        self.work = work
    
    def post_init(self) -> None:
        pass

    def to_front(self) -> None:
        target = self.parent.canvas.children
        i = target.index(self.canvas)
        target[len(target) - 1], target[i] = target[i], target[len(target) - 1]

    def draw(self) -> None:
        if not self.needToRedraw:
            return
        self.pos = (self.relativePosition[0] + self.parent.nodeRootPoint.pos[0],
                    self.relativePosition[1] + self.parent.nodeRootPoint.pos[1])
        self.label.pos = (self.pos[0] + 2.5 + self.uiScale * 0.4,
                          self.pos[1] + self.size[1] * 0.64)
        if self.canvas is not None:
            self.canvas.before.clear()
            x, y = self.pos[0], self.pos[1]
            with self.canvas.before:
                Color(self.headerColor.r, self.headerColor.g,
                      self.headerColor.b, 1, mode="rgba")
                RoundedRectangle(pos=(x - 2.5, y - 2.5), size=(self.size[0] + 5, self.size[1] + 5),
                                 radius=[10, 10, 10, 10])
                self.header = RoundedRectangle(pos=(x, y + 3 * self.size[1] / 4), size=(
                    self.size[0], self.size[1] / 4),
                    radius=[10, 10, 0, 0])
                if self.touched:
                    Color(0.2, 0.2, 0.2, 1, mode="rgba")
                else:
                    Color(0.4, 0.4, 0.4, 1, mode="rgba")
                self.body = RoundedRectangle(pos=(x, y), size=(
                    self.size[0], 3 * self.size[1] / 4),
                    radius=[0, 0, 10, 10])
        self.needToRedraw = False

    def on_touch_down(self, touch):
        if self.work and self.collide_point(*touch.pos) and touch.button == 'left' and not self.parent.panelAddNodeShowed:
            localTouchPos = self.to_local(*touch.pos)
            self.to_front()
            if localTouchPos[1] > self.header.pos[1]:
                self.touched = True
                self.touchedLocalPos = (
                    touch.pos[0] - self.pos[0],
                    touch.pos[1] - self.pos[1]
                )
                self.touchedPos = touch.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.work and self.touched:
            self.relativePosition = (
                self.relativePosition[0] + (touch.pos[0] -
                                            self.touchedPos[0]) * self.moveSpeed,
                self.relativePosition[1] +
                (touch.pos[1] - self.touchedPos[1]) * self.moveSpeed
            )
            self.needToRedraw = True
            self.draw()
            self.touchedPos = touch.pos
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.work and self.touched:
            self.touched = False
            self.needToRedraw = True
            self.draw()
        return super().on_touch_up(touch)
