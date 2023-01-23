from random import randint
from typing import Any

from kivy.graphics import Color, Line, Rectangle
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from frontend.graphicalNode import GraphicalNode


class PanelAddNode(Widget):
    state: int
    background_color: tuple[int, int, int, int]
    selectedLib: int
    libs: list[tuple[Label, str]]
    libName: Label
    libDescription: Label
    nodesWidget: Any
    disabledNodesForLibsDesign: list[GraphicalNode]
    nodeRootPoint: Widget

    def __init__(self, uiScale: float, **kwargs):
        super(PanelAddNode, self).__init__(**kwargs)
        self.uiScale: float = uiScale
        self.state = 0
        self.selectedLib = 0
        self.libs = list()
        self.nodeRootPoint = Widget(**kwargs)
        self.nodeRootPoint.pos = (0, 0)
        self.disabledNodesForLibsDesign = list()

    def libSelect(self, instance, value) -> None:
        if self.selectedLib == self.libs.index((instance, value)):
            print(value)
        else:
            self.selectedLib = self.libs.index((instance, value))
            for i in self.disabledNodesForLibsDesign:
                x, y = randint(- int(self.nodesWidget.size[0] * 0.05), int(self.nodesWidget.size[0] * 0.2)), \
                    randint(
                        self.nodesWidget.size[1] * 0.1, self.nodesWidget.size[1] - self.nodesWidget.size[1] * 0.4)
                i.relativePosition = (x, y)
                i.needToRedraw = True
                i.draw()
        self.draw()

    def post_init(self, nodesWidget) -> None:
        self.nodesWidget = nodesWidget
        self.background_color = nodesWidget.theme["panelAddNode"]["background_color"]

        self.libName = Label()
        self.libName.size = (self.uiScale, self.uiScale)
        self.libName.text_size = self.libName.size
        self.libName.color = nodesWidget.theme["panelAddNode"]["libs_name_label_color"]
        self.libName.halign = 'center'
        self.libName.valign = 'center'
        self.libName.markup = True
        self.libName.font_size = self.uiScale * 0.4
        self.libName.opacity = 0
        self.libName.disabled = True
        self.add_widget(self.libName)

        self.libDescription = Label()
        self.libDescription.size = (self.uiScale, self.uiScale)
        self.libDescription.text_size = self.libName.size
        self.libDescription.color = nodesWidget.theme["panelAddNode"]["libs_description_label_color"]
        self.libDescription.halign = 'center'
        self.libDescription.valign = 'center'
        self.libDescription.markup = True
        self.libDescription.font_size = self.uiScale * 0.4
        self.libDescription.opacity = 0
        self.libDescription.disabled = True
        self.add_widget(self.libDescription)

        for x in nodesWidget.nodesLibs:
            label = Label()
            label.size = (self.uiScale * 5, self.uiScale)
            label.text = f'[ref={x}]{nodesWidget.nodesLibs[x]["UI name"]}[/ref]'
            # F****ng mistake...
            label.bind(on_ref_press=self.libSelect)  # type: ignore
            label.color = nodesWidget.theme["panelAddNode"]["libs_labels_color"]
            label.halign = 'center'
            label.valign = 'center'
            label.text_size = label.size
            label.markup = True
            label.opacity = 0
            label.disabled = True
            self.libs.append((label, x))
            self.add_widget(label)

        for i in range(3):
            x, y = randint(- int(nodesWidget.size[0] * 0.05), int(nodesWidget.size[0] * 0.2)), \
                randint(
                    nodesWidget.size[1] * 0.1, nodesWidget.size[1] - nodesWidget.size[1] * 0.4)
            self.addNotFunctionalNodes(-1, 1, (x, y))

    def draw(self) -> None:
        for x in self.children:
            x.opacity = 0
            x.disabled = True
        if self.canvas is not None:
            self.canvas.before.clear()
            lineColor = self.nodesWidget.theme["panelAddNode"]["line_between_lib_name_desc_color"]
            with self.canvas.before:
                Color(self.background_color[0], self.background_color[1],
                      self.background_color[2], self.background_color[3], mode="rgba")
                Rectangle(pos=(0, 0), size=self.size)
                Color(lineColor[0], lineColor[1],
                      lineColor[2], lineColor[3], mode="rgba")
                Line(
                    points=(self.size[0] * 0.7, self.size[1] * 0.5, self.size[0]
                            * 0.7 + self.nodesWidget.size[0] * 0.2, self.size[1] * 0.5),
                    width=0.04 * self.uiScale,
                    cap='round'
                )
            if self.state == 0 and len(self.libs) > 0:
                current = 0
                for x in self.libs:
                    x[0].pos = (self.size[0] * 0.5 - x[0].size[0] * 0.5, self.size[1]
                                * 0.5 - x[0].size[1] * 0.5 + (current - self.selectedLib) * 50)
                    x[0].font_size = self.uiScale * 0.4 - \
                        abs(current - self.selectedLib) * 7
                    x[0].opacity = 1
                    x[0].disabled = False
                    current += 1
                self.libName.opacity = 1
                self.libName.disabled = False
                self.libDescription.opacity = 1
                self.libDescription.disabled = False
                self.libName.text = self.libs[self.selectedLib][0].text
                self.libDescription.text = self.nodesWidget.nodesLibs[self.libs[self.selectedLib][1]].get(
                    "Description", "")
                self.libName.pos = (self.size[0] * 0.7, self.size[1] * 0.5)
                self.libDescription.pos = (
                    self.size[0] * 0.7, 0)
                self.libName.size = (
                    self.nodesWidget.size[0] * 0.2, self.nodesWidget.size[1] * 0.5)
                self.libName.text_size = self.libName.size
                self.libDescription.size = (
                    self.nodesWidget.size[0] * 0.2, self.nodesWidget.size[1] * 0.5)
                self.libDescription.text_size = self.libName.size
                for x in self.disabledNodesForLibsDesign:
                    x.opacity = 1
                    x.disabled = False

    def on_touch_down(self, touch):
        if touch.button == "scrolldown" or touch.button == "scrollup":
            delta = 1 if touch.button == "scrolldown" else -1
            if self.state == 0:
                self.selectedLib = min(
                    max(self.selectedLib + delta, 0), len(self.libs) - 1)
                for i in self.disabledNodesForLibsDesign:
                    x, y = randint(- int(self.nodesWidget.size[0] * 0.05), int(self.nodesWidget.size[0] * 0.2)), \
                        randint(
                            self.nodesWidget.size[1] * 0.1, self.nodesWidget.size[1] - self.nodesWidget.size[1] * 0.4)
                    i.relativePosition = (x, y)
                    i.needToRedraw = True
                    i.draw()
            self.draw()
        return super().on_touch_down(touch)

    def addNotFunctionalNodes(self, kind: int = -1, sizeMultiplier: float = 1, position: tuple[int, int] = (0, 0)) -> None:
        newNode = GraphicalNode(self.uiScale * sizeMultiplier, False, kind)
        self.disabledNodesForLibsDesign.append(newNode)
        newNode.size_hint = (None, None)
        newNode.pos_hint = (None, None)
        newNode.size = (200, 200)
        newNode.relativePosition = position
        self.add_widget(newNode)
        newNode.draw()
