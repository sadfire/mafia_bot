from enum import Enum


class Event(Enum):
    SuccessListen = 0,


class Game:
    def __init__(self) -> None:
        super().__init__()
        self.active_player = None

    def log_event(self, event, initiator_player, target_player):
        pass
