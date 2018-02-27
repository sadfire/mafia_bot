from GameLogic import Roles, Event as E, Cards, GameInfo
from GameLogic.Models import IGameModel


class VotingModel(IGameModel):
    def __init__(self, game, is_mafia_vote=False):
        super().__init__(game)
        self.is_mafia_vote = is_mafia_vote
        self._target = None

        self.voted_out = {}

        if not is_mafia_vote:
            self.voters = self.game.get_alive(filter=lambda pl: pl[GameInfo.IsHaveVote])
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

    def init_target(self, target=None):
        if self.is_mafia_vote:
            self._target = int(target)
        else:
            max_vote = max(self.voted_out.items(), key=lambda candidate_count: candidate_count[1])[1]
            candidates = [candidate for candidate, count in self.voted_out.items() if count == max_vote]
            if len(candidates) == 1:
                self._target = candidates[0]
            else:
                self._target = candidates

    def end(self):
        self.game.log_event(self._get_event, self.voters, self._target)
        self.game.gonna_die = self._target

    @property
    def is_one_target(self):
        return not isinstance(self._target, list)

    @property
    def _get_event(self):
        return E.MafiaWantKilled if self.is_mafia_vote else E.CivilianWantKilled

    @property
    def max_voted(self):
        return max(self.voted_out.values())
