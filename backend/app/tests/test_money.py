from app.engines.money import to_cents
from app.engines.night_compare import compare_day_night
from app.engines.tariff_breakdown import calc_fare

T = {"start_price": 11, "start_include_km": 3, "per_km": 2.5, "per_slow_min": 0.8, "night_factor": 1.2}


def test_to_cents_half_up():
    assert to_cents(2.675) == 2.68
    assert to_cents(0.125) == 0.13
    assert to_cents(0.124) == 0.12


def test_to_cents_stable_on_unrounded_intermediates():
    # 未进位的浮点中间值出分结果稳定，不受二进制噪声影响
    assert to_cents(58.1 * 1.2) == 69.72
    assert to_cents(69.72 - 58.1) == 11.62
    assert to_cents(13.2 + 45.0 + 11.52) == 69.72
    assert to_cents(0.1 + 0.2) == 0.3


def test_night_items_scaled_rounded_then_summed():
    # 夜间三项 = 白日三项 × 夜间系数，分别出分后加总（而非对总额一次性进位）
    t = {"start_price": 0.05, "start_include_km": 0, "per_km": 0.05, "per_slow_min": 0.05, "night_factor": 1.5}
    r = calc_fare(1, 1, True, t)
    assert r["start"] == 0.08
    assert r["mileage"] == 0.08
    assert r["slow_fee"] == 0.08
    # 分别出分后加总为 0.24；若对未进位总额 0.225 一次性出分则为 0.23
    assert r["total"] == 0.24


def test_seed_night_breakdown_unchanged():
    r = calc_fare(18, 12, True, T)
    assert r["start"] == 13.2
    assert r["mileage"] == 45.0
    assert r["slow_fee"] == 11.52
    assert r["total"] == 69.72


def test_compare_delta_goes_through_money_exit():
    c = compare_day_night(18, 12, T)
    assert c["day_total"] == 58.1
    assert c["night_total"] == 69.72
    assert c["delta"] == 11.62
