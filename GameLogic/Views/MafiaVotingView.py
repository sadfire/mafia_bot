from GameLogic.Cards import Cards
from GameLogic.Game import Game
from GameLogic.GameEvents import Event
from GameLogic.Member import GameInfo
from GameLogic.Models.Voting import Voting
from GameLogic.Roles import Roles
from GameLogic.Views.CommissarCheck import CommissarCheck
from GameLogic.Views.Views import IGameView
from KeyboardUtils import MafiaMarkup, KeyboardFactory as kbf, emoji_number as emn


class MafiaVotingView(IGameView):
    def __init__(self, session, game: Game, next_state, model):
        self._model = Voting(game, True)
        super().__init__(session, game, next_state, self._model)
        self._next = CommissarCheck
        self.req_initiator = None

    def _greeting(self):
        self._message = self._session.send_message(text="Приветствую тебя мафия.\n"
                                                        "Кого будем убивать этой ночью?",
                                                   reply_markup=self.vote_keyboard)

    @property
    def vote_keyboard(self) -> MafiaMarkup:
        kb = kbf.button("🎴 Вербовка", self.ask_recruitment_callback) + kbf.button("🔪 Никого", self.kill_callback, -1)
        for number in self._model.get_candidate:
            kb += kbf.button(f"🔪 Игрока {emn(number)}", self.kill_confirm_callback, number)
        return kb

    def update_callback(self, bot, update):
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
        number = int(number)
        if number is -1:
            self._session.edit_message(self._message, f"Никто не под прицелом.")
        else:
            self._model.init_target(number)
            self._session.edit_message(self._message, f"Игрок {emn(number)} на грани жизни и смерти.")

        self._model.end()
        self._session.to_next_state()

    def ask_recruitment_callback(self, bot, update):
        kb = kbf.empty()
        for number in self.game.get_mafia_numbers:
            kb += kbf.button(emn(number), self.recruitment_callback, number)
        self._req_message = self._session.send_message("Кто вербует?", reply_markup=kb)

    def recruitment_callback(self, bot, update, mafia_number):
        mafia_number = int(mafia_number)
        self.game[mafia_number][GameInfo.IsCardSpent] = True
        self.game.wasted_cards.append(Cards.Recruitment)
        self.req_initiator = mafia_number

        kb = kbf.empty()
        for number in self.game.get_civilian_number:
            kb += kbf.button(emn(number), self.recruitment_process_callback, number)
        self._session.edit_message(self._req_message, "Кого вербуем?", reply_markup=kb)

    def recruitment_process_callback(self, bot, update, number):
        number = int(number)
        self.game[number][GameInfo.Role] = Roles.Mafia
        self.game.log_event(Event.Recruitment, initiator_players=self.req_initiator, target_player=number)
        self._session.edit_message(self._req_message, "Завербован {}".format(emn(number)))

    def next(self):
        if not self.game.is_commissar:
            from GameLogic.Views.IntroductionView import IntroductionView
            return IntroductionView(self._session, self.game, None, False)
        else:
            return CommissarCheck(self._session, self.game, None, None)
