import logging

import telegram
from telegram import Message

from GameLogic import Game
from SessionStates import StartState
from Utils import MPProvider, KeyboardFactory, Database, Provider as MultiPageProvider

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class Session:
    def __init__(self, updater, t_id, all_evenings, database_class=Database):
        self.t_id = t_id
        self._updater = updater

        self.db = database_class("u193019697", 'mafia_api')
        self.owner = self.db.get_member_by_telegram(self.t_id)

        self.all_evenings = all_evenings
        self.evening = None

        self.multi_page_provider = MPProvider(self.t_id,
                                              self._updater.bot.send_message,
                                              self._updater.bot.edit_message_text)

        self.state = StartState(self)

        self._handlers = []

    def send_message(self, text, reply_markup=None):
        if isinstance(reply_markup, MPProvider):
            return self.multi_page_provider.send(text, reply_markup)
        else:
            return self._updater.bot.send_message(chat_id=self.t_id, text=text, reply_markup=reply_markup)

    def edit_message(self, message, text="", reply_markup=None):
        if isinstance(message, Message):
            if text == "" or text is None:
                text = message.text

            message = message.message_id
        try:
            if isinstance(reply_markup, MPProvider):
                return self.multi_page_provider.edit(message, text, reply_markup)
            else:
                return self._updater.bot.edit_message_text(chat_id=self.t_id,
                                                           message_id=message,
                                                           text=text,
                                                           reply_markup=reply_markup)
        except telegram.error.BadRequest as e:
            logging.warning(e)

    def delete_message(self, message):
        if isinstance(message, Message):
            message = message.message_id
        self._updater.bot.delete_message(chat_id=self.t_id, message_id=message)

    def add_handler(self, handler):
        self._handlers.append(handler)
        self._updater.dispatcher.add_handler(handler)
        return handler

    def remove_handler(self, handler):
        if handler in self._handlers:
            self._updater.dispatcher.remove_handeler(handler)
            self._handlers.remove(handler)

    def to_next_state(self):
        self.state = self.state.next()

    def get_evening(self, host_id=None):
        if host_id is None:
            host_id = self.t_id

        for evening in self.all_evenings:
            if host_id in evening.hosts:
                self.evening = evening
                break
        else:
            self.evening = self.db.insert_evening(host_id)
            self.all_evenings.append(self.evening)

        return self.evening

    def close_evening(self):
        self.all_evenings.remove(self.evening)

    def start_game(self, players):
        self.evening.games[self.t_id] = Game(self.owner, self.evening, players)

    @staticmethod
    def remove_markup(update):
        if update.callback_query.data != "":
            update.effective_message.edit_text(update.effective_message.text)

    def _filter_update(self, update):
        return update.effective_message.chat_id == self.t_id

    @staticmethod
    def update_message_text(update, text):
        update.effective_message.edit_text(update.effective_message.text + text,
                                           reply_markup=update.effective_message.reply_markup)

    def reset_session_state_callback(self, bot, update):
        pass

    def send_player_info_callback(self, bot, update, player_id):
        self.send_message(self.db.get_member_statistic(player_id),
                          reply_markup=KeyboardFactory.button("Закрыть", callback_data=self.delete_message_callback))

    def to_page_callback(self, bot, update, page):
        try:
            self.multi_page_provider.callback(bot, update, page)
        except ValueError:
            logging.error("MultiPage error. Session have't this multi kb")

    @classmethod
    def delete_message_callback(cls, bot, update=None):
        if isinstance(bot, Message):
            message = bot
            chat_id = message.chat.id
            message_id = message.message_id
        else:
            chat_id = update.effective_chat.id
            message_id = update.effective_message.message_id
        bot.delete_message(chat_id=chat_id, message_id=message_id)

    @classmethod
    def remove_message_keyboard_callback(cls, bot, update):
        update.effective_message.edit_text(update.effective_message.text)
