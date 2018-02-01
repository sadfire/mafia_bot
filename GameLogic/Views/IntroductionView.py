from GameLogic.Member import GameInfo as GI
from GameLogic.Roles import Roles as R
from GameLogic.Views.Views import IGameView
from KeyboardUtils import KeyboardFactory as kbf, emoji_number


class IntroductionView(IGameView):
    def __init__(self, session, game, next_state, previous=None, is_mafia=False):
        super().__init__(session, game, next_state, previous)
        self.is_mafia = is_mafia

    def _greeting(self):
        role = "мафией" if self.is_mafia else "комиссаром"
        self._message = self._session.send_message(text="Отметье, кто из игроков является {}.".format(role),
                                                   reply_markup=self.choose_kb + kbf.button("Закончить",
                                                                                            self._end_callback))

    @property
    def choose_kb(self):
        kb = kbf.empty()
        for number, player in self.game.players.items():
            kb += kbf.button("{}{}".format(player.get_num_str, player.get_role_str),
                             self.set_role_callback,
                             player.number)
        return kb

    def set_role_callback(self, bot, update, number):
        if self.is_mafia and self.game.mafia_count == 3:
            self._session.send_message("Слишком много мафий", reply_markup=kbf.close_button())
            return

        if self.is_mafia:
            self.game.players[number][GI.Role] = R.Mafia if self.game.players[number][
                                                                GI.Role] is not R.Mafia else R.Civilian
        else:
            self.game.players[number][GI.Role] = R.Commissar if self.game.players[number][
                                                                    GI.Role] is not R.Commissar else R.Civilian

    def _end_callback(self, bot, update):
        if (self.is_mafia and self.game.mafia_count != 3) and (not self.is_mafia and not self.game.is_commissar):
            self._session.send_message("Игра не может продолжится", reply_markup=kbf.close_button())
            return

        self._session.remove_markup(update)
        self._session.to_next_state()
