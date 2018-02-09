from threading import Lock

from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from Session import Session
from UserHandler import UserHandler
from Utils import CB_Provider, kbf


class Bot:
    def __init__(self, bot_key, database):
        super(Bot, self).__init__()
        self._token = bot_key
        self._updater = Updater(bot_key)
        self._mutex = Lock()
        self._sessions = {}
        self._evenings = []

        self._wait_text = None
        self._db = database
        self._users_handler = UserHandler(self._db, self._updater)

    def start(self):
        self._add_base_handlers()
        self._updater.start_polling()
        self._updater.idle()

    def _add_base_handlers(self):
        self._updater.dispatcher.add_handler(CommandHandler("start", self._start_callback))
        self._updater.dispatcher.add_handler(CallbackQueryHandler(self.query_callback))

    def query_callback(self, bot, update):
        t_id = update.effective_chat.id

        query = update.callback_query.data
        if self._filter_callbacks(query):
            return getattr(self, query)(bot, update)

        if t_id not in self._sessions.keys():
            providers = self, self._users_handler
        else:
            providers = self, self._sessions[t_id], self._sessions[t_id].state

        return CB_Provider.process(bot, update, providers)

    def _start_callback(self, bot, update):
        t_id = update.effective_chat.id

        if t_id in self._sessions.keys():
            bot.send_message(chat_id=update.effective_chat.id,
                             text="Вы уверены, что хотите перезагрузить бота?",
                             reply_markup=kbf.confirmation(self._bot_reset_callback, self.bot_delete_message_callback))
            return
        username = update.effective_user.name
        if not self._db.check_permission_by_telegram_id(t_id) and self._db.check_permission_by_telegram_name(username):
            self._db.insert_telegram_id(username, t_id)

        if not self._db.check_permission_by_telegram_id(t_id):
            self._users_handler.start_callback(bot, update)
        else:
            self._init_session(bot, update)

    def _init_session(self, bot, update):
        self._sessions[update.effective_chat.id] = Session(updater=self._updater,
                                                           t_id=update.effective_chat.id,
                                                           all_evenings=self._evenings)

    def check_evening(self, host_id):
        for evening in self._evenings:
            if host_id in evening.hosts:
                return evening
        return None

    def _bot_reset_callback(self, bot, update):
        t_id = update.effective_chat.id
        update.effective_message.edit_text("Бот перезагружен.")
        self._sessions.pop(t_id)
        for evening in self._evenings:
            if t_id in evening.hosts and len(evening.hosts) == 1:
                self._evenings.remove(evening)
                break

        self._start_callback(bot, update)

    @classmethod
    def bot_delete_message_callback(cls, bot, update):
        bot.delete_message(update.effective_chat.id, update.effective_message.message_id)

    def _filter_callbacks(self, data):
        return data in dir(self.__class__) and data[-9:] == "_callback"
