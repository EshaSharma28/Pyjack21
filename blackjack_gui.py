import tkinter as tk
from tkinter import messagebox
import random

# ----------------------------
# GAME LOGIC
# ----------------------------
balance = 100
bet = 0

suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
ranks = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

def create_deck():
    deck = [(rank, suit) for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

def deal_card(deck):
    return deck.pop()

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

def format_card(card):
    rank, suit = card
    suit_symbols = {
        'Hearts': '♥',
        'Diamonds': '♦',
        'Clubs': '♣',
        'Spades': '♠'
    }
    return f"{rank}{suit_symbols[suit]}"

# ----------------------------
# GUI SETUP
# ----------------------------

root = tk.Tk()
root.title("Blackjack Game 🃏")
root.geometry("800x600")
root.configure(bg="darkgreen")

# Fonts
TITLE_FONT = ("Helvetica", 24, "bold")
CARD_FONT = ("Helvetica", 16)

# Title
title_label = tk.Label(root, text="🃏 Blackjack", font=TITLE_FONT, bg="darkgreen", fg="white")
title_label.pack(pady=20)

balance_label = tk.Label(root, text=f"Balance: ${balance}", font=CARD_FONT, bg="darkgreen", fg="white")
balance_label.pack()

bet_entry_label = tk.Label(root, text="Enter your bet:", font=CARD_FONT, bg="darkgreen", fg="white")
bet_entry_label.pack()

bet_entry = tk.Entry(root, font=CARD_FONT, width=10)
bet_entry.pack()

# Player frame
player_frame = tk.Frame(root, bg="darkgreen")
player_frame.pack(pady=10)

player_label = tk.Label(player_frame, text="Your Hand:", font=CARD_FONT, bg="darkgreen", fg="white")
player_label.pack()

player_cards = tk.Label(player_frame, text="", font=("Helvetica", 32), bg="darkgreen", fg="white")
player_cards.pack()

# Dealer frame
dealer_frame = tk.Frame(root, bg="darkgreen")
dealer_frame.pack(pady=10)

dealer_label = tk.Label(dealer_frame, text="Dealer's Hand:", font=CARD_FONT, bg="darkgreen", fg="white")
dealer_label.pack()

dealer_cards = tk.Label(dealer_frame, text="", font=("Helvetica", 32), bg="darkgreen", fg="white")
dealer_cards.pack()

# Button frame
button_frame = tk.Frame(root, bg="darkgreen")
button_frame.pack(pady=20)

# ----------------------------
# GAME STATE VARIABLES
# ----------------------------

deck = []
player_hand = []
dealer_hand = []

# ----------------------------
# GAME FUNCTIONS
# ----------------------------
def start_game():
    global bet, balance, deck, player_hand, dealer_hand

    try:
        bet = int(bet_entry.get())
        if bet <= 0 or bet > balance:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Invalid Bet", f"Enter a number between 1 and {balance}")
        return

    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    update_cards()
    hit_button.config(state=tk.NORMAL)
    stand_button.config(state=tk.NORMAL)
    start_button.config(state=tk.DISABLED)
    bet_entry.config(state=tk.DISABLED)

def update_cards():
    player_text = "  ".join(format_card(c) for c in player_hand)
    dealer_text = format_card(dealer_hand[0]) + "  🂠"
    player_cards.config(text=player_text)
    dealer_cards.config(text=dealer_text)

def disable_buttons():
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)

def enable_buttons():
    hit_button.config(state=tk.NORMAL)
    stand_button.config(state=tk.NORMAL)

def new_game():
    global deck, player_hand, dealer_hand
    deck = create_deck()
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    update_cards()
    enable_buttons()

def play_again():
    bet_entry.config(state=tk.NORMAL)
    bet_entry.delete(0, tk.END)
    start_button.config(state=tk.NORMAL)
    play_again_button.config(state=tk.DISABLED)
    player_cards.config(text="🂠 🂠")
    dealer_cards.config(text="🂠 🂠")

def hit():
    player_hand.append(deal_card(deck))
    update_cards()
    total = calculate_hand_value(player_hand)
    if total > 21:
        messagebox.showinfo("Busted!", "💥 You busted!")
        disable_buttons()
        balance -= bet
        balance_label.config(text=f"Balance: ${balance}")
        play_again_button.config(state=tk.NORMAL)


def stand():
    dealer_cards.config(text="  ".join(format_card(c) for c in dealer_hand))
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
        dealer_cards.config(text="  ".join(format_card(c) for c in dealer_hand))
        root.update()

    player_total = calculate_hand_value(player_hand)
    dealer_total = calculate_hand_value(dealer_hand)
    global balance
    if dealer_total > 21 or player_total > dealer_total:
        messagebox.showinfo("Result", "🎉 You win!")
        balance += bet
    elif dealer_total > player_total:
        messagebox.showinfo("Result", "😞 Dealer wins!")
        balance -= bet
    else:
        messagebox.showinfo("Result", "🤝 It's a tie!")

    balance_label.config(text=f"Balance: ${balance}")
    play_again_button.config(state=tk.NORMAL)
    
    disable_buttons()

# ----------------------------
# BUTTONS
# ----------------------------

hit_button = tk.Button(button_frame, text="Hit", font=CARD_FONT, width=10, command=hit)
hit_button.grid(row=0, column=0, padx=10)

stand_button = tk.Button(button_frame, text="Stand", font=CARD_FONT, width=10, command=stand)
stand_button.grid(row=0, column=1, padx=10)

restart_button = tk.Button(button_frame, text="New Game", font=CARD_FONT, width=10, command=new_game)
restart_button.grid(row=0, column=2, padx=10)

start_button = tk.Button(root, text="Start Game", font=CARD_FONT, command=start_game)
start_button.pack(pady=10)

play_again_button = tk.Button(root, text="Play Again", font=CARD_FONT, command=play_again, state=tk.DISABLED)
play_again_button.pack(pady=10)


# Start first game
new_game()

# Run GUI loop
root.mainloop()
