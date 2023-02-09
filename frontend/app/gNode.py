from kivy.graphics import Color, RoundedRectangle
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from backend.node import Node
from frontend.app.nodeRootPoint import AppNodeRootPoint
from frontend.AppState import AppState
from frontend.ExtendedWidget import ExtendedWidget


class AppGNode(ExtendedWidget):
    min_height: int
    min_width: int
    relativePosition: tuple[float, float]
    node: Node
    nodeRootPoint: AppNodeRootPoint
    title: Label
    params: dict[str, TextInput]
    inputs: dict[str, Label]
    outputs: dict[str, Label]
    touched: bool
    work: bool

    def __init__(self, appState: AppState, **kwargs) -> None:
        self.nodeRootPoint = appState.appNodeRootPoint
        self.node = Node([], [])
        self.title = Label(font_size=appState.uiScale * 0.3)
        self.touched = False
        self.work = True
        self.relativePosition = (0, 0)
        self.params = dict()
        self.inputs = dict()
        self.outputs = dict()
        super().__init__(appState, **kwargs)
        self.size = (
            max(self.size[0], self.appState.uiScale * 3),
            self.appState.uiScale * 2
        )
        self.update_node(self.node)
        self.add_widget(self.title, extended=False)

    def to_front(self) -> None:
        if self.parent is None:
            return
        target = self.parent.canvas.children
        i = target.index(self.canvas)
        target[len(target) - 1], target[i] = target[i], target[len(target) - 1]
        self.appState.nodeHolder.draw()

    def node_param_validate(self, *args) -> None:
        for x in self.params:
            self.node.params[x] = self.params[x].text
        self.node.onValidate()

    def update_node(self, node: Node) -> None:
        self.node = node
        self.title.text = self.node.name
        if len(self.node.params) > 0:
            self.size = (
                self.size[0],
                self.appState.uiScale * 2 + self.appState.uiScale *
                0.6 * len(self.node.params)
            )
        for x in self.params:
            self.remove_widget(self.params[x])
        self.params.clear()
        backgroundColor = self.appState.theme["AppGNode"]["background_color"]
        hintTextColor = self.appState.theme["AppGNode"]["hint_text_color"]
        foregroundColor = self.appState.theme["AppGNode"]["foreground_color"]
        disabledForegroundColor = self.appState.theme["AppGNode"]["foreground_color"]
        selectionColor = self.appState.theme["AppGNode"]["selection_color"]
        cursorColor = self.appState.theme["AppGNode"]["cursor_color"]
        paramsMargin = self.appState.theme["AppGNode"]["params_left_right_margin"]
        for x in self.node.params:
            self.params[x] = TextInput()
            self.params[x].multiline = False
            self.params[x].background_color = backgroundColor
            self.params[x].hint_text_color = hintTextColor
            self.params[x].foreground_color = foregroundColor
            self.params[x].selection_color = selectionColor
            self.params[x].cursor_color = cursorColor
            self.params[x].disabled_foreground_color = disabledForegroundColor
            self.params[x].hint_text = x
            self.params[x].bind(  # type: ignore
                on_text_validate=self.node_param_validate)
            self.params[x].pos_hint = (None, None)
            self.params[x].size_hint = (None, None)
            self.params[x].size = (
                self.size[0] * paramsMargin, self.appState.uiScale * 0.5)
            if not self.work:
                self.params[x].disabled = True
            self.add_widget(self.params[x], extended=False)

    def draw(self) -> None:
        paramsMargin = self.appState.theme["AppGNode"]["params_left_right_margin"]
        bodyColor = self.appState.theme["AppGNode"]["standard_body_color"]
        touchedBodyColor = self.appState.theme["AppGNode"]["touched_body_color"]
        selectedNodeColor = self.appState.theme["AppGNode"]["selected_node_color"]
        self.pos = (self.relativePosition[0] + self.nodeRootPoint.pos[0],
                    self.relativePosition[1] + self.nodeRootPoint.pos[1])
        if self.canvas is not None:
            self.canvas.before.clear()
            x, y = self.pos[0], self.pos[1]
            with self.canvas.before:
                if len(self.appState.nodeHolder.canvas.children) > 0 and self.canvas == self.appState.nodeHolder.canvas.children[-1]:
                    Color(selectedNodeColor[0], selectedNodeColor[1],
                          selectedNodeColor[2], selectedNodeColor[3], mode="rgba")
                else:
                    Color(self.node.color[0], self.node.color[1],
                          self.node.color[2], self.node.color[3], mode="rgba")
                RoundedRectangle(pos=(x - 2.5, y - 2.5), size=(self.size[0] + 5, self.size[1] + 5),
                                 radius=[10, 10, 10, 10])
                Color(bodyColor[0], bodyColor[1],
                      bodyColor[2], bodyColor[3], mode="rgba")
                self.body = RoundedRectangle(
                    pos=self.pos, size=self.size, radius=[10, 10, 10, 10])
                Color(self.node.color[0], self.node.color[1],
                      self.node.color[2], self.node.color[3], mode="rgba")
                self.header = RoundedRectangle(pos=(x, y + self.size[1] - self.appState.uiScale * 0.5), size=(
                    self.size[0], self.appState.uiScale * 0.5), radius=[10, 10, 0, 0])
            self.title.pos = (self.header.pos[0] + self.appState.uiScale * 0.2,
                              self.header.pos[1] - self.appState.uiScale * 0.45)
            current = 0
            for x in self.params:
                self.params[x].pos = (
                    self.pos[0] + (self.size[0] -
                                   self.params[x].size[0]) * 0.5,
                    self.pos[1] + self.size[1] - self.appState.uiScale -
                    self.appState.uiScale * 0.6 * current - paramsMargin * 10
                )
                self.params[x].size = (
                    self.size[0] * paramsMargin, self.appState.uiScale * 0.5
                )
                current += 1
        return super().draw()

    def on_move(self, *args) -> None:
        return

    def on_touch_down(self, touch):
        if self.work and self.collide_point(*touch.pos) and touch.button == 'left' and not self.appState.appNodesMovementBlocked:
            if hasattr(self, "header") and touch.pos[1] > self.header.pos[1]:
                self.touched = True
            self.to_front()
            return super().on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if self.work and self.touched:
            self.relativePosition = (
                self.relativePosition[0] + touch.dx,
                self.relativePosition[1] + touch.dy
            )
            self.draw()
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if self.work and self.touched:
            self.touched = False
            self.draw()
        return super().on_touch_up(touch)
