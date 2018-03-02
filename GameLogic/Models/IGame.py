from abc import abstractmethod

from emoji import emojize

from GameLogic.GameEvents import Event


class IGameModel:
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self._event = Event.WTF

    @property
    def get_name(self):
        return ""

    @abstractmethod
    def final(self) -> str:
        return ""


