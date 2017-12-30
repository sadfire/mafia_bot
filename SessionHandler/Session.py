from telegram.ext import CallbackQueryHandler, CommandHandler

from MafiaDatabaseApi import Database
from SessionHandler.States import StartState


class Session:
    def __init__(self, bot, updater, t_id, database_class=Database):
        self.bot = bot
        self.t_id = t_id
        self._updater = updater

        self.db = database_class("u{}".format(self.t_id), 'mafia_api')
        self.host = self.db.get_member_by_telegram(self.t_id)

        self.evening = None

        self.state = StartState(self)
        self._handlers = []

    def __del__(self):
        for handler in self._handlers:
            self._updater.dispatcher.remove_handeler(handler)

    def send_message(self, text, reply_markup=None):
        return self.bot.send_message(chat_id=self.t_id, text=text, reply_markup=reply_markup)

    def _add_handlers(self):
        self.add_handler(CallbackQueryHandler(self.query_callback))

    def add_handler(self, handler):
        self._handlers.append(handler)
        self._updater.dispatcher.add_handler(handler)

    def remove_handler(self, handler):
        if handler in self._handlers:
            self._updater.dispatcher.remove_handeler(handler)
            self._handlers.remove(handler)

    def query_callback(self, bot, update):
        if not self._update_filer(update):
            return

        self._remove_markup(update)

        if self.state.process(bot, update):
            self.state = self.state.next()

    @staticmethod
    def _remove_markup(update):
        if update.callback_query.data != "":
            update.effective_message.edit_text(update.effective_message.text)

    def _update_filer(self, update):
        return update.effective_message.chat_id == self.t_id

    @staticmethod
    def update_message_text(update, text):
        update.effective_message.edit_text(update.effective_message.text + text,
                                           reply_markup=update.effective_message.reply_markup)
