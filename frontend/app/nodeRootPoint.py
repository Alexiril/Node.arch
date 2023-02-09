from kivy.graphics import Line, Color

from frontend.ExtendedWidget import ExtendedWidget


class AppNodeRootPoint(ExtendedWidget):

    def draw(self):
        self.colorOne = self.appState.theme["AppNodeRootPoint"]["line_one_color"]
        self.colorTwo = self.appState.theme["AppNodeRootPoint"]["line_two_color"]
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
                    width=0.02 * self.appState.uiScale,
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
                    width=0.02 * self.appState.uiScale,
                    cap='round'
                )
