from emoji import emojize as em
from telegram.ext import MessageHandler, Filters

from KeyboardFactory import KeyboardFactory as KBF
from SessionHandler.States import get_query_text


class UserHandler:
    def __init__(self, db, updater) -> None:
        super().__init__()
        self._tmp_dispatcher = MessageHandler(Filters.text, self._text_wait_handler)
        self._db = db
        self._updater = updater
        self._permissions_request = {}

    def start_callback(self, bot, update):
        user = update.effective_message.from_user

        if user.username is None:
            username = user.name
        else:
            username = '@' + user.username

        bot.send_message(chat_id=update.effective_chat.id,
                         text="Приветствую тебя, {}. Это бот учета статистики игры Мафия.".format(username),
                         reply_markup=KBF.start_user(
                             self._user_open_statistic_callback, self._get_permissions_callback))

    def query_callback(self, bot, update):
        query = get_query_text(update)

        update.effective_message.edit_reply_markup()

        arguments = None
        if '.' in query:
            arguments = query.split('.')
            query = arguments[0]
            arguments = arguments[1:]

        if not self._filter_callbacks(query):
            return

        callback = getattr(self, query)

        if arguments is not None:
            return callback(bot, update, arguments)

        return callback(self, query)(bot, update)

    def _filter_callbacks(self, data):
        return data in dir(self.__class__) and data[-9:] == "_callback"

    def _open_evenings_list_callback(self, bot, update):
        pass

    def _open_games_list_callback(self, bot, update):
        kb = KBF.empty()
        for game in self._db.get_member_games(update.effective_chat.id):
            kb += KBF.button(str(game), self._open_game_callback, game.id)

        kb += KBF.button("Закрыть список", self._delete_message_callback)

        update.effective_message.edit_text(text="Список ваших игр",
                                           reply_markup=kb)

    def _open_game_callback(self, bot, update, g_id):
        game = self._db.get_game(g_id)
        bot.send_message(chat_id=update.effective_chat.id,
                         text=game.formate(),
                         reply_markup=KBF.button("Закрыть список", self._delete_message_callback))

    def _user_open_statistic_callback(self, bot, update):
        t_id = update.effective_chat.id

        keyboard = KBF.button("{} Игры".format(em(":memo:")), self._open_games_list_callback)
        keyboard += KBF.button("{} Вечера".format(em(":last_quarter_moon:")), self._open_evenings_list_callback)

        update.effective_message.edit_text(text=self._db.get_member_statistic_format(t_id),
                                           reply_markup=keyboard)

    def _text_wait_handler(self, bot, update):
        t_id = update.effective_chat.id
        self._permissions_request.update({t_id: update.effective_message})
        self._updater.dispatcher.remove_handler(self._tmp_dispatcher)
        bot.send_message(chat_id=t_id, text="Подтверждаете свои данные?",
                         reply_to_message_id=update.effective_message.message_id,
                         reply_markup=KBF.button("Да", self._info_approve_callback) +
                                      KBF.button("Повторить ввод", self._info_repeat))

    def _info_repeat(self, bot, update):
        self._updater.dispatcher.add_handler(self._tmp_dispatcher)
        update.effective_message.edit_text("Повторите ввод данных")

    def _info_approve_callback(self, bot, t_id, update):

        self._updater.dispatcher.remove_handler(self._tmp_dispatcher)

        update.effective_message.edit_text("Действие подтверждено.")
        bot.send_message(chat_id=t_id,
                         text="Введущий, что пригласил вас получил запрос на добавление вашего аккаунта Telegram в "
                              "базу. \n "
                              "Если в данный момент он ведет вечер, то запрос он получит после окончания вечера.")
        self._db.add_user_permision_request(t_id, self._permissions_request[t_id])

    def _get_permissions_callback(self, bot, t_id):
        bot.send_message(chat_id=t_id, text="Введите либо имя и свои инициалы, либо ваш номер телефона")
        self._updater.dispatcher.add_handler(self._tmp_dispatcher)

    def _delete_message_callback(self, bot, update):
        bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)