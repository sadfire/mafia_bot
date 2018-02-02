from GameLogic.Game import Event
from GameLogic.Models.Models import IGameModel


class DayTalkModel(IGameModel):
    def end(self):
        pass

    @property
    def _get_event(self):
        return Event.WTF

