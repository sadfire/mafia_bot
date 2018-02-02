from abc import abstractmethod, abstractproperty

from emoji import emojize

from GameLogic.Cards import Cards


class IGameModel:
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game

    @property
    def get_name(self):
        return emojize(':flower_playing_cards:') + " "

    @property
    @abstractmethod
    def _get_event(self):
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
        self.game.log_event(self._get_event, self._initiator, self._target)
        self.game.wasted_cards.append(self.get_card)

    @abstractproperty
    def get_card(self):
        return Cards.Neutral

    @abstractproperty
    def next_state(self):
        pass

    @abstractproperty
    def _get_event(self):
        pass

    @abstractproperty
    def is_target_needed(self):
        return True


