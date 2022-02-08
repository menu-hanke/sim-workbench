from math import log, e
from typing import Any, Optional


def grow(volume: float) -> Optional[float]:
    if volume is None:
        return None
    multiplier = 1 + 1 / log(volume, e)
    result = multiplier * volume
    print("Forest growing by factor of " + str(multiplier) + ". V = " + str(volume) + " -> " + str(multiplier * volume))
    return result


def cut(volume: float, pct: float = 100) -> Optional[float]:
    if volume is None:
        return None
    multiplier = pct / 100
    result = volume - multiplier * volume
    if can_cut(volume) is False:
        raise Exception("Can not cut " + str(pct) + " %. Tree volume " + str(result) + " is below cutting threshold.")

    print("Cutting " + str(pct) + " %. V = " + str(volume) + " -> " + str(result))
    return result


def can_cut(volume: float, threshold: float = 200) -> bool:
    return volume > threshold


def do_nothing(data: Any) -> Any:
    print("Did nothing")
    return data


def plant(volume: float, amount: int) -> Optional[float]:
    if volume is None:
        return None
    increase = amount / 100
    result = volume + increase
    print("Planting " + str(amount) + " trees. V now " + str(result))
    return result


def basal_area_thinning(X):
    print("basal area thinning")
    return X


def stem_count_thinning(X):
    print("stem count thinning")
    return X


def continuous_growth_thinning(X):
    print("continuous growth thinning")
    return X


def reporting(X):
    print('information output stub')
    return X


operation_lookup = {
    'do_nothing': do_nothing,
    'grow': grow,
    'basal_area_thinning': basal_area_thinning,
    'stem_count_thinning': stem_count_thinning,
    'continuous_growth_thinning': continuous_growth_thinning,
    'reporting': reporting
}
