import pickle


def get_query_text(update):
    return update.callback_query.data


class IState:
    def __init__(self, session, previous=None):
        if getattr(self, "is_pseudo", None) is None:
            self.is_pseudo = False

        self._message = None
        self._session = session
        self._previous = previous
        self._greeting()

        if getattr(self, "_next", None) is None:
            self._next = None

    def _greeting(self) -> None:
        pass

    @staticmethod
    def _clear(update, message="Действие отменено"):
        update.effective_message.edit_text(message)

    def process_callback(self, bot, update):
        data = get_query_text(update)
        if data == "Close":
            self._clear(update)
            if self._previous is not None:
                self._next = self._previous
                return True
            else:
                return self._session.start_callback(bot, update)

        return False

    def next(self):
        if self._next is None:
            return self
        return self._next(self._session, self.__class__)

    def back_callback(self, bot, update):
        self._session.delete_message_callback(bot, update)

        if self._previous is None:
            return self
        return self._previous(self._session, None)
