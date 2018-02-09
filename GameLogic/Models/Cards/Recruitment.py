from GameLogic import Cards, Roles
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
        return self.game.get_alive(Roles.Civilian if is_target else Roles.Mafia)
