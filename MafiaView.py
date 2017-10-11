from telegram.ext import Updater, CallbackQueryHandler

from StringResourse import Callback


class View:
    def __init__(self, session, t_id, updater) -> None:
        super().__init__()
        self.t_id = t_id
        self.session = session

        self._updater = Updater(updater)
        self._init_handlers()

        self._confirmation_wait_info = None
        self._confirmation_message_id_list = []

    def _init_handlers(self):
        self._updater.dispatcher.add_handler(CallbackQueryHandler(self._base))
        self._updater.dispatcher.add_handler(CallbackQueryHandler(self._confirmation))

    def _confirmation(self, bot, upd):
        if not self._check(upd) \
                or self._confirmation_wait_info is None \
                or upd.effective_message.id not in self._confirmation_message_id_list:
            return

        callback = self._getCallback(upd)
        if callback == Callback.ConfirmationYes:
            upd.effective_message.edit_text(self._confirmation_wait_info["YesStr"])
            self._confirmation_wait_info["Callback"](upd)
        elif callback == Callback.ConfirmationNo:
            upd.effective_message.edit_text(self._confirmation_wait_info["NoStr"])

    def _base(self, bot, upd):
        if not self._check(upd):
            return

    def start_menu(self, bot, upd):
        if not self._check(upd):
            return

    def _check(self, upd):
        return self.t_id == upd.effective_message.id

    def _getCallback(self, upd):
        return upd.effective_message.data
