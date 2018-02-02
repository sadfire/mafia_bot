from GameLogic.Game import Event as E
from GameLogic.Models.Models import IGameModel


class Voting(IGameModel):
    def __init__(self, game, is_mafia_vote):
        super().__init__(game)
        self.is_mafia_vote = is_mafia_vote
        self._target = None

        self.voted_out = {}

        if not is_mafia_vote:
            self.voters = self.game.get_alive_players(True)
        else:
            self.voters = self.game.get_mafia_numbers

    @property
    def get_candidate(self):
        return self.game.candidates if not self.is_mafia_vote else self.game.get_alive_players

    def vote(self, voters, target):
        pass

    def init_target(self, target):
        self._target = int(target)

    def end(self):
        self.game.log_event(self._get_event, self.voters, self._target)
        self.game.gonna_die = self._target

    @property
    def _get_event(self):
        return E.MafiaWantKilled if self.is_mafia_vote else E.CivilianWantKilled
