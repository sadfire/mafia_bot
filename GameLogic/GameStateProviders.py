from GameLogic import GameMode


class GameStateProviders:
    @classmethod
    def Morning(cls, game):
        return cls.DeathStart(game)

    @classmethod
    def Day(cls, game):
        from GameView import DayTalkView
        return DayTalkView

    @classmethod
    def Evening(cls, game):
        if game.mode is GameMode.Beginner:
            from GameView import CardView
            from GameLogic.Models.Cards import UndercoverModel
            return CardView, UndercoverModel
        elif game.mode is GameMode.Standard:
            from GameView import IntroductionView
            return IntroductionView, True

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
    def Card(cls, card):
        from GameView import CardView
        import GameLogic.Models.Cards as CardModels
        return CardView, getattr(CardModels, "{}Model".format(card.name), None)

    @classmethod
    def HalfOfVote(cls, game):
        from GameLogic.Models.Cards import LeaderModel
        from GameView import CardView
        return CardView, LeaderModel
