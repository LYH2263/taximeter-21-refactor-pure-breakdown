"""单一货币出口：金额的分位四舍五入统一在此完成。

计价、昼夜对比等引擎不得再各自调用内建 round 或做等价的散落进位，
一律经本模块出分。采用 Decimal + ROUND_HALF_UP，避免二进制浮点
噪声（如 0.1+0.2、69.72-58.1）影响分位结果。
"""
from decimal import ROUND_HALF_UP, Decimal

CENT = Decimal("0.01")


def quantize(value, places: int = 2) -> float:
    """按指定小数位四舍五入（half-up），返回 float。"""
    quantum = Decimal(1).scaleb(-places)
    return float(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP))


def to_cents(value) -> float:
    """金额出分：四舍五入到分位（0.01）。"""
    return quantize(value, 2)
