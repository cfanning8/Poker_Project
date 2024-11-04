import itertools
from collections import Counter
from multiprocessing import Pool
from tqdm import tqdm

def generate_all_hands(hand_size=6):
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [(rank, suit) for suit in suits for rank in ranks]
    return itertools.combinations(deck, hand_size)

def get_rank_values(ranks):
    rank_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}
    rank_values = [rank_map[rank] for rank in ranks]
    # Handle Ace as both high and low
    if 14 in rank_values:
        rank_values.append(1)
    return sorted(set(rank_values))

def has_consecutive_ranks(rank_values, size):
    rank_values = sorted(set(rank_values))
    for i in range(len(rank_values)):
        consecutive = 1
        for j in range(i+1, len(rank_values)):
            if rank_values[j] == rank_values[j-1] + 1:
                consecutive += 1
                if consecutive >= size:
                    return True
            else:
                break
    return False

def classify_hand(hand):
    ranks = [card[0] for card in hand]
    suits = [card[1] for card in hand]
    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)
    rank_values = get_rank_values(ranks)

    labels = []  # Append all hand types to this

    # Checks for flushes
    for suit in suit_counts:
        suited_cards = [card for card in hand if card[1] == suit]
        suited_ranks = [card[0] for card in suited_cards]
        suited_rank_values = get_rank_values(suited_ranks)

        # Short Royal Flush
        if set(['10', 'Jack', 'Queen', 'King', 'Ace']).issubset(suited_ranks):
            labels.append("Short Royal Flush")

        # Long Royal Flush
        if set(['9', '10', 'Jack', 'Queen', 'King', 'Ace']).issubset(suited_ranks):
            labels.append("Long Royal Flush")

        if len(suited_cards) >= 6:
            labels.append("Long Flush")
            labels.append("Short Flush")  # Long Flush is also a Short Flush
        elif len(suited_cards) >= 5:
            labels.append("Short Flush")

        # Straight Flush checks
        if has_consecutive_ranks(suited_rank_values, 5):
            labels.append("Short Straight Flush")
        if has_consecutive_ranks(suited_rank_values, 6):
            labels.append("Long Straight Flush")
            labels.append("Short Straight Flush")  # Including Short Straight Flush

    # Straights:
    if has_consecutive_ranks(rank_values, 5):
        labels.append("Short Straight")
    if has_consecutive_ranks(rank_values, 6):
        labels.append("Long Straight")
        labels.append("Short Straight")  # Long Straight includes a Short Straight

    # Four of a Kind
    if any(count >= 4 for count in rank_counts.values()):
        labels.append("Four of a Kind")
        labels.append("Three of a Kind")  # Four of a Kind includes Three of a Kind
        labels.append("One Pair")         # Four of a Kind includes One Pair
        labels.append("Two Pair")         # Four of a Kind includes Two Pairs (sort of)

    # Triplets and Pairs
    triplet_ranks = [rank for rank, count in rank_counts.items() if count >= 3]
    pair_ranks = [rank for rank, count in rank_counts.items() if count >= 2]
    num_pairs = len(pair_ranks)

    # Full House
    # at least one triplet and one pair of different ranks
    full_house = False
    for triplet_rank in triplet_ranks:
        for pair_rank in pair_ranks:
            if pair_rank != triplet_rank:
                labels.append("Full House")
                full_house = True
                break
        if full_house:
            break

    # Full Hotel
    quad_ranks = [rank for rank, count in rank_counts.items() if count >= 4]
    full_hotel = False
    for quad_rank in quad_ranks:
        for pair_rank in pair_ranks:
            if pair_rank != quad_rank:
                labels.append("Full Hotel")
                full_hotel = True
                break
        if full_hotel:
            break

    # Two Triples
    if len(triplet_ranks) >= 2:
        labels.append("Two Triples")
        labels.append("Three of a Kind")  # Includes Three of a Kind
        labels.append("One Pair")         # Each triplet includes a pair

    # Three Pair
    if num_pairs >= 3:
        labels.append("Three Pair")
        labels.append("Two Pair")  # Includes Two Pair
        labels.append("One Pair")  # Includes One Pair

    # Three of a Kind
    if triplet_ranks and "Three of a Kind" not in labels:
        labels.append("Three of a Kind")
        labels.append("One Pair")  # Includes One Pair

    # Two Pair
    if num_pairs >= 2 and "Two Pair" not in labels:
        labels.append("Two Pair")
        labels.append("One Pair")  # Includes One Pair

    # One Pair
    if num_pairs >= 1 and "One Pair" not in labels:
        labels.append("One Pair")

    labels.append("High Card")  # Every hand has a High Card

    return labels

def process_batch(hands):
    labels_list = [classify_hand(hand) for hand in hands]
    flattened_labels = [label for labels in labels_list for label in labels]
    return Counter(flattened_labels)

def simulate_all_hands(batch_size=100, num_workers=16):
    hand_counts = Counter()
    all_hands = list(generate_all_hands())
    total_hands = len(all_hands)
    hand_batches = [all_hands[i:i + batch_size] for i in range(0, total_hands, batch_size)]
    with Pool(processes=num_workers) as pool:
        for result in tqdm(pool.imap_unordered(process_batch, hand_batches), total=len(hand_batches), desc="Simulating All Hands"):
            hand_counts.update(result)
    return hand_counts