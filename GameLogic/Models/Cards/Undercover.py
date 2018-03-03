from GameLogic import GameInfo
from GameLogic.Models.ICard import ICardModel


class UndercoverModel(ICardModel):
    def get_candidate(self, is_target):
        return self.game.get_alive(is_card_closed=True)

    @property
    def is_target_needed(self):
        return False

    @property
    def get_card(self):
        from GameLogic.Cards import Cards
        return Cards.Undercover

    @property
    def next_state(self):
        from GameView import CardView
        from GameLogic.Models.Cards import ChangeRoleModel

        return CardView, ChangeRoleModel

    def final(self):
        self._target = self._initiator
        if super().final():
            self.end_message = "Игрок {} ушел под прикрытие."

        return self.next_state
