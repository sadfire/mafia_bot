from GameLogic import GameMode


class GameStateProviders:
    @classmethod
    def Morning(cls, game):
        return GameStateProviders.Death

    @classmethod
    def Death(cls, game, previous=None):
        if game.mode is GameMode.Yakudza:
            return cls._death_yakudza(game, previous)

        from GameView import CardView
        from GameLogic.Models.Cards import HealModel
        return CardView, HealModel

    @classmethod
    def _death_yakudza(cls, game, previous):
        from GameView import CardView
        from GameLogic.Models.Cards import HarakiriModel
        return CardView, HarakiriModel

    @classmethod
    def Night(cls, game):
        if game.mode is GameMode.Beginner:
            from GameView import CardView
            from GameLogic.Models.Cards import UndercoverModel
            return CardView, UndercoverModel
        from GameView import IntroductionView
        return IntroductionView, True

    @classmethod
    def DeathOut(cls, game):
        if game.mode in [GameMode.Beginner, GameMode.Standard]:
            from GameView import FrontierState
            return FrontierState

    @classmethod
    def DeathStart(cls, game):
        if game.mode in [GameMode.Beginner, GameMode.Standard]:
            from GameView import CardView
            from GameLogic.Models.Cards import HealModel
            return CardView, HealModel

    @classmethod
    def Morning(cls, game):
        pass

    @classmethod
    def Card(cls, card):
        import GameLogic.Models.Cards as CardModels
        attr = getattr(CardModels, "{}Model".format(card.name))
        attr = getattr(CardModels, "{}Model".format(card.name))
        pass
