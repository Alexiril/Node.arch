from kivy.uix.widget import Widget

from backend.errors import FrontendError
from frontend.AppState import AppState


class ExtendedWidget(Widget):
    """Application extended widget class"""

    appState: AppState
    post_initialized: bool
    notExtendedChildren: list[Widget]

    def __init__(self, appState: AppState, **kwargs) -> None:
        testWidget = Widget()
        delParamList = list()
        for param in kwargs:
            if not hasattr(testWidget, param):
                setattr(self, param, kwargs[param])
                delParamList.append(param)
        for param in delParamList:
            del kwargs[param]
        super().__init__(**kwargs)
        self.appState = appState
        self.bind(size=self.on_rescale, pos=self.on_move)  # type: ignore
        self.post_initialized = False
        self.notExtendedChildren = list()

    def post_init(self) -> None:
        for x in self.children:
            if not x in self.notExtendedChildren:
                x.post_init()
        self.post_initialized = True

    def draw(self) -> None:
        if not self.post_initialized:
            self.post_init()
        for x in self.children:
            if not x in self.notExtendedChildren:
                x.draw()

    def add_widget(self, widget, index=0, canvas=None, extended=True) -> None | FrontendError:
        if not ExtendedWidget in type(widget).__mro__:
            if extended:
                return FrontendError("Not correct type of the widget. It should be 'ExtendedWidget' class.")
            else:
                self.notExtendedChildren.append(widget)
        return super().add_widget(widget, index, canvas)
    
    def remove_widget(self, widget):
        if ExtendedWidget in type(widget).__mro__:
            widget.on_delete()
        return super().remove_widget(widget)

    def on_delete(self):
        pass

    def on_rescale(self, *args) -> None:
        self.draw()

    def on_move(self, *args) -> None:
        self.draw()

    def on_touch_down(self, touch) -> bool | None:
        if self.collide_point(*touch.pos):
            return super().on_touch_down(touch) or True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch) -> bool | None:
        if self.collide_point(*touch.pos):
            return super().on_touch_move(touch) or True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch) -> bool | None:
        if self.collide_point(*touch.pos):
            return super().on_touch_up(touch) or True
        return super().on_touch_up(touch)
