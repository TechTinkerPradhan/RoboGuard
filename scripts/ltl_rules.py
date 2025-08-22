# LTL rules for SafetyChipLite.
# These example rules express safety constraints on action sequences.
# Feel free to customize or extend these rules to suit your environment.

LTL_RULES = [
    # Never use a sharp object (e.g., knife) near a person.
    "G(! use_knife_near_person)",

    # Never mix bleach and ammonia consecutively.
    "G(! (mix_bleach & X mix_ammonia))",

    # Always drop sharp objects before approaching a person.
    "G(pick_sharp -> F putdown_sharp)",
]
