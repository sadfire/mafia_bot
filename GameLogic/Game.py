import json

from GameLogic.Cards import Cards as C
from GameLogic.CardsProvider import CardsProvider
from GameLogic.GameEvents import Event
from GameLogic.GameModes import GameMode as GM, GameModeCards
from GameLogic.Member import GameInfo as GI, Member
from GameLogic.Roles import Roles as R, Roles


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

    def __getitem__(self, key: int):
        return self.players.get(key, None)

    def __setitem__(self, key, value):
        self.players[key] = value

    def __init_game_info(self):
        for player in self.players:
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

    def get_alive(self, role: Roles = None) -> list:
        return [number for number, player in self.players.items() if
                player[GI.IsAlive] and (role is None or player[GI.Role] is role)]

    @property
    def is_commissar(self) -> bool:
        return len(self.get_alive(Roles.Commissar)) != 0

    def remove_from_vote(self, number):
        pass

    def process_card(self, card, initiator, target) -> bool:
        if isinstance(card, int):
            card = C(card)
        if card not in self.cards.keys():
            return False

        self[initiator][GI.Card] = card

        if self.cards_provider(card, initiator, target) is not False:
            self.log_event(card, initiator, target)
            self.cards[card] = True

    def log_event(self, event, initiator_players: int, target_player: int = None):
        pass
