import sched, time, enum, random


class MafiaType(enum.Enum):
    Beginner = 0,
    Blitz = 1,
    Std = 2,
    Killer = 3,
    Talk = 4,
    Makedon = 5,
    Yakuza = 6


class Role(enum.Enum):
    Citizen = 0,
    Commissar = 1,
    Mafia = 2


class Cards(enum.Enum):
    Neutral = 0,
    Aliby = 1,


class Member:
    def __init__(self, id, name, telegram_id, is_host=False) -> None:
        super().__init__()
        self.id = id
        self.name = name
        self.is_host = is_host
        self.telegram_id = telegram_id

    def __str__(self):
        return str(self.id) + ":" + self.name


class Citizen:
    def __init__(self, number, member):
        self.member = member
        self.number = number


class Evening:
    def __init__(self, host):
        self.members = []
        self.games = {}
        self.hosts = [host]

    def add_host(self, new_host):
        self.hosts = new_host

    def add_player(self, member):
        self.members.append(member)

    def start_game(self, host=None, members=None, mafia_type=MafiaType.Beginner, citizen_map=None):
        if host is None:
            host = self.hosts[0]
        elif host not in self.hosts:
            # MafiaApi.environment(host.member.id + " not host in this evening")
            return

        if members is None:
            members = self.members

        if len(members) < 8:
            # MafiaApi.environment(Not enough evening members. Pleas add members.)
            return
        elif len(members) > 10:
            # MafiaApi.environment(Few members. Please delete members from game)
            return

        if citizen_map is None:
            citizen_map = Evening._random_citizen_map(members)

        self.games[host] = Game(self, mafia_type, citizen_map)

        return self.games[host]

    @staticmethod
    def _random_citizen_map(members):
        citizen_map = {}
        random.seed()

        tmp = list(range(len(members)))
        random.shuffle(tmp)

        for member in members:
            citizen_map[member] = tmp.pop() + 1

        return citizen_map


class Game:
    def __init__(self, host, mafia_type, citizen_map):
        self.host = host
        self.citizen_map = citizen_map
        self.type = mafia_type
        self.state = State()

    def get_serialized_stats(self):
        pass


state_timers = {"State..": 0,
                "Talk..": 60,
                "Vote.Citizen.": 100,
                "Vote.Mafia.": 10,
                "Vote.Commissar.": 10,
                "CardWait.Citizen.NightVisit": 10,
                "CardWait.Citizen.ChangeRole": 10}

state_timers = {
    "Vote": 0,
    "Talk": 60,

}


class State:
    def __init__(self, timer=0, active_role=Role.Citizen, active_card=Cards.Neutral) -> None:
        super().__init__()
        self.timer = timer
        self.active_role = active_role
        self.active_card = active_card

    def start_timer(self):
        pass

    def end_timer(self):
        pass

    def next_state(self):
        pass

    def process_state(self):
        pass


class CardWait(State):
    pass


class Vote(State):
    pass


class Talk(State):
    pass
