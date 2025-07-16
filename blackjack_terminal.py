import random

# Card setup
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Create deck
def create_deck():
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

# Deal one card
def deal_card(deck):
    return deck.pop()

# Calculate hand total
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for rank, _ in hand:
        value += ranks[rank]
        if rank == 'A':
            aces += 1
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# MAIN GAME LOOP
balance = 100  # Starting money

print("🎰 Welcome to Blackjack!\n")

while balance > 0:
    print(f"\n💵 Current balance: {balance}")
    
    # Ask for bet
    while True:
        try:
            bet = int(input("Enter your bet amount: "))
            if 0 < bet <= balance:
                break
            else:
                print("❗Invalid bet. Must be between 1 and your balance.")
        except ValueError:
            print("❗Please enter a valid number.")

    # Setup hands
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    print("\n🃏 Your hand:", player_hand, "→ Total:", calculate_hand_value(player_hand))
    print("🤖 Dealer's hand: [", dealer_hand[0], ", ('?', '?') ]")

    # Player turn
    while True:
        choice = input("Do you want to Hit or Stand? (h/s): ").lower()
        if choice == 'h':
            card = deal_card(deck)
            player_hand.append(card)
            total = calculate_hand_value(player_hand)
            print("You drew:", card)
            print("Your hand:", player_hand, "→ Total:", total)
            if total > 21:
                print("💥 You busted! You lose.")
                balance -= bet
                break
        elif choice == 's':
            print("You chose to stand.")
            break
        else:
            print("❗Invalid choice. Type 'h' or 's'.")

    # If player didn't bust, dealer plays
    if calculate_hand_value(player_hand) <= 21:
        print("\n🔍 Dealer's turn...")
        print("Dealer's hand:", dealer_hand, "→ Total:", calculate_hand_value(dealer_hand))
        
        while calculate_hand_value(dealer_hand) < 17:
            card = deal_card(deck)
            dealer_hand.append(card)
            print("Dealer draws:", card)
            print("Dealer's hand:", dealer_hand, "→ Total:", calculate_hand_value(dealer_hand))
        
        dealer_total = calculate_hand_value(dealer_hand)
        player_total = calculate_hand_value(player_hand)

        print("\n🧮 Final Results:")
        print("Your total:", player_total)
        print("Dealer's total:", dealer_total)

        if dealer_total > 21:
            print("🎉 Dealer busted! You win!")
            balance += bet
        elif dealer_total < player_total:
            print("🎉 You win!")
            balance += bet
        elif dealer_total > player_total:
            print("😞 Dealer wins!")
            balance -= bet
        else:
            print("🤝 It's a tie (Push). No chips lost.")

    # Ask to play again
    if balance > 0:
        again = input("\n🔁 Do you want to play again? (y/n): ").lower()
        if again != 'y':
            print("👋 Thanks for playing! Final balance:", balance)
            break
    else:
        print("💸 You're out of money! Game over.")
