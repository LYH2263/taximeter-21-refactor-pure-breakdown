"""货币出口模块:所有金额出分(分位四舍五入)的唯一入口。

起步、里程、低速、应付、对比差值等金额一律经本模块出分,
各业务引擎不得再自行调用内建 round 或散落进位逻辑。
"""

from decimal import Decimal, ROUND_HALF_UP

CENT = Decimal("0.01")


def _d(amount) -> Decimal:
    return amount if isinstance(amount, Decimal) else Decimal(str(amount))


def to_cents(amount) -> float:
    """将金额按分位四舍五入(半进)出分,返回分的浮点表示。"""
    return float(_d(amount).quantize(CENT, rounding=ROUND_HALF_UP))


def sum_cents(*amounts) -> float:
    """对已出分的金额精确加总,结果仍为分位金额。"""
    total = Decimal("0")
    for a in amounts:
        total += _d(a)
    return float(total.quantize(CENT, rounding=ROUND_HALF_UP))
