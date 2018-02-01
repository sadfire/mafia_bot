from GameLogic.Game import Game
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.Voting import Voting
from GameLogic.Views.Views import IGameView
from KeyboardUtils import MafiaMarkup, KeyboardFactory as kbf


class MafiaVoting(IGameView):
    def __init__(self, session, game : Game, next_state, previous):
        super().__init__(session, game, next_state, previous)
        self._model = Voting(self.game, True)

    @property
    def vote_keyboard(self) -> MafiaMarkup:
        kb = kbf.button("В воздух", self.kill_callback, -1)
        for number, candidate in self._model.get_candidate:
            kb += kbf.button(f"🔪 :{number}:", self.kill_callback, number)
        return kb

    def _greeting(self):
        self._session.send_message(text="Приветствую тебя мафия. Кого будем убивать этой ночью?",
                                   reply_markup=self.vote_keyboard)

    def kill_callback(self, bot, update, number):
        self._model.init_target(number)
        self._model.end()
        self._session.to_next_state()
