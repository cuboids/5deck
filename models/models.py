""" Models 

# Some preliminary models below.

# suitable for:

# SD (short deck)
# 5D (five deck)
# LP (level poker)
# IP (infinite poker)

# rank

:class Rank(IntEnum)

:class ShortRank(Rank)  # ranks 6-Ace for short deck

# suit

:class Suit(StrEnum)

# level

:class Level(IntEnum)

:class InfLevel(Level)  # allows arbitrariliy high levels

:class ShortLevel(Level)  # levels 6-14 only (short deck)

# card

:class BaseCard(CardABC)  # a card has rank, suit, and optional level and deck_id

# deck

:abcls DeckABC(ABC)

:class BaseDeck(DeckABC)

:class StdDeck(BaseDeck)

:class ShortDeck(BaseDeck)  # a short deck with 36 cards (6-Ace)

:class InfDeck(BaseDeck)  # a deck with infinitely many cards, with InfLevels

# hand

:abcls HandABC(ABC)

:class BaseHand(HandABC)

:class OmahaHand(BaseHand)  # a hand with four playing cards, of which two need to be used

:class Omaha5Hand(BaseHand)

:class Omaha6Hand(BaseHand)

:class HoldEmHand(BaseHand)  # a hand with two playing cards

# board

:abcls BoardABC(ABC)  # a board with 0-5 x 1-3 = 0-15 playing cards
# 1-3: run it once, twice or thrice.

:class BaseBoard(BoardABC)

:class Board(BaseBoard)

# game

:abcls GameABC(ABC)

:class BaseGame(GameABC)

:class PLO(BaseGame)

:class FiveDeckPLO(PLO)

:class NLH(BaseGame)

:class LevelNLH(BaseGame)

# Later we might add FiveDeckNLH, LevelPLO, InfNLH, and InfPLO
# as well as short deck variants with 5 decks, levels, or both.

# player

:abcls PlayerABC(ABC)

:class BasePlayer(PlayerABC)

:class AIPlayer(BasePlayer)  # for AI to be a player

:class HumanPlayer(BasePlayer)

:class RandomPlayer(BasePlayer)  # always chooses a random action.

:class AlwaysCallPlayer(BasePlayer)  # always checks or calls.

# chips

:abcls ChipsABC(ABC)

:class BaseChips(ChipsABC)

:class Chips(BaseChips)

# pot

:abcls PotABC(ABC)

:class BasePot(PotABC)

:class Pot(BasePot)

# round

:abcls RoundABC(ABC)  # an entire round, from preflop to showdown

:class BaseRound(ABC)

:class Round(BaseRound)

# hand evaluation

:abcls HandEvaluatorABC(ABC)

:class BaseHandEvaluator(HandEvaluatorABC)

:class HandEvaluator(BaseHandEvaluator)

:class FiveDeckHandEvaluator(HandEvaluator)

:class LevelHandEvaluator(HandEvaluator)

@lru_cache
:func hand_evaluation

# each hand has a level, tier, category, groups, and level groups,
# in that order of importance.
#
# For example: As(3), Kc(2), 9c(2), 7d(4), 2h(2) has
#    - Level = min(3, 2, 2, 4, 2) = 2
#    - Tier = Bronze (1/5)
#    - Category = High Card (1/5 in Tier)
#    - Groups = [Ace, King, 9, 7, deuce]
#    - Levels = [3, 2, 2, 4, 2]
#
# These are together represented in a named tuple, e.g.
#
# (2, 1, 1, 14, 13, 9, 7, 2, 3, 2, 2, 4, 2) = 
# (Level=2, Tier=1, Cat=1, Group1=14, Group2=13, Group3=9,
#  Group4=7, Group5=2, Level1=3, Level2=2, Level3=2,
#  Level4=4, Level5=2)
#
# If a Group or LGroup does not apply, it is None.
#
# For example: As(3) Ks(2), Qs(2), Ts(4), Js(2) has
#    - Level = 2
#    - Tier = Diamond (5/5)
#    - Category = Royal Flush (4/5)
#    - Groups = None
#    - Levels = None
#
# (2, 5, 4) = 
# (Level=2, Tier=5, Cat=4, Group1=None, Group2=None,
#  Group3=None, Group4=None, Group5=None, Level1=None,
#  Level2=None, Level3=None, Level4=None, Level5=None)
#
# This hand would be (2, 5, 4, 3, 2, 2, 2, 4) in a five-Deck
# context though.
#
# The :func for hand_evaluation should work on:
#    - A list of one or more cards
#    - A board + hand
# but not on:
#    - A board + multiple hands.
# for that we use the :func distribute_pot

:class HandStrengthABC(ABC)  # both verbal ("a pair of aces with K87 kicker") and numerical

:class BaseHandStrength(HandStrengthABC)

:attr  level
:attr  tier
:attr  category
:attr  group1
:attr  group2
:attr  group3
:attr  group4
:attr  group5
:attr  level1
:attr  level2
:attr  level3
:attr  level4
:attr  level5
:attr  hand_strength_tup  # named tuple (with number values)
:attr  hand_strength_num
:attr  hand_strength   # named tuple (with textual values)

:class HandStrength(BaseHandStrength)

:func distribute_pot

# rule set

:abcls RuleSetABC(ABC)

:class BaseRuleSet(RuleSetABC)

:class RuleSet(BaseRuleSet)

:class FiveDeckRuleSet(BaseRuleSet)

:class LevelRuleSet(BaseRuleSet)

"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, IntEnum
from random import random
from uuid import uuid4


RANKS: list[None | str] = [None, None] + list("23456789TJQKA")


class Rank(IntEnum):
    """ Ranks of playing cards. """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        return RANKS[self.value]


class ShortRank(IntEnum):
    """ Ranks of playing cards (short deck). """
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        return RANKS[self.value]


class Suit(Enum):
    """ Suits of playing cards. """
    CLUBS = '♣'
    DIAMONDS = '♦'
    HEARTS = '♥'
    SPADES = '♠'

    def __str__(self):
        return self.value


class Level(IntEnum):
    """ Levels of playing cards. """
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14

    def __str__(self):
        return str(self.value)


class InfLevel(IntEnum):
    """ "Infinite" Levels of playing cards.
    
    With 110 levels, the chance of exceeding the highest 
    level is smaller than the chance of the Sun not rising
    tomorrow, even with a trillion cards generated...
    """
  
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14
    FIFTEEN = 15
    SIXTEEN = 16
    SEVENTEEN = 17
    EIGHTEEN = 18
    NINETEEN = 19
    TWENTY = 20
    TWENTYONE = 21
    TWENTYTWO = 22
    TWENTYTHREE = 23
    TWENTYFOUR = 24
    TWENTYFIVE = 25
    TWENTYSIX = 26
    TWENTYSEVEN = 27
    TWENTYEIGHT = 28
    TWENTYNINE = 29
    THIRTY = 30
    THIRTYONE = 31
    THIRTYTWO = 32
    THIRTYTHREE = 33
    THIRTYFOUR = 34
    THIRTYFIVE = 35
    THIRTYSIX = 36
    THIRTYSEVEN = 37
    THIRTYEIGHT = 38
    THIRTYNINE = 39
    FORTY = 40
    FORTYONE = 41
    FORTYTWO = 42
    FORTYTHREE = 43
    FORTYFOUR = 44
    FORTYFIVE = 45
    FORTYSIX = 46
    FORTYSEVEN = 47
    FORTYEIGHT = 48
    FORTYNINE = 49
    FIFTY = 50
    FIFTYONE = 51
    FIFTYTWO = 52
    FIFTYTHREE = 53
    FIFTYFOUR = 54
    FIFTYFIVE = 55
    FIFTYSIX = 56
    FIFTYSEVEN = 57
    FIFTYEIGHT = 58
    FIFTYNINE = 59
    SIXTY = 60
    SIXTYONE = 61
    SIXTYTWO = 62
    SIXTYTHREE = 63
    SIXTYFOUR = 64
    SIXTYFIVE = 65
    SIXTYSIX = 66
    SIXTYSEVEN = 67
    SIXTYEIGHT = 68
    SIXTYNINE = 69
    SEVENTY = 70
    SEVENTYONE = 71
    SEVENTYTWO = 72
    SEVENTYTHREE = 73
    SEVENTYFOUR = 74
    SEVENTYFIVE = 75
    SEVENTYSIX = 76
    SEVENTYSEVEN = 77
    SEVENTYEIGHT = 78
    SEVENTYNINE = 79
    EIGHTY = 80
    EIGHTYONE = 81
    EIGHTYTWO = 82
    EIGHTYTHREE = 83
    EIGHTYFOUR = 84
    EIGHTYFIVE = 85
    EIGHTYSIX = 86
    EIGHTYSEVEN = 87
    EIGHTYEIGHT = 88
    EIGHTYNINE = 89
    NINETY = 90
    NINETYONE = 91
    NINETYTWO = 92
    NINETYTHREE = 93
    NINETYFOUR = 94
    NINETYFIVE = 95
    NINETYSIX = 96
    NINETYSEVEN = 97
    NINETYEIGHT = 98
    NINETYNINE = 99
    ONEHUNDRED = 100
    ONEHUNDREDONE = 101
    ONEHUNDREDTWO = 102
    ONEHUNDREDTHREE = 103
    ONEHUNDREDFOUR = 104
    ONEHUNDREDFIVE = 105
    ONEHUNDREDSIX = 106
    ONEHUNDREDSEVEN = 107
    ONEHUNDREDEIGHT = 108
    ONEHUNDREDNINE = 109
    ONEHUNDREDTEN = 110

    def __str__(self):
        return str(self.value)


LEVEL_WEIGHTS: list[int] = [0, 0] + [2 ** n for n in range(len(Level), 0, -1)]
INF_LEVEL_WEIGHTS: list[int] = [0, 0] + [2 ** n for n in range(len(InfLevel), 0, -1)]


class ShortLevel(IntEnum):
    """ Short Deck Levels of playing cards. """

    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    ELEVEN = 11
    TWELVE = 12
    THIRTEEN = 13
    FOURTEEN = 14

    def __str__(self):
        return str(self.value)


@dataclass(frozen=True)
class Card:
    rank: Rank
    suit: Suit
    level: Level | None = None
    deck_id: uuid4 | None = None


class DeckABC(ABC):
    @abstractmethod
    def shuffle(self) -> None: ...

    @abstractmethod
    def deal(self, n: int) -> list[Card]: ...

    @property
    @abstractmethod
    def deck_id(self) -> uuid4: ...


class BaseDeck(DeckABC):

    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards

    def shuffle(self) -> None:
        random.shuffle(self.cards)

    def deal(self, n: int) -> list[Card]:
        return [self.cards.pop() for _ in range(n)]

    def __len__(self) -> int:
        return len(self.cards)


class FiveDeck(BaseDeck):

    def __init__(self) -> None:
        self.deck_id = _id = uuid4()
        super().__init__([
            Card(r, s, _id) for _ in range(5) for r in Rank for s in Suit
        ])                


class StdDeck(BaseDeck):

    def __init__(self) -> None:
        self.deck_id = _id = uuid4()
        super().__init__([
            Card(r, s, _id) for r in Rank for s in Suit
        ])


class ShortDeck(BaseDeck):  # a short deck with 36 cards (6-Ace)

    def __init__(self) -> None:
        self.deck_id = _id = uuid4()
        super().__init__([
            Card(r, s, _id) for r in Rank for s in Suit
        ])

class Hand:
  """ Hands with one or more playing cards. """
  pass
