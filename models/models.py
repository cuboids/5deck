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
from collections import Counter, namedtuple
from dataclasses import dataclass
from enum import Enum, IntEnum
import random
from uuid import UUID, uuid4


RANKS: list[None | str] = [None, None] + list("23456789TJQKA")
LEVELS: list[None | str] = [None, None] + [
    "", "³", "⁴", "⁵", "⁶", "⁷", "⁸", "⁹",
    "¹⁰", "¹¹", "¹²", "¹³", "¹⁴"
]


class Tier(IntEnum):
    """ Tiers of Hands """
    BRONZE = 100
    SILVER = 200
    GOLD = 300
    PLATINUM = 400
    DIAMOND = 500


class Category(IntEnum):
    """ Category of Hands """

    # Bronze
    HIGH_CARD = 110
    ONE_PAIR = 120
    TWO_PAIR = 130
    SUITED_PAIR = 140
    SEMI_SUITED_TWO_PAIR = 150

    # Silver
    THREE_OF_A_KIND = 210
    STRAIGHT = 220
    FULL_HOUSE_5D = 230
    FULL_HOUSE_SD = 230
    FLUSH = 240
    FULL_HOUSE = 245  # A full house in 1deck poker
    FLUSHED_PAIR = 250

    # Gold
    SUITED_TWO_PAIR = 310
    VILLA = 320
    FOUR_OF_A_KIND = 330
    FLUSHED_TWO_PAIR = 340
    SUITED_TRIPS = 350

    # Platinum
    MANSION = 410
    FLUSHED_TRIPS = 420
    CASTLE = 430
    FIVE_OF_A_KIND = 440
    STRAIGHT_FLUSH = 450

    # Diamond
    ROYAL_PALACE = 510
    ROYAL_GUARD = 520
    ROYAL_QUADS = 530
    ROYAL_FLUSH = 540
    ROYAL_QUINTET = 550


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


LEVEL_WEIGHTS: list[int] = [2 ** n for n in range(len(Level), 0, -1)]
INF_LEVEL_WEIGHTS: list[int] = [2 ** n for n in range(len(InfLevel), 0, -1)]


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
    deck_id: UUID | None = None

    def __repr__(self):
        if self.level is None:
            return f"{self.rank}{self.suit}"
        return f"{self.rank}{self.suit}{LEVELS[self.level.value]}"


class DeckABC(ABC):
    @abstractmethod
    def shuffle(self) -> None: ...

    @abstractmethod
    def deal(self, n: int) -> list[Card]: ...


class BaseDeck(DeckABC):

    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards
        self.shuffle()

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
            Card(r, s, None, _id) for _ in range(5) for r in Rank for s in Suit
        ])                


class StdDeck(BaseDeck):

    def __init__(self) -> None:
        self.deck_id = _id = uuid4()
        super().__init__([
            Card(r, s, None, _id) for r in Rank for s in Suit
        ])


class ShortDeck(BaseDeck):

    def __init__(self) -> None:
        self.deck_id = _id = uuid4()
        super().__init__([
            Card(r, s, None, _id) for r in Rank for s in Suit
        ])


class LevelDeck(BaseDeck):

    def __init__(self) -> None:
        self.deck_id = _id = uuid4()
        levels = random.choices(list(Level), weights=LEVEL_WEIGHTS, k=52)
        super().__init__([
            Card(r, s, levels[i], _id) for i, (r, s) in enumerate((r, s) for r in Rank for s in Suit)
        ])


class HandABC(ABC):
    pass


class BaseHand(HandABC):
    def __init__(self, cards: list[Card], deck_id: UUID) -> None:
        self.cards = cards

    def __len__(self) -> int:
        return len(self.cards)
    
    def __repr__(self):
        return f"Hand({", ".join(str(self.cards[i]) for i in range(len(self.cards)))}"


class OmahaHand(BaseHand):
    def __init__(self, deck: BaseDeck) -> None:
        super().__init__(deck.deal(4), deck.deck_id)


class HoldEmHand(BaseHand):
    def __init__(self, deck: BaseDeck) -> None:
        super().__init__(deck.deal(2), deck.deck_id)


class Board(ABC):

    @abstractmethod
    def run_it_once() -> None: ...

    @abstractmethod
    def run_it_twice() -> None: ...

    @abstractmethod
    def run_it_thrice() -> None: ...

    @abstractmethod
    def deal_flop() -> None: ...

    @abstractmethod
    def deal_turn() -> None: ...

    @abstractmethod
    def deal_river() -> None: ...


class BaseBoard(Board):
    
    def __init__(self, deck: BaseDeck) -> None:
        self.cards = []
        self._deck = deck
        self._flop_was_dealt = False
        self._turn_was_dealt = False
        self._river_was_dealt = False

    def run_it_once(self):
        if not self._flop_was_dealt:
            self.deal_flop()
        if not self._turn_was_dealt:
            self.deal_turn()
        if not self._river_was_dealt:
            self.deal_river()

    def run_it_twice(self):
        return NotImplemented
    
    def run_it_thrice():
        return NotImplemented

    def deal_flop(self):
        if self._turn_was_dealt or self._river_was_dealt:
            raise ValueError(
                "Flop cannot be dealt if turn or river has been dealt")
        self.cards.extend(self._deck.deal(3))
        self._flop_was_dealt = True

    def deal_turn(self):
        if not self._flop_was_dealt:
            raise ValueError(
                "Turn cannot be dealt if flop was not dealt")
        if self._river_was_dealt:
            raise ValueError(
                "Turn cannot be dealt if river has been dealt")
        self.cards.extend(self._deck.deal(1))
        self._turn_was_dealt = True

    def deal_river(self):
        if not self._flop_was_dealt or not self._turn_was_dealt:
            raise ValueError(
                "River cannot be dealt if flop or turn was not dealt")
        self.cards.extend(self._deck.deal(1))
        self._river_was_dealt = True

    def __repr__(self):
        return "Board: " + " ".join(str(card) for card in self.cards)


class StdBoard(BaseBoard):
    def __init__(self, deck: BaseDeck) -> None:
        super().__init__(deck)


class HandStrengthABC(ABC):

    @property
    @abstractmethod
    def level(self) -> int | None: ...

    @property
    @abstractmethod
    def tier(self) -> int | None: ...

    @property
    @abstractmethod
    def category(self) -> int | None: ...

    @property
    @abstractmethod
    def group1(self) -> int | None: ...

    @property
    @abstractmethod
    def group2(self) -> int | None: ...

    @property
    @abstractmethod
    def group3(self) -> int | None: ...

    @property
    @abstractmethod
    def group4(self) -> int | None: ...

    @property
    @abstractmethod
    def group5(self) -> int | None: ...

    @property
    @abstractmethod
    def level1(self) -> int | None: ...

    @property
    @abstractmethod
    def level2(self) -> int | None: ...

    @property
    @abstractmethod
    def level3(self) -> int | None: ...

    @property
    @abstractmethod
    def level4(self) -> int | None: ...

    @property
    @abstractmethod
    def level5(self) -> int | None: ...

    @property
    @abstractmethod
    def hand_strength_tup(self) -> namedtuple: ...

    @property
    @abstractmethod
    def hand_strength_num(self) -> float: ...

    @property
    @abstractmethod
    def hand_strength_txt(self) -> namedtuple: ...


class BaseHandStrength(HandStrengthABC):

    def __init__(self, hand: BaseHand) -> None:
        self._hand_strength_tup = BaseHandStrengthEvaluator(hand)

    @property
    def level(self) -> int | None:
        return self.hand_strength_tup["level"]

    @property
    def tier(self) -> int | None:
        return self.hand_strength_tup["tier"]

    @property
    def category(self) -> int | None:
        return self.hand_strength_tup["category"]

    @property
    def group1(self) -> int | None:
        return self.hand_strength_tup["group1"]

    @property
    def group2(self) -> int | None:
        return self.hand_strength_tup["group2"]

    @property
    def group3(self) -> int | None:
        return self.hand_strength_tup["group3"]

    @property
    def group4(self) -> int | None:
        return self.hand_strength_tup["group4"]

    @property
    def group5(self) -> int | None:
        return self.hand_strength_tup["group5"]

    @property
    def level1(self) -> int | None:
        return self.hand_strength_tup["level1"]

    @property
    def level2(self) -> int | None:
        return self.hand_strength_tup["level2"]

    @property
    def level3(self) -> int | None:
        return self.hand_strength_tup["level3"]

    @property
    def level4(self) -> int | None:
        return self.hand_strength_tup["level4"]

    @property
    def level5(self) -> int | None:
        return self.hand_strength_tup["level5"]

    @property
    def hand_strength_tup(self) -> namedtuple:
        return self._hand_strength_tup

    @property
    def hand_strength_num(self) -> float:
        return NotImplemented

    @property
    def hand_strength_txt(self) -> namedtuple:
        return NotImplemented



class HandStrengthEvaluator(ABC):

    @staticmethod
    @abstractmethod
    def evaluate_hand() -> ...: ...


HandStrengthTup = namedtuple(
    "HandStrengthTup",
    ["level", "tier", "category", "group1", "group2", "group3", "group4",
     "group5", "level1", "level2", "level3", "level4", "level5"],
    defaults = [None] * 13
)


class BaseHandStrengthEvaluator(HandStrengthEvaluator):

    @staticmethod
    def evaluate_hand(cards: list[Card]) -> namedtuple:

        level = min(card.level.value for card in cards)

        cards = sorted(
            [card for card in cards],
            key=lambda c: (c.rank.value, c.level.value, c.suit.value),
            reverse=True
        )

        ranks = [card.rank.value for card in cards]
        levels = [card.level.value for card in cards]
        suits = [card.suit for card in cards]
        count = Counter(ranks)
        counts = sorted(count.values(), reverse=True)

        is_flush = len(set(suits)) == 1
        is_straight = ranks == list(range(ranks[0], ranks[0] - 5, -1))
        
        # Handle wheel straight (A-2-3-4-5)
        if ranks == [14, 5, 4, 3, 2]:
            is_straight = True
            ranks = [5, 4, 3, 2, 1]

        if is_flush and is_straight:

            if ranks[0] == 14:

                # Royal Flush
                return HandStrengthTup(
                    level=level - 2, 
                    tier=4,
                    category=4
                    )
            
            # Straight Flush
            return HandStrengthTup(
                level=level - 2,
                tier=3,
                category=4
                )
        
        if counts == [4, 1]:

            four = [r for r, c in count.items() if c == 4]
            kicker = [r for r in ranks if r not in four]

            # Four of a Kind
            return HandStrengthTup(
                level=level - 2,
                tier=2,
                category=2,
                group1=four[0] - 2,
                group2=kicker[0] - 2,
                level5=levels[4] - 2)
        
        if counts == [3, 2]:

            triple = [r for r, c in count.items() if c == 3]
            pair = [r for r, c in count.items() if c == 2]

            # Full House
            return HandStrengthTup(
                level=level - 2,
                tier=2,
                category=1,
                group1=triple[0] - 2,
                group2=pair[0] - 2,
                level1=levels[0] - 2,
                level4=levels[3] - 2,
                level5=levels[4] - 2
                )
        
        if is_flush:
            
            # Flush
            return HandStrengthTup(
                level=level - 2,
                tier=1,
                category=3,
                group1=ranks[0] - 2,
                group2=ranks[1] - 2,
                group3=ranks[2] - 2,
                group4=ranks[3] - 2,
                group5=ranks[4] - 2,
            )

        if is_straight:

            # Straight
            return HandStrengthTup(
                level=level - 2,
                tier=1,
                category=2,
                group1=ranks[0] - 2,
                level1=levels[0] - 2,
                level2=levels[1] - 2,
                level3=levels[2] - 2,
                level4=levels[3] - 2,
                level5=levels[4] - 2
            )
        if counts == [3, 1, 1]:

            triple = [r for r, c in count.items() if c == 3]
            kickers = [r for r in ranks if r not in triple]

            # Three of a Kind
            return HandStrengthTup(
                level=level - 2,
                tier=1,
                category=0,
                group1=triple[0] - 2,
                group2=kickers[0] - 2,
                group3=kickers[1] - 2,
                level1=levels[0] - 2,
                level4=levels[3] - 2,
                level5=levels[4] - 2
            )

        if counts == [2, 2, 1]:

            pairs = sorted([r for r, c in count.items() if c == 2], reverse=True)
            kicker = [r for r in ranks if r not in pairs]

            # Two Pair
            return HandStrengthTup(
                level=level - 2,
                tier=0,
                category=2,
                group1=pairs[0] - 2,
                group2=pairs[1] - 2,
                group3=kicker[0] - 2,
                level1=levels[0] - 2,
                level2=levels[1] - 2,
                level3=levels[2] - 2,
                level4=levels[3] - 2,
                level5=levels[4] - 2
            )

        if counts == [2, 1, 1, 1]:

            pair = [r for r, c in count.items() if c == 2]
            kickers = [r for r in ranks if r not in pair]

            # One Pair
            return HandStrengthTup(
                level=level - 2,
                tier=0,
                category=1,
                group1=pair[0] - 2,
                group2=kickers[0] - 2,
                group3=kickers[1] - 2,
                group4=kickers[2] - 2,
                level1=levels[0] - 2,
                level2=levels[1] - 2,
                level3=levels[2] - 2,
                level4=levels[3] - 2,
                level5=levels[4] - 2
            )
        
        # High Card
        return HandStrengthTup(
            level=level - 2,
            tier=0,
            category=0,
            group1=ranks[0] - 2,
            group2=ranks[1] - 2,
            group3=ranks[2] - 2,
            group4=ranks[3] - 2,
            group5=ranks[4] - 2,
            level1=levels[0] - 2,
            level2=levels[1] - 2,
            level3=levels[2] - 2,
            level4=levels[3] - 2,
            level5=levels[4] - 2
            )


def main():
    out = set()
    strengths = set()
    for _ in range(100_000):
        l = LevelDeck()
        for __ in range(10):
            b = StdBoard(l)
            b.run_it_once()
            bhse = BaseHandStrengthEvaluator()
            strength = bhse.evaluate_hand(b.cards)
            if strength not in strengths:
                strengths.add(strength)
                out.add((str(b.cards), strength))

    hs = sorted(out, key=lambda hs: tuple(h for h in hs[1] if h is not None))
    for h in hs:
        print(h[1])
        print(h[0])
        print()


if __name__ == "__main__":
    main()