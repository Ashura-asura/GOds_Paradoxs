import numpy as np

# Bourbaki E8 Cartan matrix
C = np.array([
[2,0,-1,0,0,0,0,0],
[0,2,0,-1,0,0,0,0],
[-1,0,2,-1,0,0,0,0],
[0,-1,-1,2,-1,0,0,0],
[0,0,0,-1,2,-1,0,0],
[0,0,0,0,-1,2,-1,0],
[0,0,0,0,0,-1,2,-1],
[0,0,0,0,0,0,-1,2]], dtype=float)

# inner product in alpha-basis: <x,y> = x^T C y (root coordinates in simple-root basis)
G = C

def ip(x, y):
    return x @ G @ y

e6 = np.array([
[0,0,0,0,0,1,0,0],
[0,0,0,0,0,0,0,1],
[-1,-1,-1,-2,-1,-1,0,0],
[1,1,2,2,2,1,0,0],
[1,1,1,2,1,1,1,0],
[-1,0,-1,0,0,0,0,0]], dtype=float)

a2 = np.array([
[0,-1,0,0,0,0,0,0],
[-2,-2,-4,-5,-4,-3,-2,-1]], dtype=float)

print("inner products A2 x E6 (must be 0):")
for i in range(2):
    for j in range(6):
        v = ip(a2[i], e6[j])
        print(f"  a2[{i}] . e6[{j}] = {v:.4f}")

print("\ninner products among E6 simples:")
for i in range(6):
    print("  ", [round(ip(e6[i], e6[j]), 4) for j in range(6)])
print("\ninner products among A2:")
for i in range(2):
    print("  ", [round(ip(a2[i], a2[j]), 4) for j in range(2)])
