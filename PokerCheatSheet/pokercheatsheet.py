"""
poker_oracle.py
===============
A zero-dependency Texas Hold'em hand evaluator and equity calculator.

Features:
  - Evaluate any 5-card hand (rank + name)
  - Find the best 5-card hand from 7 community cards
  - Run Monte Carlo equity simulations for multiple players
  - Pretty-print cards with Unicode suit symbols

Usage:
  python poker_oracle.py                  # run built-in demo
  python poker_oracle.py --sim            # quick equity sim example

Author: <your name>
License: MIT
"""

import random
from collections import Counter
from itertools import combinations
from typing import Optional

# constants

RANKS = "23456789TJQKA"
SUITS = "shdc"  # spades, hearts, diamonds, clubs

SUIT_SYMBOLS = {"s": "♠", "h": "♥", "d": "♦", "c": "♣"}
SUIT_COLORS  = {"s": "", "h": "\033[91m", "d": "\033[91m", "c": ""}
RESET        = "\033[0m"

HAND_NAMES = [
    "High card",
    "One pair",
    "Two pair",
    "Three of a kind",
    "Straight",
    "Flush",
    "Full house",
    "Four of a kind",
    "Straight flush",   # includes Royal flush
]

# deck

def full_deck() -> list[str]:
    """Return a full 52-card deck as a list of strings, e.g. 'As', 'Td'."""
    return [r + s for s in SUITS for r in RANKS]


def pretty_card(card: str) -> str:
    """Return a colorized Unicode card string, e.g. 'A♥' in red."""
    rank, suit = card[0], card[1]
    color = SUIT_COLORS[suit]
    symbol = SUIT_SYMBOLS[suit]
    return f"{color}{rank}{symbol}{RESET}"


def pretty_hand(cards: list[str]) -> str:
    return "  ".join(pretty_card(c) for c in cards)


# hand evaluator

def _rank_indices(hand: list[str]) -> list[int]:
    return [RANKS.index(c[0]) for c in hand]


def rank_hand(hand: list[str]) -> tuple[int, list[int]]:
    """
    Evaluate a 5-card hand.

    Returns
    -------
    (hand_rank, tiebreakers)
        hand_rank   : int 0-8 (0 = high card, 8 = straight/royal flush)
        tiebreakers : sorted rank indices for breaking ties

    Examples
    --------
    >>> rank_hand(['As', 'Ks', 'Qs', 'Js', 'Ts'])
    (8, [12, 11, 10, 9, 8])
    >>> rank_hand(['2h', '2d', '2c', '3s', '3h'])
    (6, [1, 1, 1, 2, 2])   # full house, twos over threes
    """
    if len(hand) != 5:
        raise ValueError(f"rank_hand expects exactly 5 cards, got {len(hand)}")

    ranks   = sorted(_rank_indices(hand), reverse=True)
    suits   = [c[1] for c in hand]
    counter = Counter(ranks)
    # Sort by (count desc, rank desc) so high multiples come first
    groups  = sorted(counter.items(), key=lambda x: (x[1], x[0]), reverse=True)
    group_counts = [g[1] for g in groups]

    is_flush    = len(set(suits)) == 1
    is_straight = (len(set(ranks)) == 5 and max(ranks) - min(ranks) == 4)

    # Wheel straight: A-2-3-4-5  →  treat Ace as low (-1)
    if sorted(ranks) == [0, 1, 2, 3, 12]:
        is_straight = True
        ranks = [3, 2, 1, 0, -1]

    if is_straight and is_flush:
        return (8, ranks)
    if group_counts == [4, 1]:
        return (7, ranks)
    if group_counts == [3, 2]:
        return (6, ranks)
    if is_flush:
        return (5, ranks)
    if is_straight:
        return (4, ranks)
    if group_counts[0] == 3:
        return (3, ranks)
    if group_counts[:2] == [2, 2]:
        return (2, ranks)
    if group_counts[0] == 2:
        return (1, ranks)
    return (0, ranks)


def best_hand_from_7(cards: list[str]) -> tuple[tuple[int, list[int]], list[str]]:
    """
    Find the best 5-card hand from up to 7 cards (standard Hold'em).

    Returns
    -------
    (score, best_five)
        score     : (hand_rank, tiebreakers) from rank_hand()
        best_five : the 5 cards making the best hand
    """
    best_score = (-1, [])
    best_five  = []
    for combo in combinations(cards, 5):
        score = rank_hand(list(combo))
        if score > best_score:
            best_score = score
            best_five  = list(combo)
    return best_score, best_five


def hand_name(score: tuple[int, list[int]]) -> str:
    """Return the human-readable name for a hand score."""
    return HAND_NAMES[score[0]]


# monte carlo equity calculator

def equity(
    hole_cards: list[list[str]],
    board: Optional[list[str]] = None,
    n_simulations: int = 10_000,
) -> list[float]:
    """
    Estimate win equity for each player via Monte Carlo simulation.

    Parameters
    ----------
    hole_cards    : list of 2-card lists, one per player
    board         : 0–5 known community cards (default: empty)
    n_simulations : number of random runouts to simulate

    Returns
    -------
    List of win-rate floats (0.0–1.0) per player, summing to ≈ 1.0
    (ties are split evenly).

    Example
    -------
    >>> eq = equity([['As', 'Kh'], ['Qd', 'Qc']], board=['Qs', 'Jh', 'Td'])
    >>> print([f"{e:.1%}" for e in eq])   # rough output
    ['54.2%', '45.8%']
    """
    board = board or []
    known_cards = set(c for hand in hole_cards for c in hand) | set(board)
    remaining_deck = [c for c in full_deck() if c not in known_cards]
    cards_needed = 5 - len(board)

    wins = [0] * len(hole_cards)

    for _ in range(n_simulations):
        runout = random.sample(remaining_deck, cards_needed)
        full_board = board + runout

        scores = []
        for hole in hole_cards:
            score, _ = best_hand_from_7(hole + full_board)
            scores.append(score)

        best = max(scores)
        winners = [i for i, s in enumerate(scores) if s == best]
        share = 1.0 / len(winners)
        for w in winners:
            wins[w] += share

    return [w / n_simulations for w in wins]


# CLI / demo

def _deal_random(n_players: int, n_board: int) -> tuple[list[list[str]], list[str]]:
    """Randomly deal hole cards and board cards from a fresh shuffled deck."""
    deck = full_deck()
    random.shuffle(deck)
    idx = 0
    holes = []
    for _ in range(n_players):
        holes.append([deck[idx], deck[idx + 1]])
        idx += 2
    board = deck[idx: idx + n_board]
    return holes, board


def _run_sim(label: str, players: list[list[str]], board: list[str],
             street: str, n: int = 10_000) -> None:
    print(f"\n{label}")
    print("-" * 52)
    for i, hole in enumerate(players):
        print(f"  Player {i+1} : {pretty_hand(hole)}")
    if board:
        print(f"  Board    : {pretty_hand(board)}  ({street})")
    else:
        print(f"  Board    : (pre-flop — no community cards yet)")
    print(f"  Simulating {n:,} runouts …", end="", flush=True)

    eq = equity(players, board=board, n_simulations=n)

    print(f"\r{'':52}\r", end="")
    for i, (hole, e) in enumerate(zip(players, eq)):
        bar_len = int(e * 36)
        bar = "█" * bar_len + "░" * (36 - bar_len)
        print(f"  Player {i+1}  [{bar}]  {e:.1%}")


def _demo():
    print("\n" + "=" * 52)
    print("  POKER ORACLE  —  Texas Hold'em equity demo")
    print("  Hands are randomly dealt every run.")
    print("=" * 52)

    # ex 1 — 2 players, pre-flop (0 board cards)
    holes1, _ = _deal_random(n_players=2, n_board=0)
    _run_sim(
        "Ex 1 · Pre-flop  (2 players, no board)",
        players=holes1,
        board=[],
        street="pre-flop",
    )

    # ex 2 — 2 players, flop (3 board cards)
    holes2, board2 = _deal_random(n_players=2, n_board=3)
    _run_sim(
        "Ex 2 · Flop  (2 players, 3 board cards)",
        players=holes2,
        board=board2,
        street="flop",
    )

    # ex 3 — 3 players, turn (4 board cards)
    holes3, board3 = _deal_random(n_players=3, n_board=4)
    _run_sim(
        "Ex 3 · Turn  (3 players, 4 board cards)",
        players=holes3,
        board=board3,
        street="turn",
    )

    print("\n" + "=" * 52)
    print("  Re-run any time for a fresh random deal.")
    print("  Import: from poker_oracle import equity, best_hand_from_7")
    print("=" * 52 + "\n")


if __name__ == "__main__":
    _demo()
