for n in [6, 12] do
  g := DihedralGroup(2 * n);
  gens := GeneratorsOfGroup(g);
  Print("D", 2 * n, " gens: ", List(gens, Order), "\n");
  for t in gens do
    Print("   generator order ", Order(t), "\n");
  od;
  r := gens[1];
  s := gens[2];
  Print("   r order ", Order(r), ", s order ", Order(s), "\n");
  if Order(r) mod 3 = 0 then
    t := r ^ (Order(r) / 3);
    Print("   t = r^(ord/3) order ", Order(t), "\n");
    sub := Subgroup(g, [t, s]);
    Print("   <t, s> order ", Order(sub), "\n");
    Print("   <t,s> ~ S3? ", not IsomorphismGroups(sub, SymmetricGroup(3)) = fail, "\n");
  fi;
od;
