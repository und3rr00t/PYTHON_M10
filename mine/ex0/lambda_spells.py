def artifact_sorter(artifacts: list[dict]) -> list[dict]:
    return sorted(
        artifacts,
        key=lambda artifact: artifact["power"],
        reverse=True,
    )


def power_filter(mages: list[dict], min_power: int) -> list[dict]:
    return list(
        filter(
            lambda mage: mage["power"] >= min_power,
            mages,
        )
    )


def spell_transformer(spells: list[str]) -> list[str]:
    return list(map(lambda spell: f"* {spell} *", spells))


def mage_stats(mages: list[dict]) -> dict:
    if not mages:
        return {
            "max_power": 0,
            "min_power": 0,
            "avg_power": 0.0,
        }

    return {
        "max_power": max(mages, key=lambda mage: mage["power"])["power"],
        "min_power": min(mages, key=lambda mage: mage["power"])["power"],
        "avg_power": round(
            sum(map(lambda mage: mage["power"], mages)) / len(mages),
            2,
        ),
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
    artifacts = _prompt_literal(
        "Paste artifacts list",
        "[{'name': 'Fire Staff', 'power': 92, 'type': 'weapon'}]",
    )
    mages = _prompt_literal(
        "Paste mages list",
        "[{'name': 'Alex', 'power': 88, 'element': 'fire'}]",
    )
    spells = _prompt_literal(
        "Paste spells list",
        "['fireball', 'heal', 'shield']",
    )
    min_power = _prompt_literal("Paste min_power", "80")

    print("\nTesting artifact sorter...")
    print(artifact_sorter(artifacts))

    print("\nTesting power filter...")
    print(power_filter(mages, min_power))

    print("\nTesting spell transformer...")
    print(spell_transformer(spells))

    print("\nTesting mage stats...")
    print(mage_stats(mages))
