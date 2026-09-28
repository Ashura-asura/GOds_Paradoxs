g := SmallGroup(3,1);
irr := Irr(g);
chi := irr[2];
Print("chi(e) = ", chi(Identity(g)), "\n");
Print("chi(g1) = ", chi(g.1), "\n");
for x in Elements(g) do
  Print("el ", x, " -> ", chi(x), "\n");
od;
