from enum import Enum

import MySQLdb
import _mysql_exceptions
import time
from emoji import emojize as em
import logging

from GameLogic.Evening import Evening
from GameLogic.Member import Member


class Statistic(Enum):
    Date = 0,
    Location = 1,
    Role = 2,
    Card = 3,
    Result = 4


class Database:
    def __init__(self, t_id, pswrd) -> None:
        super().__init__()
        self._db = None
        self.t_id = t_id
        self.pswrd = pswrd
        self._db = None
        self._cursor = None
        self.connect()

    def connect(self):
        self._db = MySQLdb.connect(host="localhost", user=self.t_id, passwd=self.pswrd, db="mafia_rate", charset='utf8')
        self._cursor = self._db.cursor()

    def _commit_db(self):
        self._db.commit()

    def __del__(self):
        if self._db is not None:
            self._db.close()

    def __execute(self, query, arguments=None):
        while True:
            try:
                self._cursor.execute(query, arguments)
                break
            except _mysql_exceptions.OperationalError as e:
                logging.warning(e)
                self.connect()

        return self._cursor.fetchall()

    def check_permission_by_telegram_id(self, t_id):
        result = self.__execute('SELECT * FROM `Members` WHERE IdTelegram = {0} AND IsHost = TRUE'.format(t_id))
        return len(result) == 1

    def check_permission_by_telegram_name(self, name):
        result = self.__execute('SELECT * FROM `Members` WHERE NameTelegram = "{0}" AND IsHost = TRUE'.format(name))
        return len(result) == 1

    def get_member_by_telegram(self, t_id):
        return self._get_member("IdTelegram", t_id)

    def get_member(self, id):
        return self._get_member("ID", id)

    def _get_member(self, field, value):
        result = self.__execute('SELECT * FROM `Members` WHERE {} = {}'.format(field, value))
        if len(result) != 1:
            return None

        return self.init_member(result[0])

    @staticmethod
    def init_member(member_raw):
        return Member(member_raw[0], member_raw[1], member_raw[2] == 1, member_raw[3], member_raw[4])

    def get_member_statistic(self, t_id):
        results = self.__execute(
            """SELECT
                                    Evenings.Date as "Дата",
                                    Location.Title as "Место",
                                    Roles.Name as "Роль",
                                    Cards.Title as "Карта",
                                    IF(Roles.ID <> 1 AND IsMafiaWin = 1, "Проиграл", "Выиграл") AS "Результат"
                                FROM 
                                    Members
                                INNER JOIN GamesPlayers     ON Members.ID  = GamesPlayers.ID_Player
                                INNER JOIN Games 			ON Games.ID    = GamesPlayers.ID_Games
                                INNER JOIN Evenings 		ON Evenings.ID = Games.IdEvening
                                INNER JOIN Location 		ON Location.ID = Evenings.ID_Location
                                INNER JOIN Cards 			ON Cards.ID    = GamesPlayers.ID_Card
                                INNER JOIN Roles 			ON Cards.ID    = GamesPlayers.ID_Role
                                WHERE Members.IdTelegram = {}"""
                .format(t_id))
        games = []
        for result in results:
            games.append({Statistic.Date: result[0],
                          Statistic.Location: result[1],
                          Statistic.Role: result[2],
                          Statistic.Card: result[3],
                          Statistic.Result: result[4]})
        return games

    def get_member_statistic_format(self, t_id):
        result = ""
        emoji = {Statistic.Date: em(":date:"),
                 Statistic.Location: em(":round_pushpin:"),
                 Statistic.Role: '🎭',
                 Statistic.Card: em(":black_joker:"),
                 Statistic.Result: em(":dart:")}
        for game in self.get_member_statistic(t_id):
            for stat in Statistic:
                if stat == Statistic.Date:
                    game[stat] = "{}.{}.{}".format(game[stat].day, game[stat].month, game[stat].year)
                result += emoji[stat] + ": " + game[stat] + "\n"
            result += '\n'
        return result

    def find_member(self, request):
        find_request = """SELECT ID, Name, IsHost, Telephone, IdTelegram FROM Members """
        if request.isdigit():
            if request[0] == 7 and request[1] == 9 and len(request) == 11:
                field = "Members.Telephone"
            else:
                field = "Members.ID"
            result = self.__execute(find_request + 'WHERE {0} = "{1}"'.format(field, request))
        else:
            result = self.__execute(find_request + 'WHERE Members.Name = "{}"'.format(request))  # ToDo Нечеткий поиск

        result = [Member(member[0], member[1], member[2] == 1, member[3], member[4]) for member in result]
        if len(result) != 1:
            return result

        return result[0]

    def get_regular_members_by_host(self, id):  # TODO Regular id add
        return [Member(member[0], member[1], member[2] == 1, member[3], member[4]) for member in
                self.__execute("SELECT * FROM Members")]

    def add_member(self, member, is_host):
        pass

    def get_game_statistic(self, game_id):
        pass

    def get_evenings(self, date, location):
        pass

    def get_games(self, t_id, game, host):
        pass

    def get_hosts(self):
        return [self.init_member(raw) for raw in self.__execute("SELECT * FROM Members WHERE IsHost = 1")]

    def add_user_permission_request(self, t_id, message):
        self.__execute("INSERT INTO PermRequest(TelegId, Text) VALUES (%s, %s)", (t_id, message.text))
        self._commit_db()
        return 0

    def insert_telegram_id(self, username, t_id):
        self._cursor.execute(""" UPDATE Members SET IdTelegram = %s WHERE NameTelegram = %s """, (t_id, username))
        self._db.commit()

    def get_evenings(self):
        pass

    def insert_evening(self, host_id):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        self.__execute("""INSERT INTO Evenings (Date, ID_Location, ID_Initiator) VALUES ('{}', 1, 1)""".format(now))
        self._db.commit()
        id = self._cursor.lastrowid
        return Evening(id, host_id)




