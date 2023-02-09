from enum import Enum
from inspect import isclass
from os import path
from random import randint
from types import ModuleType

from kivy.graphics import Color, Line, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label

from backend.node import Node
from frontend.app.gNode import AppGNode
from frontend.AppState import AppState
from frontend.ExtendedWidget import ExtendedWidget


class AppAddNodePanel(ExtendedWidget):
    class AddNodePanelStates(Enum):
        librarySelect = 0
        nodeSelect = 1

    state: AddNodePanelStates
    selectedLib: int
    selectedNode: int
    libs: list[tuple[Label, Image | None, str, ModuleType | None]]
    nodes: list[tuple[Label, str, type]]
    objName: Label
    objDescription: Label
    exampleNode: AppGNode

    def __init__(self, appState: AppState, **kwargs) -> None:
        self.state = self.AddNodePanelStates.librarySelect
        self.selectedLib = 0
        self.selectedNode = 0
        self.libs = list()
        self.nodes = list()
        super().__init__(appState, **kwargs)

        for x in self.appState.nodesLibs:
            module = self.appState.nodesLibs[x]
            if module == None:
                continue
            label = Label()
            label.size = (self.appState.uiScale * 5, self.appState.uiScale)
            label.text = f'[ref=lib:{x}]{getattr(self.appState.nodesLibs[x], "humanName", "Unknown library")}[/ref]'
            label.bind(on_ref_press=self.optionSelect)  # type: ignore
            label.color = self.appState.theme["AppAddNodePanel"]["libs_labels_color"]
            label.halign = label.valign = 'center'
            label.text_size = label.size
            label.markup = True
            label.opacity = 0
            label.disabled = True
            image = None
            if hasattr(module, "picture"):
                pathToImg = path.join(getattr(module, "__path__")[0], getattr(
                    module, "picture").replace("/", path.sep))
                image = Image(source=pathToImg)
            self.libs.append((label, image, x, self.appState.nodesLibs[x]))
            self.add_widget(label, extended=False)

        self.objName = Label()
        self.objDescription = Label()
        self.objName.size = self.objDescription.size = (
            self.appState.uiScale, self.appState.uiScale)
        self.objName.text_size, self.objDescription.text_size = self.objName.size, self.objDescription.size
        self.objName.halign = self.objDescription.halign = 'center'
        self.objName.valign = self.objDescription.valign = 'center'
        self.objName.markup = self.objDescription.markup = True
        self.objName.font_size = self.objDescription.font_size = self.appState.uiScale * 0.4
        self.add_widget(self.objName, extended=False)
        self.add_widget(self.objDescription, extended=False)

        self.exampleNode = AppGNode(appState, nodeRootPoint=ExtendedWidget(appState), work=False)
        self.add_widget(self.exampleNode)

    def selectLibrary(self, module: ModuleType | None) -> None:
        self.state = self.AddNodePanelStates.nodeSelect
        if module == None:
            return
        label = Label(text=f'[ref=node:$back$]Back to libraries[/ref]')
        label.size = (self.appState.uiScale * 5, self.appState.uiScale)
        label.bind(on_ref_press=self.optionSelect)  # type: ignore
        label.color = self.appState.theme["AppAddNodePanel"]["nodes_labels_color"]
        label.halign = label.valign = 'center'
        label.text_size = label.size
        label.markup = True
        label.opacity = 0
        label.disabled = True
        self.nodes.append((label, "$back$", type("")))
        self.add_widget(label, extended=False)
        for x in dir(module):
            cls = getattr(module, x)
            if (not (isclass(cls))) or (not (Node in cls.__bases__)):
                continue
            label = Label()
            label.size = (self.appState.uiScale * 5, self.appState.uiScale)
            label.text = f'[ref=node:{x}]{getattr(cls, "name", "Unknown node")}[/ref]'
            label.bind(on_ref_press=self.optionSelect)  # type: ignore
            label.color = self.appState.theme["AppAddNodePanel"]["nodes_labels_color"]
            label.halign = label.valign = 'center'
            label.text_size = label.size
            label.markup = True
            label.opacity = 0
            label.disabled = True
            self.nodes.append((label, x, cls))
            self.add_widget(label, extended=False)

    def nodeSelect(self, cls: type) -> None:
        graphicalNode = AppGNode(self.appState, node=cls())
        actualNodeRootPoint = self.appState.appNodeRootPoint.pos
        graphicalNode.relativePosition = (
            randint(int(-actualNodeRootPoint[0]), int(-actualNodeRootPoint[0] + (
                self.appState.windowSize[0] - graphicalNode.size[0]))),
            randint(int(-actualNodeRootPoint[1]), int(-actualNodeRootPoint[1] + (
                self.appState.windowSize[1] - graphicalNode.size[1])))
        )
        self.appState.nodeHolder.add_widget(graphicalNode, 999)
        self.appState.appAddNodeButton.CloseAppNodePanel()
        return

    def optionSelect(self, instance: Label, value: str) -> None:
        index = -1
        kind = value.split(":")[0]
        value = value.split(":")[1]
        if kind == "lib":
            for x in range(len(self.libs)):
                if self.libs[x][2] == value:
                    index = x
            if self.selectedLib == index:
                self.selectLibrary(self.libs[index][3])
            else:
                self.selectedLib = index
        if kind == "node":
            for x in range(len(self.nodes)):
                if self.nodes[x][1] == value:
                    index = x
            if self.selectedNode == index:
                if value == "$back$":
                    self.state = self.AddNodePanelStates.librarySelect
                    for x in self.nodes:
                        self.remove_widget(x[0])
                    self.nodes.clear()
                    self.draw()
                    return
                else:
                    self.nodeSelect(self.nodes[index][2])
            else:
                self.selectedNode = index
                if len(self.nodes) > 0 and value != "$back$":
                    cls = self.nodes[self.selectedNode][2]
                    self.exampleNode.update_node(cls())
        self.draw()

    def draw(self) -> None:
        if not self.appState.appAddNodePanelOpened:
            if self.canvas is not None:
                self.canvas.before.clear()
            for x in self.children:
                x.opacity = 0
                x.disabled = True
            return
        self.objName.disabled = False
        self.objDescription.disabled = False
        self.objDescription.opacity = 1
        self.objName.opacity = 1
        self.size = self.appState.windowSize
        if self.canvas is not None:
            self.canvas.before.clear()
            background_color = self.appState.theme["AppAddNodePanel"]["background_color"]
            line_color = self.appState.theme["AppAddNodePanel"]["line_between_lib_name_desc_color"]
            with self.canvas.before:
                Color(background_color[0], background_color[1],
                      background_color[2], background_color[3], mode="rgba")
                Rectangle(pos=(0, 0), size=self.size)
                Color(line_color[0], line_color[1],
                      line_color[2], line_color[3], mode="rgba")
                Line(
                    points=(self.size[0] * 0.4, self.size[1] * 0.5, self.size[0]
                            * 0.4 + self.size[0] * 0.2, self.size[1] * 0.5),
                    width=0.04 * self.appState.uiScale,
                    cap='round'
                )
        for x in self.children:
            if x == self.objName or x == self.objDescription:
                continue
            x.opacity = 0
            x.disabled = True
        self.objName.text = "[i]No objects here :([/i]"
        self.objDescription.text = "[i]Ooopsies...[/i]"
        self.objName.pos = (self.size[0] * 0.4, self.size[1] * 0.5)
        self.objDescription.pos = (self.size[0] * 0.4, 0)
        self.objName.size = (self.size[0] * 0.2, self.size[1] * 0.5)
        self.objName.text_size = self.objName.size
        self.objDescription.size = (self.size[0] * 0.2, self.size[1] * 0.5)
        self.objDescription.text_size = self.objName.size
        if ((len(self.libs) <= 0) if self.state == self.AddNodePanelStates.librarySelect else (len(self.nodes) <= 0)):
            return super().draw()

        current = 0
        for x in (self.libs if self.state == self.AddNodePanelStates.librarySelect else self.nodes):
            x[0].pos = (self.size[0] * 0.8 - x[0].size[0] * 0.5, self.size[1]
                        * 0.5 - x[0].size[1] * 0.5 + (current -
                                                      (self.selectedLib if self.state == self.AddNodePanelStates.librarySelect else self.selectedNode)) * 50)
            x[0].font_size = self.appState.uiScale * 0.4 - \
                abs(current - (self.selectedLib if self.state ==
                    self.AddNodePanelStates.librarySelect else self.selectedNode)) * 7
            x[0].opacity = 1
            x[0].disabled = False
            current += 1

        if self.state == self.AddNodePanelStates.librarySelect:
            self.objName.text = self.libs[self.selectedLib][0].text
            self.objDescription.text = getattr(self.appState.nodesLibs[self.libs[self.selectedLib][2]],
                                               "description", "")
            img = self.libs[self.selectedLib][1]
            if img != None:
                if self.canvas is not None:
                    with self.canvas.before:
                        Color(1, 1, 1, 1)
                        rectSize = min(self.size[1] * 0.5, self.size[0] * 0.3)
                        Rectangle(pos=(self.size[0] * 0.05, self.size[1] * 0.5 - rectSize * 0.5), size=(
                            rectSize, rectSize), texture=img.texture)
        if self.state == self.AddNodePanelStates.nodeSelect:
            self.objName.text = self.nodes[self.selectedNode][0].text
            self.objDescription.text = getattr(self.nodes[self.selectedNode][2],
                                               "description", "")
            if len(self.nodes) > 1 and self.nodes[self.selectedNode][1] != "$back$":
                self.exampleNode.relativePosition = (
                    self.size[0] * 0.1, self.size[1] * 0.5 - self.exampleNode.size[1] * 0.5)
                self.exampleNode.opacity = 1
                self.exampleNode.disabled = False

        return super().draw()

    def on_rescale(self, *args) -> None:
        return

    def on_touch_down(self, touch) -> bool | None:
        if (touch.button == "scrolldown" or touch.button == "scrollup") and self.appState.appAddNodePanelOpened:
            delta = 1 if touch.button == "scrolldown" else -1
            if self.state == self.AddNodePanelStates.librarySelect:
                self.selectedLib = min(
                    max(self.selectedLib + delta, 0), len(self.libs) - 1)
            if self.state == self.AddNodePanelStates.nodeSelect:
                self.selectedNode = min(
                    max(self.selectedNode + delta, 0), len(self.nodes) - 1)
                if len(self.nodes) > 0 and self.nodes[self.selectedNode][1] != "$back$":
                    cls = self.nodes[self.selectedNode][2]
                    self.exampleNode.update_node(cls())
            self.draw()
            return super().on_touch_down(touch) or True
        return super().on_touch_down(touch) and False

    def on_touch_move(self, touch) -> bool | None:
        return
    
    def on_touch_up(self, touch) -> bool | None:
        return