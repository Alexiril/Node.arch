from inspect import isclass
from typing import Any
from random import randint
from os import path

from kivy.graphics import Color, Line, Rectangle
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.image import Image

from backend.core.node import Node
from frontend.graphicalNode import GraphicalNode


class PanelAddNode(Widget):
    state: int
    background_color: tuple[int, int, int, int]
    selectedLib: int
    selectedNode: int
    libs: list[tuple[Label, str]]
    nodesFromLibs: list[tuple[Label, type]]
    objName: Label
    objDescription: Label
    nodesWidget: Any
    designNodeAsExample: GraphicalNode
    nodeRootPoint: Widget
    libImage: ObjectProperty

    def __init__(self, uiScale: float, **kwargs):
        super(PanelAddNode, self).__init__(**kwargs)
        self.uiScale: float = uiScale
        self.state = 0
        self.selectedLib = 0
        self.selectedNode = 0
        self.libs = list()
        self.nodeRootPoint = Widget()
        self.nodeRootPoint.pos = (0, 0)
        self.disabledNodesForLibsDesign = list()
        self.nodesFromLibs = list()
        self.libImage = None

    def nodeSelectAction(self) -> None:
        if len(self.nodesFromLibs) > 0:
            cls = self.nodesFromLibs[self.selectedNode][1]
            self.designNodeAsExample.re_init_node(cls())

    def nodeSelect(self, instance, value) -> None:
        index = -1
        counter = 0
        for x in self.nodesFromLibs:
            if x[1].__name__ == value:
                index = counter
            counter += 1
        if self.selectedNode == index:
            cls = self.nodesFromLibs[index][1]
            node = cls()
            graphicalNode = GraphicalNode(self.uiScale, node)
            graphicalNode.size_hint = (None, None)
            graphicalNode.pos_hint = (None, None)
            graphicalNode.size = (200, 200)
            graphicalNode.relativePosition = (
                randint(int(-self.nodesWidget.nodeRootPoint.pos[0]), int(-self.nodesWidget.nodeRootPoint.pos[0] + (
                    self.nodesWidget.size[0] - graphicalNode.size[0]))),
                randint(int(-self.nodesWidget.nodeRootPoint.pos[1]), int(-self.nodesWidget.nodeRootPoint.pos[1] + (
                    self.nodesWidget.size[1] - graphicalNode.size[1])))
            )
            self.nodesWidget.nodesHolder.add_widget(graphicalNode, 999)
            graphicalNode.post_init()
            graphicalNode.draw()
            self.nodesWidget.Nodes.append(graphicalNode)
            self.parent.hideAddNodePanel()
            return
        else:
            self.selectedNode = index
            self.nodeSelectAction()
        self.update()

    def libSelectActions(self) -> None:
        module = self.nodesWidget.nodesLibs[self.libs[self.selectedLib][1]]
        if hasattr(module, "picture"):
            pathToImg = path.join(getattr(module, "__path__")[0], getattr(
                module, "picture").replace("/", path.sep))
            self.libImage = Image(source=pathToImg).texture
        else:
            self.libImage = None

    def libSelect(self, instance, value) -> None:
        module = self.nodesWidget.nodesLibs[value]
        if self.selectedLib == self.libs.index((instance, value)):
            self.state = 1
            for x in dir(module):
                cls = getattr(module, x)
                if (not (isclass(cls))) or (not (Node in cls.__bases__)):
                    continue
                label = Label()
                label.size = (self.uiScale * 5, self.uiScale)
                label.text = f'[ref={x}]{getattr(cls, "name")}[/ref]'
                label.bind(on_ref_press=self.nodeSelect)  # type: ignore
                label.color = self.nodesWidget.theme["panelAddNode"]["nodes_labels_color"]
                label.halign = 'center'
                label.valign = 'center'
                label.text_size = label.size
                label.markup = True
                label.opacity = 0
                label.disabled = True
                self.nodesFromLibs.append((label, cls))
                self.add_widget(label)
            if len(self.nodesFromLibs) > 0:
                cls = self.nodesFromLibs[self.selectedNode][1]
                self.designNodeAsExample.re_init_node(cls())
            self.update()
        else:
            self.selectedLib = self.libs.index((instance, value))
            self.libSelectActions()
        self.update()

    def post_init(self, nodesWidget) -> None:
        self.nodesWidget = nodesWidget
        self.theme = self.nodesWidget.theme
        self.background_color = nodesWidget.theme["panelAddNode"]["background_color"]
        self.lineColor = self.nodesWidget.theme["panelAddNode"]["line_between_lib_name_desc_color"]

        self.objName = Label()
        self.objDescription = Label()

        self.objName.size = self.objDescription.size = (
            self.uiScale, self.uiScale)
        self.objName.text_size, self.objDescription.text_size = self.objName.size, self.objDescription.size

        self.objName.color = nodesWidget.theme["panelAddNode"]["libs_name_label_color"]
        self.objDescription.color = nodesWidget.theme["panelAddNode"]["libs_description_label_color"]

        self.objName.halign = self.objDescription.halign = 'center'
        self.objName.valign = self.objDescription.valign = 'center'
        self.objName.markup = self.objDescription.markup = True
        self.objName.font_size = self.objDescription.font_size = self.uiScale * 0.4

        self.add_widget(self.objName)
        self.add_widget(self.objDescription)

        for x in nodesWidget.nodesLibs:
            label = Label()
            label.size = (self.uiScale * 5, self.uiScale)
            label.text = f'[ref={x}]{getattr(nodesWidget.nodesLibs[x], "humanName", "Unknown library")}[/ref]'
            label.bind(on_ref_press=self.libSelect)  # type: ignore
            label.color = nodesWidget.theme["panelAddNode"]["libs_labels_color"]
            label.halign = label.valign = 'center'
            label.text_size = label.size
            label.markup = True
            label.opacity = 0
            label.disabled = True
            self.libs.append((label, x))
            self.add_widget(label)

        self.designNodeAsExample = GraphicalNode(
            self.uiScale, Node([], [], []), False)
        self.designNodeAsExample.size_hint = (None, None)
        self.designNodeAsExample.size = (200, 200)
        self.add_widget(self.designNodeAsExample)
        self.designNodeAsExample.post_init()

        module = self.nodesWidget.nodesLibs[self.libs[0][1]]
        if hasattr(module, "picture"):
            pathToImg = path.join(getattr(module, "__path__")[0], getattr(
                module, "picture").replace("/", path.sep))
            self.libImage = Image(source=pathToImg).texture
        else:
            self.libImage = None

        self.draw_background()

    def draw_background(self) -> None:
        if self.canvas is not None:
            self.canvas.before.clear()
            with self.canvas.before:
                Color(self.background_color[0], self.background_color[1],
                      self.background_color[2], self.background_color[3], mode="rgba")
                Rectangle(pos=(0, 0), size=self.size)
                Color(self.lineColor[0], self.lineColor[1],
                      self.lineColor[2], self.lineColor[3], mode="rgba")
                Line(
                    points=(self.size[0] * 0.4, self.size[1] * 0.5, self.size[0]
                            * 0.4 + self.nodesWidget.size[0] * 0.2, self.size[1] * 0.5),
                    width=0.04 * self.uiScale,
                    cap='round'
                )

    def update(self) -> None:
        self.draw_background()
        for x in self.children:
            if x == self.objName or x == self.objDescription:
                continue
            x.opacity = 0
            x.disabled = True
        self.objName.text = ""
        self.objDescription.text = ""
        self.objName.pos = (self.size[0] * 0.4, self.size[1] * 0.5)
        self.objDescription.pos = (self.size[0] * 0.4, 0)
        self.objName.size = (self.size[0] * 0.2, self.size[1] * 0.5)
        self.objName.text_size = self.objName.size
        self.objDescription.size = (self.size[0] * 0.2, self.size[1] * 0.5)
        self.objDescription.text_size = self.objName.size
        if ((len(self.libs) <= 0) if self.state == 0 else (len(self.nodesFromLibs) <= 0)):
            self.objName.text = "[i]No objects here :([/i]"
            self.objDescription.text = "[i]Ooopsies...[/i]"
            return
        current = 0
        for x in (self.libs if self.state == 0 else self.nodesFromLibs):
            x[0].pos = (self.size[0] * 0.8 - x[0].size[0] * 0.5, self.size[1]
                        * 0.5 - x[0].size[1] * 0.5 + (current - (self.selectedLib if self.state == 0 else self.selectedNode)) * 50)
            x[0].font_size = self.uiScale * 0.4 - \
                abs(current - (self.selectedLib if self.state ==
                    0 else self.selectedNode)) * 7
            x[0].opacity = 1
            x[0].disabled = False
            current += 1
        if self.state == 0:
            self.objName.text = self.libs[self.selectedLib][0].text
            self.objDescription.text = getattr(self.nodesWidget.nodesLibs[self.libs[self.selectedLib][1]],
                                               "description", "")
            if self.libImage != None:
                if self.canvas is not None:
                    with self.canvas.before:
                        Color(1, 1, 1, 1)
                        rectSize = min(self.size[1] * 0.5, self.size[0] * 0.3)
                        Rectangle(pos=(self.size[0] * 0.05, self.size[1] * 0.5 - rectSize * 0.5), size=(
                            rectSize, rectSize), texture=self.libImage)

        if self.state == 1:
            self.objName.text = self.nodesFromLibs[self.selectedNode][0].text
            self.objDescription.text = getattr(self.nodesFromLibs[self.selectedNode][1],
                                               "description", "")
            self.designNodeAsExample.relativePosition = (
                self.size[0] * 0.1, self.size[1] * 0.4)
            self.designNodeAsExample.opacity = 1
            self.designNodeAsExample.disabled = False
            self.designNodeAsExample.needToRedraw = True
            self.designNodeAsExample.draw()

    def on_touch_down(self, touch):
        if (touch.button == "scrolldown" or touch.button == "scrollup") and self.parent.panelIsOpen:
            delta = 1 if touch.button == "scrolldown" else -1
            if self.state == 0:
                self.selectedLib = min(
                    max(self.selectedLib + delta, 0), len(self.libs) - 1)
                self.libSelectActions()
            if self.state == 1:
                self.selectedNode = min(
                    max(self.selectedNode + delta, 0), len(self.nodesFromLibs) - 1)
                self.nodeSelectAction()
            self.update()
            return True
        return super().on_touch_down(touch)
