import random
from Hand import Hand  # Import the Hand class for evaluating hands
import numpy as np

class Draw:
    def __init__(self):
        self.suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
        self.full_deck = [(rank, suit) for suit in self.suits for rank in self.ranks]  # List of tuples for cards

    def draw_hand(self, hand_size=6):
        # Use numpy for efficient random sampling of 6 unique cards from the full deck
        cards = random.sample(self.full_deck, hand_size)
        return Hand(cards)  # Pass the drawn cards to Hand for evaluation
