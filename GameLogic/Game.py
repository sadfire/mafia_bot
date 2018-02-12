from GameLogic import Cards as C, \
    CardsProvider, \
    GameMode as GM, \
    GameModeCards, \
    GameInfo as GI, \
    Member, \
    Roles as R
from Utils.MafiaDatabaseApi import Database as db


class Game:
    def __init__(self, host, evening, players, mode=GM.Beginner) -> None:
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

    def __getitem__(self, key: int):
        return self.players.get(key, None)

    def __setitem__(self, key, value):
        self.players[key] = value

    def __init_game_info(self):
        for player in self.players:
            player.game_info = {}
            for info in GI:
                player[info] = True

            player[GI.Card] = None
            player[GI.Role] = R.Civilian
            player[GI.Warnings] = 0

        self.players = dict([(player.number, player) for player in self.players])

    def put_on_voting(self, number):
        self.candidates.append(number)

    def clear_candidates(self):
        self.candidates.clear()

    def get_alive(self, role: R = None) -> list:
        return [number for number, player in self.players.items() if
                player[GI.IsAlive] and (role is None or player[GI.Role] is role)]

    def get_players(self, role: R = None) -> list:
        return [number for number, players in self.players.items() if (role is None or players[GI.Role] is role)]

    @property
    def is_commissar(self) -> bool:
        return len(self.get_alive(R.Commissar)) != 0

    @property
    def commissar_cards(self):
        if C.Retirement in self.cards.keys():
            return [C.Retirement]

    def remove_from_vote(self, number):
        pass

    def process_card(self, card, initiator, target, _) -> bool:
        if isinstance(card, int):
            card = C(card)
        if card not in self.cards.keys():
            return False

        self[initiator][GI.Card] = card

        if self.cards_provider(card, initiator, target) is not False:
            self.log_event(card, initiator, target)
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

    def log_event(self, event, initiator_players: int, target_player: int = None, result: bool = True):
        print(event.name, initiator_players, target_player, result)
