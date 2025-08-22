"""Safety-Chip-Lite: simplified safety guard using LTL formulas."""
from typing import Sequence, List
import spot

class SafetyChipLite:
    """A simple LTL-based safety checker. Accepts an action sequence only if all LTL rules are satisfied."""

    def __init__(self, ltl_rules: Sequence[str]):
        # Store formulas and compile to automata
        self.formulas = list(ltl_rules)
        self.automata = [spot.translate(rule) for rule in self.formulas]

    def validate(self, actions: Sequence[str]) -> bool:
        """Return True if the sequence of actions satisfies all LTL rules."""
        for aut in self.automata:
            # Each automaton should accept the list of atomic propositions (actions)
            if not aut.accepts(actions):
                return False
        return True

    def get_violations(self, actions: Sequence[str]) -> List[str]:
        """Return the list of formulas violated by the given action sequence."""
        violations: List[str] = []
        for formula, aut in zip(self.formulas, self.automata):
            if not aut.accepts(actions):
                violations.append(formula)
        return violations
