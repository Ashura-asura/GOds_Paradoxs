import numpy as np

# Bourbaki E8 simple roots in e-basis
alphas = []
v = np.zeros(8); v[0], v[7] = 0.5, 0.5
for i in range(1, 7):
    v[i] = -0.5
alphas.append(v.copy())
alphas.append(np.array([1., 1., 0, 0, 0, 0, 0, 0]))
for i in range(1, 7):
    v = np.zeros(8); v[i - 1], v[i] = -1, 1
    alphas.append(v)
A = np.array(alphas)  # rows = alphas in e-basis

# actual inner products alpha_i . alpha_j:
G_e = A @ A.T
print("alpha_i . alpha_j (e-basis):")
print(np.rint(G_e).astype(int))

# expected Cartan matrix
C = np.array([
[2,0,-1,0,0,0,0,0],
[0,2,0,-1,0,0,0,0],
[-1,0,2,-1,0,0,0,0],
[0,-1,-1,2,-1,0,0,0],
[0,0,0,-1,2,-1,0,0],
[0,0,0,0,-1,2,-1,0],
[0,0,0,0,0,-1,2,-1],
[0,0,0,0,0,0,-1,2]], dtype=float)

print("\nEqual to C?", np.allclose(G_e, C))

# now b2 in e-basis and its claimed alpha coords:
b2 = np.array([1., 0, -1., 0, 0, 0, 0, 0])
a2c2 = np.array([-2., -2., -4, -5, -4, -3, -2, -1])
print("\nreconstruct b2 from alpha coords:", np.round(a2c2 @ A, 6), " matches b2?", np.allclose(a2c2 @ A, b2))

# s4 e-vector and its claimed alpha coords:
s4 = np.array([-0.5, 0.5, -0.5, 0.5, 0.5, -0.5, -0.5, 0.5])
e6c4 = np.array([1., 1, 2, 2, 2, 1, 0, 0])
print("reconstruct s4 from alpha coords:", np.round(e6c4 @ A, 6), " matches s4?", np.allclose(e6c4 @ A, s4))

# inner product in both bases:
print("\nb2 . s4 (e-basis):", b2 @ s4)
print("a2c2^T C e6c4:", a2c2 @ C @ e6c4)
