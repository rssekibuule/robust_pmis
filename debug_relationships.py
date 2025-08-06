#!/usr/bin/env python3
"""
Debug script to check relationships between strategic objectives and programmes
"""

print("=== DEBUGGING STRATEGIC GOAL RELATIONSHIPS ===\n")

# Check strategic goals
strategic_goals = env['strategic.goal'].search([])
print(f"Strategic Goals: {len(strategic_goals)}")
for goal in strategic_goals:
    print(f"  - {goal.name}")

print()

# Check strategic objectives
strategic_objectives = env['strategic.objective'].search([])
print(f"Strategic Objectives: {len(strategic_objectives)}")
for obj in strategic_objectives:
    print(f"  - {obj.name} (Goal: {obj.strategic_goal_id.name})")
    print(f"    Programme count: {len(obj.programme_ids)}")
    for prog in obj.programme_ids:
        print(f"      * {prog.name}")

print()

# Check programmes
programmes = env['kcca.programme'].search([])
print(f"Programmes: {len(programmes)}")
for prog in programmes:
    print(f"  - {prog.name}")
    print(f"    Strategic objective count: {len(prog.strategic_objective_ids)}")
    for obj in prog.strategic_objective_ids:
        print(f"      * {obj.name}")

print()

# Check the many-to-many table directly
print("=== CHECKING MANY-TO-MANY TABLE ===")
env.cr.execute("SELECT COUNT(*) FROM objective_programme_rel")
count = env.cr.fetchone()[0]
print(f"Records in objective_programme_rel table: {count}")

if count > 0:
    env.cr.execute("""
        SELECT so.name as objective_name, kp.name as programme_name 
        FROM objective_programme_rel opr
        JOIN strategic_objective so ON so.id = opr.objective_id
        JOIN kcca_programme kp ON kp.id = opr.programme_id
        LIMIT 10
    """)
    results = env.cr.fetchall()
    print("Sample relationships:")
    for obj_name, prog_name in results:
        print(f"  {obj_name} -> {prog_name}")

print()

# Check programme-directorate relationships
print("=== CHECKING PROGRAMME-DIRECTORATE RELATIONSHIPS ===")
prog_dir_rels = env['programme.directorate.rel'].search([])
print(f"Programme-Directorate relationships: {len(prog_dir_rels)}")
for rel in prog_dir_rels[:5]:  # Show first 5
    print(f"  {rel.programme_id.name} -> {rel.directorate_id.name}")

print()

# Check division-programme relationships
print("=== CHECKING DIVISION-PROGRAMME RELATIONSHIPS ===")
div_prog_rels = env['division.programme.rel'].search([])
print(f"Division-Programme relationships: {len(div_prog_rels)}")
for rel in div_prog_rels[:5]:  # Show first 5
    print(f"  {rel.division_id.name} -> {rel.programme_id.name}")

print("\n=== DEBUG COMPLETED ===")
