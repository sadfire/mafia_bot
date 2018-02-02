from GameLogic.Member import GameInfo as GI
from GameLogic.Roles import Roles as R
from GameLogic.Views.MafiaVoting import MafiaVoting
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class IntroductionView(IGameView):
    def __init__(self, session, game, next_state, model=None, is_mafia=False):
        self.is_mafia = is_mafia
        super().__init__(session, game, next_state, model)
        self._next = MafiaVoting

    def _greeting(self):
        role = "мафией" if self.is_mafia else "комиссаром"
        self._message = self._session.send_message(text="Отметье, кто из игроков является {}.".format(role),
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
        mafia_num = self.game.get_mafia_num
        if self.is_mafia and self.game.mafia_count == 3 and number not in mafia_num:
            self._session.send_message("Слишком много мафий", reply_markup=kbf.close_button())
            return
        number = int(number)
        if self.is_mafia:
            self.game[number][GI.Role] = R.Mafia if self.game[number][GI.Role] is not R.Mafia else R.Civilian
        else:
            self.game[number][GI.Role] = R.Commissar if self.game[number][GI.Role] is not R.Commissar else R.Civilian
        self.update_message()

    def update_message(self):
        self._session.edit_message(self._message, None, self.choose_kb)

    def _end_callback(self, bot, update):
        if (self.is_mafia and self.game.mafia_count != 3) and (not self.is_mafia and not self.game.is_commissar):
            self._session.send_message("Игра не может продолжится", reply_markup=kbf.close_button())
            return

        self._session.remove_markup(update)
        self._session.to_next_state()
