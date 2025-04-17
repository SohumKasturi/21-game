#game imports
import random
import time

class Card:
    # Represents a playing card with suit and rank
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def __repr__(self):
        return self.__str__()

    def value(self):
        # Return card's numerical value for Blackjack scoring
        if self.rank in ["Jack", "Queen", "King"]:
            return 10
        elif self.rank == "Ace":
            return 11  # Will be adjusted to 1 if needed
        return int(self.rank)

# Game constants and state
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]

deck = []
player_hand = []
dealer_hand = []

# Score tracking variables
player_score = 0
dealer_score = 0
ties = 0

def calc_value(hand):
    # Calculate hand value, handling Aces as 1 or 11
    total = 0
    aces = 0
    for card in hand:
        card_val = card.value()
        total += card_val
        if card.rank == "Ace":
            aces += 1
    while total > 21 and aces > 0:
        total -= 10
        aces -= 1
    return total

def create_deck():
    full_deck = []
    for suit in suits:
        for rank in ranks:
            full_deck.append(Card(suit, rank))
    return full_deck

def shuffle_deck():
    global deck
    deck = create_deck()
    random.shuffle(deck)

def reshuffle_check():
    # Reshuffle deck when running low on cards
    if len(deck) < 15:
        print("\nDeck running low... Reshuffling.")
        time.sleep(1)
        shuffle_deck()

def deal_initial_cards():
    # Deal starting hands to player and dealer
    reshuffle_check()
    player_hand.clear()
    dealer_hand.clear()
    player_hand.extend([deck.pop(0), deck.pop(0)])
    dealer_hand.extend([deck.pop(0), deck.pop(0)])

def show_hands(hide_dealer=True):
    # Display current hands, optionally hiding dealer's second card
    print("\n--- HANDS ---")
    print("\nYour hand:")
    for card in player_hand:
        print(card)
    print(f"Your hand value: {calc_value(player_hand)}")
    
    print("\nDealer's hand:")
    if hide_dealer:
        print(dealer_hand[0], "HIDDEN")
    else:
        for card in dealer_hand:
            print(card)
        print(f"Dealer's hand value: {calc_value(dealer_hand)}")
    print("-" * 20)

def player_hit():
    reshuffle_check()
    card = deck.pop(0)
    player_hand.append(card)
    value = calc_value(player_hand)
    print(f"\nYou drew: {card}")
    print(f"Your hand value: {value}")
    return value

def dealer_play():
    # Execute dealer's turn - must hit on 16 or below, stand on 17+
    print("\n--- Dealer's Turn ---")
    time.sleep(1)
    show_hands(hide_dealer=False)
    time.sleep(1)
    while calc_value(dealer_hand) < 17:
        print("Dealer hits.")
        time.sleep(1)
        reshuffle_check()
        card = deck.pop(0)
        dealer_hand.append(card)
        print(f"Dealer drew: {card}")
        print(f"Dealer's hand value: {calc_value(dealer_hand)}")
        time.sleep(1)

def final_results():
    global player_score, dealer_score, ties
    print("\n--- FINAL RESULTS ---")
    player_val = calc_value(player_hand)
    dealer_val = calc_value(dealer_hand)
    print(f"Your final value: {player_val}")
    print(f"Dealer's final value: {dealer_val}")
    if player_val > dealer_val:
        print("You win!")
        player_score += 1
    elif dealer_val > player_val:
        print("Dealer wins!")
        dealer_score += 1
    else:
        print("It's a push (tie).")
        ties += 1

def play_game():
    # Main game loop for a single round
    global player_score, dealer_score, ties
    deal_initial_cards()
    player_val = calc_value(player_hand)
    dealer_val = calc_value(dealer_hand)
    show_hands()
    
    # Handle initial Blackjacks
    if player_val == 21:
        if dealer_val == 21:
            print("Both have Blackjack! Push.")
            ties += 1
        else:
            print("Blackjack! You win!")
            player_score += 1
        return
    if dealer_val == 21:
        print("Dealer has Blackjack! You lose.")
        dealer_score += 1
        return
    
    # Player's turn
    while True:
        choice = input("\nHit or Stand? (h/s): ").lower()
        if choice == "h":
            player_val = player_hit()
            if player_val > 21:
                print("Bust! You lose.")
                dealer_score += 1
                return
            elif player_val == 21:
                print("You have 21! Standing automatically.")
                break
        elif choice == "s":
            print("You stand.")
            break
        else:
            print("Invalid choice, try again.")
    
    # Dealer's turn and final scoring
    dealer_play()
    if calc_value(dealer_hand) > 21:
        print("Dealer busts! You win!")
        player_score += 1
    else:
        final_results()

def show_scoreboard():
    print("\n=== SCOREBOARD ===")
    print(f"Player Wins: {player_score}")
    print(f"Dealer Wins: {dealer_score}")
    print(f"Ties:        {ties}")
    print("==================")

# Game initialization and main menu
shuffle_deck()
while True:
    print("\n=====================")
    print(" Welcome to Blackjack!")
    print("=====================")
    print("1. Play")
    print("2. Show Scoreboard")
    print("3. Quit")
    choice = input("Enter your choice: ")
    
    if choice == "1":
        play_game()
        input("\nPress Enter to return to menu...")
    elif choice == "2":
        show_scoreboard()
        input("\nPress Enter to return to menu...")
    elif choice == "3":
        print("Goodbye!")
        break
    else:
        print("Invalid choice, try again.")
