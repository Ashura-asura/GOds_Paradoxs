# Task B supplementary: near-miss structure + S3 character table
s3 := SymmetricGroup(3);
Print("S3: order ", Order(s3), ", structure ", StructureDescription(s3), "\n");
Print("Irr(S3):\n");
for chi in Irr(s3) do
  Print("   deg ", DegreeOfCharacter(chi), " values ",
        List(ConjugacyClasses(s3), c -> chi[Position(ConjugacyClasses(s3), c)]),
        "\n");
od;
Print("\n");
Print("D12 = S3 x C2? ",
      not IsomorphismGroups(DihedralGroup(12),
        DirectProduct(SymmetricGroup(3), CyclicGroup(2))) = fail, "\n");
Print("\n");
Print("Near-miss structure of the 10 groups in D (all contain S3):\n");
for n in [3, 6, 9, 12, 15, 18, 21, 24, 27, 30] do
  g := DihedralGroup(2 * n);
  r := First(Elements(g), x -> Order(x) = n);
  s := First(Elements(g), x -> Order(x) = 2 and x ^ 2 = Identity(g)
             and not r ^ 2 = x);
  t := r ^ (n / 3);
  sub := Subgroup(g, [t, s]);
  Print("   D", 2 * n, ": <r^(", n, "/3), s> has order ", Order(sub),
        ", ~S3? ", not IsomorphismGroups(sub, s3) = fail, "\n");
od;
