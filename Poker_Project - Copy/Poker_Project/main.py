from Draw import Draw  # Import the Draw class
from tqdm import tqdm  # Import tqdm for the progress bar

def main():
    num_hands = int(input("Enter the number of hands to draw: "))

    draw = Draw()  # Create a Draw object

    # Define the hand hierarchy in the correct order (High Card to Long Royal Flush)
    hand_hierarchy = [
        "High Card", "One Pair", "Two Pair", "Three of a Kind", "Short Straight", 
        "Short Flush", "Full House", "Three Pair", "Long Straight", "Four of a Kind",
        "Long Flush", "Short Straight Flush", "Two Triples", "Full Hotel", 
        "Short Royal Flush", "Long Straight Flush", "Long Royal Flush"
    ]

    # Initialize hand_counts with all types from the hierarchy and set them to 0
    hand_counts = {hand_type: 0 for hand_type in hand_hierarchy}

    # Loop over num_hands and use tqdm to show the progress bar
    for _ in tqdm(range(num_hands), desc="Drawing hands"):
        hand = draw.draw_hand()  # Always draw 6 cards and evaluate the hand
        hand_counts[str(hand)] += 1  # Increment the count for this hand type

    # Print the results in hierarchy order (starting from High Card down to Long Royal Flush)
    print("\nSimulation Results:")
    for hand_type in hand_hierarchy:
        print(f"{hand_type}: {hand_counts[hand_type]}")

if __name__ == "__main__":
    main()
