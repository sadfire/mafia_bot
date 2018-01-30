from GameLogic.Game import Game
from GameLogic.Models.Voting import Voting
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, MafiaMarkup, emoji_number


class CivilianVoting(IGameView):
    def __init__(self, session, game: Game, next_state, previous):
        super().__init__(session, game, next_state, previous)
        self._model = Voting(self.game, False)

    @staticmethod
    def vote_message(number):
        return f"Кто голосует за игрока под номером {emoji_number(number)}"

    @property
    def vote_keyboard(self) -> MafiaMarkup:
        man_with_hand = "🙋🏻‍♂️"
        man_without_hand = "🙅🏽‍♂️"

        kb = kbf.empty()
        for vote_count in range(len(self._model.voters)):
            kb += kbf.button(f"{emoji_number(vote_count)} {man_with_hand*2} {man_without_hand*2} {emoji_number(vote_count)}",
                             self.vote_callback,
                             vote_count)

        return kb

    def _greeting(self):
        self._session.send_message(text="Обсуждение закончено. Начинаем голосование.",
                                   reply_markup=self.vote_keyboard)

    def vote_callback(self, bot, update, number):
        pass