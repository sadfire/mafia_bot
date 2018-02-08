from enum import Enum


class Event(Enum):
    WTF = -1
    SuccessListen = 0,
    FailedListen = 1,
    SwapRole = 2,
    MafiaWantKilled = 3,
    CivilianWantKilled = 4,
    Heal = 5,
    JacketSave = 6
    MafiaKilled = 7,
    CivilianKilled = 8,
    SuccessCommissarCheck = 9,
    FailedCommissarCheck = 10,
    Kick = 11,
    Warning = 12,
    ToVote = 13,
    Recruitment = 14
    Aliby = 15,
    Theft = 16,
    Undercover = 17