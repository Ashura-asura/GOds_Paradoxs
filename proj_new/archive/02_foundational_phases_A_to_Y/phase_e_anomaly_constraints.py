"""
Phase E: Gauged U(1)_F Anomaly Cancellation vs. FN Charges [L1, NEW]
======================================================================
Ground rules: 1-8 strictly enforced.

Question: can the Phase D Froggatt-Nielsen charges q=(3,2,0) be DERIVED,
instead of fitted, by gauging the horizontal U(1)_F and demanding
anomaly cancellation (as is done in real anomalous-U(1) FN models in
the literature)?

This phase answers that question for the MINIMAL matter content implied
by the Cl(10) x E8 core: exactly 3 chiral SO(10) 16-plets (one per
generation, from the E8 -> (16,3) branching), with NO extra vector-like
matter added.

RESULT (L1, proved below):
  1. Anomaly cancellation forces q1+q2+q3=0 and q1^3+q2^3+q3^3=0.
  2. These two conditions together force charges of the form (n,-n,0).
  3. q=(3,2,0) VIOLATES both conditions -> not anomaly-free if gauged.
  4. The anomaly-free family (n,-n,0) is DEGENERATE: it only produces
     2 distinct Yukawa suppression tiers, but the observed mass
     hierarchy needs 3 distinct tiers.
  5. Therefore: for this minimal fermion content, gauged U(1)_F
     anomaly-freedom and the observed 3-generation mass hierarchy are
     STRUCTURALLY INCOMPATIBLE. This is a new L1 structural no-go,
     in the sense of Rule 8 (Phase B).

This does NOT mean anomaly cancellation is useless for FN model
building in general -- real papers use it successfully. It means it
cannot rescue *this* model's charges without adding matter beyond the
3 complete 16-plets that Cl(10) x E8 actually gives you. Adding that
matter reopens new free choices (new fields, their charges, their
masses), so Rule 6 is not restored by this route either.
"""

import numpy as np
from itertools import product

print('='*72)
print('Phase E: Gauged U(1)_F Anomaly Cancellation vs. FN Charges [L1]')
print('='*72)

# =====================================================================
# 1. Fermion content: hypercharges within one SO(10) 16, with multiplicity
# =====================================================================
print('\n--- Step 1: One SO(10) 16, hypercharge content ---')
# (multiplicity, Y) for Q, u^c, d^c, L, e^c, nu^c
fields = [(6, 1/6), (3, -2/3), (3, 1/3), (2, -1/2), (1, 1), (1, 0)]
Ytrace = sum(mult * Y for mult, Y in fields)
dim16 = sum(mult for mult, _ in fields)
print(f'  Sum of hypercharges within one 16 (weighted by multiplicity) = {Ytrace:.6f}')
print(f'  (This vanishing is the standard fact underlying SM anomaly freedom')
print(f'   per generation -- confirmed, not assumed.)')
print(f'  dim(16) = {dim16} chiral Weyl fermion states per generation')

# =====================================================================
# 2. Anomaly conditions for a gauged U(1)_F with charge q_i per generation
# =====================================================================
print('\n--- Step 2: Anomaly conditions for gauged U(1)_F ---')
print('''
  Since q_i is a FAMILY charge (whole 16 carries the same q_i, as
  required by the SU(3)_f -> U(1)_F embedding), each mixed anomaly
  factorizes as (per-generation SM anomaly coefficient) x q_i, summed
  over generations:

    [SU(3)_c]^2 U(1)_F  propto  (q1+q2+q3)
    [SU(2)_L]^2 U(1)_F  propto  (q1+q2+q3)
    [U(1)_Y]^2  U(1)_F  propto  (q1+q2+q3)
    gravity     U(1)_F  propto  (q1+q2+q3)
    U(1)_Y [U(1)_F]^2   propto  (q1^2+q2^2+q3^2) x Ytrace = 0  (auto, since Ytrace=0)
    [U(1)_F]^3          propto  (q1^3+q2^3+q3^3)

  Nontrivial conditions:  q1+q2+q3 = 0   AND   q1^3+q2^3+q3^3 = 0
''')

def check(q):
    q1, q2, q3 = q
    lin = q1 + q2 + q3
    cubic = q1**3 + q2**3 + q3**3
    return lin, cubic

print('--- Step 3: Test the Phase D charges q=(3,2,0) ---')
lin, cubic = check((3, 2, 0))
print(f'  q=(3,2,0):  sum(q_i) = {lin}  (need 0)   sum(q_i^3) = {cubic}  (need 0)')
print(f'  -> ANOMALOUS if U(1)_F is gauged. Phase D charges are NOT anomaly-free.')

# =====================================================================
# 3. Solve the anomaly conditions exactly
# =====================================================================
print('\n--- Step 4: Solve q1+q2+q3=0 and q1^3+q2^3+q3^3=0 exactly ---')
print('''
  Algebraic identity: a^3+b^3+c^3 - 3abc = (a+b+c)(a^2+b^2+c^2-ab-bc-ca)
  If a+b+c = 0, then a^3+b^3+c^3 = 3abc.
  Combined with a^3+b^3+c^3 = 0  =>  3abc = 0  =>  abc = 0
  => at least one of q1,q2,q3 MUST be exactly zero.
  => the other two must be equal and opposite: (n, -n, 0).
''')

sols = []
for q1, q2, q3 in product(range(-6, 7), repeat=3):
    if (q1, q2, q3) == (0, 0, 0):
        continue
    if q1 + q2 + q3 == 0 and q1**3 + q2**3 + q3**3 == 0:
        sols.append((q1, q2, q3))
uniq = sorted(set(tuple(sorted(s)) for s in sols))
print(f'  Brute-force check (|q_i|<=6): {len(sols)} solutions found (incl. permutations/signs).')
print(f'  Distinct sorted patterns: {uniq}')
print(f'  CONFIRMS: every anomaly-free solution has the form {{n, -n, 0}}.')

# =====================================================================
# 4. Test whether (n,-n,0) can reproduce the observed hierarchy
# =====================================================================
print('\n--- Step 5: Can anomaly-free charges (n,-n,0) fit the SM hierarchy? ---')
print('  FN diagonal Yukawa suppression: Y_ii ~ eps^|2 q_i|')
for n in [1, 2, 3, 4]:
    q = [n, -n, 0]
    diag_powers = [abs(2 * qi) for qi in q]
    print(f'  q=({q[0]:+d},{q[1]:+d},{q[2]:+d}): diagonal powers |2q_i| = {diag_powers}'
          f'  -> {len(set(diag_powers))} distinct tier(s)')

print('''
  Observed charged-fermion hierarchy (e.g. m_u : m_c : m_t or
  m_e : m_mu : m_tau) spans THREE distinct, well-separated tiers.
  (n,-n,0) always yields diagonal powers {2n, 2n, 0}: generations
  1 and 2 are FORCED DEGENERATE at this order. This is not a fitting
  failure -- it is forced by the anomaly conditions themselves.
''')

# =====================================================================
# SUMMARY
# =====================================================================
print('='*72)
print('PHASE E RESULT (L1)')
print('='*72)
print('''
  THEOREM: For the minimal Cl(10) x E8 fermion content (exactly 3
  chiral SO(10) 16-plets, no extra matter), gauging the horizontal
  U(1)_F and imposing anomaly cancellation forces charges of the form
  (n,-n,0). This set is structurally INCOMPATIBLE with a 3-tier mass
  hierarchy: it only distinguishes 2 tiers.

  COROLLARY: q=(3,2,0) (used in Phase D to fit CKM/masses) is NOT
  anomaly-free. Anomaly cancellation does not derive it -- it rules
  it out. Reconciling anomaly-freedom with the observed hierarchy
  requires adding vector-like matter beyond the 3 complete 16-plets
  (as real anomalous-U(1) FN papers do). That matter's charges and
  masses are new free choices, so Rule 6 (zero free parameters) is
  not restored by this route -- the free-parameter problem is moved,
  not solved.

  Ground rules compliance:
  [Rule 1, no numerology]        HONORED: charges tested against a
                                   derived condition, not fit to data.
  [Rule 2, no reverse-engineer]  HONORED: anomaly conditions derived
                                   BEFORE checking against (3,2,0).
  [Rule 8, structural failure    HONORED: incompatibility proved, not
   = result]                      asserted.
''')
