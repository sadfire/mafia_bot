from GameLogic.Cards import Cards
from GameLogic.GameEvents import Event
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.IGameModel import IGameModel


class DayTalkModel(IGameModel):
    def end(self):
        pass

    @property
    def _get_event(self):
        return Event.WTF

    def warning(self, number: int):
        self.game.log_event(Event.Warning, None, number)
        self.game[number][GI.Warnings] += 1

    def kick(self, number: int, _=None):
        self.game.log_event(Event.Kick, None, number)
        self.game[number][GI.IsAlive] = False

    def to_vote(self, initiator: int, target: int):
        if not self.game[initiator][GI.IsExhibited]:
            if self.game[target][GI.IsImmunitet]:
                return "Игрок не может быть выставлен"

            self.game.log_event(Event.ToVote, initiator, target)
            self.game.candidates.append(target)
            self.game[initiator][GI.IsExhibited] = True
            return "{} Выставлен".format(self.game[target].get_num_str)
        return "Вы уже выставляли игрока"

    def process_card(self, initiator: int = None, target: int = None, card: Cards = Cards.Neutral, result: bool=True):
        self.game.process_card(card=card, initiator=initiator, target=target, result=result)

    def is_can_talk(self, number: int):
        return self.game[number][GI.IsTalked] and not self.game[number][GI.IsSilence]

    @property
    def get_possible_cards(self, is_day=True):
        return [card for card in self.game.cards if not is_day or Cards.is_day_card(card)]

    @property
    def is_day_can_end(self):
        for number in self.game.get_alive_players:
            if self.game[number][GI.IsTalked]:
                return False
        return True

    def try_kill(self, number):
        self.game.gonna_die = number
