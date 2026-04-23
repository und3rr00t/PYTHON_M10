from collections.abc import Callable


def mage_counter() -> Callable[[], int]:
    count = 0

    def counter() -> int:
        nonlocal count
        count += 1
        return count

    return counter


def spell_accumulator(initial_power: int) -> Callable[[int], int]:
    total_power = initial_power

    def accumulator(power_gain: int) -> int:
        nonlocal total_power
        total_power += power_gain
        return total_power

    return accumulator


def enchantment_factory(enchantment_type: str) -> Callable[[str], str]:
    def apply_enchantment(item_name: str) -> str:
        return f"{enchantment_type} {item_name}"

    return apply_enchantment


def memory_vault() -> dict[str, Callable]:
    memories: dict[str, object] = {}

    def store(key: str, value: object) -> None:
        memories[key] = value

    def recall(key: str) -> object | str:
        return memories.get(key, "Memory not found")

    return {
        "store": store,
        "recall": recall,
    }


def _prompt_literal(message: str, example: str):
    from ast import literal_eval

    while True:
        print(message)
        print(f"Example: {example}")
        try:
            return literal_eval(input("> ").strip())
        except (SyntaxError, ValueError):
            print("Invalid format. Paste a valid Python literal.\n")


if __name__ == "__main__":
    initial_power = _prompt_literal("Paste initial power", "100")
    additions = _prompt_literal("Paste additions list", "[20, 30]")
    enchantment_types = _prompt_literal(
        "Paste enchantment types list",
        "['Flaming', 'Frozen']",
    )
    items = _prompt_literal("Paste items list", "['Sword', 'Shield']")

    counter_a = mage_counter()
    counter_b = mage_counter()
    accumulator = spell_accumulator(initial_power)
    first_enchantment = enchantment_factory(enchantment_types[0])
    second_enchantment = enchantment_factory(enchantment_types[1])
    vault = memory_vault()

    print("\nTesting mage counter...")
    print(f"counter_a call 1: {counter_a()}")
    print(f"counter_a call 2: {counter_a()}")
    print(f"counter_b call 1: {counter_b()}")

    print("\nTesting spell accumulator...")
    for addition in additions:
        print(f"Added {addition}: {accumulator(addition)}")

    print("\nTesting enchantment factory...")
    print(first_enchantment(items[0]))
    print(second_enchantment(items[1]))

    print("\nTesting memory vault...")
    vault["store"]("secret", initial_power)
    print(f"Recall 'secret': {vault['recall']('secret')}")
    print(f"Recall 'unknown': {vault['recall']('unknown')}")
