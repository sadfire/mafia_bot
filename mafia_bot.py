"""
This is main MafiaBot module class.

For example
>>> from Utils import Database
>>> db = Database("username", "password")
>>> bot = Bot("400346126:AAHEXx97I80X-14gOnvl8E1nzhPhk95BQI8", db)
"""
from threading import Lock

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from Session import Session
from UserHandler import UserHandler
from Utils import CB_Provider, kbf


class Bot:
    """
    Main class. To create, process and work with mafia game statistic - work with this class.
    """
    def __init__(self, bot_key, database):
        """

        :param bot_key: Token from BotFather telegram bot
        :param database: Initialized database instance
        """
        super(Bot, self).__init__()
        self._token = bot_key
        self._updater = Updater(bot_key)
        self._mutex = Lock()
        self._sessions = {}
        self._evenings = []

        self._db = database
        self._users_handler = UserHandler(self._db, self._updater)

    def start(self) -> None:
        """
        Start work of bot
        """
        self._add_base_handlers()
        self._updater.start_polling()
        self._updater.idle()

    def _add_base_handlers(self) -> None:
        """
        Add handlers to command start and buttons
        """
        self._updater.dispatcher.add_handler(CommandHandler("start", self._start_cmd_callback))
        self._updater.dispatcher.add_handler(CallbackQueryHandler(self._query_callback))

    def _query_callback(self, bot, update):
        """
        All query handler

        :param bot: Formal param from telegram lib
        :param update: Formal param from telegram lib
        :return: Result from callback process
        """
        t_id = update.effective_chat.id

        query = update.callback_query.data
        if self._filter_callbacks(query):
            return getattr(self, query)(bot, update)

        if t_id not in self._sessions.keys():
            providers = self, self._users_handler
        else:
            providers = self, self._sessions[t_id], self._sessions[t_id].state

        return CB_Provider.process(bot, update, providers)

    def _start_cmd_callback(self, bot, update):
        """
        Start command handler. If session exist, ask question to reset session.

        :param bot: Formal param from telegram lib
        :param update: Formal param from telegram lib
        """
        t_id = update.effective_chat.id

        if t_id in self._sessions.keys():
            bot.send_message(chat_id=update.effective_chat.id,
                             text="Вы уверены, что хотите перезагрузить бота?",
                             reply_markup=kbf.confirmation(
                                 self._bot_reset_callback,
                                 self.bot_delete_message_callback))
            return

        username = update.effective_user.name
        if not self._db.check_permission(t_id=t_id) and \
                self._db.check_permission(t_name=username):
            self._db.insert_telegram_id(username, t_id)

        if not self._db.check_permission(t_id=t_id):
            self._users_handler.start_callback(bot, update)
        else:
            self._init_session(update.effective_chat.id)

    def _init_session(self, t_id):
        """
        Insert session to session list
        :param t_id: Telegram id for new session
        """
        self._sessions[t_id] = \
            Session(updater=self._updater,
                    t_id=t_id,
                    all_evenings=self._evenings)

    def _check_evening(self, host_id):
        """
        Get exist evening from evening list
        :param host_id: If of host
        :return:
        """
        for evening in self._evenings:
            if host_id in evening.hosts:
                return evening
        return None

    def _bot_reset_callback(self, bot, update):
        """
        Reset session and create new callback
        :param bot: Formal param from telegram lib
        :param update: Formal param from telegram lib
        """
        t_id = update.effective_chat.id
        update.effective_message.edit_text("Бот перезагружен.")
        self._sessions.pop(t_id)
        for evening in self._evenings:
            if t_id in evening.hosts and len(evening.hosts) == 1:
                self._evenings.remove(evening)
                break

        self._start_cmd_callback(bot, update)

    @classmethod
    def bot_delete_message_callback(cls, bot, update):
        """
        Delete message from callback
        :param bot: Formal param from telegram lib
        :param update: Formal param from telegram lib
        """
        bot.delete_message(chat_id=update.effective_chat.id,
                           message_id=update.effective_message.message_id)

    def _filter_callbacks(self, data):
        """
        Filter query data
        :param data: query text
        :return: if data is method of this class - return true
        """
        return data in dir(self.__class__) and data[-9:] == "_callback"
