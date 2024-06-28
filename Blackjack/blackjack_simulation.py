import random


def simulate_blackjack(num_simulations):
    def draw_card(deck):
        """Draw a card from the deck."""
        if not deck:
            deck.extend(reshuffled_deck)
            random.shuffle(deck)
        return deck.pop()

    reshuffled_deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 24
    random.shuffle(reshuffled_deck)

    results = []

    player_results = {
        'bust': 0, '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, 'blackjack': 0
    }
    dealer_results = {
        '17': 0, '18': 0, '19': 0, '20': 0, '21': 0, 'blackjack': 0
    }

    player_wins = 0
    dealer_wins = 0

    for _ in range(num_simulations):
        deck = reshuffled_deck.copy()
        random.shuffle(deck)

        player_hand = []
        while sum(player_hand) < 17:
            player_hand.append(draw_card(deck))
            if sum(player_hand) > 21 and 11 in player_hand:
                player_hand[player_hand.index(11)] = 1  # Convert ace from 11 to 1

        player_final = sum(player_hand)
        if player_final > 21:
            player_results['bust'] += 1
        elif player_final == 21 and len(player_hand) == 2:
            player_results['blackjack'] += 1
        elif player_final == 21:
            player_results['21'] += 1
        elif player_final == 20:
            player_results['20'] += 1
        elif player_final == 19:
            player_results['19'] += 1
        elif player_final == 18:
            player_results['18'] += 1
        elif player_final == 17:
            player_results['17'] += 1

        dealer_hand = []
        while sum(dealer_hand) < 17:
            dealer_hand.append(draw_card(deck))
            if sum(dealer_hand) > 21 and 11 in dealer_hand:
                dealer_hand[dealer_hand.index(11)] = 1  # Convert ace from 11 to 1

        dealer_final = sum(dealer_hand)
        if dealer_final == 21 and len(dealer_hand) == 2:
            dealer_results['blackjack'] += 1
        elif dealer_final == 21:
            dealer_results['21'] += 1
        elif dealer_final == 20:
            dealer_results['20'] += 1
        elif dealer_final == 19:
            dealer_results['19'] += 1
        elif dealer_final == 18:
            dealer_results['18'] += 1
        elif dealer_final == 17:
            dealer_results['17'] += 1

        if player_final > 21:
            dealer_wins += 1
        elif dealer_final > 21:
            player_wins += 1
        elif player_final > dealer_final:
            player_wins += 1
        elif dealer_final > player_final:
            dealer_wins += 1

    return player_results, dealer_results, player_wins, dealer_wins


def main():
    simulation_counts = [1000, 10000, 100000, 1000000]
    print("Choose the number of simulations:")
    for i, count in enumerate(simulation_counts, 1):
        print(f"{i}. {count}")

    choice = int(input("Enter your choice (1-4): "))
    if choice not in range(1, 5):
        print("Invalid choice.")
        return

    num_simulations = simulation_counts[choice - 1]
    player_results, dealer_results, player_wins, dealer_wins = simulate_blackjack(num_simulations)

    print(f"\nOut of {num_simulations} simulations:")
    print("Player results:")
    print(f"  Busted: {player_results['bust']} times")
    print(f"  Had 17: {player_results['17']} times")
    print(f"  Had 18: {player_results['18']} times")
    print(f"  Had 19: {player_results['19']} times")
    print(f"  Had 20: {player_results['20']} times")
    print(f"  Had 21: {player_results['21']} times")
    print(f"  Had blackjack: {player_results['blackjack']} times")

    print("\nDealer results:")
    print(f"  Had 17: {dealer_results['17']} times")
    print(f"  Had 18: {dealer_results['18']} times")
    print(f"  Had 19: {dealer_results['19']} times")
    print(f"  Had 20: {dealer_results['20']} times")
    print(f"  Had 21: {dealer_results['21']} times")
    print(f"  Had blackjack: {dealer_results['blackjack']} times")

    print("\nTotal wins:")
    print(f"  Player: {player_wins}")
    print(f"  Dealer: {dealer_wins}")


if __name__ == "__main__":
    main()
