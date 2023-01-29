from random import random

from backend.core.node import Node

from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import RoundedRectangle, Color

class GraphicalNode(Widget):
    # Core part
    node: Node
    Id: int
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
    label: Label
    nodesWidget: Widget

    def __init__(self, uiScale: float, node: Node, work: bool = True, moveSpeed: float = 1, **kwargs) -> None:
        super(GraphicalNode, self).__init__(**kwargs)
        self.uiScale = uiScale
        self.needToRedraw = True
        self.touched = False
        self.headerColor = node.color
        self.relativePosition = (0, 0)
        self.moveSpeed = moveSpeed
        self.node = node
        self.Id = id(self)
        self.name = node.name
        self.label = Label(text=self.name, font_size=uiScale * 0.4)
        self.add_widget(self.label)
        self.work = work
        self.nodesWidget = None

    def re_init_node(self, node: Node) -> None:
        self.needToRedraw = True
        self.headerColor = node.color
        self.node = node
        self.name = node.name
        self.label.text = self.name

    def post_init(self) -> None:
        bufParent = self.parent
        while not hasattr(bufParent, "nodeRootPoint"):
            bufParent = bufParent.parent
        self.nodesWidget = bufParent
        self.bodyColor = self.nodesWidget.theme["graphicalNode"]["standard_body_color"]
        self.touchedBodyColor = self.nodesWidget.theme["graphicalNode"]["touched_body_color"]
        self.selectedNodeColor = self.nodesWidget.theme["graphicalNode"]["selected_node_color"]
        

    def to_front(self) -> None:
        target = self.parent.canvas.children
        i = target.index(self.canvas)
        target[len(target) - 1], target[i] = target[i], target[len(target) - 1]
        for node in self.nodesWidget.Nodes:
            node.needToRedraw = True
            node.draw()

    def draw(self) -> None:
        if not self.needToRedraw or self.nodesWidget == None:
            return
        self.pos = (self.relativePosition[0] + self.nodesWidget.nodeRootPoint.pos[0],
                    self.relativePosition[1] + self.nodesWidget.nodeRootPoint.pos[1])
        self.label.pos = (self.pos[0] + 2.5 + self.uiScale * 0.4,
                          self.pos[1] + self.size[1] * 0.64)
        if self.canvas is not None:
            self.canvas.before.clear()
            x, y = self.pos[0], self.pos[1]
            with self.canvas.before:
                if self.canvas == self.parent.canvas.children[len(self.parent.canvas.children) - 1]:
                    Color(self.selectedNodeColor[0], self.selectedNodeColor[1],
                        self.selectedNodeColor[2], self.selectedNodeColor[3], mode="rgba")
                else:
                    Color(self.headerColor[0], self.headerColor[1],
                        self.headerColor[2], self.headerColor[3], mode="rgba")
                RoundedRectangle(pos=(x - 2.5, y - 2.5), size=(self.size[0] + 5, self.size[1] + 5),
                                 radius=[10, 10, 10, 10])
                Color(self.headerColor[0], self.headerColor[1],
                      self.headerColor[2], self.headerColor[3], mode="rgba")
                self.header = RoundedRectangle(pos=(x, y + 3 * self.size[1] / 4), size=(
                    self.size[0], self.size[1] / 4),
                    radius=[10, 10, 0, 0])
                if self.touched:
                    Color(self.touchedBodyColor[0], self.touchedBodyColor[1],
                          self.touchedBodyColor[2], self.touchedBodyColor[3], mode="rgba")
                else:
                    Color(self.bodyColor[0], self.bodyColor[1],
                          self.bodyColor[2], self.bodyColor[3], mode="rgba")
                self.body = RoundedRectangle(pos=(x, y), size=(
                    self.size[0], 3 * self.size[1] / 4),
                    radius=[0, 0, 10, 10])
        self.needToRedraw = False

    def on_touch_down(self, touch):
        if self.work and self.collide_point(*touch.pos) and touch.button == 'left' and not self.nodesWidget.panelAddNodeShowed:
            localTouchPos = self.to_local(*touch.pos)
            self.to_front()
            if localTouchPos[1] > self.header.pos[1]:
                self.touched = True
                self.touchedLocalPos = (
                    touch.pos[0] - self.pos[0],
                    touch.pos[1] - self.pos[1]
                )
                self.touchedPos = touch.pos
            return True
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
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.work and self.touched:
            self.touched = False
            self.needToRedraw = True
            self.draw()
            return True
        return super().on_touch_up(touch)
