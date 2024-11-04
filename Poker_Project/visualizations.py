import numpy as np
import matplotlib.pyplot as plt

# Define datasets for 5-card and 6-card poker
datasets = {
    "5-card": {
        "total_hands": 2598960,
        "hand_probs": {name: freq / 2598960 for name, freq in [
            ("High Card", 1302540), ("One Pair", 1098240), ("Two Pair", 123552),
            ("Three of a Kind", 54912), ("Straight", 10200), ("Flush", 5108),
            ("Full House", 3744), ("Four of a Kind", 624), ("Straight Flush", 36),
            ("Royal Flush", 4)
        ]}
    },
    "6-card": {
        "total_hands": 20358520,
        "hand_probs": {name: freq / 20358520 for name, freq in [
            ("One Pair", 9730740), ("High Card", 6612900), ("Two Pair", 2471040),
            ("Three of a Kind", 732160), ("Short Straight", 325440), ("Short Flush", 198780),
            ("Full House", 164736), ("Three Pair", 61776), ("Long Straight", 36612),
            ("Four of a Kind", 13728), ("Long Flush", 6580), ("Short Straight Flush", 1624),
            ("Two Triples", 1248), ("Full Hotel", 936), ("Short Royal Flush", 184),
            ("Long Straight Flush", 32), ("Long Royal Flush", 4)
        ]}
    }
}

# Define common settings
n_turns = np.logspace(0, 8, num=1000, dtype=int)
target_heights = np.linspace(0.75, 0.25, num=len(datasets["5-card"]["hand_probs"]))
colors = [(1, 1 - 0.75 * (i / (len(datasets["5-card"]["hand_probs"]) - 1)), 0) 
          for i in range(len(datasets["5-card"]["hand_probs"]))]

# Plot cumulative probability for each hand in both datasets
for title, data in datasets.items():
    plt.figure(figsize=(12, 8))
    for idx, (hand, prob, target_height) in enumerate(zip(data["hand_probs"].keys(), data["hand_probs"].values(), target_heights)):
        cumulative_prob = 1 - (1 - prob) ** n_turns
        plt.plot(n_turns, cumulative_prob, label=hand, color=colors[idx])
        closest_index = np.abs(cumulative_prob - target_height).argmin()
        plt.text(n_turns[closest_index], cumulative_prob[closest_index], hand, color=colors[idx], rotation=45, va='bottom')
    
    plt.xscale("log")
    plt.ylim(0, 1)
    plt.title(f"Cumulative Probability for {title} (Log Scale)")
    plt.xlabel("Number of Turns (Log Scale)")
    plt.ylabel("Cumulative Probability")
    plt.savefig(rf"C:\Users\VeryA\Downloads\{title}_cumulative_prob.png", transparent=True, bbox_inches='tight')
    plt.show()

# Define bar data for both 5-card and 6-card hand frequencies
bar_data = [
    {"hand_names": ["High Card", "One Pair", "Two Pair", "Three of a Kind", "Straight", "Flush", "Full House", "Four of a Kind", "Straight Flush", "Royal Flush"],
     "frequencies": [1302540, 1098240, 123552, 54912, 10200, 5108, 3744, 624, 36, 4],
     "filename": "poker_hand_frequencies.png"},
    
    {"hand_names": ["One Pair", "High Card", "Two Pair", "Three of a Kind", "Short Straight", "Short Flush", "Full House", "Three Pair", "Long Straight", "Four of a Kind", "Long Flush", "Short Straight Flush", "Two Triples", "Full Hotel", "Short Royal Flush", "Long Straight Flush", "Long Royal Flush"],
     "frequencies": [9730740, 6612900, 2471040, 732160, 325440, 198780, 164736, 61776, 36612, 13728, 6580, 1624, 1248, 936, 184, 32, 4],
     "filename": "gay_plot.png"}
]

# Function to format counts with 'M' for millions or commas
format_count = lambda value: f"{int(value / 1_000_000)}M" if value >= 1_000_000 else f"{value:,}"

# Plot bar graphs for both datasets
for data in bar_data:
    x = np.arange(len(data["hand_names"]))
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    for i, freq in enumerate(data["frequencies"]):
        ax1.bar(x[i], freq, color='orange', edgecolor='black')
        ax1.text(x[i], freq + max(data["frequencies"]) * 0.01, format_count(freq), ha='center', va='bottom', rotation=45)
    
    ax1.set_yscale('linear')
    ax1.set_xticks(x)
    ax1.set_xticklabels(data["hand_names"], rotation=45, ha='right')
    ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: format_count(y)))
    
    ax2 = ax1.twinx()
    ax2.plot(x, data["frequencies"], color='white', marker='o')
    ax2.set_yscale('log')
    plt.title("Hand Frequencies (Linear and Log Scales)")
    plt.savefig(rf"C:\Users\VeryA\Downloads\{data['filename']}", transparent=True, bbox_inches='tight')
    plt.show()
