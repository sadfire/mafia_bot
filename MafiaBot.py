from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from CallbackProvider import CallbackProvider
from KeyboardFactory import KeyboardFactory as KBF
from MafiaDatabaseApi import Database
from SessionHandler.Session import Session
from UserHandler import UserHandler


class Bot:
    def __init__(self, bot_key):
        super(Bot, self).__init__()
        self._updater = Updater(bot_key)
        self._sessions = {}
        self._wait_text = None
        self._db = Database('bot', 'YWqYvadPZ35eDHDs')
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

        if t_id not in self._sessions.keys():
            providers = self, self._users_handler
        else:
            providers = self, self._sessions[t_id], self._sessions[t_id].state

        return CallbackProvider.process_callback(bot, update, providers)

    def _start_callback(self, bot, update):
        t_id = update.effective_chat.id

        if t_id in self._sessions.keys():
            bot.send_message(chat_id=update.effective_chat.id,
                             text="Вы уверены, что хотите перезагрузить бота?",
                             reply_markup=KBF.button("Да", self._bot_reset_callback) +
                                          KBF.button("Нет", self.bot_delete_message_callback))
            return
        # and not self._db.check_permission_by_telegram_name(update.effective_user.name)
        username = update.effective_user.name
        if not self._db.check_permission_by_telegram_id(t_id) and self._db.check_permission_by_telegram_name(username):
            self._db.insert_telegram_id(username, t_id)

        if not self._db.check_permission_by_telegram_id(t_id):
            self._users_handler.start_callback(bot, update)
        else:
            self._init_session(bot, update)

    def _init_session(self, bot, update):
        self._sessions[update.effective_chat.id] = Session(bot, self._updater, update.effective_chat.id)

    def _bot_reset_callback(self, bot, update):
        update.effective_message.edit_text("Бот перезагружен.")
        self._sessions.pop(update.effective_chat.id)
        self._start_callback(bot, update)

    def bot_delete_message_callback(self, bot, update):
        bot.delete_message(update.effective_chat.id, update.effective_message.id)