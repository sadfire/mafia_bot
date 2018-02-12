from enum import Enum


class Event(Enum):
    WTF = -1
    SuccessListen = 0,
    FailedListen = 1,
    MafiaWantKilled = 3,
    CivilianWantKilled = 4,
    JacketSave = 6
    MafiaKilled = 7,
    CivilianKilled = 8,
    CommissarCheck = 9,
    Kick = 11,
    Warning = 12,
    ToVote = 13