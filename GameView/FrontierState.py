from GameView import IGameView
from GameLogic import GSP


class FrontierState(IGameView):
    def __init__(self, session, game, **args):
        super().__init__(session, game, None, False)
        self.game.next_course()
        self.is_pseudo = True

    @property
    def _next(self):
        if self.game.course_count % 2 != 0:
            return GSP.Day(self.game)
        else:
            return GSP.Evening(self.game)