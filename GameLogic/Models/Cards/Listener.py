from GameLogic import GameInfo as GI, Event, Cards, Roles
from GameLogic.Models import ICardModel

from GameView.DayTalkView import DayTalkView


class ListenerModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._event = Event.SuccessListen, Event.FailedListen

    @property
    def get_result(self):
        if self.game[self._target][GI.Role] is Roles.Civilian:
            return self.game[self._initiator][GI.Role] is Roles.Mafia

        return self.game[self._initiator][GI.Role] is Roles.Commissar

    @property
    def next_state(self):
        return DayTalkView

    @property
    def get_card(self):
        return Cards.Listener

    def get_candidate(self, is_target):
        if not is_target:
            return [number for number in self.game.get_alive(is_card_closed=True)
                    if self.game[number][GI.Role] is not Roles.Commissar]

        return self.game.get_alive()

    @property
    def is_target_needed(self):
        return True

    def end(self):
        if super().end():
            return "Игрок услышал " + self.game[self._target].get_role_str

        return None
