#!/usr/bin/env python3
# Fraction Math oracle - mirrors engine.js.
import json, math, re

def _int(x, label, lo, hi):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or math.floor(x) != x or x < lo or x > hi:
        raise ValueError(f"{label} must be a whole number from {lo} to {hi}")
    return int(x)

def _mixed(p, q):
    neg = p < 0; a = -p if neg else p
    return ("-" if neg else "") + f"{a // q} {a % q}/{q}"

def _dec(p, q):
    neg = p < 0; a = -p if neg else p
    scaled = (2 * a * 10000 + q) // (2 * q)
    exact = (a * 10000) % q == 0
    whole, frac = divmod(scaled, 10000)
    f = f"{frac:04d}".rstrip("0")
    text = ("-" if neg and scaled > 0 else "") + str(whole) + ("." + f if f else "")
    return scaled, exact, text

def _describe(p, q, typed=None):
    if p == 0:
        p, q = 0, 1
    else:
        g = math.gcd(p, q); p //= g; q //= g
    if q == 1:
        return f"{p}."
    a = -p if p < 0 else p
    head = f"{p}/{q}" + (f" ({_mixed(p, q)} as a mixed number)" if a > q and _mixed(p, q) != typed else "")
    scaled, exact, text = _dec(p, q)
    if scaled == 0:
        return head + ", a value smaller than 0.0001 in size."
    return head + ", " + ("exactly " if exact else "about ") + text + "."

WORDS = {"add": "plus", "subtract": "minus", "multiply": "times", "divide": "divided by"}

def op_truth(n1, d1, n2, d2, op):
    a = _int(n1, "first numerator", 0, 1000000); b = _int(d1, "first denominator", 1, 1000000)
    c = _int(n2, "second numerator", 0, 1000000); d = _int(d2, "second denominator", 1, 1000000)
    if op not in WORDS:
        raise ValueError("operation must be add, subtract, multiply or divide")
    if op == "add": p, q = a * d + c * b, b * d
    elif op == "subtract": p, q = a * d - c * b, b * d
    elif op == "multiply": p, q = a * c, b * d
    else:
        if c == 0:
            raise ValueError("cannot divide by a fraction equal to zero")
        p, q = a * d, b * c
    return f"{n1}/{d1} {WORDS[op]} {n2}/{d2} is " + _describe(p, q)

def mixed_truth(whole, num, den):
    w = _int(whole, "whole part", 0, 1000000); n = _int(num, "numerator", 0, 1000000); d = _int(den, "denominator", 1, 1000000)
    typed = f"{whole} {num}/{den}"
    return f"{typed} is " + _describe(w * d + n, d, typed)

def decimal_truth(text):
    t = text.strip() if isinstance(text, str) else ""
    if not re.fullmatch(r"-?[0-9]{1,12}(\.[0-9]{1,12})?", t):
        raise ValueError("enter a decimal number such as 0.375 or -2.5 with up to 12 digits on each side of the point")
    neg = t[0] == "-"; body = t[1:] if neg else t
    parts = body.split("."); k = len(parts[1]) if len(parts) == 2 else 0
    p = int(parts[0] + (parts[1] if len(parts) == 2 else "")); q = 10 ** k
    if neg: p = -p
    if p == 0:
        p, q = 0, 1
    else:
        g = math.gcd(p, q); p //= g; q //= g
    if q == 1:
        return f"{t} is exactly {p}."
    a = -p if p < 0 else p
    return f"{t} is exactly {p}/{q}" + (f" ({_mixed(p, q)} as a mixed number)" if a > q else "") + "."

FNS = {"opTruth": op_truth, "mixedTruth": mixed_truth, "decimalTruth": decimal_truth}
CASES = [
    ("opTruth", [3, 4, 5, 6, "add"]), ("opTruth", [1, 2, 1, 2, "add"]), ("opTruth", [1, 3, 1, 6, "add"]), ("opTruth", [1, 2, 1, 3, "subtract"]),
    ("opTruth", [1, 3, 1, 2, "subtract"]), ("opTruth", [1, 2, 1, 2, "subtract"]), ("opTruth", [2, 3, 3, 4, "multiply"]), ("opTruth", [6, 8, 0, 5, "multiply"]),
    ("opTruth", [3, 4, 3, 8, "divide"]), ("opTruth", [1, 7, 1, 7, "divide"]), ("opTruth", [0, 5, 3, 4, "divide"]), ("opTruth", [1, 1000000, 1, 1000000, "multiply"]),
    ("opTruth", [999999, 1000000, 999998, 999999, "add"]), ("opTruth", [1, 32, 0, 3, "add"]), ("opTruth", [1000000, 1, 1000000, 1, "multiply"]),
    ("opTruth", [1, 3, 5, 8, "subtract"]), ("opTruth", [1, 1000000, 0, 1, "add"]), ("opTruth", [7, 2, 1, 4, "add"]), ("opTruth", [5, 5, 1, 1, "multiply"]),
    ("opTruth", [3, 4, 0, 5, "divide"]), ("opTruth", [-1, 2, 1, 2, "add"]), ("opTruth", [1, 0, 1, 2, "add"]), ("opTruth", [1, 2, 1, 2.5, "add"]), ("opTruth", [1, 2, 1, 2, "power"]), ("opTruth", [1000001, 2, 1, 2, "add"]),
    ("mixedTruth", [2, 3, 4]), ("mixedTruth", [0, 1, 3]), ("mixedTruth", [2, 7, 4]), ("mixedTruth", [5, 0, 8]), ("mixedTruth", [0, 0, 5]), ("mixedTruth", [1, 1, 8]),
    ("mixedTruth", [1000000, 999999, 1000000]), ("mixedTruth", [3, 6, 8]), ("mixedTruth", [2, 3, 0]), ("mixedTruth", [-1, 1, 2]), ("mixedTruth", [1, 1.5, 2]),
    ("decimalTruth", ["0.375"]), ("decimalTruth", ["3.5"]), ("decimalTruth", ["-2.5"]), ("decimalTruth", ["5"]), ("decimalTruth", ["5.000"]), ("decimalTruth", ["0.333"]),
    ("decimalTruth", ["-0.75"]), ("decimalTruth", ["0"]), ("decimalTruth", ["-0.0"]), ("decimalTruth", ["0.000000000001"]), ("decimalTruth", ["999999999999.999999999999"]),
    ("decimalTruth", [" 1.25 "]), ("decimalTruth", [""]), ("decimalTruth", [".5"]), ("decimalTruth", ["1/2"]), ("decimalTruth", ["1.2.3"]), ("decimalTruth", ["1.0000000000001"]), ("decimalTruth", [5]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
