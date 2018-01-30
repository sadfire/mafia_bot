from Game.Game import Event
from Game.Member import GameInfo as GI
from Game.Models.Models import ICardModel


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
        super().end()
        self.game.players[self._initiator][GI.Role], self.game.players[self._target][GI.Role] = \
        self.game.players[self._target][GI.Role],    self.game.players[self._initiator][GI.Role]


