from os.path import join

from kivy.uix.image import Image

from frontend.app.background import AppBackground
from frontend.app.nodeRootPoint import AppNodeRootPoint
from frontend.app.addNodeButton import AppAddNodeButton
from frontend.app.addNodePanel import AppAddNodePanel
from frontend.AppState import AppState
from frontend.ExtendedWidget import ExtendedWidget


class AppRootWidget(ExtendedWidget):

    def __init__(self, appState: AppState, **kwargs) -> None:
        super().__init__(appState, **kwargs)
        self.appState.rootObject = self
        background_tx = Image(
            source=join("themes", self.appState.theme["AppBackground"]["texture_source"]))
        tx_multiplier = self.appState.theme["AppBackground"]["texture_multiplier"]
        tx_color = self.appState.theme["AppBackground"]["texture_color"]
        bg_color = self.appState.theme["AppBackground"]["background_color"]
        self.add_widget(AppBackground(
            appState,
            texture=background_tx,
            texture_multiplier=tx_multiplier,
            color=tx_color,
            color_background=bg_color
        ))
        self.appState.appNodeRootPoint = AppNodeRootPoint(appState)
        self.appState.nodeHolder = ExtendedWidget(appState)
        self.appState.appAddNodeButton = AppAddNodeButton(appState)
        self.appState.appAddNodePanel = AppAddNodePanel(appState, disabled=True)
        self.add_widget(self.appState.nodeHolder)
        self.add_widget(self.appState.appNodeRootPoint)
        self.add_widget(self.appState.appAddNodePanel)
        self.add_widget(self.appState.appAddNodeButton)
    
    def on_rescale(self, *args) -> None:
        self.appState.windowSize = self.size
        return super().on_rescale(*args)
    
    def on_touch_down(self, touch) -> bool | None:
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if not self.appState.appNodeRootPointBlocked and touch.button == "middle":
            moveSceneSpeed = self.appState.globalSettings["scene moving speed"]
            self.appState.appNodeRootPoint.pos = (
                self.appState.appNodeRootPoint.pos[0] + (touch.dx) * moveSceneSpeed,
                self.appState.appNodeRootPoint.pos[1] + (touch.dy) * moveSceneSpeed
            )
            self.draw()
        return super().on_touch_move(touch)