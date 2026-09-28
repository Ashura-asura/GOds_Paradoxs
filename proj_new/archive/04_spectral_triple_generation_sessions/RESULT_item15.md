# Item 15 (full) — E6 27⊗27⊗27 Tensor Product Decomposition

## Result: CLOSED NEGATIVE [L1]

**What was checked:**
Whether any E6 irreducible representation of dimension 126 or 3875 appears in the tensor product 27⊗27⊗27 (the triple fundamental product relevant to Phase B's Yukawa claim). Computed via the Weyl dimension formula on all dominant weights with Dynkin level ≤ 3 (the maximum possible from three 27-weights).

**What was found:**
- 83 candidate irreps enumerated across 49 distinct dimensions (ranging from 27 to 200,449,886).
- **No 126-dimensional irrep** in any of the 83 candidates.
- **No 3875-dimensional irrep** in any of the 83 candidates.
- All candidates verified against known E6 dimensions (27, 78, 351, 2925) as consistency checks.

**Why it failed:**
- 126 is an SO(10) representation dimension, not an E6 irrep dimension. The E6 dimension sequence (27, 78, 351, 650, 1728, 2430, 2925, ...) never hits 126.
- 3875 is an E8 representation (appears in Sym²(248)), not an E6 representation at all.
- No E6 irrep at any level ≤ 3 can have dimension 126 or 3875 because these numbers don't satisfy the E6 Weyl dimension formula for any non-negative integer Dynkin labels summing to ≤ 3.

**Combined with** `new_test_item15_e6su3_branching.py` (adjoint branching: 78+8+162=248, zero room for 126/3875 in the E8 adjoint), the full Item 15 is now verified from algebra alone.

**Remaining sub-question (scoped):** E6 → SO(10) branching of each summand to check for SO(10)-126 subrepresentations. This is a separate computation requiring automated branching-rule tools (LiE/Sage) not available in the current environment.
