from GameLogic.Game import Game
from GameLogic.Models.Voting import Voting
from GameLogic.Views.CommissarCheck import CommissarCheck
from GameLogic.Views.Views import IGameView
from KeyboardUtils import MafiaMarkup, KeyboardFactory as kbf, emoji_number as emn


class MafiaVoting(IGameView):
    def __init__(self, session, game: Game, next_state, previous):
        self._model = Voting(game, True)
        super().__init__(session, game, next_state, self._model)
        self._next = CommissarCheck

    def _greeting(self):
        self._message = self._session.send_message(text="Приветствую тебя мафия.\n"
                                                        "Кого будем убивать этой ночью?",
                                                   reply_markup=self.vote_keyboard)

    @property
    def vote_keyboard(self) -> MafiaMarkup:
        kb = kbf.button("🔪 Никого", self.kill_callback, -1)
        for number  in self._model.get_candidate:
            kb += kbf.button(f"🔪 Игрока {emn(number)}", self.kill_confirm_callback, number)
        return kb

    def update_callback(self):
        self._session.edit_message(message=self._message,
                                   text="Приветствую тебя мафия. Кого будем убивать этой ночью?",
                                   reply_markup=self.vote_keyboard)

    def kill_confirm_callback(self, bot, update, number):
        self._session.edit_message(self._message,
                                   text="🔪 Убиваем игрока {}?".format(emn(number)),
                                   reply_markup=kbf.confirmation(no_callback=self.update_callback,
                                                                 yes_callback=self.kill_callback,
                                                                 yes_message="🔪 Да",
                                                                 yes_argument=number))

    def kill_callback(self, bot, update, number):
        self._model.init_target(number)
        self._model.end()
        self._session.edit_message(self._message, f"Игрок {emn(number)} на грани жизни и смерти.")

        self._session.to_next_state()

    def next(self):
        if not self.game.is_commissar:
            from GameLogic.Views.IntroductionView import IntroductionView
            return IntroductionView(self._session, self.game, None, None, False)
        else:
            return CommissarCheck(self._session, self.game, None, None)