import random
from collections import Counter

import matplotlib.pyplot as plt


from typing import Optional

def simulate_dice_rolls(n_rolls: int, seed: Optional[int] = 42) -> dict[int, float]:
    """
    Симулює n_rolls кидків двох кубиків і повертає ймовірності сум 2..12.
    """
    if n_rolls <= 0:
        raise ValueError("n_rolls має бути > 0")

    if seed is not None:
        random.seed(seed)

    counts = Counter()

    for _ in range(n_rolls):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        counts[d1 + d2] += 1

    probs = {s: counts[s] / n_rolls for s in range(2, 13)}
    return probs


def analytical_probabilities() -> dict[int, float]:
    """
    Аналітичні ймовірності сум 2..12 для двох чесних кубиків.
    (кількість способів / 36)
    """
    ways = {
        2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6,
        8: 5, 9: 4, 10: 3, 11: 2, 12: 1
    }
    return {s: ways[s] / 36 for s in range(2, 13)}


def print_comparison_table(mc: dict[int, float], an: dict[int, float]) -> None:
    print("Сума | Monte-Carlo | Аналітична | Різниця (MC-AN)")
    print("-" * 50)
    for s in range(2, 13):
        diff = mc[s] - an[s]
        print(f"{s:>4} | {mc[s]:>10.5f} | {an[s]:>10.5f} | {diff:>+12.5f}")


def plot_probabilities(mc: dict[int, float], an: dict[int, float]) -> None:
    sums = list(range(2, 13))
    mc_vals = [mc[s] for s in sums]
    an_vals = [an[s] for s in sums]

    plt.figure(figsize=(10, 5))
    plt.plot(sums, mc_vals, marker="o", label="Monte-Carlo")
    plt.plot(sums, an_vals, marker="o", label="Аналітична")
    plt.xticks(sums)
    plt.xlabel("Сума (2..12)")
    plt.ylabel("Ймовірність")
    plt.title("Ймовірності сум при киданні двох кубиків")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main() -> None:
    n_rolls = 2_000  # можна змінити (чим більше — тим точніше, але довше працює)
    mc = simulate_dice_rolls(n_rolls=n_rolls, seed=42)
    an = analytical_probabilities()

    print(f"Кількість симуляцій: {n_rolls}")
    print_comparison_table(mc, an)
    plot_probabilities(mc, an)

    # Короткий висновок:
    max_abs_diff = max(abs(mc[s] - an[s]) for s in range(2, 13))
    print("\nВисновок:")
    print(
        f"За {n_rolls} симуляцій оцінки Монте-Карло наближені до аналітичних. "
        f"Максимальна абсолютна різниця: {max_abs_diff:.5f}."
    )


if __name__ == "__main__":
    main()
