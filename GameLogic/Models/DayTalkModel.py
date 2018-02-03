from GameLogic.Cards import Cards
from GameLogic.Game import Event
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.Models import IGameModel


class DayTalkModel(IGameModel):
    def end(self):
        pass

    @property
    def _get_event(self):
        return Event.WTF

    def warning(self, number: int, _=None):
        self.game.log_event(Event.Warning, None, number)
        self.game[number][GI.Warnings] += 1

    def kick(self, number: int, _=None):
        self.game.log_event(Event.Kick, None, number)
        self.game[number][GI.IsAlive] = False

    def to_vote(self, initiator: int, target: int):
        self.game.log_event(Event.ToVote, initiator, target)
        self.game.candidates += target

    def withdraw_from_voting(self, number, _=None):
        pass

    def card(self, initiator: int=None, target: int=None, card: Cards=Cards.Neutral):
        pass
