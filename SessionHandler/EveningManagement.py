from emoji import emojize as em
from telegram.ext import MessageHandler, Filters

from Game.Evening import Evening
from KeyboardFactory import KeyboardFactory as KBF
from SessionHandler.IStates import IState
from SessionHandler.CalculationOfPlayers import CalculationOfPlayers


class EveningManagement(IState):
    def _greeting(self):
        self._session.bot.send_message(self._session.t_id,
                                       text="Начнем вечер!\n"
                                            "Добавьте игроков. \n"
                                            "Для добавления игрока отправьте мне"
                                            " его личный номер, номер телефона или полное имя. (NFC in progress)\n"
                                            "Возможность удалить игроков из списка вам представится после.")

    def __init__(self, session, previous=None):
        super().__init__(session, previous)

        self._next = CalculationOfPlayers

        self._handler = MessageHandler(Filters.text, self._add_member_handler)
        self._session.add_handler(self._handler)
        self._members_list_message = None
        self._session.evening = Evening(self._session.host)
        self._update_players_message()

    def __del__(self):
        self._session.remove_handler(self._handler)
        self._message = self._session.send_message(text="Игроки:\n", reply_markup=self._get_main_kb)

    def _add_member_handler(self, bot, updater):
        txt = updater.effective_message.text
        request_result = self._session.db.find_member(txt)

        if isinstance(request_result, list):
            if len(request_result) == 0:
                self._session.send_message("Пользователь не найден. Попробуйте снова.")
            else:
                self._choose_member(request_result)
            return

        member = request_result

        if not self._session.evening.add_member(member):
            self._session.send_message("Ошибка при добавление пользователя. Попробуйте снова.")
            return

        self._session.send_message(
            "Игрок {} добавлен. \n Введите следующего или нажмите 'Закончить' вверху.".format(member.name))
        self._update_players_message()

    def _update_players_message(self):
        kb = KBF.players_with_emoji(players=self._session.evening.members.values(),
                                    callback_player=self._session.send_player_info_callback,
                                    callback_emoji=self._remove_member_callback,
                                    second_line_emoji="❌")
        kb += self._get_main_kb

        if self._message is None:
            self._message = self._session.send_message("Вы пока не добавили игроков", reply_markup=kb)
        else:
            self._message = self._message.edit_text("👥 Игроки:", reply_markup=kb)

    def _end_added_players_callback(self, bot, update):
        if self._session.evening.is_ready():
            if self._members_list_message is not None:
                self._session.bot.delete_message(chat_id=self._session.t_id,
                                                 message_id=self._members_list_message.message_id)

            self._session.bot.delete_message(self._session.t_id, self._message.message_id)

            members = ["{} {} \n".format(em(":bust_in_silhouette:"), member.name)
                       for member in self._session.evening.members.values()]

            #self._session.send_message("Игроки: \n{}".format("".join(members)))
            self._session.to_next_state()
        else:
            self._update_players_message()
            self._session.send_message("Не хватает участников")

    def _remove_member_callback(self, data):
        self._session.evening.remove_member(int(data))
        self._update_players_message()

    def _open_member_list_callback(self, bot, update):
        kb = self._get_regular_members_kb
        if not kb.is_empty():
            self._members_list_message = self._session.send_message(em(':necktie: Ваши постоянные игроки'), reply_markup=kb)
            self._members_list_message = None
        else:
            self._session.send_message("Список пуст")

        self._update_players_message()

    def _add_member_callback(self, bot, update, id):
        if not self._session.evening.add_member(self._session.db.get_member(int(id))):
            self._session.send_message("Ошибка при добавление пользователя. Попробуйте снова.")

        kb = self._get_regular_members_kb
        if kb.is_empty():
            self._session.delete_message_callback(bot, update)
        else:
            update.effective_message.edit_reply_markup(reply_markup=kb)
            self._update_players_message()

    def _choose_member(self, request_result):
        self._session.bot.send_message(self._session.t_id,
                                       text="Под ваш запрос подходит несколько игроков. Ввыберите подходящее",
                                       reply_markup=KBF.players_with_emoji(
                                           request_result,
                                           em(":heavy_plus_sign:"),
                                           self._session.send_player_info_callback,
                                           self._choose_member_callback))

    def _choose_member_callback(self, bot, update, id):
        member = self._session.db.get_member(id)
        self._session.evening.add_member(member)
        self._session.bot.send_message(self._session.t_id,
                                       text="Игрок добавлен. \n Введите следующего или нажмите '{}' вверху.".format(
                                           em(":+1:")))

    @property
    def _get_regular_members_kb(self):
        members = [member
                   for member in self._session.db.get_regular_members_by_host(self._session.host.id)
                   if member.id not in self._session.evening.members.keys()]

        if len(members) == 0:
            return KBF.empty()

        return KBF.players_with_emoji(members, em(":heavy_plus_sign:"),
                                      self._session.send_player_info_callback,
                                      self._add_member_callback) + KBF.button("Закрыть", self._session.delete_message_callback)

    @property
    def _get_main_kb(self):
        kb = KBF.button("Последние игроки", self._open_member_list_callback)
        if self._session.evening.is_ready():
            kb += KBF.button("Закончить", self._end_added_players_callback)
        else:
            kb += KBF.button("Отменить вечер", self.back_callback)
        return kb