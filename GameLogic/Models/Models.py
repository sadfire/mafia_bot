from abc import abstractmethod

from emoji import emojize


class IGameModel:
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    @property
    def get_name(self):
        return emojize(':flower_playing_cards:') + " "

    @abstractmethod
    @property
    def _get_action(self):
        pass

    @abstractmethod
    def end(self):
        pass


class ICardModel(IGameModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._initiator = None
        self._target = None

    def init_initiator(self, number):
        self._initiator = number

    def init_target(self, number):
        self._target = number

    def end(self):
        self.game.log_event(self._get_action, self._initiator, self._target)

    @abstractmethod
    @property
    def _get_action(self):
        pass

    @property
    def is_target_needed(self):
        return True


