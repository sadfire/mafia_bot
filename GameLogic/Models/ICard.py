from abc import abstractmethod

from GameLogic.Cards import Cards
from GameLogic.Models.IGame import IGameModel


class ICardModel(IGameModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._initiator = None
        self._target = None
        self.initiator_ask = False
        self.end_message = ""

    @property
    def is_wasted(self):
        return self.get_card not in self.game.get_available_cards

    @property
    def target(self):
        return self._target

    @property
    def is_initiator_needed(self) -> bool:
        return True

    def init_initiator(self, number):
        self._initiator = int(number)

    def init_target(self, number=None):
        if number is None:
            return
        self._target = int(number)

    @property
    def get_result(self):
        return None

    @abstractmethod
    def final(self):
        if (self.is_initiator_needed and self._initiator is None) or (self.is_target_needed and self._target is None):
            return False

        self.game.process_card(card=self.get_card,
                               initiator=self._initiator,
                               target=self._target,
                               result=self.get_result)

        self.game.cards[self.get_card] = False
        return True

    @property
    @abstractmethod
    def get_card(self) -> Cards:
        return Cards.Neutral

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

    @property
    def get_initiator_question(self):
        return "Номер игрока, использующего карту:"

    @property
    def get_target_question(self):
        return "Номер цели использования карты"

    @property
    def is_target_message_needed(self):
        return True
