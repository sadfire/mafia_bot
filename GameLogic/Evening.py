import copy
import json

from GameLogic.Game import Game
from GameLogic.Member import Member


class Evening:
    def __init__(self, id, host_id :int, db) -> None:
        super().__init__()
        self.id = id
        self.members = {}
        self.hosts = [host_id]
        self.games = {}
        self.db = db

    def decode(self):
        member_raw = [member.decode() for _, member in self.members.items()]
        game_raw = dict([(host_id, game.decode()) for host_id, game in self.games])
        return json.dumps((self.id, member_raw, self.hosts, game_raw))

    @staticmethod
    def encode(dump, db):
        tmp = json.loads(dump)
        id = tmp[0]
        evening = Evening(id, tmp[1][0], db)
        evening.hosts = tmp[1]
        evening.games = dict([(h_id, Game.encode(raw, evening)) for h_id, raw in tmp[2]])
        evening.members = dict([(member.id, member) for member in [Member.encode(raw) for raw in tmp[0]]])

        return evening

    def add_member(self, member):
        if not isinstance(member, Member) or member.id in self.members.keys():
            return False

        self.members[member.id] = member
        return True

    def get_busy_players_id(self) -> list:
        busy = []
        for game in self.games.values():
            busy += [player.id for player in game.players()]
            busy.append(game.host.id)
        return busy

    def get_game(self, host):
        return self.games.get(host.id, None)

    def add_host(self, host):
        if isinstance(host, int):
            self.hosts.append(host)

        if isinstance(host, Member) and host.is_host:
            self.hosts.append(host.id)

    def remove_member(self, member):
        if isinstance(member, Member):
            member = member.id

        self.members.pop(member)

    def is_ready(self):
        return len(self.members) > 2  # TODO More checks # TODO 2 only for debug

    def get_hosts_ids(self):
        return self.hosts
