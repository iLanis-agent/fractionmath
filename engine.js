// Fraction Math engine - add, subtract, multiply and divide fractions, mixed numbers, and decimals as fractions.
// Mirrored by oracle.py; keep the op order identical.
// Numerators and whole parts run 0 to 1000000, denominators 1 to 1000000. Arithmetic is exact (big integers).
// Decimals are shown to 4 places, half away from zero, and marked "exactly" only when they are exact at 4 places.

function _int(x, label, min, max) {
  if (typeof x !== "number" || !isFinite(x) || Math.floor(x) !== x || x < min || x > max) {
    throw new Error(label + " must be a whole number from " + min + " to " + max);
  }
  return BigInt(x);
}

function _gcd(a, b) {
  if (a < 0n) a = -a;
  if (b < 0n) b = -b;
  while (b !== 0n) { var t = a % b; a = b; b = t; }
  return a;
}

function _mixed(p, q) {
  var neg = p < 0n, a = neg ? -p : p;
  return (neg ? "-" : "") + (a / q) + " " + (a % q) + "/" + q;
}

function _dec(p, q) {
  var neg = p < 0n, a = neg ? -p : p;
  var scaled = (2n * a * 10000n + q) / (2n * q);
  var exact = (a * 10000n) % q === 0n;
  var whole = scaled / 10000n, frac = String(scaled % 10000n);
  while (frac.length < 4) frac = "0" + frac;
  while (frac.length > 0 && frac.charAt(frac.length - 1) === "0") frac = frac.slice(0, -1);
  return { scaled: scaled, exact: exact, text: (neg && scaled > 0n ? "-" : "") + whole + (frac ? "." + frac : "") };
}

function _describe(p, q, typed) {
  var g = _gcd(p, q);
  if (p === 0n) { p = 0n; q = 1n; } else { p = p / g; q = q / g; }
  if (q === 1n) return p + ".";
  var a = p < 0n ? -p : p;
  var head = p + "/" + q + (a > q && _mixed(p, q) !== typed ? " (" + _mixed(p, q) + " as a mixed number)" : "");
  var d = _dec(p, q);
  if (d.scaled === 0n) return head + ", a value smaller than 0.0001 in size.";
  return head + ", " + (d.exact ? "exactly " : "about ") + d.text + ".";
}

var WORDS = { add: "plus", subtract: "minus", multiply: "times", divide: "divided by" };

// The op truth: two fractions and one operation, reduced.
function opTruth(n1, d1, n2, d2, op) {
  var a = _int(n1, "first numerator", 0, 1000000), b = _int(d1, "first denominator", 1, 1000000);
  var c = _int(n2, "second numerator", 0, 1000000), d = _int(d2, "second denominator", 1, 1000000);
  if (!WORDS.hasOwnProperty(op)) throw new Error("operation must be add, subtract, multiply or divide");
  var p, q;
  if (op === "add") { p = a * d + c * b; q = b * d; }
  else if (op === "subtract") { p = a * d - c * b; q = b * d; }
  else if (op === "multiply") { p = a * c; q = b * d; }
  else {
    if (c === 0n) throw new Error("cannot divide by a fraction equal to zero");
    p = a * d; q = b * c;
  }
  return n1 + "/" + d1 + " " + WORDS[op] + " " + n2 + "/" + d2 + " is " + _describe(p, q);
}

// The mixed truth: a whole number plus a fraction, as one fraction.
function mixedTruth(whole, num, den) {
  var w = _int(whole, "whole part", 0, 1000000), n = _int(num, "numerator", 0, 1000000), d = _int(den, "denominator", 1, 1000000);
  var typed = whole + " " + num + "/" + den;
  return typed + " is " + _describe(w * d + n, d, typed);
}

// The decimal truth: a decimal written out as the exact fraction it names.
function decimalTruth(text) {
  var t = typeof text === "string" ? text.trim() : "";
  if (!/^-?[0-9]{1,12}(\.[0-9]{1,12})?$/.test(t)) {
    throw new Error("enter a decimal number such as 0.375 or -2.5 with up to 12 digits on each side of the point");
  }
  var neg = t.charAt(0) === "-", body = neg ? t.slice(1) : t;
  var parts = body.split("."), k = parts.length === 2 ? parts[1].length : 0;
  var p = BigInt(parts[0] + (parts[1] || "")), q = 10n ** BigInt(k);
  if (neg) p = -p;
  var g = _gcd(p, q);
  if (p === 0n) { p = 0n; q = 1n; } else { p = p / g; q = q / g; }
  if (q === 1n) return t + " is exactly " + p + ".";
  var a = p < 0n ? -p : p;
  return t + " is exactly " + p + "/" + q + (a > q ? " (" + _mixed(p, q) + " as a mixed number)" : "") + ".";
}
