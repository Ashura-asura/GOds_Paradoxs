# Convert Bourbaki-numbered E8 coordinates to LiE numbering.
# LiE E8 diagram: chain 1-3-4-5-6-7-8, node 2 attached to node 3.
# Bourbaki E8 diagram: chain 1-3-4-5-6-7-8, node 2 attached to node 4.
# Fork node: LiE 3 = Bourbaki 4. Chain mapping from the fork:
#   LiE 3 -> Bour 4, LiE 4 -> Bour 5, ..., LiE 7 -> Bour 8, LiE 8 -> Bour 3
#   LiE 1 -> Bour 1, LiE 2 -> Bour 2
bour2lie = {1: 1, 2: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7, 3: 8}

def to_lie(c_bour):
    out = [0] * 8
    for b in range(1, 9):
        out[bour2lie[b] - 1] = c_bour[b - 1]
    return out

# A2 roots and E6 simple roots in Bourbaki coordinates (from tmp_e8_e6a2_exact2.py)
a2s1 = [0, -1, 0, 0, 0, 0, 0, 0]
a2s2 = [-2, -2, -4, -5, -4, -3, -2, -1]
e6s = [
    [0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [-1, -1, -1, -2, -1, -1, 0, 0],
    [1, 1, 2, 2, 2, 1, 0, 0],
    [1, 1, 1, 2, 1, 1, 1, 0],
    [-1, 0, -1, 0, 0, 0, 0, 0],
]

print("A2 simple roots (LiE coords):")
print("  a2s1:", to_lie(a2s1))
print("  a2s2:", to_lie(a2s2))
print("E6 simple roots (LiE coords):")
for s in e6s:
    print("  ", to_lie(s))
