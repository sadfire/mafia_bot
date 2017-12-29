import time
from emoji import emojize as em
from telegram.ext import MessageHandler, Filters

from Game.Evening import Evening
from Game.States import CardWait, MafiaNight
from Game.Cards import CardsBeginner as Cards
from KeyboardFactory import KBFactory


def get_data(update):
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

    def process(self, bot, update):
        data = get_data(update)
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
            return False
        return self._next(self._session, self.__class__)


class StartState(IState):
    def _greeting(self) -> None:
        appeal = self._session.host.name if self._session.host.name != "" else "Ведущий"
        self._session.send_message(text="Приветствую {}. \n "
                                        "Я бот учета статистики игры мафия {}".format(appeal, '🕵'),
                                   reply_markup=KBFactory.main())

    def process(self, bot, update):
        data = get_data(update)

        if data == "statistic_menu":
            self._next = OpenStatistic
        elif data == "start_evening":
            self._next = EveningManagement
        elif data == "players_menu":
            self._next = PlayerManagement
        else:
            return super().process(bot, update)

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
        return KBFactory.button("Открыть 'завсегдатаев'", "open_regular") + KBFactory.approve("end_evening_adding")

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
            reply_markup=KBFactory.players(self._session.evening.members.values()) + self._main_keyboard)

    def process(self, bot, update):
        data = get_data(update)
        if data == "end_evening_adding_approve":
            if self._session.evening.is_ready():
                self._session.bot.delete_message(self._session.t_id, self._message.message_id)
                members = ["{} {} \n".format(em(":bust_in_silhouette:"), member.name) for member in
                           self._session.evening.members.values()]
                self._session.send_message("Игроки: \n{}".format("".join(members)))
                self._next = Game
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
            return KBFactory.button(em(":no_good:"), "close")

        return KBFactory.players(members, "_add", em(":heavy_plus_sign:")) + KBFactory.button(em(":x:"), "close")

    def _choose_member(self, request_result):
        self._session.bot.send_message(self._session.t_id,
                                       text="Под ваш запрос подходит несколько игроков. Ввыберите подходящее",
                                       reply_markup=KBFactory.choose("choose_member",
                                                                     [em(":bust_in_silhouette:") + str(
                                                                         member.id) + ":" + member.name for member in
                                                                      request_result]))


class Game(IState):
    def __init__(self, session, previous=None):
        super().__init__(session, previous)
        self._game_state = CardWait(Cards.ChangeRole, self, MafiaNight)
        self._session.send_message("Будет ли использована карта смена роли?", KBFactory.confirm())

    def process(self, bot, update):
        pass

    def _greeting(self) -> None:
        super()._greeting()
        self._session.send_message("Игра начинается")  # TODO Добавить счетчик игр и чтобы тут писался номер игры
        time.sleep(1)


class PlayerManagement(IState):
    pass
