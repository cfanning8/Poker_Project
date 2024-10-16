from collections import Counter

class Hand:
    def __init__(self, cards):
        self.cards = cards
        self.ranks = [card[0] for card in cards]  # Extract ranks from the cards
        self.suits = [card[1] for card in cards]  # Extract suits from the cards
        self.rank_counts = Counter(self.ranks)    # Count occurrences of each rank
        self.hand_type = self.evaluate_hand()     # Evaluate and label the hand

    def __repr__(self):
        return self.hand_type

    def evaluate_hand(self):
        # Method to evaluate the hand and return the highest-ranked type
        if self.is_long_royal_flush():
            return "Long Royal Flush"
        elif self.is_long_straight_flush():
            return "Long Straight Flush"
        elif self.is_short_royal_flush():
            return "Short Royal Flush"
        elif self.is_full_hotel():
            return "Full Hotel"
        elif self.is_two_triples():
            return "Two Triples"
        elif self.is_short_straight_flush():
            return "Short Straight Flush"
        elif self.is_long_flush():
            return "Long Flush"
        elif self.is_short_flush():
            return "Short Flush"
        elif self.is_four_of_a_kind():
            return "Four of a Kind"
        elif self.is_long_straight():
            return "Long Straight"
        elif self.is_three_pair():
            return "Three Pair"
        elif self.is_full_house():
            return "Full House"
        elif self.is_short_straight():
            return "Short Straight"
        elif self.is_three_of_a_kind():
            return "Three of a Kind"
        elif self.is_two_pair():
            return "Two Pair"
        elif self.is_one_pair():
            return "One Pair"
        else:
            return "High Card"  # Default if no other hand type matches

    # Helper methods for hand evaluations

    def is_flush(self, size):
        # Check if there's a flush with exactly `size` cards using Counter for suits
        suit_counts = Counter(self.suits)
        return any(count >= size for count in suit_counts.values())

    def is_straight(self, size):
        # Map rank strings to their values
        rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                    'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

        # Convert ranks to their numeric values
        rank_values = sorted(set(rank_map[rank] for rank in self.ranks), reverse=True)

        # Check if there is a straight of `size` cards
        for i in range(len(rank_values) - size + 1):
            if all(rank_values[i] - rank_values[i + j] == j for j in range(size)):
                return True
        return False

    def is_royal(self, size):
        # Check if the hand is a Royal Flush (9 to Ace for size 6, 10 to Ace for size 5)
        royal_ranks = ['9', '10', 'Jack', 'Queen', 'King', 'Ace'] if size == 6 else ['10', 'Jack', 'Queen', 'King', 'Ace']
        return set(royal_ranks).issubset(self.ranks)

    def is_long_royal_flush(self):
        return self.is_flush(6) and self.is_royal(6)

    def is_short_royal_flush(self):
        return self.is_flush(5) and self.is_royal(5)

    def is_long_straight_flush(self):
        return self.is_flush(6) and self.is_straight(6)

    def is_short_straight_flush(self):
        return self.is_flush(5) and self.is_straight(5)

    def is_long_flush(self):
        return self.is_flush(6)

    def is_short_flush(self):
        return self.is_flush(5)

    def is_full_hotel(self):
        # Full Hotel: Four of a kind and a pair
        return list(self.rank_counts.values()).count(4) == 1 and list(self.rank_counts.values()).count(2) == 1

    def is_two_triples(self):
        # Two Triples: Two distinct three-of-a-kinds
        return list(self.rank_counts.values()).count(3) == 2

    def is_four_of_a_kind(self):
        return 4 in self.rank_counts.values()

    def is_long_straight(self):
        return self.is_straight(6)

    def is_three_pair(self):
        return list(self.rank_counts.values()).count(2) == 3

    def is_full_house(self):
        return 3 in self.rank_counts.values() and 2 in self.rank_counts.values()

    def is_short_straight(self):
        return self.is_straight(5)

    def is_three_of_a_kind(self):
        return 3 in self.rank_counts.values()

    def is_two_pair(self):
        return list(self.rank_counts.values()).count(2) == 2

    def is_one_pair(self):
        return list(self.rank_counts.values()).count(2) == 1
