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
                                   reply_markup=KBF.main())

    def process_callback(self, bot, update):
        data = get_query_text(update)

        if data == "statistic_menu":
            self._next = OpenStatistic
        elif data == "start_evening":
            self._next = EveningManagement
        elif data == "players_menu":
            self._next = PlayerManagement
        else:
            return super().process_callback(bot, update)

        return True


class OpenStatistic(IState):
    pass


class EveningManagement(IState):
    def __init__(self, session, previous=None):
        super().__init__(session, previous)

        self._handler = MessageHandler(Filters.text, self._add_member)
        self._session.add_handler(self._handler)

        self._session.evening = Evening(self._session.host)

    def __del__(self):
        self._session.remove_handler(self._handler)

    def _greeting(self):
        self._session.bot.send_message(self._session.t_id,
                                       text="Начнем вечер!\n"
                                            "Добавьте игроков. \n"
                                            "Для добавления игрока отправьте мне его личный номер, номер телефона или полное имя. (NFC in progress)\n"
                                            "Возможность удалить игроков из списка вам представится после.")
        self._message = self._session.send_message(text="Игроки:\n", reply_markup=self._main_keyboard)

    @property
    def _main_keyboard(self):
        return KBF.button("Открыть 'завсегдатаев'", "open_regular") + KBF.approve("end_evening_adding")

    def _add_member(self, bot, updater):
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
        self._message = self._message.edit_reply_markup(
            reply_markup=KBF.players(self._session.evening.members.values()) + self._main_keyboard)

    def process_callback(self, bot, update):
        data = get_query_text(update)

        if data == "end_evening_adding_approve":
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

        elif data.isdigit():  # ID for delete from evening
            self._remove_member_callback(data)

        elif len(data) > 4 and data[:-4].isdigit():  # ID to add to evening
            self._add_member_callback(data, update)

        elif data == "open_regular":
            self._open_regular_callback()

        elif data == "close":
            self._session.bot.delete_message(self._session.t_id, update.effective_message.message_id)

        elif data.find("choose_member.") != -1:
            self._choose_member_callback(data)

    def _remove_member_callback(self, data):
        self._session.evening.remove_member(int(data))
        self._update_players_message()

    def _choose_member_callback(self, data):
        member = data.split('.')[1]
        self._session.evening.add_member(member)
        self._session.bot.send_message(self._session.t_id,
                                       text="Игрок добавлен. \n Введите следующего или нажмите '{}' вверху.".format(
                                           em(":+1:")))

    def _open_regular_callback(self):
        self._session.send_message(em(':necktie: Ваши постоянные игроки'), reply_markup=self.regular_members)
        self._update_players_message()

    def _add_member_callback(self, data, update):

        if not self._session.evening.add_member(self._session.db.get_member(data[:-4])):
            self._session.send_message("Ошибка при добавление пользователя. Попробуйте снова.")

        update.effective_message.edit_reply_markup(reply_markup=self.regular_members)
        self._update_players_message()

    @property
    def regular_members(self):
        members = []
        for member in self._session.db.get_regular_members(self._session.host.id):
            if member.id not in self._session.evening.members.keys():
                members.append(member)

        if len(members) == 0:
            return KBF.button(em(":no_good:"), "close")

        return KBF.players(members, "_add", em(":heavy_plus_sign:")) + KBF.button(em(":x:"), "close")

    def _choose_member(self, request_result):
        self._session.bot.send_message(self._session.t_id,
                                       text="Под ваш запрос подходит несколько игроков. Ввыберите подходящее",
                                       reply_markup=KBF.choose("choose_member",
                                                                           [em(":bust_in_silhouette:") + str(
                                                                         member.id) + ":" + member.name for member in
                                                                      request_result]))


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
                text_left = '*'+text_left
            if self._active_number == index:
                text_right = '*' + text_right

            kb = kb + KBF.button_line(( (text_left, f"{self.get_member_prefix}{member.id}"), (text_right,f"{self.get_number_prefix}{index}")))

        self._session.bot.edit_message_reply_markup(chat_id=self._message.chat_id, message_id=self._message.message_id, reply_markup=kb + KBF.button("Закончить расчет игроков", self.get_end_query))

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

        self.players[self._active_number], self.players[swap_index] = self.players[swap_index], self.players[self._active_number]
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
