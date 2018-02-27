from GameLogic import Game
from GameLogic.Models import VotingModel

from GameView import IGameView

from Utils import kbf, MafiaMarkup, emoji_number


class CivilianVotingView(IGameView):
    def __init__(self, session, game: Game, next_state=None, previous=None, model=None):
        super().__init__(session=session,
                         game=game,
                         next_state=next_state,
                         model=VotingModel(game, False),
                         is_greeting=True)

        self.candidates = list(self.game.candidates)

        if len(self.candidates) == 1:
            self.game.gonna_die = self.candidates.pop(0)
            self.game.clear_candidates()
            self.is_pseudo = True
            self._init_next()
        else:
            self._voters_count = len(self._model.voters)
            self.current_candidate = self.candidates.pop(0)
            self._session.send_message(self.vote_message, self.vote_keyboard)

    def _init_next(self):
        if not self.is_pseudo:
            if not self._model.is_one_target:
                from GameView import CardView
                from GameLogic.Models.Cards import LeaderModel
                self._next = CardView, LeaderModel

            else:
                from GameView import CardView
                from GameLogic.Models.Cards import HealModel
                self._next = CardView, HealModel
        else:
            from GameView import DeathView
            self._next = DeathView

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
        self._session.send_message(text="Обсуждение закончено. Начинаем голосование.")

    def vote_callback(self, bot, update, count):
        self._session.edit_message(update,
                                   "За {} проголосовали {} человек".format(emoji_number(self.current_candidate), count))

        self._voters_count -= count
        self._model.voted_out[self.current_candidate] = count

        if len(self.candidates) == 1:
            last_candidate = self.candidates.pop(0)
            self._model.voted_out[last_candidate] = self._voters_count
            self._session.send_message("За {} проголосовали {} человек".format(emoji_number(last_candidate),
                                                                               self._voters_count))
            self.end_vote()

        elif self._model.max_voted > self._voters_count:
            self.end_vote()

        else:
            self.current_candidate = self.candidates.pop(0)
            self._session.send_message(self.vote_message, self.vote_keyboard)

    def end_vote(self):
        self._model.init_target()

        self._session.send_message("Голосование окончено")

        self._model.end()
        self._init_next()

        self._session.to_next_state()
