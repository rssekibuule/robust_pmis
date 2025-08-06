#!/usr/bin/env python3
"""
Script to restore Transport Programme Performance Indicators
This script creates the complete hierarchy for the Integrated Transport Infrastructure and Services programme
"""

def restore_transport_indicators(env):
    """
    Restore the Transport Programme indicators with proper hierarchical relationships
    """
    print("=== RESTORING TRANSPORT PROGRAMME INDICATORS ===")
    
    # Step 1: Find or create the Programme
    programme = env['kcca.programme'].search([
        ('name', '=', 'Integrated Transport Infrastructure and Services')
    ])

    if not programme:
        print("✗ Programme not found. Please create the programme first.")
        return

    print(f"Found existing programme: {programme.name}")

    # Step 2: Create Programme Objective
    prog_objective_data = {
        'name': 'To develop the road and seamless transport infrastructure and services',
        'programme_id': programme.id
    }

    existing_objective = env['programme.objective'].search([
        ('name', '=', prog_objective_data['name']),
        ('programme_id', '=', programme.id)
    ])

    if not existing_objective:
        prog_objective = env['programme.objective'].create(prog_objective_data)
        print(f"Creating programme objective: {prog_objective_data['name']}")
    else:
        prog_objective = existing_objective[0]
        print("Found existing programme objective")

    # Step 3: Create Outcomes (Intermediate Outcomes)
    outcomes_data = [
        {
            'name': 'Reduced travel time',
            'description': 'Intermediate Outcome 1.1',
            'objective_id': prog_objective.id
        },
        {
            'name': 'Increased stock of transport infrastructure',
            'description': 'Intermediate Outcome 1.2',
            'objective_id': prog_objective.id
        },
        {
            'name': 'Enhanced transport safety',
            'description': 'Intermediate Outcome 1.3',
            'objective_id': prog_objective.id
        }
    ]

    outcomes = {}
    for outcome_data in outcomes_data:
        existing = env['intermediate.outcome'].search([
            ('name', '=', outcome_data['name']),
            ('objective_id', '=', outcome_data['objective_id'])
        ])

        if not existing:
            print(f"Creating outcome: {outcome_data['name']}")
            outcome = env['intermediate.outcome'].create(outcome_data)
        else:
            outcome = existing[0]
            print(f"Found existing outcome: {outcome_data['name']}")

        outcomes[outcome_data['name']] = outcome
    
    # Step 4: Create Interventions first (required for outputs)
    interventions_data = [
        {
            'name': 'Construct and upgrade strategic transport infrastructure',
            'description': 'Intervention 1.1.1',
            'outcome_id': outcomes['Reduced travel time'].id
        },
        {
            'name': 'Increase capacity of existing transport infrastructure and services',
            'description': 'Intervention 1.2.1',
            'outcome_id': outcomes['Increased stock of transport infrastructure'].id
        },
        {
            'name': 'Enhance transport safety',
            'description': 'Intervention 1.3.1',
            'outcome_id': outcomes['Enhanced transport safety'].id
        }
    ]
    
    interventions = {}
    for intervention_data in interventions_data:
        existing = env['intervention'].search([
            ('name', '=', intervention_data['name']),
            ('outcome_id', '=', intervention_data['outcome_id'])
        ])

        if not existing:
            print(f"Creating intervention: {intervention_data['name']}")
            intervention = env['intervention'].create(intervention_data)
        else:
            intervention = existing[0]
            print(f"Found existing intervention: {intervention_data['name']}")

        interventions[intervention_data['name']] = intervention

    # Step 5: Create Outputs
    outputs_data = [
        {
            'name': 'Capacity of existing transport infrastructure and services upgraded/enhanced',
            'description': 'Output 1.2.1',
            'intervention_id': interventions['Increase capacity of existing transport infrastructure and services'].id
        },
        {
            'name': 'Road Transport Safety Enhanced',
            'description': 'Output 1.3.1',
            'intervention_id': interventions['Enhance transport safety'].id
        }
    ]

    outputs = {}
    for output_data in outputs_data:
        existing = env['output'].search([
            ('name', '=', output_data['name']),
            ('intervention_id', '=', output_data['intervention_id'])
        ])

        if not existing:
            print(f"Creating output: {output_data['name']}")
            output = env['output'].create(output_data)
        else:
            output = existing[0]
            print(f"Found existing output: {output_data['name']}")

        outputs[output_data['name']] = output
    
    # Step 6: Create Performance Indicators
    print(f"\nCreating performance indicators...")
    print("----------------------------------------------------------------")

    indicators_data = [
        # Outcome 1.1 indicators
        {
            'name': 'Average Travel time (Minutes) on KCCA Road Links',
            'outcome_id': outcomes['Reduced travel time'].id,
            'baseline_value': 4.2,
            'target_value': 3.0,
            'current_value': 4.2,
            'measurement_unit': 'Minutes'
        },
        {
            'name': 'Proportion of Commuters using mass public transport (Bus & BRT)',
            'outcome_id': outcomes['Reduced travel time'].id,
            'baseline_value': 5.0,
            'target_value': 30.0,
            'current_value': 5.0,
            'measurement_unit': 'Percentage'
        },

        # Intervention 1.1.1 indicators
        {
            'name': 'Km of BRT Network constructed',
            'outcome_id': outcomes['Reduced travel time'].id,
            'baseline_value': 0.0,
            'target_value': 14.4,
            'current_value': 0.0,
            'measurement_unit': 'Kilometers'
        },
        {
            'name': 'No of Traffic Diversion Flyovers constructed',
            'outcome_id': outcomes['Reduced travel time'].id,
            'baseline_value': 2.0,
            'target_value': 3.0,
            'current_value': 2.0,
            'measurement_unit': 'Number'
        },
        {
            'name': 'Km of meter gauge commuter rail revamped',
            'outcome_id': outcomes['Reduced travel time'].id,
            'baseline_value': 26.8,
            'target_value': 20.0,
            'current_value': 26.8,
            'measurement_unit': 'Kilometers'
        },
        {
            'name': 'Km of Cable Car System constructed',
            'outcome_id': outcomes['Reduced travel time'].id,
            'baseline_value': 0.0,
            'target_value': 7.0,
            'current_value': 0.0,
            'measurement_unit': 'Kilometers'
        },
        {
            'name': '% completion of Feasibility study & detailed design for LRT',
            'outcome_id': outcomes['Reduced travel time'].id,
            'baseline_value': 0.0,
            'target_value': 100.0,
            'current_value': 0.0,
            'measurement_unit': 'Percentage'
        },

        # Outcome 1.2 indicators
        {
            'name': 'Proportion of city road network paved',
            'outcome_id': outcomes['Increased stock of transport infrastructure'].id,
            'baseline_value': 17.0,
            'target_value': 54.0,
            'current_value': 17.0,
            'measurement_unit': 'Percentage'
        },
        {
            'name': 'Km of KCCA Road Paved',
            'outcome_id': outcomes['Increased stock of transport infrastructure'].id,
            'baseline_value': 371.5,
            'target_value': 1394.88,
            'current_value': 371.5,
            'measurement_unit': 'Kilometers'
        }
    ]

    created_count = 0
    for indicator_data in indicators_data:
        # Search by name and outcome_id to avoid duplicates
        search_domain = [('name', '=', indicator_data['name'])]
        if 'outcome_id' in indicator_data:
            search_domain.append(('outcome_id', '=', indicator_data['outcome_id']))
        elif 'output_id' in indicator_data:
            search_domain.append(('output_id', '=', indicator_data['output_id']))

        existing = env['performance.indicator'].search(search_domain)

        if not existing:
            indicator = env['performance.indicator'].create(indicator_data)
            print(f"✓ Created: {indicator_data['name']}")
            created_count += 1
        else:
            print(f"- Exists: {indicator_data['name']}")

    print(f"\n=== SUMMARY ===")
    print(f"✓ Programme: {programme.name}")
    print(f"✓ Programme Objective: {prog_objective.name}")
    print(f"✓ Outcomes: {len(outcomes)} created")
    print(f"✓ Interventions: {len(interventions)} created")
    print(f"✓ Outputs: {len(outputs)} created")
    print(f"✓ Performance Indicators: {created_count} created")
    print("================================================================")

    return True

if __name__ == "__main__":
    print("This script should be run from within Odoo shell")
    print("Usage: python3 odoo-bin shell -d your_database")
    print("Then: exec(open('restore_transport_indicators_fixed.py').read())")
    print("Then: restore_transport_indicators(env)")
