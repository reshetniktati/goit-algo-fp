from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


ItemsDict = Dict[str, Dict[str, int]]


@dataclass(frozen=True)
class ChoiceResult:
    chosen: List[str]
    total_cost: int
    total_calories: int


def greedy_algorithm(items: ItemsDict, budget: int) -> ChoiceResult:
    """
    Жадібний підхід: сортуємо страви за (calories / cost) спаданням
    і беремо, поки є бюджет.

    Важливо: цей підхід НЕ гарантує оптимум, але часто дає непоганий результат.
    """
    # Підготуємо список (name, cost, calories, ratio)
    ranked = []
    for name, meta in items.items():
        cost = meta["cost"]
        calories = meta["calories"]
        ratio = calories / cost
        ranked.append((name, cost, calories, ratio))

    ranked.sort(key=lambda x: x[3], reverse=True)

    chosen: List[str] = []
    total_cost = 0
    total_calories = 0

    for name, cost, calories, _ in ranked:
        if total_cost + cost <= budget:
            chosen.append(name)
            total_cost += cost
            total_calories += calories

    return ChoiceResult(chosen, total_cost, total_calories)


def dynamic_programming(items: ItemsDict, budget: int) -> ChoiceResult:
    """
    ДП (0/1 knapsack):
    dp[b] = макс. калорійність при бюджеті b
    Також зберігаємо "батьків" для відновлення набору.
    """
    names = list(items.keys())
    costs = [items[n]["cost"] for n in names]
    calories = [items[n]["calories"] for n in names]
    n = len(names)

    # dp[b] - максимум калорій при бюджеті b
    dp = [0] * (budget + 1)

    # parent[b] = (prev_budget, item_index) якщо ми покращили dp[b], інакше None
    parent: List[Tuple[int, int] | None] = [None] * (budget + 1)

    for i in range(n):
        c = costs[i]
        cal = calories[i]
        # Ідемо у зворотному напрямку, щоб кожен item брати максимум 1 раз
        for b in range(budget, c - 1, -1):
            candidate = dp[b - c] + cal
            if candidate > dp[b]:
                dp[b] = candidate
                parent[b] = (b - c, i)

    # Знайдемо бюджет b*, на якому dp максимальний (може бути < budget)
    best_b = max(range(budget + 1), key=lambda b: dp[b])

    # Відновлюємо набір
    chosen_indices = []
    b = best_b
    while parent[b] is not None:
        prev_b, i = parent[b]
        chosen_indices.append(i)
        b = prev_b

    chosen_indices.reverse()
    chosen = [names[i] for i in chosen_indices]

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = sum(items[name]["calories"] for name in chosen)

    return ChoiceResult(chosen, total_cost, total_calories)


if __name__ == "__main__":
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350},
    }

    budget = 100

    g = greedy_algorithm(items, budget)
    d = dynamic_programming(items, budget)

    print("Greedy:", g)
    print("DP:", d)
