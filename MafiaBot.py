from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from KeyboardFactory import KeyboardFactory
from MafiaDatabaseApi import Database
from SessionHandler.Session import Session
from SessionHandler.States import get_query_text
from UserHandler import UserHandler


class Bot:
    def __init__(self, bot_key):
        super(Bot, self).__init__()
        self._updater = Updater(bot_key)
        self._sessions = {}
        self._wait_text = None
        self._db = Database('bot', 'YWqYvadPZ35eDHDs')
        self._users_handler = UserHandler(self._updater, self._db, self._sessions.keys())

    def start(self):
        self._add_base_handlers()
        self._updater.start_polling()
        self._updater.idle()

    def _add_base_handlers(self):
        self._updater.dispatcher.add_handler(CommandHandler("start", self._start_callback))
        self._updater.dispatcher.add_handler(CallbackQueryHandler(self._query_handler))

    def _query_handler(self, bot, update):
        t_id = update.effective_chat.id

        if get_query_text(update) == "BOT_RESET_CALLBACK":
            self._bot_reset_session_callback(bot, t_id, update)
            return
        elif get_query_text(update) == "BOT_NOT_RESET_CALLBACK":
            update.effective_message.edit_text("Перезагрузка отменена")
            return

        if t_id not in self._sessions.keys():
            return self._users_handler.request_handler(bot, update)
        else:
            return self._sessions[t_id].query_callback(bot, update)

    def _bot_reset_session_callback(self, bot, t_id, update):
        update.effective_message.edit_text("Бот перезагружен.")
        self._sessions.pop(t_id)
        self._start_callback(bot, update)

    def _start_callback(self, bot, update):
        t_id = update.effective_chat.id

        if t_id in self._sessions.keys():
            bot.send_message(chat_id=update.effective_chat.id,
                             text="Вы уверены, что хотите перезагрузить бота?",
                             reply_markup=KeyboardFactory.button("Да", "BOT_RESET_CALLBACK") + KeyboardFactory.button("Нет", "BOT_NOT_RESET_CALLBACK"))
            return

        if not self._db.check_permission(t_id):
            self._users_handler.query_handler(bot, update)
        else:
            self._init_session(bot, update)

    def _init_session(self, bot, update):
        self._sessions[update.effective_chat.id] = Session(bot, self._updater, update.effective_chat.id)
