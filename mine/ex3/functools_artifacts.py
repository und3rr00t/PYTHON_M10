from collections.abc import Callable
from functools import lru_cache, partial, reduce, singledispatch
from operator import add, gt, lt, mul
from typing import Any


def spell_reducer(spells: list[int], operation: str) -> int:
    if not spells:
        return 0

    operations = {
        "add": add,
        "multiply": mul,
        "max": lambda left, right: left if gt(left, right) else right,
        "min": lambda left, right: left if lt(left, right) else right,
    }

    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")

    return reduce(operations[operation], spells)


def partial_enchanter(
    base_enchantment: Callable[[int, str, str], str],
) -> dict[str, Callable[[str], str]]:
    if not callable(base_enchantment):
        raise TypeError("base_enchantment must be callable.")

    return {
        "fire": partial(base_enchantment, 50, "fire"),
        "ice": partial(base_enchantment, 50, "ice"),
        "lightning": partial(base_enchantment, 50, "lightning"),
    }


@lru_cache(maxsize=None)
def memoized_fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative.")
    if n < 2:
        return n
    return memoized_fibonacci(n - 1) + memoized_fibonacci(n - 2)


def spell_dispatcher() -> Callable[[Any], str]:
    @singledispatch
    def dispatch(spell: Any) -> str:
        return "Unknown spell type"

    @dispatch.register
    def _(spell: int) -> str:
        return f"Damage spell: {spell} damage"

    @dispatch.register
    def _(spell: str) -> str:
        return f"Enchantment: {spell}"

    @dispatch.register(list)
    def _(spell: list[Any]) -> str:
        return f"Multi-cast: {len(spell)} spells"

    return dispatch


def _prompt_literal(message: str, example: str):
    from ast import literal_eval

    while True:
        print(message)
        print(f"Example: {example}")
        try:
            return literal_eval(input("> ").strip())
        except (SyntaxError, ValueError):
            print("Invalid format. Paste a valid Python literal.\n")


def _base_enchantment(power: int, element: str, target: str) -> str:
    return (
        f"{element.title()} enchantment grants {target} "
        f"{power} mystical power"
    )


if __name__ == "__main__":
    spell_powers = _prompt_literal(
        "Paste spell powers list",
        "[10, 20, 30, 40]",
    )
    items = _prompt_literal(
        "Paste enchantment items list",
        "['Sword', 'Shield', 'Spear']",
    )
    fibonacci_tests = _prompt_literal(
        "Paste fibonacci tests list",
        "[0, 1, 10, 15]",
    )
    spell_names = _prompt_literal(
        "Paste spell names list",
        "['fireball', 'heal', 'shield']",
    )

    enchantments = partial_enchanter(_base_enchantment)
    dispatcher = spell_dispatcher()

    print("\nTesting spell reducer...")
    for operation in ["add", "multiply", "max", "min"]:
        print(f"{operation}: {spell_reducer(spell_powers, operation)}")

    print("\nTesting partial enchanter...")
    print(enchantments["fire"](items[0]))
    print(enchantments["ice"](items[1]))
    print(enchantments["lightning"](items[2]))

    print("\nTesting memoized fibonacci...")
    for value in fibonacci_tests:
        print(f"Fib({value}): {memoized_fibonacci(value)}")

    print("\nTesting spell dispatcher...")
    print(dispatcher(spell_powers[0]))
    print(dispatcher(spell_names[0]))
    print(dispatcher(spell_names))
    print(dispatcher({"spell": "mystery"}))
