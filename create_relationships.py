#!/usr/bin/env python3
"""
Script to manually create the strategic objective-programme relationships
"""

print("=== CREATING STRATEGIC OBJECTIVE-PROGRAMME RELATIONSHIPS ===\n")

# Define the relationships based on the master table
relationships = {
    'strategic_objective_economic_growth': [
        'programme_agro_industrialization',
        'programme_private_sector_dev', 
        'programme_transport_infrastructure',
        'programme_dev_plan_implementation',
        'programme_tourism_development',
        'programme_natural_resources',
        'programme_sustainable_urbanization',
        'programme_digital_transformation',
        'programme_sustainable_energy_dev'
    ],
    'strategic_objective_productivity_wellbeing': [
        'programme_human_capital_dev',
        'programme_sustainable_energy_dev'
    ],
    'strategic_objective_governance': [
        'programme_legislation_oversight',
        'programme_admin_justice',
        'programme_governance_security'
    ],
    'strategic_objective_climate_resilience': [
        'programme_natural_resources',
        'programme_dev_plan_implementation',
        'programme_digital_transformation'
    ],
    'strategic_objective_institutional_capacity': [
        'programme_natural_resources',
        'programme_dev_plan_implementation',
        'programme_public_sector_transformation'
    ]
}

# Get all strategic objectives and programmes
strategic_objectives = {obj.get_external_id()[obj.id]: obj for obj in env['strategic.objective'].search([])}
programmes = {prog.get_external_id()[prog.id]: prog for prog in env['kcca.programme'].search([])}

print(f"Found {len(strategic_objectives)} strategic objectives")
print(f"Found {len(programmes)} programmes")

# Create relationships
total_created = 0
for obj_xml_id, prog_xml_ids in relationships.items():
    # Find the strategic objective
    obj_full_id = f'robust_pmis.{obj_xml_id}'
    if obj_full_id not in strategic_objectives:
        print(f"Strategic objective not found: {obj_xml_id}")
        continue
    
    strategic_obj = strategic_objectives[obj_full_id]
    print(f"\nProcessing: {strategic_obj.name}")
    
    programme_ids = []
    for prog_xml_id in prog_xml_ids:
        prog_full_id = f'robust_pmis.{prog_xml_id}'
        if prog_full_id not in programmes:
            print(f"  Programme not found: {prog_xml_id}")
            continue
        
        programme = programmes[prog_full_id]
        programme_ids.append(programme.id)
        print(f"  + {programme.name}")
    
    # Create the many-to-many relationships
    if programme_ids:
        strategic_obj.write({
            'programme_ids': [(6, 0, programme_ids)]
        })
        total_created += len(programme_ids)
        print(f"  Created {len(programme_ids)} relationships")

print(f"\n=== TOTAL RELATIONSHIPS CREATED: {total_created} ===")

# Verify the relationships
print("\n=== VERIFICATION ===")
for obj in env['strategic.objective'].search([]):
    print(f"{obj.name}: {len(obj.programme_ids)} programmes")

# Force recomputation of strategic goal counts
strategic_goals = env['strategic.goal'].search([])
for goal in strategic_goals:
    goal.recompute_all_counts()
    print(f"\nStrategic Goal: {goal.name}")
    print(f"  Programme count: {goal.programme_count}")
    print(f"  Directorate count: {goal.directorate_count}")
    print(f"  Division count: {goal.division_count}")

print("\n=== COMPLETED ===")
