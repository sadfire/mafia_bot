from GameLogic.Cards import Cards
from GameLogic.GameEvents import Event
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.Models import ICardModel


class SwapRoleModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._event = Event.SwapRole

    @property
    def next_state(self):
        from GameView.IntroductionView import IntroductionView
        return IntroductionView, True

    @property
    def get_card(self):
        return Cards.ChangeRole

    @property
    def get_name(self):
        return super().get_name + 'Смена Роли'

    def get_candidate(self, is_target):
        return self.game.get_alive_players

    @property
    def is_target_needed(self):
        return True

    def end(self):
        if self._initiator is not None and self._target is not None:
            self.game[self._initiator][GI.Role], self.game[self._target][GI.Role] =\
                self.game[self._target][GI.Role], self.game[self._initiator][GI.Role]
            super().end()
            self.game[self._initiator][GI.IsCardSpent] = True
            return "Игроки сменили ролью"
        return None

