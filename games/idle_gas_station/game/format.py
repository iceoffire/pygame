"""Money formatting. Pure Python (no pygame) so it can be unit-tested anywhere."""

CURRENCY = "R$"
SUFFIXES = ((10**12, "T"), (10**9, "B"), (10**6, "M"), (10**3, "K"))


def short_number(value):
    """999 -> '999', 1234 -> '1.2K', 3_456_789 -> '3.4M'. Rounds down so it never overstates."""
    whole = int(value)
    if whole < 0:
        return "-" + short_number(-value)
    for unit, suffix in SUFFIXES:
        if whole >= unit:
            tenths = whole * 10 // unit  # integer math: no float rounding surprises
            return f"{tenths // 10}.{tenths % 10}{suffix}"
    return str(whole)


def money(value):
    """'R$ 999', 'R$ 1.2K', 'R$ 3.4M', 'R$ 5.6B'."""
    return f"{CURRENCY} {short_number(value)}"


def rate(value):
    """Income per second; keeps one decimal for small fractional rates ('R$ 0.5/s')."""
    if value < 100 and value != int(value):
        tenths = int(value * 10 + 1e-9)
        return f"{CURRENCY} {tenths // 10}.{tenths % 10}/s"
    return f"{money(value)}/s"


def duration(seconds):
    """3725 -> '1h 2m', 95 -> '1m 35s'."""
    seconds = int(seconds)
    hours, rest = divmod(seconds, 3600)
    minutes, secs = divmod(rest, 60)
    if hours:
        return f"{hours}h {minutes}m"
    if minutes:
        return f"{minutes}m {secs}s"
    return f"{secs}s"
