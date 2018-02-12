import logging

from emoji import emojize as em
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters

from SessionStates import IState
from SessionStates.EveningHostAdd import EveningHostAdd

from Utils import kbf, mkbf


class EveningManagement(IState):
    def _greeting(self):
        self._session.send_message(text="Начнем вечер!\n"
                                        "Добавьте игроков. \n"
                                        "Вы можете открыть список игроков")

    def __init__(self, session, previous=None):
        super().__init__(session, previous)

        self._next = EveningHostAdd

        self._handler = self._session.add_handler(MessageHandler(Filters.text, self._add_member_handler))
        self._evening = self._session.evening
        self._members_message = None
        # TODO Evening manager connect mode

        if self._evening is None:
            self._evening = self._session.get_evening()

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
                self._send_choose_member_message(request_result)
                self._update_member_list()
            return

        member = request_result

        if not self._evening.add_member(member):
            self._session.send_message("Ошибка при добавление пользователя. Попробуйте снова.")
            return

        self._session.send_message(
            "Игрок {} добавлен. \n Введите следующего или нажмите 'Закончить' вверху.".format(member.name))

        self._update_players_message()

    def _update_players_message(self):
        remove_button = ("❌", self._remove_member_callback)
        empty_button = ("", "empty")

        busy = self._evening.get_busy_players_id()
        kb = kbf.empty()
        for id, player in self._evening.members.items():
            kb += kbf.action_line((str(player), self._session.send_player_info_callback, player.id),
                                  remove_button if id not in busy else empty_button)

        kb = mkbf(kb, 7, self._get_main_kb)

        if self._message is None:
            self._message = self._session.send_message("Вы пока не добавили игроков", reply_markup=kb)
        else:
            self._session.edit_message(self._message, "👥 Игроки:", reply_markup=kb)

    def _remove_member_callback(self, bot, update, data):
        self._evening.remove_member(int(data))
        self._update_players_message()
        self._update_member_list()

    def _send_choose_member_message(self, request_result):
        self._session.send_message(chat_id=self._session.t_id,
                                   text="Под ваш запрос подходит несколько игроков. Ввыберите подходящее",
                                   reply_markup=kbf.players_with_action(
                                       request_result,
                                       em(":heavy_plus_sign:"),
                                       self._session.send_player_info_callback,
                                       self._choose_member_callback))

    def _choose_member_callback(self, bot, update, id):
        member = self._session.db.get_member(id)
        self._evening.add_member(member)
        self._session.send_message(chat_id=self._session.t_id,
                                   text="Игрок добавлен. \n Введите следующего или нажмите '{}' вверху.".format(
                                       em(":+1:")),
                                   reply_markup=kbf.close_button())

    def _open_member_list_callback(self, bot, update):
        kb = self._get_regular_members_kb
        if not kb.is_empty():
            self._members_message = self._session.send_message(em(':necktie: Ваши постоянные игроки'),
                                                               reply_markup=kb)
        else:
            self._session.send_message("Список пуст")

        self._update_players_message()

    def _update_member_list(self):
        kb = self._get_regular_members_kb
        if not kb.is_empty():
            self._session.edit_message(self._members_message, self._members_message.text, kb)
        else:
            self._session.delete_message_callback(self._members_message)
            self._members_message = None

    def _close_member_list_callback(self, bot, update):
        self._session.delete_message_callback(bot, update)
        self._members_message = None
        self._update_players_message()

    def _add_member_callback(self, bot, update, id):
        if not self._evening.add_member(self._session.db.get_member(int(id))):
            self._session.send_message(text="Ошибка при добавление пользователя. Попробуйте снова.",
                                       reply_markup=kbf.close_button())
            return

        kb = self._get_regular_members_kb
        if kb.is_empty():
            self._session.delete_message_callback(bot, update)
        else:
            self._session.edit_message(update.effective_message, update.effective_message.text, kb)

        self._update_players_message()

    @property
    def _get_regular_members_kb(self):
        busy = self._evening.get_busy_players_id() + list(self._evening.members.keys())
        members = [member for member in self._session.db.get_regular_members_by_host(self._session.owner.id)
                   if member.id not in busy]
        members = sorted(members, key=lambda m: m.name)

        if len(members) == 0:
            return kbf.empty()

        return mkbf(kbf.players_with_action(members, "💁🏼‍♂️",
                                            self._session.send_player_info_callback,
                                            self._add_member_callback),
                    5,
                    kbf.button(f"{em(':x:')} Закрыть", self._close_member_list_callback))

    @property
    def _get_main_kb(self):
        kb = kbf.empty()

        if not self._get_regular_members_kb.is_empty() and self._members_message is None:
            kb = kbf.button("Последние игроки", self._open_member_list_callback)

        if self._evening.is_ready():
            kb += kbf.button("Закончить", self._end_added_players_callback)
        else:
            kb += kbf.button("Отменить", self._back_callback)
        return kb

    def _back_callback(self, bot, update):
        from SessionStates import StartState

        self._next = StartState

        self._session.delete_message_callback(bot, update)
        self._session.to_next_state()

    def _end_added_players_callback(self, _, __):
        if self._evening.is_ready():
            if self._members_message is not None:
                try:
                    self._session.delete_message(self._members_message)
                except BadRequest:
                    logging.warning("Cant delete message in {}.{}".format(self.__class__, "_end_added_players_callback"))

            self._session.delete_message(self._message)
            self._session.to_next_state()
        else:
            self._update_players_message()
            self._session.send_message("Не хватает участников", reply_markup=kbf.close_button())
