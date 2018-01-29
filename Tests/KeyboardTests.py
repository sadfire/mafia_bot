import sys

from telegram.ext import Updater, CallbackQueryHandler

from CallbackProvider import Provider

from KeyboardUtils import KeyboardFactory as kbf, MultiPageKeyboardFactory


class KeyboardTests:
    def __init__(self):
        self.kb = None

    def callback_test(self, bot, update):
        Provider.process(bot, update, (self,))
        return True

    def to_page_callback(self, bot, update, page):
        update.effective_message.edit_text(text=update.effective_message.text + "+1",
                                           reply_markup=self.kb.to_markup(int(page)))

    def kb_test(self):
        updater = Updater(sys.argv[1])
        updater.dispatcher.add_handler(CallbackQueryHandler(self.callback_test))
        self.kb = kbf.double_button("Button1", "Button", "Button1", "Button") + \
                  kbf.button(text="Button2", callback_data="Button") + \
                  kbf.double_button("Button3", "Button", "Button3", "Button") + \
                  kbf.button(text="Button4", callback_data="Button") + \
                  kbf.double_button("Button5", "Button", "Button5", "Button") + \
                  kbf.button(text="Button6", callback_data="Button")

        self.kb = MultiPageKeyboardFactory(self.kb, 2, kbf.button("Закончить", "end"))

        updater.bot.send_message(chat_id=193019697, text="Test", reply_markup=self.kb.to_markup(0))
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    test = KeyboardTests()
    test.kb_test()
