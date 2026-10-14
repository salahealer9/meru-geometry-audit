"""Pre-freeze QC boundaries; no registered fixtures, IO or evaluation at import."""
import math
import re


def require(condition, message):
    """Preserve invariant failures even when Python removes assert statements."""
    if not condition:
        raise AssertionError(message)


def parse_pi_bounds(value):
    """Parse only [pi +/- unsigned rational, pi +/- unsigned rational].

    No eval, names other than pi, arithmetic chains or zero denominators.
    This parser binds the existing serialized bounds without changing geometry.
    """
    if not isinstance(value, str) or len(value) > 128:
        raise ValueError('bounds must be a short pi/rational interval string')
    match = re.fullmatch(
        r'\[\s*pi\s*([+-])\s*(\d+)\s*/\s*([1-9]\d*)\s*,\s*'
        r'pi\s*([+-])\s*(\d+)\s*/\s*([1-9]\d*)\s*\]', value,
        flags=re.ASCII)
    if match is None:
        raise ValueError('invalid pi/rational bounds syntax')
    groups = match.groups()
    bounds = []
    for start in (0, 3):
        sign, numerator, denominator = groups[start:start+3]
        offset = int(numerator)/int(denominator)
        bounds.append(math.pi + (offset if sign == '+' else -offset))
    if not all(math.isfinite(x) for x in bounds) or bounds[0] >= bounds[1]:
        raise ValueError('bounds must be finite and strictly ordered')
    return bounds
