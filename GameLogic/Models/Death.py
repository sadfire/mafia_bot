from GameLogic import Event
from GameLogic.Models.IGame import IGameModel


class DeathModel(IGameModel):
    @property
    def is_pseudo(self):
        return self.game.gonna_die is None

    def final(self):
        if self.game.gonna_die is None:
            self.end_message = "Никто не умер"
        else:
            number = self.game[self.game.gonna_die].get_num_str
            self.game.log_event(Event.Death, None, self.game.gonna_die)
            self.end_message = "Игрок {} мертв".format(number)

        from GameView import FrontierState
        return FrontierState

    @property
    def get_cards(self) -> list:
        from GameLogic.GameModes import AfterDeathCards
        return [card for card in self.game.get_available_cards if card in AfterDeathCards]
