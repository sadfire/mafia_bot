import copy
import json

from GameLogic import Game
from GameLogic.Member import Member


class Evening:
    def __init__(self, host) -> None:
        super().__init__()
        self.members = {}
        self.hosts = [host]
        self.games = {}

    def decode(self):
        return json.dumps(
            ([member.decode() for member in self.members], [host.decode() for host in self.hosts], dict([(host_id, game.decode()) for host_id, game in self.games])))

    @staticmethod
    def encode(dump):
        tmp = json.loads(dump)
        hosts = [Member.encode(raw) for raw in tmp[1]]

        evening = Evening(hosts[0])
        evening.hosts = hosts
        evening.games = dict([(h_id, Game.encode(raw)) for h_id, raw in tmp[2]])
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
        if host.is_host:
            self.hosts.append(host)

    def remove_member(self, member):
        if isinstance(member, Member):
            member = member.id

        self.members.pop(member)

    def is_ready(self):
        return len(self.members) > 2  # TODO More checks # TODO 2 only for debug

    def get_hosts_ids(self):
        return [host.id for host in self.hosts]
