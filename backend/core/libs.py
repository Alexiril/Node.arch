from importlib import util
from os import path, DirEntry
from typing import Any

from backend.core.errors import LibError


def parseLib(lib: DirEntry) -> Any:
    modulePath = path.join(lib, "__init__.py")
    moduleSpec = util.spec_from_file_location(
        lib.name, modulePath
    )
    if moduleSpec is None:
        LibError(
            "Not correct module spec. Please, check module path, if it's possible.", lib.path)
        return
    module = util.module_from_spec(moduleSpec)
    if moduleSpec.loader is None:
        LibError(
            "Have no idea how that had happen. Sorry. Module spec loader was None. Whaaat?..", lib.path)
        return
    moduleSpec.loader.exec_module(module)
    return module
