from GameLogic import Event
from GameLogic.Models.IGame import IGameModel


class DeathModel(IGameModel):
    def __init__(self, game):
        super().__init__(game)
        self.game.course_count += 1

    @property
    def is_pseudo(self):
        return self.game.gonna_die is None

    def end(self) -> str:
        if self.game.gonna_die is None:
            return "Никто не умер"

        number = self.game[self.game.gonna_die].get_num_str
        self.game.log_event(Event.Death, None, self.game.gonna_die)
        self.game.gonna_die = None
        return "Игрок {} мертв".format(number)

    @property
    def get_cards(self) -> list:
        from GameLogic.GameModes import AfterDeathCards
        return [card for card in self.game.get_available_cards if card in AfterDeathCards]
