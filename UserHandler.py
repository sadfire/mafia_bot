from telegram.ext import MessageHandler, Filters

from KeyboardFactory import KeyboardFactory
from SessionHandler.States import get_query_text


class UserHandler:
    def __init__(self, updater, db, keys) -> None:
        super().__init__()
        self._tmp_dispatcher = MessageHandler(Filters.text, self._text_wait)
        self._db = db
        self._updater = updater
        self._keys = keys
        self._permissions_request = {}

    @staticmethod
    def query_handler(bot, update):
        t_id = update.effective_chat.id
        user = update.effective_message.from_user
        if user.username is None:
            tmp = user.name
        else:
            tmp = '@' + user.username
        bot.send_message(chat_id=t_id,
                         text="Приветствую тебя, {}. Это бот учета статистики игры Мафия.".format(tmp),
                         reply_markup=KeyboardFactory.start_user())

    def query_callback(self, bot, update):
        t_id = update.effective_chat.id
        if t_id in self._keys:
            return

        data = get_query_text(update)

        update.effective_message.edit_text(data)

        if data == "UserOpenStatistic":
            self._user_open_statistic_callback(t_id, update)

        elif data == "GetPermissions":
            self._get_permissions_callback(bot, t_id)

        elif data == "Info_approve": #TODO: Придумать что-то со стилем названий и блятскими колбеками
            self._info_approve_callback(bot, t_id, update)

        elif data.find("OpenGameStat") != -1:
            self._open_game_statistic_callback(bot, data, t_id)

        elif data.find("OpenEveningStat") != -1:
            self._open_evening_statistic_callback(bot, data, t_id)

        elif data == "OpenGame":
            pass

    def _open_evening_statistic_callback(self, bot, data, t_id):
        e_id = data.split('.')[1]
        bot.send_message(chat_id=t_id, text=self._db.get_evening_statistic(e_id),
                         reply_markup=KeyboardFactory.statistic_reply())

    def _open_game_statistic_callback(self, bot, data, t_id):
        g_id = data.split('.')[1]
        bot.send_message(chat_id=t_id, text=self._db.get_game_statistic(g_id),
                         reply_markup=KeyboardFactory.button("Открыть подробнее", "open_advancer"))

    def _info_approve_callback(self, bot, t_id, update):
        self._updater.dispatcher.remove_handler(self._tmp_dispatcher)
        update.effective_message.edit_text("Действие подтверждено.")
        bot.send_message(chat_id=t_id,
                         text="Введущий, что пригласил вас получил запрос на добавление вашего аккаунта  Telegram в базу. \n "
                              "Если в данный момент он ведет вечер, то запрос он получит после окончания вечера.")
        self._db.add_user_permision_request(t_id, self._permissions_request[t_id])

    def _get_permissions_callback(self, bot, t_id):
        bot.send_message(chat_id=t_id, text="Введите либо имя и свои инициалы, либо ваш номер телефона")
        self._updater.dispatcher.add_handler(self._tmp_dispatcher)

    def _user_open_statistic_callback(self, t_id, update):
        update.effective_message.edit_text(text=self._db.get_member_statistic_format(t_id),
                                           reply_markup=KeyboardFactory.statistic_reply())

    def _text_wait(self, bot, update):
        t_id = update.effective_chat.id
        self._permissions_request.update({t_id: update.effective_message})
        bot.send_message(chat_id= t_id, text="Подтверждаете свои данные?",
                         reply_to_message_id=update.effective_message.message_id, reply_markup=KeyboardFactory.approve("Info"))