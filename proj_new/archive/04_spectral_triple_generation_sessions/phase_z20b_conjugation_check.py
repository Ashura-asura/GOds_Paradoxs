"""
Phase Z20b (v2): same check as v2, but using a manual noncommutative
word-reduction (sympy's .replace() is unreliable for noncommutative Mul
patterns) instead of sympy's built-in replace.

We represent each term as an ordered tuple of atomic symbols (a "word"),
and reduce words by cancelling adjacent (U,Ui) or (Ui,U) pairs directly,
which is unambiguous and exact for this free-monoid computation.
"""
import sympy as sp

U, Ui, D, a, b = sp.symbols('U Ui D a b')  # commutative=True is fine here;
# we track noncommutativity ourselves via explicit word order, so we
# never rely on sympy reordering factors.

RhoA = sp.Symbol('RhoA')

def word_reduce(word):
    """word: list of symbols. Cancel adjacent U,Ui or Ui,U pairs repeatedly,
    AND apply the commutant relations U*a=a*U, U*b=b*U, Ui*a=a*Ui, Ui*b=b*Ui
    (U, Ui commute with the algebra elements a, b by definition of being
    in the commutant A'). RhoA is NOT assumed to commute with U (it's
    built from D, not from A), so no swap rule is applied to it."""
    changed = True
    while changed:
        changed = False
        for i in range(len(word) - 1):
            if (word[i] == U and word[i+1] == Ui) or (word[i] == Ui and word[i+1] == U):
                word = word[:i] + word[i+2:]
                changed = True
                break
            if word[i] in (U, Ui) and word[i+1] in (a, b):
                word = word[:i] + [word[i+1], word[i]] + word[i+2:]
                changed = True
                break
    return tuple(word)


def expand_terms(term_words, coeff=1):
    """term_words: list of (coeff, [word]) pairs. Just bookkeeping."""
    return term_words


# Build D1 = [U, D, Ui] as a word (with a symbolic coefficient +1)
D1 = [U, D, Ui]

# a, b are single-symbol words
A = [a]
B = [b]

# RhoA1 = [U, RhoA, Ui]
RhoA1 = [U, RhoA, Ui]


def mul(*words):
    out = []
    for w in words:
        out += w
    return out


def sub_condition(Dw, Aw, RhoAw, Bw):
    """
    Compute [[D,a]_rho, b] = (D a - RhoA D) b - b (D a - RhoA D)
    as a signed sum of words, using the abstract D, a, RhoA, b words
    given (each may itself be a compound word like D1, RhoA1).
    Returns list of (sign, word) terms, each word already reduced.
    """
    term1 = (+1, word_reduce(mul(Dw, Aw, Bw)))         # D a b
    term2 = (-1, word_reduce(mul(RhoAw, Dw, Bw)))      # -RhoA D b
    term3 = (-1, word_reduce(mul(Bw, Dw, Aw)))         # -b D a
    term4 = (+1, word_reduce(mul(Bw, RhoAw, Dw)))      # +b RhoA D
    return [term1, term2, term3, term4]


# original condition, with D (not D1) and RhoA (not RhoA1):
orig = sub_condition([D], A, [RhoA], B)

# new condition with D1, RhoA1 in place of D, RhoA:
new = sub_condition(D1, A, RhoA1, B)

# target: U * orig * Ui, term by term
target = []
for sign, w in orig:
    target.append((sign, word_reduce(mul([U], list(w), [Ui]))))

def normalize(terms):
    # combine identical words (sum signs), drop zero-coeff, sort for compare
    from collections import defaultdict
    acc = defaultdict(int)
    for sign, w in terms:
        acc[w] += sign
    return sorted(((w, c) for w, c in acc.items() if c != 0), key=lambda wc: str(wc[0]))

new_norm = normalize(new)
target_norm = normalize(target)

print("New condition (U D U^-1, twisted by U rho U^-1), reduced & combined:")
for w, c in new_norm:
    print(f"  {c:+d} * {' '.join(str(s) for s in w)}")
print()
print("Target: U * [[D,a]_rho,b] * U^-1, reduced & combined:")
for w, c in target_norm:
    print(f"  {c:+d} * {' '.join(str(s) for s in w)}")
print()
print(f"MATCH: {new_norm == target_norm}")
