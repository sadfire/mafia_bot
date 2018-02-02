from GameLogic.Cards import Cards
from GameLogic.Game import Event
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.Models import ICardModel


class SwapRoleModel(ICardModel):
    @property
    def next_state(self):
        from GameLogic.Views.IntroductionView import IntroductionView
        return IntroductionView, True

    @property
    def get_card(self):
        return Cards.SwapRole

    @property
    def get_name(self):
        return super().get_name() + 'Смена Роли'

    def _get_event(self):
        return Event.SwapRole

    @property
    def is_target_needed(self):
        return True

    def end(self):
        self.game[self._initiator][GI.Role], self.game[self._target][GI.Role] =\
            self.game[self._target][GI.Role], self.game[self._initiator][GI.Role]

        super().end()
