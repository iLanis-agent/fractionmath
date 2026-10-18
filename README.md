# Fraction Math

Fraction arithmetic. Add the tops and add the bottoms is the classic wrong answer.

## What it computes

- **The op truth** - add, subtract, multiply or divide two fractions: the reduced fraction, its mixed number when it is bigger than 1, and its decimal.
- **The mixed truth** - a whole number plus a fraction as one reduced fraction.
- **The decimal truth** - a decimal written out as the exact fraction it names.

Arithmetic is exact with big integers. Numerators and whole parts run 0 to 1000000, denominators 1 to 1000000. Decimals show 4 places, half away from zero, and say "exactly" only when they are exact at 4 places, otherwise "about".

## Boundary

Arithmetic only. Fraction Math does not know how a class, recipe or specification wants an answer rounded or written. Check that where it applies.

## Files

- `index.html` - landing page.
- `app.html` - the interactive calculator.
- `engine.js` - the arithmetic.
- `oracle.py` - the Python mirror that generates `expected.json`.
- `test.js` - compares every engine output against `expected.json` (54 cases).
- `expected.json` - the golden answers.

## Test

```
python3 oracle.py
node test.js
```

Live: https://ilanis-agent.github.io/fractionmath/
Repo: https://github.com/iLanis-agent/fractionmath
