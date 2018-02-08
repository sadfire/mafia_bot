import copy
import json

from GameLogic.Game import Game
from GameLogic.Member import Member


class Evening:
    def __init__(self, id, host_id: int) -> None:
        super().__init__()
        self.id = id
        self.members = {}
        self.hosts = [host_id]
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
        return self.games.get(host.t_id, None)

    def add_host(self, host):
        if isinstance(host, int):
            self.hosts.append(host)

        if isinstance(host, Member) and host.is_host:
            self.hosts.append(host.t_id)

    def remove_member(self, member):
        if isinstance(member, Member):
            member = member.id

        self.members.pop(member)

    def is_ready(self):
        return len(self.members) > 8  # TODO More checks # TODO 2 only for debug

    def get_hosts_ids(self):
        return self.hosts
