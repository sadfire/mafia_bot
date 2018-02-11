from abc import abstractproperty, abstractmethod

from emoji import emojize

from GameLogic.Cards import Cards
from GameLogic.Models.IGameModel import IGameModel


class ICardModel(IGameModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._initiator = None
        self._target = None
        self.initiator_ask = False

    @property
    def is_wasted(self):
        return not self.game.cards[self.get_card]

    @property
    def target(self):
        return self._target

    @property
    def is_initiator_needed(self) -> bool:
        return True

    def init_initiator(self, number):
        self._initiator = int(number)

    def init_target(self, number):
        self._target = int(number)

    @property
    def get_result(self):
        return None

    def end(self):
        if (self.is_initiator_needed and self._initiator is None) or (self.is_target_needed and self._target is None):
            return

        self.game.process_card(card=self.get_card,
                               initiator=self._initiator,
                               target=self._target,
                               result=self.get_result)
        self.game.cards[self.get_card] = False

    @property
    @abstractmethod
    def get_card(self) -> Cards:
        return Cards.Neutral

    @property
    @abstractmethod
    def next_state(self):
        pass

    @property
    @abstractmethod
    def is_target_needed(self) -> bool:
        return True

    @abstractmethod
    def get_candidate(self, is_target) -> list:
        pass

    @property
    def get_name(self) -> str:
        return Cards.get_name(self.get_card)

