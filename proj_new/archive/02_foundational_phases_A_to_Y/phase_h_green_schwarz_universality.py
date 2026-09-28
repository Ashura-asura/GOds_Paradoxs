"""
Phase H: The Actual Green-Schwarz Universality Condition [L1, NEW]
======================================================================
Ground rules: 1-8 strictly enforced.

Phases E/F/G only ever tested the PURE U(1)_F conditions -- linear
(sum q_i = 0) and cubic (sum q_i^3 = 0) -- plus gravity. "Green-Schwarz"
properly refers to something more specific: the MIXED anomalies between
U(1)_F and each Standard Model gauge factor,

    A(U(1)_F - SU(3)^2),  A(U(1)_F - SU(2)^2),  A(U(1)_F - U(1)_Y^2),

must all cancel via a single Green-Schwarz counterterm, which requires
them to be UNIVERSAL -- proportional to each gauge group's own level
(Kac-Moody level / normalization), not just each individually zero.

THIS PHASE ASKS, DIRECTLY (not assumed): does this universality
condition impose any NEW constraint on the FN charges, beyond what
Phases E/F/G already tested -- or is it automatically satisfied?

METHOD: compute the Dynkin index of a full SO(10) 16-plet under each
SM gauge factor (GUT-normalized), and check whether the mixed
anomalies for an arbitrary set of charge-q complete-16-plet fields are
automatically proportional across gauge groups.
"""

from fractions import Fraction as F

print('=' * 72)
print('Phase H: Does Green-Schwarz Universality Add a New Constraint?')
print('=' * 72)

# =====================================================================
# 1. Dynkin index of a single SO(10) 16 under each SM gauge factor
#    (GUT-normalized hypercharge: Y_GUT^2 = (3/5) Y_SM^2)
# =====================================================================
# 16 -> Q=(3,2,1/6), u^c=(3bar,1,-2/3), d^c=(3bar,1,1/3),
#       L=(1,2,-1/2), e^c=(1,1,1), nu^c=(1,1,0)


def su3_index_of_16():
    # color (anti)triplets: Q (x2 weak), u^c, d^c -- fundamental index 1/2 each
    return F(1, 2) * 2 + F(1, 2) + F(1, 2)


def su2_index_of_16():
    # weak doublets: Q (x3 color), L -- fundamental index 1/2 each
    return F(1, 2) * 3 + F(1, 2)


def u1y_index_of_16():
    fields = [
        (6, F(1, 6)),    # Q: 3 color x 2 weak states
        (3, F(-2, 3)),   # u^c: 3 color states
        (3, F(1, 3)),    # d^c: 3 color states
        (2, F(-1, 2)),   # L: 2 weak states
        (1, F(1)),       # e^c
        (1, F(0)),       # nu^c
    ]
    raw = sum(mult * y ** 2 for mult, y in fields)
    return F(3, 5) * raw  # GUT normalization


I3, I2, IY = su3_index_of_16(), su2_index_of_16(), u1y_index_of_16()
print(f"\nIndex of one SO(10) 16 under SU(3):            {I3}")
print(f"Index of one SO(10) 16 under SU(2):            {I2}")
print(f"Index of one SO(10) 16 under U(1)_Y (GUT-norm): {IY}")
print(f"Ratio I3 : I2 : IY  =  {I3} : {I2} : {IY}")

# =====================================================================
# 2. General argument: for ANY set of charges {q_i} on complete
#    16-plets (chiral generations and/or vector-like messenger pairs),
#    the mixed anomaly with gauge group a is A_a = (sum_i q_i) * I_a.
# =====================================================================
print('''
For ANY assignment of U(1)_F charges {q_i} to fields that are each a
complete SO(10) 16 (chiral or vector-like), the mixed anomaly with
gauge factor a is:

    A_a  =  ( sum_i q_i )  *  I_a^(16)

Because I3, I2, IY are FIXED numbers -- properties of the 16
representation itself, the same for every copy regardless of its
U(1)_F charge -- the ratios A3 : A2 : AY = I3 : I2 : IY hold
IDENTICALLY, for every possible charge assignment. In particular:

  sum_i q_i = 0   (the linear condition already imposed in Phase E/F/G)
       =>   A3 = A2 = AY = 0   automatically, with no further condition.
''')

print('VERIFICATION with a concrete example (Phase D charges + Phase F messenger):')
example_charges = [3, 2, 0, -3, 2]  # q=(3,2,0) chiral + Phase F messenger (-3,+2)
lin = sum(example_charges)
A3 = lin * I3
A2 = lin * I2
AY = lin * IY
print(f"  charges = {example_charges}, sum = {lin}")
print(f"  A(U(1)_F-SU(3)^2) = {lin} * {I3} = {A3}")
print(f"  A(U(1)_F-SU(2)^2) = {lin} * {I2} = {A2}")
print(f"  A(U(1)_F-U(1)_Y^2) = {lin} * {IY} = {AY}")
print(f"  All equal (as required): {A3 == A2 == AY}")
print("  (Nonzero here because this specific set does not satisfy sum=0 on its own;")
print("   the point is that A3=A2=AY regardless -- proportionality is automatic.)")

# =====================================================================
# SUMMARY
# =====================================================================
print('\n' + '=' * 72)
print('PHASE H RESULT')
print('=' * 72)
print('''
  RESULT (L1, verified by direct computation): the Green-Schwarz
  "universality" condition -- that mixed U(1)_F-gauge anomalies be
  proportional across all Standard Model factors -- is AUTOMATICALLY
  satisfied for any matter content built entirely from complete SO(10)
  16-plets. This is not a coincidence of the specific charges tried in
  Phases D-G; it follows from GUT-normalized SO(10) representation
  theory alone (the equal indices I3=I2=IY=2 computed above), and
  holds for every possible charge assignment.

  CONSEQUENCE: doing "the real Green-Schwarz mechanism" properly, as
  far as it can be tested from SO(10) representation theory alone,
  adds ZERO new constraints beyond the linear and cubic conditions
  Phases E/F/G already imposed. This closes off the possibility that
  a more careful anomaly analysis (rather than more messenger fields)
  was the missing ingredient.

  WHAT THE LITERATURE'S STRONGER CLAIM ACTUALLY REQUIRES: reducing
  charge freedom to "as few as three integers" (as cited in the Phase
  F/G literature survey) relies on additional input that genuine
  Green-Schwarz constructions get from a STRING COMPACTIFICATION --
  a fixed normalization of the anomalous U(1) against the string
  coupling, and quantized modular weights tied to a specific choice of
  compact manifold or orbifold. These are not group-theory facts about
  SO(10) or E8; they are extra, model-specific data that a particular
  string vacuum supplies. Cl(10)xE8 representation theory has no
  mechanism to generate or fix that data on its own.

  HONEST CONCLUSION: this is as far as "R4" can be taken rigorously
  from inside this framework. Reproducing the literature's
  charge-reduction result would require importing a specific string
  compactification's data wholesale -- which would mean the numbers
  come from that separate model, not from Cl(10)xE8. Presenting such
  a result as a Cl(10)xE8 derivation would be exactly the kind of
  reverse-engineering Rule 2 forbids. No further progress on this
  specific avenue is possible without a genuinely different starting
  framework (see RESEARCH_ROADMAP.md, R1).
''')
