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
            self.game.gonna_die = self.candidates.pop()
            self.game.clear_candidates()
            self.is_pseudo = True

        else:
            self._voters_count = len(self._model.voters)
            self.current_candidate = self.candidates.pop()
            self._session.send_message(self.vote_message, self.vote_keyboard)

        self._init_next()

    def _init_next(self):
        if self.is_pseudo:
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
        for vote_count in range(self._voters_count):
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
        self._voters_count -= count
        self._model.voted_out[self.current_candidate] = count

        if len(self.candidates) != 0:
            self.current_candidate = self.candidates.pop()
            self._session.send_message(self.vote_message, self.vote_keyboard)

        elif self._model.max_voted > self._voters_count or self._voters_count == 0:
            self._session.send_message("Голосование окончено")
            self._model.init_target()
