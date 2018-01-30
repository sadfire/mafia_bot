import logging

from emoji import emojize as em
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters

from Game.Evening import Evening
from KeyboardUtils import KeyboardFactory as KBF
from KeyboardUtils import MultiPageKeyboardFactory as MKBF
from SessionHandler.EveningHostAdd import EveningHostAdd
from SessionHandler.IStates import IState


class EveningManagement(IState):
    def _greeting(self):
        self._session.send_message(text="Начнем вечер!\n"
                                        "Добавьте игроков. \n"
                                        "Вы можете открыть список игроков")

    def __init__(self, session, previous=None):
        super().__init__(session, previous)

        self._next = EveningHostAdd

        self._handler = self._session.add_handler(MessageHandler(Filters.text, self._add_member_handler))

        self._members_message = None

        # TODO Evening manager connect mode

        if self._session.evening is None:
            self._session.evening = Evening(self._session.owner)

        self._update_players_message()

    def __del__(self):
        self._session.remove_handler(self._handler)

    def _add_member_handler(self, bot, updater):
        txt = updater.effective_message.text
        request_result = self._session.db.find_member(txt)

        if isinstance(request_result, list):
            if len(request_result) == 0:
                self._session.send_message("Пользователь не найден. Попробуйте снова.")
            else:
                self._choose_member(request_result)
                self._update_member_list()
            return

        member = request_result

        if not self._session.evening.add_member(member):
            self._session.send_message("Ошибка при добавление пользователя. Попробуйте снова.")
            return

        self._session.send_message(
            "Игрок {} добавлен. \n Введите следующего или нажмите 'Закончить' вверху.".format(member.name))

        self._update_players_message()

    def _update_players_message(self):
        kb = KBF.players_with_action(players=self._session.evening.get_game_bidder(self._session.owner),
                                     callback_player=self._session.send_player_info_callback,
                                     callback_emoji=self._remove_member_callback,
                                     second_line_emoji="❌")

        kb = MKBF(kb, 7, self._get_main_kb)

        if self._message is None:
            self._message = self._session.send_message("Вы пока не добавили игроков", reply_markup=kb)
        else:
            self._session.edit_message(self._message, "👥 Игроки:", reply_markup=kb)

    def _end_added_players_callback(self, bot, update):
        if self._session.evening.is_ready():
            if self._members_message is not None:
                try:
                    self._session.bot.delete_message(chat_id=self._session.t_id,
                                                     message_id=self._members_message.message_id)
                except BadRequest:
                    logging.warning("Cant delete message in _end_added_players_callback")

            self._session.bot.delete_message(self._session.t_id, self._message.message_id)
            self._session.to_next_state()
        else:
            self._update_players_message()
            self._session.send_message("Не хватает участников")

    def _remove_member_callback(self, bot, update, data):
        self._session.evening.remove_member(int(data))
        self._update_players_message()

    def _open_member_list_callback(self, bot, update):
        kb = self._get_regular_members_kb
        if not kb.is_empty():
            self._members_message = self._session.send_message(em(':necktie: Ваши постоянные игроки'),
                                                               reply_markup=kb)
        else:
            self._session.send_message("Список пуст")

        self._update_players_message()

    def _add_member_callback(self, bot, update, id):
        if not self._session.evening.add_member(self._session.db.get_member(int(id))):
            self._session.send_message(text="Ошибка при добавление пользователя. Попробуйте снова.",
                                       reply_markup=KBF.button(f"{em(':x:')} Закрыть",
                                                               self._session.delete_message_callback))

        kb = self._get_regular_members_kb
        if kb.is_empty():
            self._session.delete_message_callback(bot, update)
        else:
            self._session.edit_message(update.effective_message, update.effective_message.text, kb)

        self._update_players_message()

    def _choose_member(self, request_result):
        self._session.send_message(chat_id=self._session.t_id,
                                   text="Под ваш запрос подходит несколько игроков. Ввыберите подходящее",
                                   reply_markup=KBF.players_with_action(
                                       request_result,
                                       em(":heavy_plus_sign:"),
                                       self._session.send_player_info_callback,
                                       self._choose_member_callback))

    def _choose_member_callback(self, bot, update, id):
        member = self._session.db.get_member(id)
        self._session.evening.add_member(member)
        self._session.send_message(chat_id=self._session.t_id,
                                   text="Игрок добавлен. \n Введите следующего или нажмите '{}' вверху.".format(
                                       em(":+1:")))

    def _close_member_list_callback(self, bot, update):
        self._session.delete_message_callback(bot, update)
        self._members_message = None
        self._update_players_message()

    def _update_member_list(self):
        kb = self._get_regular_members_kb
        if not kb.is_empty():
            self._session.edit_message(self._members_message, self._members_message.text, kb)
        else:
            self._session.delete_message_callback(self._members_message)
            self._members_message = None

    @property
    def _get_regular_members_kb(self):
        members = [member
                   for member in self._session.db.get_regular_members_by_host(self._session.owner.id)
                   if member.id not in self._session.evening.get_players_id(self._session.owner)]

        if len(members) == 0:
            return KBF.empty()

        return MKBF(KBF.players_with_action(members, em(":heavy_plus_sign:"),
                                            self._session.send_player_info_callback,
                                            self._add_member_callback),
                    5,
                    KBF.button(f"{em(':x:')} Закрыть", self._close_member_list_callback))

    @property
    def _get_main_kb(self):
        kb = KBF.empty()

        if not self._get_regular_members_kb.is_empty() and self._members_message is None:
            kb = KBF.button("Последние игроки", self._open_member_list_callback)

        if self._session.evening.is_ready():
            kb += KBF.button("Закончить", self._end_added_players_callback)
        else:
            kb += KBF.button("Отменить вечер", self.back_callback)
        return kb
