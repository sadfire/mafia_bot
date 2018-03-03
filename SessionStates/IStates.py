import pickle
from abc import abstractmethod


def get_query_text(update):
    return update.callback_query.data


class IState:
    def __init__(self, session, is_greeting=True):

        if getattr(self, "_session", None) is None:
            self._session = session

        if getattr(self, "is_pseudo", None) is None:
            self.is_pseudo = False

        if getattr(self, "_next_state", None) is None:
            self._next_state = None

        if getattr(self, "_message", None) is None:
            self._message = None

        if is_greeting:
            self._greeting()

    @property
    def _next(self):
        return self._next_state

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
