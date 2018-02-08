from emoji import emojize

from GameLogic.Cards import Cards
from GameLogic.GameEvents import Event
from GameLogic.Member import GameInfo
from GameLogic.Models.CardsModel.HealModel import HealModel


class JacketModel(HealModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._event = Event.JacketSave
        self.init_target(self.game.gonna_die)

    @property
    def is_initiator_needed(self):
        return False

    @property
    def get_card(self):
        return Cards.FlakJacket

    @property
    def get_name(self):
        return emojize(':flower_playing_cards:') + " Бронежилет"

    def end(self) -> str:
        if self._initiator is None and self.initiator_ask is False:
            self.game.try_kill()
            return "Игрок {} умер"

        self._initiator = self._target
        self.game.log_event(self._event, self._initiator, self._target)
        self.game.wasted_cards.append(self.get_card)
        self.game[self._initiator][GameInfo.IsCardSpent] = True
        self.game.gonna_die = None
        return "Игрок выжил"