from GameLogic import Cards, Roles as R, GameInfo as GI
from GameLogic.Models import ICardModel


class RecruitmentModel(ICardModel):
    @property
    def is_target_needed(self) -> bool:
        return True

    @property
    def next_state(self):
        from GameView import MafiaVotingView
        return MafiaVotingView

    @property
    def get_card(self) -> Cards:
        return Cards.Recruitment

    def get_candidate(self, is_target) -> list:
        if is_target:
            return [number for number in self.game.get_alive() if self.game[number][GI.Role] is not R.Mafia]
        return self.game.get_alive(R.Mafia)
