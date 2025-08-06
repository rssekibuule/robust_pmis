#!/usr/bin/env python3
"""
Script to fix the zero counts in the strategic goal dashboard
"""

# Force recomputation of strategic goal counts
strategic_goals = env['strategic.goal'].search([])
print(f"Found {len(strategic_goals)} strategic goals")

for goal in strategic_goals:
    print(f"\nProcessing: {goal.name}")
    
    # Get strategic objectives
    objectives = goal.strategic_objective_ids
    print(f"  Strategic Objectives: {len(objectives)}")
    
    # Get programmes from objectives
    programmes = objectives.mapped('programme_ids')
    print(f"  Programmes: {len(programmes)}")
    
    # Get directorates from programme relationships
    prog_dir_rels = env['programme.directorate.rel'].search([
        ('programme_id', 'in', programmes.ids)
    ])
    directorates = prog_dir_rels.mapped('directorate_id')
    print(f"  Directorates: {len(directorates)}")
    
    # Get divisions from programme relationships
    div_prog_rels = env['division.programme.rel'].search([
        ('programme_id', 'in', programmes.ids)
    ])
    divisions = div_prog_rels.mapped('division_id')
    print(f"  Divisions: {len(divisions)}")
    
    # Force recomputation
    goal.recompute_all_counts()
    
    print(f"  After recomputation:")
    print(f"    Programme count: {goal.programme_count}")
    print(f"    Directorate count: {goal.directorate_count}")
    print(f"    Division count: {goal.division_count}")

print("\nRecomputation completed!")
