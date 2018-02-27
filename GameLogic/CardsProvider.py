from GameLogic import Cards as C, GameInfo as GI, Roles


class CardsProvider:
    def __init__(self, game):
        self.game = game
        self.callbacks = {}
        for card in self.game.cards:
            self.callbacks[card] = getattr(self, card.name, self.Neutral)

    def __call__(self, card: C, initiator: int, target: int = None):
        return self.callbacks[card](initiator, target)

    def Neutral(_, __, ___):
        return False

    def Zen(_, __, ___):
        pass

    def Alibi(self, _, target=None):
        self.game[target][GI.IsNotImmunity] = True
        self.game.remove_from_vote(target)

    def Banzai(self, initiator, target):
        pass

    def FlakJacket(self, initiator, target):
        if initiator != target:
            return False

        if self.game.gonna_die == target:
            self.game.gonna_die = None

    def Waru(self, initiator, target):
        return self.Theft(initiator, target)

    def Recruitment(self, initiator, target):
        self.game[target][GI.Role] = Roles.Mafia

    def YinYang(self, initiator, target):
        pass

    def Keiko(self, initiator, target):
        pass

    def Kitsune(self, initiator, target):
        pass

    def Theft(self, initiator, target):
        self.game[initiator][GI.Card], self.game[target][GI.Card] = \
            self.game[target][GI.Card], self.game[initiator][GI.Card]

    def Mole(self, initiator, target):
        pass

    def Rat(self, initiator, target):
        self.game[initiator][GI.Role] = Roles.Rat

    def Heal(self, initiator, target):
        if self.game[initiator][GI.Role] is Roles.Commissar:
            return False

        if target == self.game.gonna_die:
            self.game.gonna_die = None

    def Leader(self, initiator, target):
        self.game.gonna_die = target

    def Mina(self, initiator, target):
        pass

    def Retirement(self, initiator, target):
        pass

    def Demoman(self, initiator, target):
        pass

    def Ghost(self, initiator, target):
        pass

    def Listener(self, initiator, target):
        pass

    def Sensei(self, initiator, target):
        return self.Leader(initiator, target)

    def ChangeRole(self, initiator, target):
        self.game[initiator][GI.Role], self.game[target][GI.Role] = \
            self.game[target][GI.Role], self.game[initiator][GI.Role]

    def Shuriken(self, initiator, target):
        pass

    def Fugue(self, initiator, target):
        pass

    def Harakiri(self, initiator, target):
        pass

    def Yakuza(self, initiator, target):
        pass

    def Undercover(self, initiator, target):
        self.game[initiator][GI.IsNotImmunity] = True
        self.game[initiator][GI.IsNotHidden] = True

    def TheLastShot(self, initiator, target):
        pass

    def Exposure(self, initiator, target):
        pass

    def DeadlyShot(self, initiator, target):
        pass
