"""Money, upgrades, pricing and offline earnings. Pure Python (no pygame) so it is easy to test."""
import math
import time
from dataclasses import dataclass

BILL_VALUES = (1, 2, 5, 10, 20, 50, 100)  # one image per value: assets/images/bills/bill_<n>.png


@dataclass(frozen=True)
class Upgrade:
    key: str  # stable id used in save.json
    name: str
    icon: str  # "image:<path>" for a bundled image, otherwise a drawn icon name (see game/ui.py)
    base_price: float
    growth: float  # price = base_price * growth ** level
    income: float = 0.0  # R$ per second added by each level (idle upgrades)
    max_level: int | None = None


BIGGER_BILLS = "bigger_bills"

UPGRADES = (
    Upgrade("underwear", "Underwear Size", "image:images/upgrades/underwear.png", 15, 1.15, income=0.5),
    Upgrade(BIGGER_BILLS, "Bigger Bills", "bills", 40, 4.0, max_level=len(BILL_VALUES) - 1),
    Upgrade("fuel_pump", "Fuel Pump", "pump", 100, 1.15, income=3),
    Upgrade("store", "Convenience Store", "store", 1_100, 1.15, income=20),
    Upgrade("car_wash", "Car Wash", "car_wash", 12_000, 1.15, income=120),
    Upgrade("refinery", "Oil Refinery", "refinery", 130_000, 1.15, income=800),
)
UPGRADES_BY_KEY = {upgrade.key: upgrade for upgrade in UPGRADES}


def price(base_price, growth, level):
    """Exponential pricing: base * growth^level, rounded up to whole Reais."""
    return math.ceil(base_price * growth**level - 1e-9)


def bill_value(level):
    """Click value for a 'Bigger Bills' level: 1 -> 2 -> 5 -> 10 -> 20 -> 50 -> 100."""
    return BILL_VALUES[max(0, min(level, len(BILL_VALUES) - 1))]


def compute_idle_income(levels):
    """Total idle income in R$ per second for a {key: level} mapping."""
    return sum(UPGRADES_BY_KEY[key].income * level for key, level in levels.items() if key in UPGRADES_BY_KEY)


def offline_earnings(income_per_second, last_timestamp, now, cap_seconds):
    """(earned, seconds_counted) for the time the game was closed. Clock skew never pays negative."""
    if not last_timestamp:
        return 0.0, 0.0
    seconds = min(max(0.0, now - last_timestamp), cap_seconds)
    return income_per_second * seconds, seconds


class Economy:
    def __init__(self, money=0.0, levels=None):
        self.money = float(money)
        self.levels = {upgrade.key: 0 for upgrade in UPGRADES}
        for key, level in (levels or {}).items():
            if key in self.levels:
                try:
                    self.levels[key] = max(0, int(level))
                except (TypeError, ValueError):
                    pass  # a hand-edited save with junk in it just keeps level 0
        if (cap := UPGRADES_BY_KEY[BIGGER_BILLS].max_level) is not None:
            self.levels[BIGGER_BILLS] = min(self.levels[BIGGER_BILLS], cap)

    # --- queries -----------------------------------------------------
    @property
    def bill_value(self):
        return bill_value(self.levels[BIGGER_BILLS])

    @property
    def idle_income(self):
        return compute_idle_income(self.levels)

    def level(self, upgrade):
        return self.levels[upgrade.key]

    def is_maxed(self, upgrade):
        return upgrade.max_level is not None and self.level(upgrade) >= upgrade.max_level

    def price(self, upgrade):
        return price(upgrade.base_price, upgrade.growth, self.level(upgrade))

    def can_afford(self, upgrade):
        return not self.is_maxed(upgrade) and self.money >= self.price(upgrade)

    # --- actions -----------------------------------------------------
    def click(self):
        """Clicking the flag: earn one bill. Returns its value."""
        value = self.bill_value
        self.money += value
        return value

    def try_buy(self, upgrade):
        if not self.can_afford(upgrade):
            return False
        self.money -= self.price(upgrade)
        self.levels[upgrade.key] += 1
        return True

    def add_idle_income(self, dt):
        self.money += self.idle_income * dt

    # --- persistence ---------------------------------------------------
    def to_save(self, now=None):
        return {"money": self.money, "levels": dict(self.levels), "timestamp": time.time() if now is None else now}

    @classmethod
    def from_save(cls, data):
        try:
            money = float(data.get("money", 0.0))
            levels = dict(data.get("levels", {}))
        except (TypeError, ValueError, AttributeError):
            money, levels = 0.0, {}
        if not math.isfinite(money) or money < 0:
            money = 0.0
        return cls(money, levels)
