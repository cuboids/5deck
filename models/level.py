from dataclasses import dataclass

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
