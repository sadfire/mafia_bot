from GameLogic import Cards, GSP
from GameLogic.Models import ICardModel


class LeaderModel(ICardModel):
    def __init__(self, game) -> None:
        super().__init__(game)

    def get_candidate(self, is_target) -> list:
        if is_target:
            return self.game.gonna_die
        else:
            return self.game.get_alive(is_card_closed=True)

    @property
    def is_target_needed(self) -> bool:
        return True

    @property
    def get_card(self) -> Cards:
        return Cards.Leader

    @property
    def is_initiator_needed(self) -> bool:
        return True

    def init_initiator(self, number):
        super().init_initiator(number)

    @property
    def is_wasted(self):
        return not isinstance(self.game.gonna_die, list)

    @property
    def get_target_question(self):
        return "Кого 👨🏽‍⚖️ лидер отправляет на казнь?"

    def final(self):
        result = super().final()

        if result is False:
            self.end_message = "Никто не умирает"
            from GameView import FrontierState
            return FrontierState
        else:
            self.game.cards[self.get_card] = True
            self.end_message = "👨🏽‍⚖️ Лидер сделал свой выбор"
            return GSP.DeathStart(self.game)
