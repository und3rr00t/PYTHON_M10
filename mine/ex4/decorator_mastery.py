from collections.abc import Callable
from functools import wraps
from time import perf_counter, sleep
from typing import Any


def spell_timer(func: Callable[..., str]) -> Callable[..., str]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> str:
        print(f"Casting {func.__name__}...")
        start_time = perf_counter()
        result = func(*args, **kwargs)
        elapsed = perf_counter() - start_time
        print(f"Spell completed in {elapsed:.3f} seconds")
        return result

    return wrapper


def power_validator(
    min_power: int,
) -> Callable[[Callable[..., str]], Callable[..., str]]:
    def decorator(func: Callable[..., str]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> str:
            power = kwargs.get("power")
            if power is None and args and isinstance(args[0], int):
                power = args[0]
            if power is None and len(args) >= 2 and isinstance(args[-1], int):
                power = args[-1]
            if power is None or power < min_power:
                return "Insufficient power for this spell"
            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_spell(
    max_attempts: int,
) -> Callable[[Callable[..., str]], Callable[..., str]]:
    if max_attempts < 1:
        raise ValueError("max_attempts must be at least 1.")

    def decorator(func: Callable[..., str]) -> Callable[..., str]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> str:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts:
                        return (
                            "Spell casting failed after "
                            f"{max_attempts} attempts"
                        )
                    print(
                        "Spell failed, retrying... "
                        f"(attempt {attempt}/{max_attempts})"
                    )
            return f"Spell casting failed after {max_attempts} attempts"

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        stripped_name = name.strip()
        return (
            len(stripped_name) >= 3
            and all(
                character.isalpha() or character.isspace()
                for character in stripped_name
            )
        )

    @power_validator(10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return f"Successfully cast {spell_name} with {power} power"


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


if __name__ == "__main__":
    spell_names = _prompt_literal(
        "Paste spell names list",
        "['fireball', 'lightning', 'heal', 'shield']",
    )
    powers = _prompt_literal("Paste powers list", "[15, 5, 18, 9]")
    valid_name = _prompt_text("Paste a valid mage name", "Aeris")
    invalid_name = _prompt_text("Paste an invalid mage name", "Ae1")

    while len(spell_names) < 4:
        spell_names.append(f"spell_{len(spell_names) + 1}")
    while len(powers) < 2:
        powers.append(5)

    def build_timed_spell(spell_name: str) -> Callable[[], str]:
        def cast() -> str:
            sleep(0.1)
            return f"{spell_name.title()} cast!"

        cast.__name__ = spell_name.replace(" ", "_").lower()
        return spell_timer(cast)

    def build_retry_success(spell_name: str) -> Callable[[], str]:
        attempts = {"count": 0}

        @retry_spell(3)
        def cast() -> str:
            attempts["count"] += 1
            if attempts["count"] < 3:
                raise RuntimeError("Temporary failure")
            return f"{spell_name.title()} cast after steadying the magic!"

        return cast

    def build_retry_failure(spell_name: str) -> Callable[[], str]:
        @retry_spell(3)
        def cast() -> str:
            raise RuntimeError(f"{spell_name.title()} collapsed.")

        return cast

    guild = MageGuild()
    timed_spell = build_timed_spell(spell_names[0])
    failed_spell = build_retry_failure(spell_names[1])
    recovered_spell = build_retry_success(spell_names[2])
    valid_power = max(powers)
    invalid_power = min(powers)
    if invalid_power >= 10:
        invalid_power = max(1, invalid_power // 2)

    print("\nTesting spell timer...")
    print(f"Result: {timed_spell()}")

    print("\nTesting retrying spell...")
    print(failed_spell())
    print(recovered_spell())

    print("\nTesting MageGuild...")
    print(MageGuild.validate_mage_name(valid_name))
    print(MageGuild.validate_mage_name(invalid_name))
    print(guild.cast_spell(spell_names[3].title(), valid_power))
    print(guild.cast_spell(spell_names[3].title(), invalid_power))
