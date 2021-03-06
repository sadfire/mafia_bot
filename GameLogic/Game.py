from GameLogic import Cards as C, CardsProvider, GameMode as GM, GameModeCards, GameInfo as GI, Member, Roles as R, \
    Event
from Utils.MafiaDatabaseApi import Database as db, Database


class Game:
    def __init__(self, host, evening, players, mode=GM.Super) -> None:
        self.course_count = 0
        self._evening = evening

        self.mode = mode

        self.gonna_die = None

        self.cards = dict([(card, True) for card in GameModeCards[mode]])
        self.cards_provider = CardsProvider(self)

        self.events = []
        self.current_player = None

        if isinstance(host, Member):
            self._host_id = host.id
        elif isinstance(host, int):
            self._host_id = host

        self.players = players
        if not isinstance(players, dict):
            self.__init_game_info()

        self.candidates = []

        self.id = db().insert_game(host.id, evening.id)

    def set_mode(self, mode: GM):
        self.mode = mode
        cards = GameModeCards[self.mode]
        self.cards = dict([(card, True) for card in cards])

    def __getitem__(self, key: int):
        if key is 0:
            return Database().get_member(self._host_id)
        return self.players.get(key, None)

    def __setitem__(self, key, value):
        self.players[key] = value

    def __init_game_info(self):
        for player in self.players:
            player.game_info = {}
            for info in GI:
                player[info] = True

            player[GI.Card] = None
            player[GI.IsOnVote] = False
            player[GI.Role] = R.Civilian
            player[GI.Warnings] = 0
            player[GI.Seconds] = 0

        self.players = dict([(player.number, player) for player in self.players])

    def put_on_voting(self, number):
        self.candidates.append(number)

    def clear_candidates(self):
        self.candidates.clear()

    def get_alive(self, role: R = None, *, is_card_closed=None, is_role_reverse=False, filter=None):
        roles = [role]
        if is_role_reverse:
            roles = list(R)
            roles.remove(role)

        if filter is None:
            def filter(player): return True

        return [number for number, player in self.players.items() if
                filter(player) and
                player[GI.IsAlive] and
                (role is None or player[GI.Role] in roles) and
                (is_card_closed is None or player[GI.Card] is None)]

    @property
    def get_commissar(self):
        commisars = self.get_alive(R.Commissar)
        if len(commisars) == 0:
            return None
        return commisars[0]

    def get_players(self, role: R = None) -> list:
        return [number for number, players in self.players.items() if (role is None or players[GI.Role] is role)]

    @property
    def get_mafia_count(self):
        return len(self.get_alive(R.Mafia))

    @property
    def is_commissar(self) -> bool:
        return len(self.get_alive(R.Commissar)) != 0

    @property
    def commissar_cards(self):
        if C.Retirement in self.cards.keys():
            return [C.Retirement]

    def remove_from_vote(self, number):
        pass

    def process_card(self, card, initiator, target, result) -> bool:
        if isinstance(card, int):
            card = C(card)
        if card not in self.cards.keys():
            return False

        self[initiator][GI.Card] = card

        if self.cards_provider(card, initiator, target) is not False:
            self.log_event(card, initiator, target, result)
            self.cards[card] = True

    def get_state(self, current):
        from GameView import CardView
        from GameLogic.Models.Cards import UndercoverModel

        return CardView, UndercoverModel

    def is_player_card_closed(self, number):
        card = self[number][GI.Card]
        if card is None:
            return True
        return self.cards[card]

    @property
    def get_available_cards(self):
        return [card for card, available in self.cards.items() if available]

    @property
    def get_wasted_cards(self):
        return [card for card, available in self.cards.items() if not available]

    def log_event(self, event, initiator_players: int, target_player: int = None, result: bool = True):
        if event is Event.Death:
            self.players[self.gonna_die][GI.IsAlive] = False
            self.gonna_die = None

        print(event.name, initiator_players, target_player, result)

    def next_course(self):
        self.course_count += 1
        for number in self.get_alive():
            self.players[number][GI.IsOnVote] = False
            self.players[number][GI.IsNotTalked] = True
            self.players[number][GI.IsHaveVote] = True
            self.players[number][GI.Seconds] = 0

        self.candidates.clear()
