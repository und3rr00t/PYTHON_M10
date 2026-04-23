from collections.abc import Callable


Spell = Callable[[str, int], str]
Condition = Callable[[str, int], bool]


def spell_combiner(
    spell1: Spell, spell2: Spell,
) -> Callable[[str, int], tuple[str, str]]:
    if not callable(spell1) or not callable(spell2):
        raise TypeError("Both spells must be callable.")

    def combined(target: str, power: int) -> tuple[str, str]:
        return spell1(target, power), spell2(target, power)

    return combined


def power_amplifier(base_spell: Spell, multiplier: int) -> Spell:
    if not callable(base_spell):
        raise TypeError("base_spell must be callable.")

    def amplified(target: str, power: int) -> str:
        return base_spell(target, power * multiplier)

    return amplified


def conditional_caster(condition: Condition, spell: Spell) -> Spell:
    if not callable(condition) or not callable(spell):
        raise TypeError("condition and spell must be callable.")

    def caster(target: str, power: int) -> str:
        if condition(target, power):
            return spell(target, power)
        return "Spell fizzled"

    return caster


def spell_sequence(spells: list[Spell]) -> Callable[[str, int], list[str]]:
    if not all(callable(spell) for spell in spells):
        raise TypeError("Every item in spells must be callable.")

    def sequence(target: str, power: int) -> list[str]:
        return [spell(target, power) for spell in spells]

    return sequence


def _prompt_literal(message: str, example: str):
    from ast import literal_eval

    while True:
        print(message)
        print(f"Example: {example}")
        try:
            return literal_eval(input("> ").strip())
        except (SyntaxError, ValueError):
            print("Invalid format. Paste a valid Python literal.\n")


def _prompt_text(message: str, default: str) -> str:
    value = input(f"{message} (default: {default}): ").strip()
    return value or default


def _build_spell(spell_name: str) -> Spell:
    normalized_name = spell_name.strip().lower()

    def spell(target: str, power: int) -> str:
        if normalized_name == "heal":
            return f"{spell_name.title()} restores {target} for {power} HP"
        if normalized_name == "shield":
            return f"{spell_name.title()} protects {target} with {power} force"
        return f"{spell_name.title()} hits {target} for {power} damage"

    return spell


if __name__ == "__main__":
    spell_names = _prompt_literal(
        "Paste spell names list",
        "['fireball', 'heal', 'shield']",
    )
    target = _prompt_text("Paste target", "Dragon")
    power = _prompt_literal("Paste power", "15")
    threshold = _prompt_literal("Paste condition threshold", "12")

    spells = [_build_spell(spell_name) for spell_name in spell_names]
    while len(spells) < 3:
        spells.append(_build_spell(f"spell_{len(spells) + 1}"))

    print("\nTesting spell combiner...")
    combined = spell_combiner(spells[0], spells[1])
    print(combined(target, power))

    print("\nTesting power amplifier...")
    amplified = power_amplifier(spells[0], 3)
    print(amplified(target, power))

    print("\nTesting conditional caster...")
    guarded = conditional_caster(
        lambda chosen_target, chosen_power: (
            len(chosen_target) > 3 and chosen_power >= threshold
        ),
        spells[1],
    )
    print(guarded(target, power))
    print(guarded(target[:3], max(0, threshold - 1)))

    print("\nTesting spell sequence...")
    sequence = spell_sequence(spells[:3])
    print(sequence(target, power))
