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
    rank_values_set = set(rank_values)

    # Ace also mapped to 1 if 2, 3, 4, 5 are present
    if 14 in rank_values_set and {2, 3, 4, 5}.intersection(rank_values_set):
        rank_values.append(1)
    return sorted(set(rank_values))

# straights of length 'size'
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
    
    triplet_ranks = [rank for rank, count in rank_counts.items() if count == 3]
    quad_ranks = [rank for rank, count in rank_counts.items() if count == 4]
    pair_ranks = [rank for rank, count in rank_counts.items() if count == 2]
    num_pairs = len(pair_ranks)
    num_triplets = len(triplet_ranks)
    
    # Sort rank_values for straight checks
    rank_values = sorted(set(rank_values))
    
    # Long Royal Flush
    for suit in suit_counts:
        suited_cards = [card for card in hand if card[1] == suit]
        suited_ranks = [card[0] for card in suited_cards]
        if set(['9', '10', 'Jack', 'Queen', 'King', 'Ace']).issubset(suited_ranks):
            return "Long Royal Flush"
    
    # Long Straight Flush
    for suit in suit_counts:
        suited_cards = [card for card in hand if card[1] == suit]
        suited_rank_values = get_rank_values([card[0] for card in suited_cards])
        if has_consecutive_ranks(suited_rank_values, 6):
            return "Long Straight Flush"
    
    # Short Royal Flush
    for suit in suit_counts:
        suited_cards = [card for card in hand if card[1] == suit]
        suited_ranks = [card[0] for card in suited_cards]
        if set(['10', 'Jack', 'Queen', 'King', 'Ace']).issubset(suited_ranks):
            return "Short Royal Flush"
    
    # Full Hotel
    if quad_ranks and num_pairs >= 1:
        # pair needs to be a different rank
        for pair_rank in pair_ranks:
            if pair_rank not in quad_ranks:
                return "Full Hotel"
    
    # Two Triples
    if num_triplets >= 2:
        return "Two Triples"
    
    # Short Straight Flush
    for suit in suit_counts:
        suited_cards = [card for card in hand if card[1] == suit]
        suited_rank_values = get_rank_values([card[0] for card in suited_cards])
        if has_consecutive_ranks(suited_rank_values, 5):
            return "Short Straight Flush"
    
    # Long Flush
    if any(count >= 6 for count in suit_counts.values()):
        return "Long Flush"
    
    # Four of a Kind
    if quad_ranks:
        return "Four of a Kind"
    
    # Long Straight
    if has_consecutive_ranks(rank_values, 6):
        return "Long Straight"
    
    # Three Pair
    if num_pairs >= 3:
        return "Three Pair"
    
    # Full House
    if num_triplets >= 1 and num_pairs >= 1:
        # Triplet and pair need to be different ranks
        for triplet_rank in triplet_ranks:
            for pair_rank in pair_ranks:
                if triplet_rank != pair_rank:
                    return "Full House"
    
    # Short Flush
    if any(count >= 5 for count in suit_counts.values()):
        return "Short Flush"
    
    # Short Straight
    if has_consecutive_ranks(rank_values, 5):
        return "Short Straight"
    
    # Three of a Kind
    if num_triplets >= 1:
        return "Three of a Kind"
    
    # Two Pair
    if num_pairs >= 2:
        return "Two Pair"
    
    # One Pair
    if num_pairs == 1:
        return "One Pair"
    
    # High Card
    return "High Card"

def process_batch(hands):
    labels = [classify_hand(hand) for hand in hands]
    return Counter(labels)

def simulate_all_hands(batch_size=100, num_workers=16):
    hand_counts = Counter()
    all_hands = list(generate_all_hands())
    total_hands = len(all_hands)
    hand_batches = [all_hands[i:i + batch_size] for i in range(0, total_hands, batch_size)]
    with Pool(processes=num_workers) as pool:
        for result in tqdm(pool.imap_unordered(process_batch, hand_batches), total=len(hand_batches), desc="Simulating All Hands"):
            hand_counts.update(result)
    return hand_counts