from GameView.CommissarCheck import CommissarCheck
from GameView.Views import IGameView

from GameLogic.Cards import Cards
from GameLogic.Member import GameInfo as GI
from GameLogic.Roles import Roles as R
from GameView.MafiaVotingView import MafiaVotingView
from Utils.KeyboardUtils import KeyboardFactory as kbf


class IntroductionView(IGameView):
    def __init__(self, session, game, next_state, model=False):
        self.is_mafia = model

        if self.is_mafia:
            self._next = MafiaVotingView
        else:
            self._next = CommissarCheck

        if (self.is_mafia and len(game.get_players(R.Mafia)) == 3) or\
                (not self.is_mafia and game.is_commissar):
            self._session.to_next_state()
            return

        super().__init__(session, game, next_state, None)

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
        return (self.is_mafia and self.game.mafia_count == 3) or (not self.is_mafia and (self.game.is_commissar or
                                                                                         Cards.Recruitment in self.game.wasted_cards))

    def _end_callback(self, bot, update):
        if not self.is_ready:
            self._session.send_message("Игра не может продолжится", reply_markup=kbf.close_button())
            return

        self._session.remove_markup(update)
        self._session.to_next_state()
