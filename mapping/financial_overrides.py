import re

UP_POS = {
    "rise","rises","rose","rising","gain","gains","gained","surge","surges","surged","jump","jumps","jumped",
    "soar","soars","soared","rally","rallies","rallied","advance","advances","advanced","climb","climbs","climbed",
    "up","higher","record high","upper circuit","hit upper circuit","premium","beats estimates"
}
DOWN_NEG = {
    "fall","falls","fell","falling","drop","drops","dropped","slip","slips","slipped","sink","sinks","sank",
    "plunge","plunges","plunged","tumble","tumbles","tumbled","decline","declines","declined","crash","crashes","crashed",
    "down","lower","record low","hits record low","discount","misses estimates","under pressure"
}

BAD_UP = {
    "inflation","yields","bond yields","interest rates","rates","unemployment","jobless","deficit","loss","losses",
    "debt","defaults","npas","npa","liabilities","expenses","costs","rupee sinks","rupee falls"
}

GOOD_DOWN = {
    "inflation","yields","bond yields","interest rates","rates","unemployment","jobless","deficit","loss","losses",
    "debt","costs","expenses","oil prices"
}

BEARISH_CONTEXT = {
    "subdued demand",
    "weak demand",
    "headwinds",
    "slowdown",
    "pressure",
    "margin pressure",
    "uncertainty",
    "downgrades"
}

def _has_any(text: str, phrases: set[str]) -> bool:
    t = text.lower()
    for p in phrases:
        if " " in p:
            if p in t:
                return True
        else:
            if re.search(rf"\b{re.escape(p)}\b", t):
                return True
    return False


def directional_override(title: str) -> float:
    t = title.lower()
    adj = 0.0

    has_up = _has_any(t, UP_POS)
    has_down = _has_any(t, DOWN_NEG)

    bad_up = _has_any(t, BAD_UP)
    good_down = _has_any(t, GOOD_DOWN)

    if has_up and has_down:
        adj += 0.0
    elif has_up:
        adj += 0.18
    elif has_down:
        adj -= 0.18

    if has_up and bad_up:
        adj -= 0.28
    if has_down and good_down:
        adj += 0.28

    if "upper circuit" in t:
        adj += 0.20
    if "record low" in t:
        adj -= 0.20
        
    has_bearish_context = _has_any(t, BEARISH_CONTEXT)

    if has_down and has_bearish_context:
        adj -= 0.20


    return max(-0.35, min(0.35, adj))

