# -*- coding: utf-8 -*-
print("🚀 STARTING: Enhance Infrastructure Development Objective")

# Find the Strategic Objective for "Infrastructure Development"
objective = env['strategic.objective'].search([('name', '=', 'Infrastructure Development')], limit=1)

if not objective:
    print("❌ ERROR: Strategic Objective 'Infrastructure Development' not found.")
    print("Please ensure this objective exists.")
else:
    print(f"✅ Found Strategic Objective: {objective.name} (ID: {objective.id})")

    # --- 1. KRA: Road Infrastructure ---
    kra_road, created = env['key.result.area'].get_or_create({
        'name': 'Improved Road Network',
        'strategic_objective_id': objective.id,
        'description': 'Focuses on expanding and upgrading the city\'s road network.'
    })
    if created: print(f"   - Created KRA: {kra_road.name}")
    env['key.performance.indicator'].get_or_create({
        'name': 'Kilometers of Paved Roads Added',
        'kra_id': kra_road.id, 'target_value': 50, 'current_value': 15, 'unit_of_measure': 'km'
    })

    # --- 2. KRA: Public Transport ---
    kra_transport, created = env['key.result.area'].get_or_create({
        'name': 'Efficient Public Transportation',
        'strategic_objective_id': objective.id,
        'description': 'Improving the public transport system.'
    })
    if created: print(f"   - Created KRA: {kra_transport.name}")
    env['key.performance.indicator'].get_or_create({
        'name': 'Public Transport On-Time Arrival Rate',
        'kra_id': kra_transport.id, 'target_value': 95, 'current_value': 78, 'unit_of_measure': '%'
    })

    # --- 3. KRA: Traffic Management ---
    kra_traffic, created = env['key.result.area'].get_or_create({
        'name': 'Advanced Traffic Management',
        'strategic_objective_id': objective.id,
        'description': 'Implementing smart solutions to reduce congestion.'
    })
    if created: print(f"   - Created KRA: {kra_traffic.name}")
    env['key.performance.indicator'].get_or_create({
        'name': 'Reduction in Average Commute Time',
        'kra_id': kra_traffic.id, 'target_value': 20, 'current_value': 5, 'unit_of_measure': '%'
    })

    # --- 4. KRA: Pedestrian and Cycling Infrastructure ---
    kra_non_motorized, created = env['key.result.area'].get_or_create({
        'name': 'Safe Pedestrian & Cycling Paths',
        'strategic_objective_id': objective.id,
        'description': 'Developing infrastructure for non-motorized transport.'
    })
    if created: print(f"   - Created KRA: {kra_non_motorized.name}")
    env['key.performance.indicator'].get_or_create({
        'name': 'Kilometers of New Cycling Lanes',
        'kra_id': kra_non_motorized.id, 'target_value': 100, 'current_value': 25, 'unit_of_measure': 'km'
    })

    # --- 5. KRA: Infrastructure Resilience ---
    kra_resilience, created = env['key.result.area'].get_or_create({
        'name': 'Climate-Resilient Infrastructure',
        'strategic_objective_id': objective.id,
        'description': 'Ensuring infrastructure can withstand climate change impacts.'
    })
    if created: print(f"   - Created KRA: {kra_resilience.name}")
    env['key.performance.indicator'].get_or_create({
        'name': 'Number of Upgraded Drainage Systems',
        'kra_id': kra_resilience.id, 'target_value': 20, 'current_value': 8, 'unit_of_measure': 'systems'
    })

    # Link the programmes to the objective
    programmes = env['kcca.programme'].search([('name', 'ilike', 'transport')])
    if programmes:
        objective.programme_ids = [(6, 0, programmes.ids)]
        print(f"   - Linked {len(programmes)} transport programmes.")

    env.cr.commit()
    print("✅ DONE: Demo data for Infrastructure Development created successfully.")
