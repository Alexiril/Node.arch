from typing import Any
from types import ModuleType

class AppState:
    """Application state class"""

    # Global state structures
    globalSettings: dict
    nodesLibs: dict[str, ModuleType | None]
    theme: dict

    # UI data
    uiScale: float
    windowSize: tuple[int, int]

    # Application process variables
    rootObject: Any
    nodeHolder: Any
    appNodeRootPoint: Any
    appAddNodeButton: Any
    appAddNodePanel: Any
    appNodeRootPointBlocked: bool
    appAddNodePanelOpened: bool
    appNodesMovementBlocked: bool

    def __init__(self) -> None:
        self.globalSettings = dict()
        self.nodesLibs = dict()
        self.theme = dict()
        self.uiScale = 1
        self.windowSize = (0, 0)
        self.rootObject = Any
        self.nodeHolder = Any
        self.appAddNodeButton = Any
        self.appAddNodePanel = Any
        self.appNodeRootPoint = None
        self.appNodeRootPointBlocked = False
        self.appAddNodePanelOpened = False