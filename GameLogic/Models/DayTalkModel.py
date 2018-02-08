from GameLogic.Cards import Cards
from GameLogic.Game import Event
from GameLogic.Member import GameInfo as GI
from GameLogic.Models.Models import IGameModel


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

    def process_card(self, initiator: int = None, target: int = None, card_id: Cards = Cards.Neutral.value):
        event = None
        self.game.wasted_cards.append(Cards(card_id))

        if card_id is Cards.Alibi.value:
            event = Event.Aliby
            self.game[initiator][GI.IsCardSpent] = True
            self.game[target][GI.IsImmunitet] = True
            if target in self.game.candidates:
                self.game.candidates.remove(target)
        elif card_id is Cards.Undercover.value:
            event = Event.Undercover
            self.game[initiator][GI.IsSilence] = True
            self.game[initiator][GI.IsCardSpent] = True
        elif card_id is Cards.Theft.value:
            event = Event.Theft
            self.game[initiator][GI.Card], self.game[target][GI.Card] = \
                self.game[target][GI.Card], self.game[initiator][GI.Card]

            self.game[initiator][GI.IsCardSpent] = False
            self.game[target][GI.IsCardSpent] = True

        self.game.log_event(event, initiator, target)


    def is_can_talk(self, number: int):
        return self.game[number][GI.IsTalked] and not self.game[number][GI.IsSilence]

    def timer_on(self, number: int):
        self.game[number][GI.IsTimer] = True

    def get_cards(self):
        return self.game.alive_cards()

    @property
    def is_all_talks(self):
        for number in self.game.get_alive_players:
            if self.game[number][GI.IsTalked]:
                return False
        return True

    def kill(self, number):
        self.game.gonna_die = number