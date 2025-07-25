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
LEVEL_WEIGHTS = (
    4096, 2048, 1024, 512, 
    256, 128, 64, 32, 
    16, 8, 4, 2,
    1
)


@dataclass(frozen=True, slots=True)
class LevelCard:
    """

    Level Card.

    level: 0 (Level 2) - 12 (Level 14)
    rank: 0 (deuce) - 12 (ace)
    suit: 0 (spaces), 1 (hearts), 2 (diamonds), 3 (clubs)
    
    """
    level: int
    rank: int
    suit: int

    def __repr__(self):
        return f"{LEVEL_RANKS[self.rank]}{LEVEL_SUITS[self.suit]}{LEVEL_LEVELS[self.level]}"


class BitfieldLevelDeck:
    """High-performance deck using bitfields for card representation."""
    
    def __init__(self):
        self._cards = self._generate_deck()
        self._index = 0

    def _generate_deck(self) -> list[int]:
        cards: list[int] = []
        base_pairs = [(r, s) for r in range(13) for s in range(4)]
        levels = random.choices(range(13), weights=LEVEL_WEIGHTS, k=52)
        for (r, s), lvl in zip(base_pairs, levels):
            cards.append(encode_card(r, s, lvl))
        random.shuffle(cards)
        return cards

    def shuffle(self) -> None:
        random.shuffle(self._cards)
        self._index = 0

    def deal(self, n: int) -> list[int]:
        i = self._index
        self._index += n
        return self._cards[i:i + n]

    def __len__(self) -> int:
        return len(self._cards) - self._index


def _encode_level_card(level: int, rank: int, suit: int) -> int:
    return (level << 6) | (rank << 2) | suit


def _decode_level_card(card: int) -> tuple[int, int, int]:
    return (card >> 6) & 0b1111, (card >> 2) & 0b1111, card & 0b11


def _evaluate_hand(hand: tuple(int, int, int, int, int)) -> int:
    ...
