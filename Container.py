from random import randrange
from typing import Dict
from hashlib import md5
from time import sleep


class ThreadContainerLock:
    def __init__(self, dicts: list) -> None:
        self.dicts: list[list[Dict[str, tuple]]] = [
            [{md5(f"{randrange(0,9999999)}".encode()).hexdigest(): d}] for d in dicts
        ]
        self.currentIndex = 0

    def GetNext(self) -> list[Dict[str, tuple]] | None:
        try:
            self.currentIndex += 1
            return list(list(self.dicts[self.currentIndex - 1][0].items())[0])[1]
        except:
            return None

    def isNotNone(self) -> bool:
        try:
            self.dicts[self.currentIndex - 1]
            return True
        except:
            return False


class RestartRouterLock:
    def __init__(self) -> None:
        self.isLocked = False

    def GetNext(self):
        while self.isLocked:
            sleep(1)
