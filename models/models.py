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

:abcls CardABC(ABC)  # a card has rank, suit, and level | None

:class BaseCard(CardABC)

:class Card(BaseCard)

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

from enum import IntEnum
from lru_cache import lru_cache


class Rank(IntEnum):
  """ Ranks of playing cards. """
  ...


...


class Hand:
  """ Hands with one or more playing cards. """
  pass
