from GameLogic.Game import Game

from KeyboardUtils import KeyboardFactory as KBF
from telegram import InlineKeyboardButton as Button
from SessionStates.GameStartConfirmation import GameStartConfirmation
from SessionStates.IStates import IState


class TestGameManagement(IState):
    def _greeting(self):
        self._session.send_message(text="Проверка функционала игры \n", reply_markup=KBF.button("start", self._start))

    def __init__(self, session, previous=None):
        super().__init__(session, previous)
        self._next = GameStartConfirmation
        self._evening = self._session.get_evening()
        busy = self._evening.get_busy_players_id() + list(self._evening.members.keys())
        members = [member for member in self._session.db.get_regular_members_by_host(self._session.owner.id)
                   if member.id not in busy]
        members = sorted(members, key=lambda m: m.name)

        for member in members:
            self._evening.add_member(member)

        players = members[:5]
        for i in range(0,5):
            players[i].number = i
        self._evening.games[session.t_id] = Game(session.owner, self._evening, players)


    def _start(self, bot, update):
        self._next = GameStartConfirmation
        self._session.remove_markup(update)
        self._session.to_next_state()