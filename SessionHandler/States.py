import operator
from random import shuffle
from collections import OrderedDict

from emoji import emojize as em
from telegram.ext import MessageHandler, Filters

from Game.Evening import Evening
from KeyboardFactory import KeyboardFactory as KBF


def get_query_text(update):
    return update.callback_query.data


class IState:
    def __init__(self, session, previous=None):
        self._message = None
        self._next = StartState
        self._session = session
        self._previous = previous
        self._greeting()

    def _greeting(self) -> None:
        pass

    @staticmethod
    def _clear(update, message="Действие отменено"):
        update.effective_message.edit_text(message)

    def process_callback(self, bot, update):
        data = get_query_text(update)
        if data == "Close":
            self._clear(update)
            if self._previous is not None:
                self._next = self._previous
                return True
            else:
                return self._session.start_callback(bot, update)

        return False

    def next(self):
        if self._next is None:
            return self
        return self._next(self._session, self.__class__)


class StartState(IState):
    def _greeting(self) -> None:
        appeal = self._session.host.name if self._session.host.name != "" else "Ведущий"
        self._session.send_message(text="Приветствую {}. \n "
                                        "Я бот учета статистики игры мафия {}".format(appeal, '🕵'),
                                   reply_markup=KBF.main(self._evening_manager_callback,
                                                         self._open_statistic_callback,
                                                         self._player_manager_callback))

    def _open_statistic_callback(self, bot, update):
        self._next = OpenStatistic
        return True

    def _evening_manager_callback(self, bot, update):
        self._next = EveningManagement
        return True

    def _player_manager_callback(self, bot, update):
        self._next = PlayerManagement
        return True


class OpenStatistic(IState):
    pass


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

        self._handler = MessageHandler(Filters.text, self._add_member_handler)
        self._session.add_handler(self._handler)
        self._regular_members_message = None
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
        if self._message is None:
            self._message = self._session.send_message("Текущий вечер:")
        self._message = self._message.edit_reply_markup(reply_markup=kb + self._get_main_kb)

    def _end_evenings_callback(self, bot, update):
        if self._session.evening.is_ready():

            self._session.bot.delete_message(self._session.t_id, self._message.message_id)

            members = ["{} {} \n".format(em(":bust_in_silhouette:"), member.name)
                       for member in self._session.evening.members.values()]

            self._session.send_message("Игроки: \n{}".format("".join(members)))
            self._next = CalculationOfPlayers
            return True
        else:
            self._update_players_message()
            self._session.send_message("Не хватает участников")

    def _remove_member_callback(self, data):
        self._session.evening.remove_member(int(data))
        self._update_players_message()

    def _open_regular_callback(self, bot, update):
        kb = self._get_regular_members_kb
        if not kb.is_empty():
            self._regular_members_message = self._session.send_message(em(':necktie: Ваши постоянные игроки'), reply_markup=kb)
        else:
            self._session.send_message("Список пуст")

        self._update_players_message()

    def _add_member_callback(self, bot, update, id):
        if not self._session.evening.add_member(self._session.db.get_member(int(id))):
            self._session.send_message("Ошибка при добавление пользователя. Попробуйте снова.")

        update.effective_message.edit_reply_markup(reply_markup=self._get_regular_members_kb)
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
        return KBF.button("Последние игроки", self._open_regular_callback) + \
               KBF.button("Закончить", self._end_evenings_callback)


def emoji_number(num: object) -> object:
    return ["0", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟", "0️⃣"][num]


class CalculationOfPlayers(IState):
    # TODO Добавить счетчик игр и чтобы тут писался номер игры
    def _greeting(self) -> None:
        super()._greeting()
        self._message = self._session.send_message("Расчет игроков")

    def __init__(self, session, previous=None):
        super().__init__(session, previous)
        self.players = {}
        self._active_number = None
        self._active_member_id = None

        self.process_randomize_calculation()

        self._update_message()
        self._next = GameInProcess

    def process_randomize_calculation(self):
        self.players.clear()
        indexes = list(range(len(self._session.evening.members)))
        shuffle(indexes)
        for id, member in self._session.evening.members.items():
            self.players[indexes.pop()] = member

    def process_callback(self, bot, update):
        data = get_query_text(update)

        if self.get_number_prefix in data:
            self._number_callback(data.split('_')[-1])

        elif self.get_member_prefix in data:
            self._member_callback(data.split('_')[-1])

        elif self.get_random_query == data:
            self.process_randomize_calculation()

        elif self.get_end_query == data:
            return True

        self._update_message()

    def _update_message(self):
        kb = KBF.button("Перемешать", self.get_random_query)
        for index, member in sorted(self.players.items(), key=operator.itemgetter(0)):

            text_left = member.name
            text_right = emoji_number(index + 1)

            if self._active_member_id == member.id:
                text_left = '*' + text_left
            if self._active_number == index:
                text_right = '*' + text_right

            kb = kb + KBF.button_line(
                ((text_left, f"{self.get_member_prefix}{member.id}"), (text_right, f"{self.get_number_prefix}{index}")))

        self._session.bot.edit_message_reply_markup(chat_id=self._message.chat_id, message_id=self._message.message_id,
                                                    reply_markup=kb + KBF.button("Закончить расчет игроков",
                                                                                 self.get_end_query))

    def _member_callback(self, id):
        self._active_member_id = int(id)
        self._update_calculating()

    def _number_callback(self, index):
        self._active_number = int(index)
        self._update_calculating()

    def _update_calculating(self):
        if self._active_member_id is None or self._active_number is None:
            return

        for index, player in self.players.items():
            if player.id == self._active_member_id:
                swap_index = index
                break
        else:
            raise ValueError()

        self.players[self._active_number], self.players[swap_index] = self.players[swap_index], self.players[
            self._active_number]
        self._active_number, self._active_member_id = None, None

    @property
    def get_random_query(self):
        return "randomize"

    @property
    def get_end_query(self):
        return "end"

    @property
    def get_number_prefix(self):
        return "select_number_"

    @property
    def get_member_prefix(self):
        return "select_member_"


class GameInProcess(IState):
    pass


class PlayerManagement(IState):
    pass
