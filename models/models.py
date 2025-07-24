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

:class ShortLevel(Level)  # levels 6-14 only for short deck

# card

:class Card(StrEnum)  # a card has rank, suit, and level | None

# deck

:class Deck

:class ShortDeck(Deck)  # a short deck with 36 cards: 6-Ace

:class InfDeck(Deck)  # a deck with infinitely many cards, with InfLevels

# hand

:class Hand

:class OmahaHand(Hand)  # a hand with four playing cards

:class HoldEmHand(Hand)  # a hand with two playing cards

# board

:class Board  # a board with 0-5 x 1-3 = 0-15 playing cards
# 1-3: run it once, twice or thrice.

# game

:class Game

:class PLO(Game)

:class FiveDeckPLO(PLO)

:class NLH(Game)

:class LevelNLH(NLH)

# Later we might add FiveDeckNLH, LevelPLO, InfNLH, and InfPLO
# as well as short deck variants with 5 decks, levels, or both.

# player

:class Player

:class AIPlayer(Player)  # for AI to be a player

# chips

:class Chips

# pot

:class Pot

# round

:class Round  # an entire round, from preflop to showdown

# hand evaluation

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
#    - Level Groups = [3, 2, 2, 4, 2]
#
# These are together represented in a named tuple, e.g.
#
# (2, 1, 1, 14, 13, 9, 7, 2, 3, 2, 2, 4, 5) = 
# (Level=2, Tier=1, Cat=1, Group1=14, Group2=13, Group3=9,
#  Group4=7, Group5=2, LGroup1=3, LGroup2=2, LGroup3=2,
#  LGroup4=4, LGroup5=5)
#
# If a Group or LGroup does not apply, it is None.
#
# For example: As(3) Ks(2), Qs(2), Ts(4), Js(2) has
#    - Level = 2
#    - Tier = Diamond (5/5)
#    - Category = Royal Flush (4/5)
#    - Groups = None
#    - Level Groups = None
#
# (2, 5, 4) = 
# (Level=2, Tier=5, Cat=4, Group1=None, Group2=None,
#  Group3=None, Group4=None, Group5=None, LGroup1=None,
#  LGroup2=None, LGroup3=None, LGroup4=None, LGroup5=None)
#
# The :func for hand_evaluation should work on:
#    - A list of one or more cards
#    - A board + hand
# but not on:
#    - A board + multiple hands.
# for that we use the :func distribute_pot

:class HandLevel

:class HandTier

:class HandCategory

:class HandGroup1

:class HandGroup2

:class HandGroup3

:class HandGroup4

:class HandGroup5

:class HandLevelGroup1

:class HandLevelGroup2

:class HandLevelGroup3

:class HandLevelGroup4

:class HandLevelGroup5

:func distribute_pot

"""
