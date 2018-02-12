from GameLogic import Roles, Event as E, Cards
from GameLogic.Models import IGameModel


class VotingModel(IGameModel):
    def __init__(self, game, is_mafia_vote=False):
        super().__init__(game)
        self.is_mafia_vote = is_mafia_vote
        self._target = None

        self.voted_out = {}

        if not is_mafia_vote:
            self.voters = self.game.get_alive_players(True)
        else:
            self.voters = self.game.get_alive(Roles.Mafia)

    @property
    def available_cards(self):
        cards = self.game.get_available_cards
        if self.is_mafia_vote:
            cards = [card for card in cards
                     if card in [Cards.Recruitment, Cards.Mole, Cards.Rat, Cards.Kitsune, Cards.DeadlyShot]]
        return cards

    @property
    def get_candidate(self):
        return self.game.candidates if not self.is_mafia_vote else self.game.get_alive()

    def init_target(self, target):
        self._target = int(target)

    def end(self):
        self.game.log_event(self._get_event, self.voters, self._target)
        self.game.gonna_die = self._target

    @property
    def _get_event(self):
        return E.MafiaWantKilled if self.is_mafia_vote else E.CivilianWantKilled
