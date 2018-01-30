import sys
from random import random

from emoji import emojize as em
from telegram.ext import Updater, CallbackQueryHandler

from CallbackProvider import Provider

from KeyboardUtils import KeyboardFactory as kbf, MultiPageKeyboardFactory, emoji_number


class KeyboardTests:
    def __init__(self, token):
        self.kb = None
        self.token = token
        self.updater = Updater(self.token)
        self.t_id = 193019697

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

        self.updater.bot.send_message(chat_id=self.t_id, text="Test", reply_markup=self.kb.to_markup(0))
        self.updater.start_polling()
        self.updater.idle()

    def callback_player(self, bot, update, id):
        pass

    def callback_action(self, bot, update, id):
        return True

    def game_view_test(self):
        kb = kbf.empty()
        self.updater.bot.send_message(chat_id=self.t_id, text=f"🗡 Убивали игрока 1️⃣\n"
                                                              f"Будет ли использована "
                                                              f"{em(':flower_playing_cards:')} карта лечение?",
                                      reply_markup=kbf.confirmation(self.callback_action, self.callback_action))
        self.updater.bot.send_message(chat_id=self.t_id, text=f"Игрок 1️⃣ есть ли у вас"
                                                              f"{em(':flower_playing_cards:')}карта Бронижилет?",
                                      reply_markup=kbf.confirmation(self.callback_action, self.callback_action))
        warning_button = (":warning:", self.callback_action)
        warning_button2 = (":warning: 2", self.callback_action)
        warning_button3 = (":no_entry_sign:", self.callback_action)
        voting_button = (":white_circle:", self.callback_action)
        no_voting_button = (":red_circle:", self.callback_action)
        card_button = (':flower_playing_cards:', self.callback_player)
        no_card_button = ('🚬', self.callback_player)
        clock_button = (":sound:", self.callback_action)
        no_clock_button = (":mute:", self.callback_action)

        for i in range(2, 11):
            role = '🕵🏼' if i in [2, 5, 8] else '👨🏼‍💼'
            role = role if i != 4 else '👮🏼'
            kb += kbf.action_line((str(emoji_number(i)) + role, self.callback_player, 123),
                                  warning_button if i not in [4, 9] else (
                                  warning_button2 if i != 4 else warning_button3),
                                  voting_button if i not in [3, 7] else no_voting_button,
                                  card_button if i not in [8, 2, 1] else no_card_button,
                                  clock_button if i >= 6 else no_clock_button)

        self.updater.bot.send_message(chat_id=self.t_id,
                                      text=f"День №1\n"
                                           f"🗡 Убили игрока 1️⃣\n"
                                           f"{em(':cop:')} Коммисар попал\n"
                                           f"{em(':flower_playing_cards:')} Прослушки не было\n"
                                           f"{'🔪'*4} Меню Игры {'🔪'*4}"
                                           f"Выставлены игроки под номерами 3️⃣, 7️⃣",
                                      reply_markup=kb)

        kb = kbf.action_line(("⏸", self.callback_action, 1),
                             (em(":arrow_forward:"), self.callback_action),
                             ("⏹", self.callback_action))
        self.updater.bot.send_message(chat_id=self.t_id,
                                      text=f"Минута игрока номер 6️⃣\nОсталось 40 секунд {em(':alarm_clock:')}",
                                      reply_markup=kb)
        kb = kbf.empty()
        man_with_hand = "🙋🏻‍♂️"
        man_without_hand = "🙅🏽‍♂️"
        for i in range(0, 10):
            kb += kbf.button(f"{emoji_number(i)} {man_with_hand*2} {man_without_hand*2} {emoji_number(i)}", self.callback_action, 2)

        self.updater.bot.send_message(chat_id=self.t_id,
                                      text=f"На голосование выставлены игроки под номерами 3️⃣, 7️⃣")
        self.updater.bot.send_message(chat_id=self.t_id,
                                      text="Кто голосует за игрока номер 3️⃣",
                                      reply_markup=kb)
        self.updater.start_polling()
        self.updater.idle()


if __name__ == "__main__":
    test = KeyboardTests(sys.argv[1])
    test.game_view_test()
