from GameLogic.Member import GameInfo as GI
from GameLogic.Roles import Roles as R
from GameLogic.Views.CommissarCheck import CommissarCheck
from GameLogic.Views.MafiaVoting import MafiaVoting
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class IntroductionView(IGameView):
    def __init__(self, session, game, next_state, model=None, is_mafia=False):
        self.is_mafia = is_mafia
        super().__init__(session, game, next_state, model)
        if self.is_mafia:
            self._next = MafiaVoting
        else:
            self._next = CommissarCheck

    def _greeting(self):
        role = "мафия" if self.is_mafia else "коммисар"
        self._message = self._session.send_message(text="Город засыпает, а просыпается {0}\n\n"
                                                        "Отметье, кто из игроков {0}.".format(role),
                                                   reply_markup=self.choose_kb)

    @property
    def choose_kb(self):
        kb = kbf.empty()
        for number, player in self.game.players.items():
            kb += kbf.button("{}{}".format(player.get_num_str, player.get_role_str),
                             self.set_role_callback,
                             player.number)
        return kb + kbf.button("Закончить", self._end_callback)

    def set_role_callback(self, bot, update, number):
        number = int(number)
        if self.is_mafia and self.game.mafia_count == 3 and number not in self.game.get_mafia_numbers:
            self._session.send_message("Слишком много мафий", reply_markup=kbf.close_button())
            return

        if self.is_mafia:
            self.game[number][GI.Role] = R.Mafia if self.game[number][GI.Role] is not R.Mafia else R.Civilian
        else:
            if self.game[number][GI.Role] is R.Mafia:
                self._session.send_message("Мафия не может быть комиссаром", reply_markup=kbf.close_button())
                return
            if self.game.is_commissar:
                self.game[self.game.get_commissar_number][GI.Role] = R.Civilian

            self.game[number][GI.Role] = R.Commissar if self.game[number][GI.Role] is not R.Commissar else R.Civilian

        self.update_message()

    def update_message(self):
        self._session.edit_message(self._message, None, self.choose_kb)

    @property
    def is_ready(self):
        return (self.is_mafia and self.game.mafia_count == 3) or (not self.is_mafia and self.game.is_commissar)

    def _end_callback(self, bot, update):
        if not self.is_ready:
            self._session.send_message("Игра не может продолжится", reply_markup=kbf.close_button())
            return

        self._session.remove_markup(update)
        self._session.to_next_state()
