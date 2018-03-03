from GameLogic import Game, GameInfo, Roles, GameMode
from GameLogic.Models.Cards import JacketModel
from GameView import DayTalkView, IntroductionView, DeathView, CardView, CommissarCheck, MafiaVotingView

from SessionStates import IState, GameStartConfirmation

from Utils import kbf


class TestGameManagement(IState):
    def _greeting(self):
        self._session.send_message(text="Проверка функционала игры \n", reply_markup=kbf.button("Начать", self._start))

    @property
    def _next(self):
        return GameStartConfirmation

    def __init__(self, session):
        super().__init__(session)
        self._evening = self._session.get_evening()
        busy = self._evening.get_busy_players_id() + list(self._evening.members.keys())
        members = [member for member in self._session.db.get_regular_members_by_host(self._session.owner.id)
                   if member.id not in busy]
        members = sorted(members, key=lambda m: m.name)

        for member in members:
            self._evening.add_member(member)

        size = 10
        players = members[:size]
        for i in range(0, size):
            players[i].number = i + 1
        self._evening.games[session.t_id] = Game(session.owner, self._evening, players, mode=GameMode.Beginner)
        self._evening.games[session.t_id][1][GameInfo.Role] = Roles.Mafia
        self._evening.games[session.t_id][2][GameInfo.Role] = Roles.Mafia
        self._evening.games[session.t_id][4][GameInfo.Role] = Roles.Commissar
        self._evening.games[session.t_id].candidates = [1]
        self._evening.games[session.t_id].course_count += 1

    def _start(self, bot, update):
        self._session.remove_markup(update)
        self._session.to_next_state()

    def next(self):
        return DayTalkView(session=self._session, game=self._evening.games[self._session.t_id])
