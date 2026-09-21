from app.engines.money import sum_cents, to_cents
from app.engines.night_compare import compare_day_night
from app.engines.tariff_breakdown import calc_fare

SEED_TARIFF = {"start_price": 11, "start_include_km": 3, "per_km": 2.5, "per_slow_min": 0.8, "night_factor": 1.2}


def test_to_cents_half_up_stable():
    # 未进位中间值:二进制浮点下 2.675 实际偏小,内建 round 会给 2.67,货币出口须稳定出 2.68
    assert to_cents(2.675) == 2.68
    assert to_cents(1.005) == 1.01
    assert to_cents(17.605) == 17.61
    assert to_cents(2.675) == to_cents(2.675)


def test_to_cents_idempotent_on_rounded():
    assert to_cents(17.6) == 17.6
    assert to_cents(69.72) == 69.72


def test_sum_cents_exact():
    assert sum_cents(13.2, 45.0, 11.52) == 69.72
    assert sum_cents(0.1, 0.2) == 0.3


def test_night_items_rounded_then_summed():
    # 夜间三项 = 白日三项 × 夜间系数,分别出分后再加总
    t = {"start_price": 10, "start_include_km": 0, "per_km": 6.25, "per_slow_min": 3.75, "night_factor": 1.3}
    r = calc_fare(1, 1, True, t)
    assert r["start"] == 13.0    # 10 × 1.3
    assert r["mileage"] == 8.13  # 6.25 × 1.3 = 8.125 → 8.13
    assert r["slow_fee"] == 4.88  # 3.75 × 1.3 = 4.875 → 4.88
    assert r["total"] == 26.01   # 13.0 + 8.13 + 4.88,而非对总额 20 × 1.3 = 26.0 整体出分


def test_seed_amounts_unchanged():
    day = calc_fare(5, 2, False, SEED_TARIFF)
    assert day["total"] == 17.6
    c = compare_day_night(18, 12, SEED_TARIFF)
    assert c["day_total"] == 58.1
    assert c["night_total"] == 69.72
    assert c["delta"] == 11.62
