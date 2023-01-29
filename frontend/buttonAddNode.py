from kivy.graphics import RoundedRectangle, Line

from frontend.computedSpriteButton import ComputedSpriteButton
from frontend.panelAddNode import PanelAddNode


class ButtonAddNode(ComputedSpriteButton):

    panelIsOpen: bool
    panelAddNode: PanelAddNode

    def __init__(self, uiScale: float, **kwargs):
        super().__init__(uiScale, **kwargs)
        self.click = self.showAddNodePanel
        self.panelAddNode = PanelAddNode(self.uiScale, **kwargs)
        self.panelAddNode.size_hint = (None, None)
        self.panelAddNode.pos_hint  = (None, None)
        self.panelAddNode.opacity = 0
        self.panelAddNode.disabled = True
        self.panelIsOpen = False

    def post_init(self) -> None:
        self.line_one_color = self.parent.theme["buttonAddNode"]["line_one_color"]
        self.line_two_color = self.parent.theme["buttonAddNode"]["line_two_color"]
        self.baseColor = self.parent.theme["buttonAddNode"]["base_color"]
        self.pressedColor = self.parent.theme["buttonAddNode"]["pressed_color"]
        self.panelAddNode.post_init(self.parent)

    def showAddNodePanel(self) -> None:
        self.add_widget(self.panelAddNode)
        self.panelAddNode.state = 0
        self.panelAddNode.opacity = 1
        self.panelAddNode.disabled = False
        self.panelAddNode.selectedLib = 0
        self.panelAddNode.selectedNode = 0
        self.panelAddNode.size = self.parent.size
        self.panelAddNode.libSelectActions()
        self.panelAddNode.update()
        self.parent.panelAddNodeShowed = True
        self.panelIsOpen = True
        self.click = self.hideAddNodePanel
        self.parent.nodeRootPoint.opacity = 0
        self.parent.nodeRootPoint.disabled = True
        

    def hideAddNodePanel(self) -> None:
        for x in self.panelAddNode.nodesFromLibs:
            self.panelAddNode.remove_widget(x[0])
        self.panelAddNode.nodesFromLibs.clear()
        self.panelAddNode.opacity = 0
        self.panelAddNode.disabled = True
        self.parent.panelAddNodeShowed = False
        self.panelIsOpen = False
        self.click = self.showAddNodePanel
        self.parent.nodeRootPoint.opacity = 1
        self.parent.nodeRootPoint.disabled = False
        self.remove_widget(self.panelAddNode)
        self.draw()

    def draw(self) -> None:
        self.needToRedraw = False
        if self.canvas is not None:
            self.canvas.after.clear()
            if self.panelIsOpen:
                self.panelAddNode.size = self.parent.size
                self.panelAddNode.update()
            with self.canvas.after:
                if self.state == 0:
                    self.getColor(self.baseColor)
                elif self.state == 2 or self.state == 3:
                    self.getColor(self.pressedColor)
                x = self.pos[0]
                y = self.pos[1]
                RoundedRectangle(
                    pos=(x, y),
                    size=(self.uiScale, self.uiScale),
                    radius=[10, 10, 10, 10]
                )
                self.getColor(self.line_one_color)
                if not self.panelIsOpen:
                    Line(
                        points=(
                            x + self.uiScale / 2,
                            y + self.uiScale / 2 + self.uiScale / 4,
                            x + self.uiScale / 2,
                            y + self.uiScale / 2 - self.uiScale / 4
                        ),
                        width=0.04 * self.uiScale,
                        cap='round'
                    )
                    self.getColor(self.line_two_color)
                    Line(
                        points=(
                            x + self.uiScale / 2 + self.uiScale / 4,
                            y + self.uiScale / 2,
                            x + self.uiScale / 2 - self.uiScale / 4,
                            y + self.uiScale / 2
                        ),
                        width=0.04 * self.uiScale,
                        cap='round'
                    )
                else:
                    Line(
                        points=(
                            x + self.uiScale / 2 + self.uiScale / 5,
                            y + self.uiScale / 2 + self.uiScale / 5,
                            x + self.uiScale / 2 - self.uiScale / 5,
                            y + self.uiScale / 2 - self.uiScale / 5
                        ),
                        width=0.04 * self.uiScale,
                        cap='round'
                    )
                    self.getColor(self.line_two_color)
                    Line(
                        points=(
                            x + self.uiScale / 2 - self.uiScale / 5,
                            y + self.uiScale / 2 + self.uiScale / 5,
                            x + self.uiScale / 2 + self.uiScale / 5,
                            y + self.uiScale / 2 - self.uiScale / 5
                        ),
                        width=0.04 * self.uiScale,
                        cap='round'
                    )
