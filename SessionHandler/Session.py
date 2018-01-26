from telegram.ext import CallbackQueryHandler, CommandHandler

from MafiaDatabaseApi import Database
from SessionHandler.IStates import get_query_text
from SessionHandler.StartState import StartState
import logging

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
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    def __del__(self):
        pass

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
        if not self._filter_update(update):
            return

        self._remove_markup(update)
        query = get_query_text(update)

        if len(query) == 0:
            return
        elif query[0] != '_' and self._filter_callbacks(query):
            return getattr(self, query)(bot, update)

        query, *arguments = query.split('.') + [None]

        if len(arguments) < 3:
            arguments = arguments[0]

        try:
            callback = getattr(self.state, query, self.state.process_callback)
            if arguments is None:
                is_next = callback(bot, update)
            else:
                is_next = callback(bot, update, arguments)

            if is_next:
                self.state = self.state.next()
        except AttributeError as er:
            logging.warning(er)
            logging.warning("Callback error: ",query, arguments)

    @staticmethod
    def _remove_markup(update):
        if update.callback_query.data != "":
            update.effective_message.edit_text(update.effective_message.text)

    def _filter_update(self, update):
        return update.effective_message.chat_id == self.t_id

    @staticmethod
    def update_message_text(update, text):
        update.effective_message.edit_text(update.effective_message.text + text,
                                           reply_markup=update.effective_message.reply_markup)

    def delete_message_callback(self, bot, update):
        bot.delete_message(chat_id=update.effective_chat.id, message_id=update.effective_message.message_id)

    def send_player_info_callback(self, bot, update, player_id):
        self.send_message(self.db.get_member_statistic(player_id), reply_markup=self.delete_message_callback)

    def _filter_callbacks(self, data):
        return len(data) != 0 and data in dir(self.__class__) and data[-9:] == "_callback"
