from dependent_simulations import simulate_all_hands as simulate_dependent_hands
from independent_simulations import simulate_all_hands as simulate_independent_hands

def main():
    batch_size = 100
    num_workers = 16


    print("Running Independent Simulation...")
    independent_counts = simulate_independent_hands(batch_size, num_workers)

    print("\nIndependent Simulation Results:")
    for hand_type, count in sorted(independent_counts.items(), key=lambda x: -x[1]):
        print(f"{hand_type}: {count}")


    print("Running Dependent Simulation...")
    dependent_counts = simulate_dependent_hands(batch_size, num_workers)

    print("\nDependent Simulation Results:")
    for hand_type, count in sorted(dependent_counts.items(), key=lambda x: -x[1]):
        print(f"{hand_type}: {count}")

if __name__ == "__main__":
    main()
