import pickle
from abc import abstractmethod


def get_query_text(update):
    return update.callback_query.data


class IState:
    def __init__(self, session, is_greeting=True):
        if getattr(self, "is_pseudo", None) is None:
            self.is_pseudo = False

        self._message = None
        self._session = session
        if is_greeting:
            self._greeting()

    @property
    def _next(self):
        return None

    @abstractmethod
    def _greeting(self) -> None:
        pass

    @staticmethod
    def _clear(update, message="Действие отменено"):
        update.effective_message.edit_text(message)

    def next(self):
        if self._next is None:
            return self
        return self._next(self._session)
