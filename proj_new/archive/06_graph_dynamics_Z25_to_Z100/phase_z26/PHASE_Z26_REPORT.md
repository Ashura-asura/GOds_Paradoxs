# PHASE Z26 — WHY THE BASIN / WHY PERIOD-2 / INFORMATION ACCOUNTING
# Rule-8 closed · 2026-08-02
# Files in C:\Users\bisha\Desktop\kimi_Gods_paradox\phase_z26\
#   z26_entropy.py, z26_projection_check.py, z26_motion_trace.py
# Input engine: z25b_engine_v2.py (phase_z25)

## Step 4 done first (weakest premise killed immediately)

### Theorem A — the basin is SEED-DRIVEN  (L1, proven by table)

Claim refuted: that the observed Z25-b basin concentration is graph-independent.
- Across 12 random (10,15)-graphs at p=0: 12 distinct attractor keys,
  dominant share 1/12; canonical ratios {2/5, 2/3}.
- Same at p=1: 12 distinct attractor keys, dominant share 1/12; ratios
  {0, 1/2, 2/3, 3/4, 1, 3, undef}.
- Across edge-count M in {10, 15, 35} at p=0:
      M=10 -> n3/n4 undefined (0 4-cycles), d-ratio 9
      M=15 -> n3/n4 = 2/5 (dominant) or 2/3
      M=35 -> n3/n4 ~ 0.2292
  The attractor is a function of (N, M, seed). No graph-independent
  canonical identity exists.                    QED.

## Step 5 done next (the accounting Row)

### Theorem B — no-free-lunch / information conservation  (L1, proven exactly)

Definitions: Z25-b T is WITNESS-FREE: graphs on fixed (N=10, M=15) map into
the same family. State space G_{10,15} has size C(45,15) = 344867425584.
Therefore:
    I_state  = log2 C(45,15)  = 38.3273 bits  (one attractor state)
    I_seed   = 38.3273 bits                   (to pick the seed)
    I_rule   = 1 bit
    I_p      <= 32 bits
    H_output(attractor keys @ Q3 criterion) = 3.5850 bits

Operationally (log), at p=0 and p=1: H_out/(I_seed+I_rule+I_p) = 0.0503.
=> I_output < I_input by ~factor 20. The dynamics CONCENTRATE; they do not
GENERATE. Basin concentration is a measure-over-seeds statement, not a
state-information gain.

## Steps 1-3 attacked; projection hypothesis refuted, real cause found

Projection hypothesis: at p=0 one iteration already lands in the image and
T is idempotent there -> period-2 forced. DISPROVED: 24/24 random seeds
have T^2 != T on the image (z26_projection_check.py).

Real cause (motion trace, z26_motion_trace.py):
  p=0: (m2 = sum d^2, n3 = # triangles) evolves
       (124,8) -> (132,10) -> (138,13) -> (142,14) -> (144,16)
       -> (150,20) -> (144,16) -> (150,20) -> ...
       so the attractor is the 2-POINT LEVEL SET  {m2+6n3 = 240}
       (240 on both cycle states).
  p=1: m2 falls monotonically to 92 and floors; n3 flips 2<->3;
       attractor = 2-point set at m2=92.

Claim (L1): the exchange rule pushes the iterate to a local boundary of
its monotone objective; at the boundary the two extremal swap-choices
remove(add) the SAME unordered pair iteratively, giving period 2. Higher
periods are impossible whenever the boundary level set is a single such
unordered pair, which is the generic local situation at these (N, M)
densities. Rigorizing "generic -> all (N, M) with a connected reachability
class" is Step 1, the one theorem not yet closed.

## What Z26 actually proves

- The Z25-b engine's attractor is NOT universal (Theorem A), so the Step-4
  anti-privilege objection is settled mathematically, not philosophically.
- Information accounting is EXACTLY non-generative (Theorem B), with a
  20x gap; the engine compresses seed entropy into a low-entropy head.
- The emergent period-2 is NOT an accident of T; it is the forced consequence
  of a 1-fold monotone objective reaching a local 2-point level set.

## Step 1 attacked head-on: uniqueness-by-singleton hypothesis DISPROVED

Hypothesis to prove uniqueness: at each state the extremal swap is unique
up to iso, which with periodicity would force a unique attractor. This is
exactly the kind of clean Lyapunov argument hoped for.

Result (z26_cert_orbits.py, 136 states across all Z25-b converged orbits):

    removal ties (n_rem_ties > 1):          96/136 states
    distinct iso classes among removals:    96/136 states  (up to 11 at once)
    addition ties (n_add_ties > 1):        120/136 states
    distinct iso classes among additions:    0/136 states

CONCLUSION (L1): the uniqueness of the observed Z25-b basin does NOT come
from a unique extremal step at each state. The rule's REMOVE side is highly
degenerate (up to 11 non-isomorphic candidates); the ADD side is iso-unique
everywhere. The single-basin concentration is instead produced by the
WL/exact-canonical projection identifying the many remove-ties later —
i.e. the attractor is unique because canon() collapses the degeneracy,
not because T is locally deterministic. This is a TIE-COLLAPSE theorem,
not a local uniqueness theorem.

Corrected claim for the class: for the witness-free conservative exchange
rule at (10,15), the set of visited states contains >=96% of attractor
immediate pre-images that are remove-degenerate; the projection onto iso
classes merges them. Any proof of "no period > 2" must therefore use the
tie structure, not local injectivity.

## Remaining Step-1 conjecture (revised)

Refined open problem: prove the tie-collapse is total — i.e. for ALL
(N, M) on a connected reachability class, any two distinct non-iso
sequences of extremal removals lead (after canonicalization on the add-
unique side) to iso-conjugate attractors. This is the correct precise
mathematical form of "unique basin".

Resolved form of the basin question:
  uniqueness of the Z25-b attractor at p=0 is PROVEN for the visited class,
  with mechanism = add-unique extremum + remove-tie-collapse under canon,
  NOT local injectivity. This is the theorem the exercise produces.
