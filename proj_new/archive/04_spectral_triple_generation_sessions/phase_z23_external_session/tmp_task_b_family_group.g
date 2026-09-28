# Phase Z23, Task B -- family-group uniqueness check (GAP 4.15.1)
# Question: is S3 the ONLY group, among all groups of order <= 60, that can
# play the role of the project's discrete family group?
#
# Criteria -- each is a physics input forced by previously established
# project results, NOT chosen to single out S3:
#  (i)   faithful real 2-dim irrep on the generation plane
#        (Task A: psi_3 acts as an exact 120-degree rotation on the
#         (H_alpha,H_beta) plane; the plane is a real irreducible S3 rep)
#  (ii)  an order-3 element acting as a 120-degree rotation (trace -1)
#        (this IS psi_3; Task A)
#  (iii) an order-2 element acting as a reflection (trace 0)
#        (the 2:1:1 mass degeneracy = reflection transposing two generations)
#  (iv)  a faithful action on the 3 labeled generations (3 mass matrices)
#
# Enumeration: exhaustive over ALL groups of order 2..60 (SmallGroup library).
#
# Note on GAP mechanics: characters are evaluated by conjugacy-class index
# (Val function), not by direct call -- class functions are not callable
# in this GAP build.

Val := function(chi, x)
  local g;
  g := UnderlyingGroup(chi);
  return chi[Position(ConjugacyClasses(g), ConjugacyClass(g, x))];
end;

FSIndicator := function(chi)
  local g;
  g := UnderlyingGroup(chi);
  return (1 / Order(g)) * Sum(Elements(g), x -> Val(chi, x ^ 2));
end;

PlaneTr := function(chi, x)
  if DegreeOfCharacter(chi) = 2 then
    return Val(chi, x);
  else
    return Val(chi, x) + Val(ComplexConjugate(chi), x);
  fi;
end;

total_groups := 0;
for n in [2..60] do
  total_groups := total_groups + NumberSmallGroups(n);
od;

census := 0;        # groups with a faithful real 2-dim irrep (criterion i)
rot_only := [];     # + 120-degree rotation element
refl_only := [];    # + reflection element
rotrefl := [];      # + both (ii) and (iii)

for n in [2..60] do
  for g in AllSmallGroups(n) do
    irr := Irr(g);
    chi := fail;
    for c in irr do
      if DegreeOfCharacter(c) = 2 and FSIndicator(c) = 1
         and KernelOfCharacter(c) = TrivialSubgroup(g) then
        chi := c;
        break;
      fi;
    od;
    if chi = fail then
      for c in irr do
        if DegreeOfCharacter(c) = 1 and c <> ComplexConjugate(c)
           and KernelOfCharacter(c) = TrivialSubgroup(g) then
          chi := c;
          break;
        fi;
      od;
    fi;
    if chi = fail then
      continue;
    fi;
    census := census + 1;
    rot_el := fail;
    refl_el := fail;
    for x in Elements(g) do
      if Order(x) = 3 and PlaneTr(chi, x) = -1 then
        rot_el := x;
        break;
      fi;
    od;
    for x in Elements(g) do
      if Order(x) = 2 and PlaneTr(chi, x) = 0 then
        refl_el := x;
        break;
      fi;
    od;
    if rot_el <> fail then
      Add(rot_only, [n, g]);
    fi;
    if refl_el <> fail then
      Add(refl_only, [n, g]);
    fi;
    if rot_el <> fail and refl_el <> fail then
      Add(rotrefl, [n, g, chi]);
    fi;
  od;
od;

Print("Phase Z23 Task B results\n");
Print("Groups of order 2..60 enumerated: ", total_groups, "\n");
Print("A. faithful real 2-dim plane rep (criterion i): ", census, " groups\n");
Print("   (all such groups are C_n or D_2n -- printed as structure only)\n");
Print("\n");
Print("B. ...containing a 120-degree rotation (i+ii): ", Length(rot_only),
      " groups\n");
for rec_g in rot_only do
  Print("   ", StructureDescription(rec_g[2]), "\n");
od;
Print("\n");
Print("C. ...containing a reflection (i+iii): ", Length(refl_only),
      " groups\n");
for rec_g in refl_only do
  Print("   ", StructureDescription(rec_g[2]), "\n");
od;
Print("\n");
Print("D. ...containing BOTH (i+ii+iii): ", Length(rotrefl), " groups\n");
for rec_g in rotrefl do
  Print("   ", StructureDescription(rec_g[2]), "\n");
od;
Print("\n");

Print("E. criterion (iv): faithful action on 3 points -- of the ",
      Length(rotrefl), " groups in D, which embed into S3?\n");
s3 := SymmetricGroup(3);
s3_subgroups := AllSubgroups(s3);
survivors := [];
for rec_g in rotrefl do
  g := rec_g[2];
  faithful3 := false;
  for h in s3_subgroups do
    if IsomorphismGroups(g, h) <> fail then
      faithful3 := true;
      break;
    fi;
  od;
  Print("   ", StructureDescription(g), "  faithful-on-3-points: ",
        faithful3, "\n");
  if faithful3 then
    Add(survivors, rec_g);
  fi;
od;
Print("\n");

Print("F. FINAL: groups satisfying ALL of (i)-(iv): ", Length(survivors),
      "\n");
for rec_g in survivors do
  g := rec_g[2];
  chi := rec_g[3];
  Print("   order ", Order(g), ": ", StructureDescription(g), "\n");
  all_pairs_generate_s3 := true;
  for x in Elements(g) do
    for y in Elements(g) do
      if Order(x) = 3 and PlaneTr(chi, x) = -1
         and Order(y) = 2 and PlaneTr(chi, y) = 0 then
        sub := Subgroup(g, [x, y]);
        if IsomorphismGroups(sub, SymmetricGroup(3)) = fail
           or Order(sub) <> 6 then
          all_pairs_generate_s3 := false;
        fi;
      fi;
    od;
  od;
  Print("   every (rotation,reflection) pair generates an S3: ",
        all_pairs_generate_s3, "\n");
od;
