from abc import abstractmethod, abstractproperty

from emoji import emojize

from GameLogic.Cards import Cards
from GameLogic.Game import Event


class IGameModel:
    def __init__(self, game) -> None:
        super().__init__()
        self.game = game
        self._event = Event.WTF

    @property
    def get_name(self):
        return emojize(':flower_playing_cards:') + " "

    @abstractmethod
    def end(self) -> str:
        return ""


class ICardModel(IGameModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._initiator = None
        self._target = None
        self.initiator_ask = False

    @property
    def target(self):
        return self._target

    @property
    def is_initiator_needed(self):
        return True

    def init_initiator(self, number):
        self._initiator = int(number)

    def init_target(self, number):
        self._target = int(number)

    def end(self):
        self.game.log_event(self._event, self._initiator, self._target)
        self.game.wasted_cards.append(self.get_card)

    @abstractproperty
    def get_card(self):
        return Cards.Neutral

    @abstractproperty
    def next_state(self):
        pass

    @abstractproperty
    def is_target_needed(self):
        return True

    @abstractmethod
    def get_candidate(self, is_target):
        pass