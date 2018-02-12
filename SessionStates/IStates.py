import pickle
from abc import abstractmethod


def get_query_text(update):
    return update.callback_query.data


class IState:
    def __init__(self, session, previous=None, is_greeting=True):
        if getattr(self, "is_pseudo", None) is None:
            self.is_pseudo = False

        self._message = None
        self._session = session
        self._previous = previous
        if is_greeting:
            self._greeting()

        if getattr(self, "_next", None) is None:
            self._next = None

    @abstractmethod
    def _greeting(self) -> None:
        pass

    @staticmethod
    def _clear(update, message="Действие отменено"):
        update.effective_message.edit_text(message)

    def next(self):
        if self._next is None:
            return self
        return self._next(self._session, self.__class__)