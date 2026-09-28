from fractions import Fraction

def alpha_bourbaki():
    a1 = [Fraction(0)] * 8
    a1[0], a1[7] = Fraction(1, 2), Fraction(1, 2)
    for i in range(1, 7):
        a1[i] = -Fraction(1, 2)
    a2 = [Fraction(0)] * 8
    a2[0], a2[1] = Fraction(1), Fraction(1)
    A = [a1, a2]
    for i in range(1, 7):
        v = [Fraction(0)] * 8
        v[i - 1], v[i] = -Fraction(1), Fraction(1)
        A.append(v)
    return A

A = alpha_bourbaki()
print("alpha1 =", A[0])
print("alpha2 =", A[1])
print("alpha3 =", A[2])
print("alpha8 =", A[7])

# test: express alpha2 itself -> should be e_2 (the second basis vector)
def matvec(m, v):
    n = len(m)
    M = [row[:] + [v[i]] for i, row in enumerate(m)]
    for col in range(n):
        piv = next(r for r in range(col, n) if M[r][col] != 0)
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [x / pv for x in M[col]]
        for r in range(n):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f * y for x, y in zip(M[r], M[col])]
    return [M[i][n] for i in range(n)]

e2 = [Fraction(0)] * 8; e2[1] = Fraction(1)
print("coeffs of alpha2:", matvec(A, e2))
