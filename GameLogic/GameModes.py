from enum import Enum

from GameLogic import Cards as C


class GameMode(Enum):
    Low = 0
    Super = 1
    Beginner = 2
    Standard = 3
    Macedonia = 4
    Killer = 5
    LetsTalk = 6
    Yakudza = 7

    @staticmethod
    def get_name(mode) -> str:
        from Utils import Database
        return "{0} {1} {0}".format("🍷", Database().get_game_mode_name(mode.value))


GameModeCards = {GameMode.Low: (),
                 GameMode.Super: tuple(C),
                 GameMode.Beginner:
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

AfterDeathCards = (C.TheLastShot, C.Mina, C.Demoman, C.Exposure)
