import sys
from random import random

from emoji import emojize
from telegram.ext import Updater, CallbackQueryHandler

from CallbackProvider import Provider

from KeyboardUtils import KeyboardFactory as kbf, MultiPageKeyboardFactory, emoji_number


class KeyboardTests:
    def __init__(self, token):
        self.kb = None
        self.token = token
        self.updater = Updater(self.token)

    def callback_test(self, bot, update):
        Provider.process(bot, update, (self,))
        return True

    def to_page_callback(self, bot, update, page):
        update.effective_message.edit_text(text=update.effective_message.text + "+1",
                                           reply_markup=self.kb.to_markup(int(page)))

    def multi_page_test(self):
        self.updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_test))
        self.kb = kbf.double_button("Button1", "Button", "Button1", "Button") + \
                  kbf.button(text="Button2", callback_data="Button") + \
                  kbf.double_button("Button3", "Button", "Button3", "Button") + \
                  kbf.button(text="Button4", callback_data="Button") + \
                  kbf.double_button("Button5", "Button", "Button5", "Button") + \
                  kbf.button(text="Button6", callback_data="Button")

        self.kb = MultiPageKeyboardFactory(self.kb, 2, kbf.button("Закончить", "end"))

        self.updater.bot.send_message(chat_id=193019697, text="Test", reply_markup=self.kb.to_markup(0))
        self.updater.start_polling()
        self.updater.idle()

    def callback_player(self, bot, update, id):
        pass

    def callback_action(self, bot, update, id):
        return True

    def game_view_test(self):
        kb = kbf.empty()
        self.updater.bot.send_message(chat_id=193019697, text=f"🗡 Убивали игрока 1️⃣\n"
                                                              f"Будет ли использована "
                                                              f"{emojize(':flower_playing_cards:')} карта лечение?",
                                      reply_markup=kbf.confirmation(self.callback_action, self.callback_action))
        self.updater.bot.send_message(chat_id=193019697, text=f"🗡 Игрока 1️⃣\nЕсть ли у вас"
                                                              f"{emojize(':flower_playing_cards:')}карта Бронижилет?",
                                      reply_markup=kbf.confirmation(self.callback_action, self.callback_action))

        for i in range(2, 11):
            kb += kbf.player_action_line((emoji_number(i), self.callback_player, 123),
                                         (":pushpin:", self.callback_action),
                                         (":fist:", self.callback_action),
                                         (':flower_playing_cards:', self.callback_player),
                                         (":alarm_clock:", self.callback_action))
        self.updater.bot.send_message(chat_id=193019697, text=f"День №1\n"
                                                              f"🗡 Убили игрока 1️⃣\n"
                                                              f"{emojize(':cop:')} Коммисар попал\n"
                                                              f"{emojize(':flower_playing_cards:')} Прослушки не было",
                                      reply_markup=kb)
        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    test = KeyboardTests(sys.argv[1])
    test.game_view_test()
