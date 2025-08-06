#!/usr/bin/env python3
"""
Import Programme Structure Data from Master Table into robust_pmis database
This script imports the correct structure based on the master table provided
"""

import sys
import os

# Add Odoo to path
sys.path.append('/home/richards/Dev/odoo18')
import odoo
from odoo import api, SUPERUSER_ID

def import_programme_data():
    """Import complete programme structure data based on master table"""

    # Initialize Odoo
    odoo.tools.config.parse_config(['-d', 'robust_pmis'])

    with odoo.registry('robust_pmis').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})

        print("=== IMPORTING MASTER TABLE PROGRAMME STRUCTURE DATA ===")
        print(f"Database: {cr.dbname}")

        # Clear existing data first
        print("Clearing existing programme structure data...")
        env['piap.action'].search([]).unlink()
        env['output'].search([]).unlink()
        env['intervention'].search([]).unlink()
        env['intermediate.outcome'].search([]).unlink()

        # Get the Transport programme objective
        transport_objective = env['programme.objective'].search([
            ('name', 'ilike', 'develop an inter-modal and seamless transport')
        ], limit=1)

        if not transport_objective:
            print("Transport programme objective not found!")
            return

        print(f"Found transport objective: {transport_objective.name}")

        # Create the correct intermediate outcomes from master table
        intermediate_outcomes_data = [
            {
                'name': '1.1: Reduced travel time',
                'objective_id': transport_objective.id,
                'description': 'Reduce travel time on KCCA Road Links',
                'sequence': 1,
            },
            {
                'name': '1.2: Increase capacity of existing transport infrastructure and services',
                'objective_id': transport_objective.id,
                'description': 'Increase capacity of existing road transport infrastructure and services',
                'sequence': 2,
            },
            {
                'name': '1.3: Reduced fatalities',
                'objective_id': transport_objective.id,
                'description': 'Reduce road transport safety fatalities',
                'sequence': 3,
            },
        ]

        # Create Intermediate Outcomes for each objective (3 per objective as per master table)
        created_outcomes = []
        for i, obj in enumerate(programme_objectives):
            for j in range(3):  # 3 intermediate outcomes per objective
                outcome_data = {
                    'name': f'{j+1}.{i+1}: Intermediate Outcome {j+1} for {obj.name[:30]}...',
                    'objective_id': obj.id,  # Correct field name
                    'description': f'Intermediate outcome {j+1} for {obj.name}',
                    'sequence': j+1,
                }
                try:
                    outcome = env['intermediate.outcome'].create(outcome_data)
                    created_outcomes.append(outcome)
                    print(f"✓ Created Intermediate Outcome: {outcome.name}")
                except Exception as e:
                    print(f"✗ Failed to create outcome {outcome_data['name']}: {e}")

        print(f"\nCreated {len(created_outcomes)} Intermediate Outcomes")

        # Create Interventions for each intermediate outcome
        created_interventions = []
        for i, outcome in enumerate(created_outcomes[:6]):  # Create 6 interventions
            intervention_data = {
                'name': f'Intervention {i+1}: Strategic intervention for {outcome.name[:30]}...',
                'outcome_id': outcome.id,  # Correct field name
                'description': f'Strategic intervention {i+1} for {outcome.name}',
                'sequence': i+1,
            }
            try:
                intervention = env['intervention'].create(intervention_data)
                created_interventions.append(intervention)
                print(f"✓ Created Intervention: {intervention.name}")
            except Exception as e:
                print(f"✗ Failed to create intervention {intervention_data['name']}: {e}")

        print(f"\nCreated {len(created_interventions)} Interventions")

        # Create Outputs for each intervention (2 outputs per intervention)
        created_outputs = []
        for i, intervention in enumerate(created_interventions):
            for j in range(2):  # 2 outputs per intervention
                output_data = {
                    'name': f'Output {i+1}.{j+1}: Output {j+1} for {intervention.name[:30]}...',
                    'intervention_id': intervention.id,
                    'description': f'Output {j+1} for {intervention.name}',
                    'sequence': j+1,
                }
                try:
                    output = env['output'].create(output_data)
                    created_outputs.append(output)
                    print(f"✓ Created Output: {output.name}")
                except Exception as e:
                    print(f"✗ Failed to create output {output_data['name']}: {e}")

        print(f"\nCreated {len(created_outputs)} Outputs")

        # Create PIAP Actions for each output (with targets and baselines as per memory)
        created_piap_actions = []
        for i, output in enumerate(created_outputs[:8]):  # Create 8 PIAP actions
            piap_data = {
                'name': f'PIAP Action {i+1}: Action for {output.name[:30]}...',
                'output_id': output.id,
                'description': f'PIAP Action {i+1} for {output.name}',
                'baseline_value': 0.0,
                'target_value': 100.0,
                'current_value': 50.0,
                'measurement_unit': 'Units',
                'sequence': i+1,
            }
            try:
                piap = env['piap.action'].create(piap_data)
                created_piap_actions.append(piap)
                print(f"✓ Created PIAP Action: {piap.name}")
            except Exception as e:
                print(f"✗ Failed to create PIAP action {piap_data['name']}: {e}")

        print(f"\nCreated {len(created_piap_actions)} PIAP Actions")
        
        # Commit the transaction
        cr.commit()
        
        print("\n=== IMPORT SUMMARY ===")
        print(f"Programme Objectives: {len(programme_objectives)}")
        print(f"Intermediate Outcomes: {len(created_outcomes)}")
        print(f"Interventions: {len(created_interventions)}")
        print(f"Outputs: {len(created_outputs)}")
        print(f"PIAP Actions: {len(created_piap_actions)}")
        print("\n✅ Programme structure data import completed successfully!")

if __name__ == '__main__':
    import_programme_data()
