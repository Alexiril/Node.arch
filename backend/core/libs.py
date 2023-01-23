import json
from importlib import util
from os import getcwd, path
from typing import Any

from backend.core.errors import LibError


def parseLib(lib: str) -> dict:
    result = dict()
    with open(path.join(getcwd(), "libs", lib, "nodes.json"), 'r') as libJson:
        result = json.loads(libJson.read().replace("\n", ""))
    return result


def parseLibs(libsTree: str) -> dict[str, dict]:
    result = dict()
    tree = json.loads(libsTree)
    for lib in tree:
        if result.get(lib, None) is not None:
            LibError(
                "Come on! Someone is going to rewrite a library. It's not cool! By the way, the library is ", lib)
        else:
            result[lib] = parseLib(lib)
    return result


def getModule(lib: str, moduleName: str) -> Any:
    modulePath = path.join(getcwd(), "libs", lib, "__init__.py")
    moduleSpec = util.spec_from_file_location(
        lib, modulePath
    )
    if moduleSpec is None:
        LibError(
            "Not correct module spec. Please, check module path, if it's possible.", lib, moduleName)
        return
    module = util.module_from_spec(moduleSpec)
    if moduleSpec.loader is None:
        LibError(
            "Have no idea how that had happen. Sorry. Module spec loader was None. Whaaat?..", lib, moduleName)
        return
    moduleSpec.loader.exec_module(module)
    return getattr(getattr(getattr(module, "libs"), lib), moduleName)


def getObjectFromModule(lib: str, moduleName: str, objName: str) -> Any:
    module = getModule(lib, moduleName)
    return getattr(module, objName, None)
