from kivy.graphics import Color, Line, RoundedRectangle

from frontend.AppState import AppState
from frontend.Button import AppButton


class AppAddNodeButton(AppButton):

    def __init__(self, appState: AppState, **kwargs) -> None:
        super().__init__(appState, **kwargs)
        self.on_click = self.OpenAppNodePanel

    def OpenAppNodePanel(self) -> None:
        self.on_click = self.CloseAppNodePanel
        self.appState.appAddNodePanelOpened = True
        self.appState.appNodeRootPointBlocked = True
        self.appState.appNodesMovementBlocked = True
        self.appState.appAddNodePanel.disabled = False
        self.appState.rootObject.draw()

    def CloseAppNodePanel(self) -> None:
        self.on_click = self.OpenAppNodePanel
        self.appState.appAddNodePanelOpened = False
        self.appState.appNodeRootPointBlocked = False
        self.appState.appNodesMovementBlocked = False
        self.appState.appAddNodePanel.disabled = True
        self.appState.rootObject.draw()

    def draw(self) -> None:
        self.pos = (
            self.appState.windowSize[0] - self.appState.uiScale - 0.1 * self.appState.uiScale,
            self.appState.windowSize[1] - self.appState.uiScale - 0.1 * self.appState.uiScale
        )
        if self.canvas is not None:
            line_one_color = self.appState.theme["AppAddNodeButton"]["line_one_color"]
            line_two_color = self.appState.theme["AppAddNodeButton"]["line_two_color"]
            baseColor = self.appState.theme["AppAddNodeButton"]["base_color"]
            pressedColor = self.appState.theme["AppAddNodeButton"]["pressed_color"]
            self.canvas.after.clear()
            with self.canvas.after:
                if self.state == 0:
                    Color(baseColor[0], baseColor[1], baseColor[2], baseColor[3], mode="rgba")
                elif self.state == 2 or self.state == 3:
                    Color(pressedColor[0], pressedColor[1], pressedColor[2], pressedColor[3], mode="rgba")
                x = self.pos[0]
                y = self.pos[1]
                RoundedRectangle(
                    pos=(x, y),
                    size=(self.appState.uiScale, self.appState.uiScale),
                    radius=[10, 10, 10, 10]
                )
                Color(line_one_color[0], line_one_color[1], line_one_color[2], line_one_color[3], mode="rgba")
                if not self.appState.appAddNodePanelOpened:
                    Line(
                        points=(
                            x + self.appState.uiScale / 2,
                            y + self.appState.uiScale / 2 + self.appState.uiScale / 4,
                            x + self.appState.uiScale / 2,
                            y + self.appState.uiScale / 2 - self.appState.uiScale / 4
                        ),
                        width=0.04 * self.appState.uiScale,
                        cap='round'
                    )
                else:
                    Line(
                        points=(
                            x + self.appState.uiScale / 2 + self.appState.uiScale / 5,
                            y + self.appState.uiScale / 2 + self.appState.uiScale / 5,
                            x + self.appState.uiScale / 2 - self.appState.uiScale / 5,
                            y + self.appState.uiScale / 2 - self.appState.uiScale / 5
                        ),
                        width=0.04 * self.appState.uiScale,
                        cap='round'
                    )
                Color(line_two_color[0], line_two_color[1], line_two_color[2], line_two_color[3], mode="rgba")
                if not self.appState.appAddNodePanelOpened:
                    Line(
                        points=(
                            x + self.appState.uiScale / 2 + self.appState.uiScale / 4,
                            y + self.appState.uiScale / 2,
                            x + self.appState.uiScale / 2 - self.appState.uiScale / 4,
                            y + self.appState.uiScale / 2
                        ),
                        width=0.04 * self.appState.uiScale,
                        cap='round'
                    )
                else:
                    Line(
                        points=(
                            x + self.appState.uiScale / 2 - self.appState.uiScale / 5,
                            y + self.appState.uiScale / 2 + self.appState.uiScale / 5,
                            x + self.appState.uiScale / 2 + self.appState.uiScale / 5,
                            y + self.appState.uiScale / 2 - self.appState.uiScale / 5
                        ),
                        width=0.04 * self.appState.uiScale,
                        cap='round'
                    )

    def on_move(self, *args) -> None:
        return