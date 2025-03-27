import random

suits = ['♠', '♥', '♦', '♣']
ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
rank_values = {rank: i for i, rank in enumerate(ranks, start=2)}

# deck setup
def make_deck():
    return [r + s for s in suits for r in ranks]

def deal_hand(deck, n=5):
    return [deck.pop() for _ in range(n)]

def show_hand(hand):
    return ' '.join(hand)

# rank evaluation
def evaluate_hand(hand):
    values = sorted([rank_values[card[:-1]] for card in hand], reverse=True)
    suits_in_hand = [card[-1] for card in hand]
    ranks_in_hand = [card[:-1] for card in hand]
    value_counts = {v: values.count(v) for v in set(values)}
    counts = sorted(value_counts.values(), reverse=True)

    is_flush = len(set(suits_in_hand)) == 1
    is_straight = values == list(range(values[0], values[0] - 5, -1))

    if is_flush and is_straight:
        return (8, values[0])  # straight flush
    elif 4 in counts:
        return (7, get_key_by_value(value_counts, 4))  # four of a kind
    elif 3 in counts and 2 in counts:
        return (6, get_key_by_value(value_counts, 3))  # full house
    elif is_flush:
        return (5, values)  # flush
    elif is_straight:
        return (4, values[0])  # straight
    elif 3 in counts:
        return (3, get_key_by_value(value_counts, 3))  # three of a kind
    elif counts.count(2) == 2:
        return (2, get_highest_pair(value_counts))  # two pair
    elif 2 in counts:
        return (1, get_key_by_value(value_counts, 2))  # one pair
    else:
        return (0, values)  # high card

def get_key_by_value(d, target):
    for k, v in d.items():
        if v == target:
            return k

def get_highest_pair(d):
    pairs = [k for k, v in d.items() if v == 2]
    return max(pairs)

def compare_hands(player_score, comp_score):
    if player_score > comp_score:
        return "You win!"
    elif player_score < comp_score:
        return "Computer wins!"
    else:
        return "It's a tie!"

def poker_game():
    print("♠ Text-Based Poker: Player vs Computer ♠")
    deck = make_deck()
    random.shuffle(deck)

    player_hand = deal_hand(deck)
    comp_hand = deal_hand(deck)

    print("\nYour hand:")
    print(show_hand(player_hand))

    input("\nPress Enter to reveal computer's hand...")

    print("\nComputer's hand:")
    print(show_hand(comp_hand))

    # evaluate hands
    player_score = evaluate_hand(player_hand)
    comp_score = evaluate_hand(comp_hand)

    print("\nResult:")
    print(compare_hands(player_score, comp_score))

poker_game()

