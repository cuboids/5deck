from dataclasses import dataclass


LEVEL_RANKS = (
    "2", "3", "4", "5",
    "6", "7", "8", "9",
    "T", "J", "Q", "K",
    "A"
)
LEVEL_SUITS = (
    '♠', '♥', '♦', '♣', 
)
LEVEL_LEVELS = (
    "", "³", "⁴", "⁵", 
    "⁶", "⁷", "⁸", "⁹",
    "¹⁰", "¹¹", "¹²", "¹³", 
    "¹⁴"
)


@dataclass(frozen=True, slots=True)
class _LevelCard:
    """

    Level Card.

    rank: 0 (deuce) - 12 (ace)
    suit: 0 (spaed), 1 (hearts), 2 (diamonds), 3 (clubs)
    level: 0 (Level 2) - 12 (Level 14)
    
    """
    rank: int
    suit: int
    level: int

    def __repr__(self):
        return f"{LEVEL_RANKS[self.rank]}{LEVEL_SUITS[self.suit]}{LEVEL_LEVELS[self.level]}"
