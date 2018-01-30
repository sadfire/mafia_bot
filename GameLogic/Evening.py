import copy

from GameLogic import Game
from GameLogic.Member import Member


class Evening:
    def __init__(self, host) -> None:
        super().__init__()
        self.members = {}
        self.hosts = [host]
        self.games = {}

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

    def get_game_bidder(self, host) -> list:
        stop_list = self.get_busy_players_id() + [host.id]
        return [member for member in self.members if member.id not in stop_list]

    def get_players_id(self, host):
        return [player.id for player in self.get_game_bidder(host)]

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