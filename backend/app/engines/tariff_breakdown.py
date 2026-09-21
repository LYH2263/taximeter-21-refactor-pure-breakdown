from app.engines.money import sum_cents, to_cents


def calc_fare(distance_km: float, slow_min: float, night: bool, tariff: dict) -> dict:
    base = float(tariff["start_price"])
    include = float(tariff["start_include_km"])
    per_km = float(tariff["per_km"])
    per_slow = float(tariff["per_slow_min"])
    night_f = float(tariff.get("night_factor", 1.0)) if night else 1.0
    dist = max(0.0, float(distance_km) - include)
    mile = dist * per_km
    slow = float(slow_min) * per_slow
    start = to_cents(base * night_f)
    mileage = to_cents(mile * night_f)
    slow_fee = to_cents(slow * night_f)
    return {
        "distance_km": round(float(distance_km), 2),
        "slow_min": round(float(slow_min), 1),
        "night": night,
        "night_factor": night_f,
        "start": start,
        "mileage": mileage,
        "slow_fee": slow_fee,
        "total": sum_cents(start, mileage, slow_fee),
    }
