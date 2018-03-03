from GameLogic import Game, GSP
from GameLogic.Models import VotingModel

from GameView import IGameView

from Utils import kbf, MafiaMarkup, emoji_number


class CivilianVotingView(IGameView):
    def __init__(self, session, game, model=None, is_greeting=True):
        super().__init__(session=session, game=game, is_greeting=True, model=None)
        self._model = VotingModel(game)
        self.candidates = list(self.game.candidates)

        if len(self.candidates) == 0:
            from GameView import DeathView
            self.__next = DeathView
            self.is_pseudo = True
            return

        if len(self.candidates) == 1:
            self.game.gonna_die = self.candidates.pop()
            self.is_pseudo = True
            self._init_next()
            self._session.edit_message(self._message, "Выставлен только игрок {}".format(emoji_number(self.game.gonna_die)))
            return

        self._voters_count = len(self._model.voters)
        self._send_vote_message()

    def _init_next(self):
        if self._model.is_one_target:
            self._next_state = GSP.DeathStart(self.game)
        else:
            self._next_state = GSP.HalfOfVote(self.game)

    @property
    def vote_message(self):
        return f"Кто голосует за игрока под номером {emoji_number(self.current_candidate)}"

    @property
    def vote_keyboard(self) -> MafiaMarkup:
        man_with_hand = "🙋🏻‍♂️"
        man_without_hand = "🙅🏽‍♂️"

        kb = kbf.empty()
        for vote_count in range(self._voters_count + 1):
            kb += kbf.button(f"{emoji_number(vote_count)}"
                             f"{man_with_hand*2}"
                             f"{emoji_number(vote_count)}"
                             f"{man_without_hand*2}"
                             f"{emoji_number(vote_count)}",
                             self.vote_callback, vote_count)

        return kb

    def _greeting(self):
        self._message = self._session.send_message(text="Обсуждение закончено. Начинаем голосование.")

    def vote_callback(self, bot, update, count):
        self._session.edit_message(update,
                                   "За {} проголосовали {} человек".format(emoji_number(self.current_candidate), count))

        self._voters_count -= count
        self._model.voted_out[self.current_candidate] = count

        if len(self.candidates) == 0 or self._model.max_voted > self._voters_count:
            self.end_vote()
        else:
            self._send_vote_message()

    def end_vote(self):
        self._model.init_target()

        self._session.send_message("Голосование окончено")

        self._model.final()
        self._init_next()

        self._session.to_next_state()

    def _send_vote_message(self):
        self.current_candidate = self.candidates.pop(0)

        if len(self.candidates) == 0:
            self.vote_callback(None, self._session.send_message("За {} проголосовали {} человек"), self._voters_count)

        self._session.send_message(self.vote_message, self.vote_keyboard)
