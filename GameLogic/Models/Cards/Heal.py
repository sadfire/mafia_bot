from GameLogic import Roles
from GameLogic.Cards import Cards
from GameLogic.Models.ICard import ICardModel


class HealModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)
        self._target = game.gonna_die

    def get_candidate(self, is_target):
        if is_target:
            return [self.game.gonna_die]

        candidate = [number for number in self.game.get_alive(Roles.Commissar, is_role_reverse=True, is_card_closed=True)
                     if number != self.game.gonna_die]

        return candidate

    @property
    def is_wasted(self):
        return super().is_wasted or self.game.gonna_die is None

    @property
    def target(self):
        return self._target

    @property
    def get_card(self):
        return Cards.Heal

    @property
    def is_target_needed(self):
        return False

    def end(self):
        return "Игрок {} выжил" if super().end() else None

    @property
    def next_state(self):
        from GameView import CardView
        from GameLogic.Models.Cards import JacketModel
        return CardView, JacketModel
