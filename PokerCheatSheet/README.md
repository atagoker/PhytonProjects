# Poker Cheat Sheet 

A zero-dependency Texas Hold'em hand evaluator and equity calculator in pure Python. Evaluate hands, find the best 5-card combo from 7 cards, and run Monte Carlo equity simulations — all from the command line or as an importable module.

---

## Features

- **Hand evaluator** — rank any 5-card hand and get its name
- **Best-hand finder** — pick the strongest 5-card combo from 7 (hole + board)
- **Equity simulator** — Monte Carlo win-rate for 2 or 3 players at any street
- **Random demo** — every run deals fresh random hands, no two runs the same
- **Terminal display** — Unicode suit symbols ♠ ♥ ♦ ♣ with red/black coloring
- **No dependencies** — standard library only (`random`, `collections`, `itertools`)

---

## Requirements

- Python 3.10 or higher
- No third-party packages needed

---

## Installation

```bash
git clone https://github.com/your-username/poker_oracle.git
cd poker_oracle
```

That's it. No `pip install` required.

---

## Quick start

Run the built-in demo — 3 randomly dealt equity simulations:

```bash
python poker_oracle.py
```

Example output (yours will differ every run):

```
====================================================
  POKER ORACLE  —  Texas Hold'em equity demo
  Hands are randomly dealt every run.
====================================================

Ex 1 · Pre-flop  (2 players, no board)
----------------------------------------------------
  Player 1 : Q♥  Q♦
  Player 2 : 9♣  J♦
  Board    : (pre-flop — no community cards yet)
  Player 1  [██████████████████████████████░░░░░░]  85.6%
  Player 2  [█████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  14.4%

Ex 2 · Flop  (2 players, 3 board cards)
----------------------------------------------------
  Player 1 : 4♠  T♠
  Player 2 : 8♣  5♦
  Board    : 2♠  7♦  3♥  (flop)
  Player 1  [████████████████████████████░░░░░░░░]  79.0%
  Player 2  [███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  21.0%

Ex 3 · Turn  (3 players, 4 board cards)
----------------------------------------------------
  Player 1 : Q♦  Q♣
  Player 2 : 2♠  5♣
  Player 3 : K♣  9♠
  Board    : 4♦  6♣  J♥  8♣  (turn)
  Player 1  [███████████████████████░░░░░░░░░░░░░]  66.3%
  Player 2  [██████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  19.4%
  Player 3  [█████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░]  14.3%
```

---

## Card format

Cards are two-character strings: **rank** + **suit**.

| Ranks | `2 3 4 5 6 7 8 9 T J Q K A` |
|-------|------------------------------|
| Suits | `s` ♠ spades · `h` ♥ hearts · `d` ♦ diamonds · `c` ♣ clubs |

**Examples:** `As` = Ace of spades · `Td` = Ten of diamonds · `2h` = Two of hearts · `Kc` = King of clubs

---

## Hand rankings

| Rank | Name | Example |
|------|------|---------|
| 8 | Straight flush (incl. royal) | A♠ K♠ Q♠ J♠ T♠ |
| 7 | Four of a kind | K♠ K♥ K♦ K♣ 7 |
| 6 | Full house | Q♠ Q♥ Q♦ 9♥ 9♦ |
| 5 | Flush | A♥ J♥ 8♥ 5♥ 2♥ |
| 4 | Straight | 5♠ 6♥ 7♣ 8♦ 9♠ |
| 3 | Three of a kind | J♠ J♥ J♦ 7 3 |
| 2 | Two pair | A♠ A♣ K♥ K♦ Q |
| 1 | One pair | Q♥ Q♦ A 8 3 |
| 0 | High card | A♠ J 8 5 2 |

---

## API reference

### `rank_hand(hand)`

Evaluate a 5-card hand.

```python
from poker_oracle import rank_hand, hand_name

score = rank_hand(['As', 'Ks', 'Qs', 'Js', 'Ts'])
print(score)             # (8, [12, 11, 10, 9, 8])
print(hand_name(score))  # Straight flush
```

Returns `(hand_rank, tiebreakers)` where `hand_rank` is an int 0–8 and `tiebreakers` is a sorted list of rank indices used to break ties between hands of the same type.

---

### `best_hand_from_7(cards)`

Find the best 5-card hand from 7 cards (2 hole + 5 board).

```python
from poker_oracle import best_hand_from_7, hand_name

hole  = ['Ah', 'Kh']
board = ['Qh', 'Jh', 'Th', '2c', '7d']

score, best5 = best_hand_from_7(hole + board)
print(best5)             # ['Ah', 'Kh', 'Qh', 'Jh', 'Th']
print(hand_name(score))  # Straight flush
```

Tries all C(7,5) = 21 combinations and returns the highest-scoring five.

---

### `equity(hole_cards, board, n_simulations)`

Estimate each player's win probability via Monte Carlo simulation.

```python
from poker_oracle import equity

# Pre-flop: Aces vs Kings
eq = equity([['As', 'Ad'], ['Kh', 'Kd']])
print([f"{e:.1%}" for e in eq])   # e.g. ['82.1%', '17.9%']

# With a known flop
eq = equity(
    [['As', 'Ad'], ['Kh', 'Kd']],
    board=['Kc', '2h', '7d'],
    n_simulations=50_000
)
print([f"{e:.1%}" for e in eq])   # e.g. ['27.5%', '72.5%']

# Three players on the turn
eq = equity(
    [['5s', '5d'], ['6h', '7h'], ['Qc', 'Tc']],
    board=['5h', '8c', '9d', 'Th']
)
print([f"{e:.1%}" for e in eq])   # e.g. ['21.0%', '71.8%', '7.2%']
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `hole_cards` | `list[list[str]]` | required | 2-card list per player |
| `board` | `list[str]` | `[]` | 0–5 known community cards |
| `n_simulations` | `int` | `10_000` | More = more accurate, slower |

Ties are split evenly between all winners. Results vary slightly between runs — increase `n_simulations` for tighter confidence intervals.

---

### `pretty_hand(cards)`

Return a colorized terminal string for a list of cards.

```python
from poker_oracle import pretty_hand
print(pretty_hand(['Ah', 'Kh', 'Qh']))   # A♥  K♥  Q♥  (red in terminal)
```

---

## Starting hand tiers (quick reference)

| Tier | Hands | Suggested play |
|------|-------|----------------|
| Premium | AA, KK, QQ, AK suited | Raise / re-raise any position |
| Strong | JJ, TT, AK, AQ suited, KQ suited | Raise most positions |
| Playable | 99–88, AQ, AJ suited, KQ, QJ suited | Raise or call by position |
| Speculative | 77–22, suited connectors, A10s | Call late position only |
| Marginal | K10, Q10, offsuit connectors | Mostly fold |
| Trash | Everything else | Fold pre-flop |

---

## Project structure

```
poker_oracle/
├── poker_oracle.py   # full library + CLI demo
└── README.md
```

---

## License

MIT — free to use, modify, and distribute.
