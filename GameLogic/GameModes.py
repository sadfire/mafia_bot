from enum import Enum

from GameLogic import Cards as C


class GameMode(Enum):
    Beginner = 0,
    Standard = 1,
    Killer = 2,
    LetsTalk = 3,
    Macedonia = 4
    Yakudza = 5


GameModeCards = {GameMode.Beginner:
                     (C.Neutral,
                      C.Alibi,
                      C.FlakJacket,
                      C.Recruitment,
                      C.Theft,
                      C.Heal,
                      C.Leader,
                      C.ChangeRole,
                      C.Undercover,
                      C.Listener),
                 GameMode.Standard:
                     (C.FlakJacket,
                      C.Recruitment,
                      C.Theft,
                      C.Rat,
                      C.Mole,
                      C.Heal,
                      C.Leader,
                      C.Mina,
                      C.Retirement,
                      C.Listener,
                      C.Exposure,
                      C.DeadlyShot),
                 GameMode.Killer:
                     (C.FlakJacket,
                      C.Recruitment,
                      C.Theft,
                      C.Theft,
                      C.Mole,
                      C.Mina,
                      C.Mina,
                      C.Demoman,
                      C.Exposure,
                      C.DeadlyShot),
                 GameMode.LetsTalk: (),
                 GameMode.Macedonia: (),
                 GameMode.Yakudza: ()}

class GameModeScenario:
    @classmethod
    def __call__(cls, mode, card):
        return getattr(cls, mode.name, card)

    @classmethod
    def Beginner(cls, current_state=None):
        pass

    @classmethod
    def Standard(cls):
        pass
