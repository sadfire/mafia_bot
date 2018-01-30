from GameLogic.Game import Event
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.Models import ICardModel


class SwapRoleModel(ICardModel):
    @property
    def get_name(self):
        return super().get_name() + 'Смена Роли'

    def _get_action(self):
        return Event.SwapRole

    @property
    def is_target_needed(self):
        return True

    def end(self):
        self.game[self._initiator][GI.Role], self.game[self._target][GI.Role] =\
            self.game[self._target][GI.Role], self.game[self._initiator][GI.Role]

        super().end()
