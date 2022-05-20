# Import GUI
import tkinter
import random
from PIL import Image, ImageTk
from tkinter import messagebox
# Create a Window
window = tkinter.Tk()
window.title("Black Jack")
# Center window on pc screen
app_width = 1000
app_height = 500
# Get size of screen
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
# Calculate middle of screen
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
# Adjust size of window based on dimensions of pc screen
window.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
# Set Background color
window.configure(background="green")
# Stand option
def stand():
    global player_total, dealer_total, player_points
    player_total = 0
    dealer_total = 0

    for score in dealer_points:
        dealer_total += score

    for score in player_points:
        player_total += score
    # Disable buttons
    card_button.config(state="disabled")
    stand_button.config(state="disabled")

    if dealer_total >= 17:
        if dealer_total > 21:
            # Check for a bust
            messagebox.showinfo("Player won!", f"You won! Dealer: {dealer_total} Player: {player_total}")
        elif dealer_total == player_total:
            # Tie
            messagebox.showinfo("Tie!", f"It's a tie! Dealer: {dealer_total} Player: {player_total}")
        elif dealer_total > player_total:
            # Dealer won
            messagebox.showinfo("Dealer won!", f"Dealer won! Dealer: {dealer_total} Player: {player_total}")
        else:
            # Player won
            messagebox.showinfo("Player won!", f"You won! Dealer: {dealer_total} Player: {player_total}")
    else:
        # Add card to dealer / recalculate
        dealer_hit()
        stand()
# Check for black jack on shuffle
def is_blackjack(player):
    global player_total, dealer_total
    # Keep track of totals
    player_total = 0
    dealer_total = 0
    if player == "dealer":
        if len(dealer_points) == 2:
            if dealer_points[0] + dealer_points[1] == 21:
                # Update status of black jack
                blackjack_status["dealer"] = "yes"
    if player == "player":
        if len(player_points) == 2:
            if player_points[0] + player_points[1] == 21:
                # Update status of black jack
                blackjack_status["player"] = "yes"
        else:
            for score in player_points:
                player_total += score
                if player_total == 21:
                    blackjack_status["player"] = "yes"
                elif player_total > 21:
                    # Check for Ace value
                    for card_num, card in enumerate(player_points):
                        if card == 11:
                            player_points[card_num] = 1
                            # Clear player total & Re calculate
                            player_total = 0
                            for score in player_points:
                                player_total += score
                            if player_total > 21:
                                blackjack_status["player"] = "bust"
                    else:
                        if player_total == 21:
                            blackjack_status["player"] = "yes"
                        if player_total > 21:
                            blackjack_status["player"] = "bust"
                    blackjack_status["player"] = "bust"
    # Check for Push / Tie
    if len(dealer_points) == 2 and len(player_points) == 2:
        if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":
            # Tie
            messagebox.showinfo("Push!", "It's a tie!")
            card_button.config(state="disabled")
            stand_button.config(state="disabled")
        # Check if dealer won
        elif blackjack_status["dealer"] == "yes":
            messagebox.showinfo("Dealer Wins!", "Blackjack for dealer!")
            # Disable Buttons
            card_button.config(state="disabled")
            stand_button.config(state="disabled")
        # Check if you won
        elif blackjack_status["player"] == "yes":
            messagebox.showinfo("You Won!", "Blackjack! Congratulations!")
            # Disable Buttons
            card_button.config(state="disabled")
            stand_button.config(state="disabled")
    # Check for 21 during game
    else:
        if blackjack_status["dealer"] == "yes" and blackjack_status["player"] == "yes":
            # Tie
            messagebox.showinfo("Push!", "It's a tie!")
            card_button.config(state="disabled")
            stand_button.config(state="disabled")
        # Check if dealer won
        elif blackjack_status["dealer"] == "yes":
            messagebox.showinfo("Dealer Wins!", "21 for dealer!")
            # Disable Buttons
            card_button.config(state="disabled")
            stand_button.config(state="disabled")
        # Check if you won
        elif blackjack_status["player"] == "yes":
            messagebox.showinfo("You Won!", "21! Congratulations!")
            # Disable Buttons
            card_button.config(state="disabled")
            stand_button.config(state="disabled")
    if blackjack_status["player"] == "bust":
        messagebox.showinfo("You Busted!", f"Player lost! {player_total}")
        # Disable Buttons
        card_button.config(state="disabled")
        stand_button.config(state="disabled")
# Resize Cards
def resize_cards(card):
    # Open image
    our_card_img = Image.open(card)
    # Resize Image
    our_card_resize_img = our_card_img.resize((150, 218))
    # Output the card
    global our_card_image
    our_card_image = ImageTk.PhotoImage(our_card_resize_img)
    # Return the card
    return our_card_image
# Shuffle the Cards
def shuffle():
    # Keep track of winning
    global blackjack_status, player_total, dealer_total
    player_total = 0
    dealer_total = 0
    blackjack_status = {"dealer": "no", "player": "no"}
    # Re-enable buttons
    card_button.config(state="normal")
    stand_button.config(state="normal")
    # Clear Cards from previous games
    dealer_label_1.config(image="")
    dealer_label_2.config(image="")
    dealer_label_3.config(image="")
    dealer_label_4.config(image="")
    dealer_label_5.config(image="")

    player_label_1.config(image="")
    player_label_2.config(image="")
    player_label_3.config(image="")
    player_label_4.config(image="")
    player_label_5.config(image="")

    suits = ["diamonds", "clubs", "spades", "hearts"]
    values = range(2, 15)
    # 14 = Ace / 13 = King / 12 = Queen / 11 = Jack
    global deck
    deck = []
    for suit in suits:
        for value in values:
            deck.append(f'{value}_of_{suit}')
    # Create Players
    global dealer, player, dealer_spot, player_spot, player_points, dealer_points
    dealer = []
    player = []
    player_points = []
    dealer_points = []
    dealer_spot = 0
    player_spot = 0

    # Get 2 cards for player and dealer
    dealer_hit()
    dealer_hit()
    player_hit()
    player_hit()

def dealer_hit():
    global dealer_spot, player_total, dealer_total, dealer_points
    if dealer_spot <= 5:
        try:
            # Get the player card
            dealer_card = random.choice(deck)
            # Remove card from deck
            deck.remove(dealer_card)
            # Add to player list
            dealer.append(dealer_card)
            # Add to dealer score list
            dcard = int(dealer_card.split("_", 1)[0])
            if dcard == 14:
                dealer_points.append(11)
            elif dcard == 11 or dcard == 12 or dcard == 13:
                dealer_points.append(10)
            else:
                dealer_points.append(dcard)
            # Output to screen
            global dealer_img1, dealer_img2, dealer_img3, dealer_img4, dealer_img5

            if dealer_spot == 0:
                # Resize Card
                dealer_img1 = resize_cards(f'cards/{dealer_card}.png')
                # Output Card
                dealer_label_1.config(image=dealer_img1)
                # Increment player spot counter
                dealer_spot += 1
            elif dealer_spot == 1:
                # Resize Card
                dealer_img2 = resize_cards(f'cards/{dealer_card}.png')
                # Output Card
                dealer_label_2.config(image=dealer_img2)
                # Increment player spot counter
                dealer_spot += 1
            elif dealer_spot == 2:
                # Resize Card
                dealer_img3 = resize_cards(f'cards/{dealer_card}.png')
                # Output Card
                dealer_label_3.config(image=dealer_img3)
                # Increment player spot counter
                dealer_spot += 1
            elif dealer_spot == 3:
                # Resize Card
                dealer_img4 = resize_cards(f'cards/{dealer_card}.png')
                # Output Card
                dealer_label_4.config(image=dealer_img4)
                # Increment player spot counter
                dealer_spot += 1
            elif dealer_spot == 4:
                # Resize Card
                dealer_img5 = resize_cards(f'cards/{dealer_card}.png')
                # Output Card
                dealer_label_5.config(image=dealer_img5)
                # Increment player spot counter
                dealer_spot += 1
                # See if 5 card bust
                player_total = 0
                dealer_total = 0
                # Get player score
                for score in player_points:
                    player_total += score

                # Get dealer score
                for score in dealer_points:
                    dealer_total += score
                # Check if  <= 21
                if dealer_total <= 21:
                    # Dealer won
                    card_button.config(state="disabled")
                    stand_button.config(state="disabled")
                    messagebox.showinfo("Dealer won!", f"Dealer won! Dealer: {dealer_total} Player: {player_total}")
        except:
            window.title(f'No more cards in deck')
        # Check for black jack
        is_blackjack("dealer")
def player_hit():
    global player_spot, player_total, dealer_total, player_points
    if player_spot <= 5:
        try:
            # Get the player card
            player_card = random.choice(deck)
            # Remove card from deck
            deck.remove(player_card)
            # Add to player list
            player.append(player_card)
            pcard = int(player_card.split("_", 1)[0])
            if pcard == 14:
                player_points.append(11)
            elif pcard == 11 or pcard == 12 or pcard == 13:
                player_points.append(10)
            else:
                player_points.append(pcard)
            # Output to screen
            global player_img1, player_img2, player_img3, player_img4, player_img5

            if player_spot == 0:
                # Resize Card
                player_img1 = resize_cards(f'cards/{player_card}.png')
                # Output Card
                player_label_1.config(image=player_img1)
                # Increment player spot counter
                player_spot += 1
            elif player_spot == 1:
                # Resize Card
                player_img2 = resize_cards(f'cards/{player_card}.png')
                # Output Card
                player_label_2.config(image=player_img2)
                # Increment player spot counter
                player_spot += 1
            elif player_spot == 2:
                # Resize Card
                player_img3 = resize_cards(f'cards/{player_card}.png')
                # Output Card
                player_label_3.config(image=player_img3)
                # Increment player spot counter
                player_spot += 1
            elif player_spot == 3:
                # Resize Card
                player_img4 = resize_cards(f'cards/{player_card}.png')
                # Output Card
                player_label_4.config(image=player_img4)
                # Increment player spot counter
                player_spot += 1
            elif player_spot == 4:
                # Resize Card
                player_img5 = resize_cards(f'cards/{player_card}.png')
                # Output Card
                player_label_5.config(image=player_img5)
                # Increment player spot counter
                player_spot += 1

                # See if 5 card bust
                player_total = 0
                dealer_total = 0
                # Get player score
                for score in player_points:
                    player_total += score

                # Get dealer score
                for score in dealer_points:
                    dealer_total += score
                # Check if  <= 21
                if player_total <= 21:
                    # Player won
                    card_button.config(state="disabled")
                    stand_button.config(state="disabled")
                    messagebox.showinfo("Player won!", f"Player won! Dealer: {dealer_total} Player: {player_total}")
        except:
            window.title(f'No more cards in deck')
        # Check for black jack
        is_blackjack("player")

""" Start of Game Code """
# Create Frames for Cards
my_frame = tkinter.Frame(window, bg="green")
my_frame.pack(pady=20)
dealer_frame = tkinter.LabelFrame(my_frame, text="Dealer", bd=0)
dealer_frame.pack(padx=20, ipadx=20)
player_frame = tkinter.LabelFrame(my_frame, text="Player", bd=0)
player_frame.pack(ipadx=20, pady=10)
# Put Dealer Cards in Frames
dealer_label_1 = tkinter.Label(dealer_frame, text="")
dealer_label_1.grid(row=0, column=0, pady=20, padx=20)

dealer_label_2 = tkinter.Label(dealer_frame, text="")
dealer_label_2.grid(row=0, column=1, pady=20, padx=20)

dealer_label_3 = tkinter.Label(dealer_frame, text="")
dealer_label_3.grid(row=0, column=2, pady=20, padx=20)

dealer_label_4 = tkinter.Label(dealer_frame, text="")
dealer_label_4.grid(row=0, column=3, pady=20, padx=20)

dealer_label_5 = tkinter.Label(dealer_frame, text="")
dealer_label_5.grid(row=0, column=4, pady=20, padx=20)
# Put Player Cards in Frames
player_label_1 = tkinter.Label(player_frame, text="")
player_label_1.grid(row=1, column=0, pady=20, padx=20)

player_label_2 = tkinter.Label(player_frame, text="")
player_label_2.grid(row=1, column=1, pady=20, padx=20)

player_label_3 = tkinter.Label(player_frame, text="")
player_label_3.grid(row=1, column=2, pady=20, padx=20)

player_label_4 = tkinter.Label(player_frame, text="")
player_label_4.grid(row=1, column=3, pady=20, padx=20)

player_label_5 = tkinter.Label(player_frame, text="")
player_label_5.grid(row=1, column=4, pady=20, padx=20)
# Create Button Frame
button_frame = tkinter.Frame(window, bg="green")
button_frame.pack(pady=20)
# Create Buttons
# Shuffle Cards Button
shuffle_button = tkinter.Button(button_frame, text="Shuffle Deck", font=("Helvetica", 14), command=shuffle)
shuffle_button.grid(row=0, column=0)
# Hit Button
card_button = tkinter.Button(button_frame, text="Hit", font=("Helvetica", 14), command=player_hit)
card_button.grid(row=0, column=1, padx=10)
# Stand Button
stand_button = tkinter.Button(button_frame, text="Stand", font=("Helvetica", 14), command=stand)
stand_button.grid(row=0, column=2)
""" End of Game Code """
shuffle()
""" Menu Creation """
# Create a dropdown menu
menu = tkinter.Menu(window)
dropdown_item = tkinter.Menu(menu)
dropdown_item.add_command(label="New")
menu.add_cascade(label="File", menu=dropdown_item)
window.config(menu=menu)
# Run (Put last)
window.mainloop()
