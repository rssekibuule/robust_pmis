#!/usr/bin/env python3
"""
Script to verify division count calculation
"""

print("=== VERIFYING DIVISION COUNT ===\n")

# Get the strategic goal
strategic_goal = env['strategic.goal'].search([], limit=1)
print(f"Strategic Goal: {strategic_goal.name}")

# Get programmes from strategic objectives
programmes = strategic_goal.strategic_objective_ids.mapped('programme_ids')
print(f"Total programmes: {len(programmes)}")

# Check implementing divisions for each programme
all_divisions = env['kcca.division']
for prog in programmes:
    implementing_divs = prog.implementing_division_ids
    print(f"  {prog.name}: {len(implementing_divs)} divisions")
    for div in implementing_divs:
        print(f"    - {div.name}")
    all_divisions = all_divisions | implementing_divs

print(f"\nUnique divisions implementing programmes: {len(all_divisions)}")
for div in all_divisions:
    print(f"  - {div.name} ({div.directorate_id.name})")

# Check division-programme relationships
div_prog_rels = env['division.programme.rel'].search([
    ('programme_id', 'in', programmes.ids)
])
print(f"\nDivision-Programme relationships: {len(div_prog_rels)}")

unique_divisions_from_rels = div_prog_rels.mapped('division_id')
print(f"Unique divisions from relationships: {len(unique_divisions_from_rels)}")

# Force recomputation
strategic_goal._compute_smart_card_counts()
print(f"\nAfter recomputation:")
print(f"  Division count: {strategic_goal.division_count}")

print("\n=== COMPLETED ===")
