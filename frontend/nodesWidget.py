from os.path import join
from random import randint

from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import Metrics
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.widget import Widget

from frontend.buttonAddNode import ButtonAddNode
from frontend.computedSpriteButton import ComputedSpriteButton
from frontend.graphicalNode import GraphicalNode


class NodeRootPoint(Widget):

    def __init__(self, uiScale: float, **kwargs):
        super().__init__(**kwargs)
        self.uiScale = uiScale

    def post_init(self) -> None:
        self.colorOne = self.parent.theme["nodeRootPoint"]["line_one_color"]
        self.colorTwo = self.parent.theme["nodeRootPoint"]["line_two_color"]

    def draw(self):
        if self.canvas is not None:
            self.canvas.after.clear()

            with self.canvas.after:
                Color(self.colorOne[0], self.colorOne[1],
                      self.colorOne[2], self.colorOne[3], mode="rgba")
                Line(
                    points=(
                        self.pos[0] - 25,
                        self.pos[1] - 25,
                        self.pos[0] + 25,
                        self.pos[1] + 25
                    ),
                    width=0.02 * self.uiScale,
                    cap='round'
                )
                Color(self.colorTwo[0], self.colorTwo[1],
                      self.colorTwo[2], self.colorTwo[3], mode="rgba")
                Line(
                    points=(
                        self.pos[0] + 25,
                        self.pos[1] - 25,
                        self.pos[0] - 25,
                        self.pos[1] + 25
                    ),
                    width=0.02 * self.uiScale,
                    cap='round'
                )


class NodesWidget(Widget):
    Nodes: list[GraphicalNode]
    nodesLibs: dict
    backgroundTexture: ObjectProperty
    Buttons: list[ComputedSpriteButton]
    touched: bool
    touchedPos: tuple[int, int]
    nodeRootPoint: NodeRootPoint
    moveSceneSpeed: float
    panelAddNodeShowed: bool
    theme: dict
    color_background: tuple[int, int, int, int]
    color_texture: tuple[int, int, int, int]
    started: bool
    nodesHolder: Widget

    def __init__(self, uiSize: float, nodesLibs: dict, theme: dict, **kwargs):
        super(NodesWidget, self).__init__(**kwargs)
        self.nodesHolder = Widget()
        self.nodesHolder.size_hint = (None, None)
        self.nodesHolder.pos = (0, 0)
        self.nodesHolder.size = self.size
        self.add_widget(self.nodesHolder, 0)
        self.theme = theme
        self.color_background = self.theme["nodesWidget"]["background_color"]
        self.color_texture = self.theme["nodesWidget"]["texture_color"]
        self.touched = False
        self.nodesLibs = nodesLibs
        self.touchedPos = (0, 0)
        self.uiScale = Metrics.dpi * uiSize
        self.started = False
        self.nodeRootPoint = NodeRootPoint(self.uiScale, **kwargs)
        self.nodeRootPoint.pos_hint = (None, None)
        self.nodeRootPoint.size_hint = (None, None)
        self.panelAddNodeShowed = False
        self.moveSceneSpeed = 0.5
        self.backgroundTexture = Image(
            source=join("frontend", "themes", self.theme["nodesWidget"]["texture_source"])).texture
        self.textureMultiplier = self.theme["nodesWidget"]["texture_multiplier"]
        self.backgroundTexture.wrap = 'repeat'
        self.backgroundTexture.uvsize = (1, 1)
        self.Nodes = list()
        self.Buttons = list()
        self.Buttons.append(ButtonAddNode(self.uiScale, **kwargs))
        self.Buttons[0].size_hint = (None, None)
        self.bind(size=self.rescale, pos=self.move)  # type: ignore

    def add_widget(self, widget, index=0, canvas=None):
        result = super().add_widget(widget, index, canvas)
        if hasattr(widget, "post_init"):
            widget.post_init()
        return result

    def check_node_id(self, Id: int) -> int:
        ids = [x.Id for x in self.Nodes]
        if not Id in ids:
            return Id
        else:
            x = randint(0, 72_057_594_037_927_935)
            while x in ids:
                x = randint(0, 72_057_594_037_927_935)
            return x

    def draw(self):
        if not self.started:
            self.add_widget(self.nodeRootPoint)
            for obj in self.Buttons:
                self.add_widget(obj)
            self.started = True
        self.draw_background()
        self.draw_objects()
        self.draw_gui()
        self.nodeRootPoint.draw()

    def draw_objects(self):
        if self.canvas is not None:
            with self.canvas:
                for obj in self.Nodes:
                    obj.draw()

    def draw_gui(self):
        if self.canvas is not None:
            with self.canvas:
                self.Buttons[0].size = (
                    self.uiScale, self.uiScale)
                self.Buttons[0].pos = (self.width - self.uiScale - 0.1 *
                                       self.uiScale, self.height - self.uiScale - 0.1 * self.uiScale)
                for obj in self.Buttons:
                    obj.draw()

    def draw_background(self):
        if self.canvas is not None:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(self.color_background[0], self.color_background[1],
                      self.color_background[2], self.color_background[3], mode="rgba")
                Rectangle(pos=(0, 0), size=self.size)
                Color(self.color_texture[0], self.color_texture[1],
                      self.color_texture[2], self.color_texture[3], mode="rgba")
                self.backgroundTexture.uvsize = (
                    -(self.size[0] / self.backgroundTexture.size[0]
                      * self.textureMultiplier),
                    -(self.size[1] / self.backgroundTexture.size[1]
                      * self.textureMultiplier)
                )
                Rectangle(pos=(0, 0), size=self.size,
                          texture=self.backgroundTexture)

    def rescale(self, *args):
        self.draw()

    def move(self, *args):
        self.draw()

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos) and touch.button == "middle":
            self.touched = True
            self.touchedPos = touch.pos
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.touched and (touch.is_double_tap or touch.button == "middle") and not self.panelAddNodeShowed:
            self.nodeRootPoint.pos = (
                self.nodeRootPoint.pos[0] + (touch.pos[0] -
                                             self.touchedPos[0]) * self.moveSceneSpeed,
                self.nodeRootPoint.pos[1] + (touch.pos[1] -
                                             self.touchedPos[1]) * self.moveSceneSpeed
            )
            for obj in self.Nodes:
                obj.needToRedraw = True
                obj.draw()
            self.nodeRootPoint.draw()
            self.touchedPos = touch.pos
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.touched and (touch.is_double_tap or touch.button == "middle"):
            self.touched = False
        return super().on_touch_up(touch)
