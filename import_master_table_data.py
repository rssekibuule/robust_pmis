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

def import_master_table_data():
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
        
        print("Creating intermediate outcomes...")
        outcomes = []
        for outcome_data in intermediate_outcomes_data:
            outcome = env['intermediate.outcome'].create(outcome_data)
            outcomes.append(outcome)
            print(f"  Created: {outcome.name}")
        
        # Create interventions based on master table structure
        interventions_data = [
            # For Outcome 1.1: Reduced travel time
            {
                'name': '1.1.1: Construct and upgrade strategic transport infrastructure',
                'outcome_id': outcomes[0].id,
                'description': 'Construct and upgrade strategic transport infrastructure',
                'sequence': 1,
            },
            # For Outcome 1.2: Increase capacity
            {
                'name': '1.2.1: Capacity of existing road transport infrastructure and services increased',
                'outcome_id': outcomes[1].id,
                'description': 'Increase capacity of existing road transport infrastructure and services',
                'sequence': 1,
            },
            # For Outcome 1.3: Reduced fatalities  
            {
                'name': '1.3.1: Road Transport Safety Enhanced',
                'outcome_id': outcomes[2].id,
                'description': 'Enhance road transport safety to reduce fatalities',
                'sequence': 1,
            },
        ]
        
        print("Creating interventions...")
        interventions = []
        for intervention_data in interventions_data:
            intervention = env['intervention'].create(intervention_data)
            interventions.append(intervention)
            print(f"  Created: {intervention.name}")
        
        # Create outputs based on master table
        outputs_data = [
            # For Intervention 1.1.1
            {
                'name': '1.1.1.1: Strategic transport infrastructure constructed and upgraded',
                'intervention_id': interventions[0].id,
                'description': 'Strategic transport infrastructure constructed and upgraded',
                'sequence': 1,
            },
            # For Intervention 1.2.1
            {
                'name': '1.2.1.1: Capacity of existing road transport infrastructure and services increased',
                'intervention_id': interventions[1].id,
                'description': 'Capacity of existing road transport infrastructure and services increased',
                'sequence': 1,
            },
            {
                'name': '1.2.1.2: Implement road improvement projects',
                'intervention_id': interventions[1].id,
                'description': 'Implement road improvement projects under various funding sources',
                'sequence': 2,
            },
            # For Intervention 1.3.1
            {
                'name': '1.3.1.1: Road Transport Safety Enhanced',
                'intervention_id': interventions[2].id,
                'description': 'Road transport safety enhanced through various measures',
                'sequence': 1,
            },
        ]
        
        print("Creating outputs...")
        outputs = []
        for output_data in outputs_data:
            output = env['output'].create(output_data)
            outputs.append(output)
            print(f"  Created: {output.name}")
        
        # Create PIAP Actions based on master table with ALL data
        piap_actions_data = [
            # For Output 1.1.1.1 - Strategic transport infrastructure
            {
                'name': 'Complete detailed design & Construct BRT Pilot Corridor (Busega-Jinja Road)',
                'output_id': outputs[0].id,
                'description': 'Complete detailed design & Construct BRT Pilot Corridor (Busega-Jinja Road)',
                'sequence': 1,
                'baseline_value': 0.0,
                'target_value': 1.0,
                'current_value': 0.0,
                'measurement_unit': 'Corridor',
            },
            {
                'name': 'Complete detailed & implement the Kampala Flyover Phase 2',
                'output_id': outputs[0].id,
                'description': 'Complete detailed & implement the Kampala Flyover Phase 2 comprising of Mukwano, Kigun House, Africana, Prime House and Garden City Junctions',
                'sequence': 2,
                'baseline_value': 0.0,
                'target_value': 5.0,
                'current_value': 168.75,
                'measurement_unit': 'Junctions',
            },
            {
                'name': 'Support the improvement of passenger railway services by Uganda Railways Corporation',
                'output_id': outputs[0].id,
                'description': 'Support the improvement of passenger railway services by Uganda Railways Corporation in terms of the Kampala-Portbell-Kyengera meter gauge railway line',
                'sequence': 3,
                'baseline_value': 0.0,
                'target_value': 1.0,
                'current_value': 0.0,
                'measurement_unit': 'Railway Line',
            },
            {
                'name': 'Undertake feasibility studies and detailed designs for the Kampala Cable Car project',
                'output_id': outputs[0].id,
                'description': 'Undertake feasibility studies and detailed designs for the Kampala Cable Car project',
                'sequence': 4,
                'baseline_value': 0.0,
                'target_value': 1.0,
                'current_value': 0.0,
                'measurement_unit': 'Project',
            },
            {
                'name': 'Undertake feasibility studies and detailed designs for the Kampala light rail system',
                'output_id': outputs[0].id,
                'description': 'Undertake feasibility studies and detailed designs for the Kampala light rail system',
                'sequence': 5,
                'baseline_value': 0.0,
                'target_value': 1.0,
                'current_value': 3.75,
                'measurement_unit': 'System',
            },
            # For Output 1.2.1.1 - Capacity increase
            {
                'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP',
                'output_id': outputs[1].id,
                'description': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP',
                'sequence': 1,
                'baseline_value': 44.90,
                'target_value': 44.90,
                'current_value': 24.00,
                'measurement_unit': 'Km',
            },
            {
                'name': 'Km of KCCA roads & junctions upgraded/reconstructed under GMAUUP',
                'output_id': outputs[1].id,
                'description': 'Km of KCCA roads & junctions upgraded/reconstructed under GMAUUP',
                'sequence': 2,
                'baseline_value': 0.0,
                'target_value': 25.00,
                'current_value': 21.34,
                'measurement_unit': 'Km',
            },
            {
                'name': 'Km of KCCA roads & junctions upgraded/reconstructed under GMAUUP services Project',
                'output_id': outputs[1].id,
                'description': 'Km of KCCA roads & junctions upgraded/reconstructed under GMAUUP services Project',
                'sequence': 3,
                'baseline_value': 0.0,
                'target_value': 25.00,
                'current_value': 24.00,
                'measurement_unit': 'Km',
            },
            {
                'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP (Colas Project)',
                'output_id': outputs[1].id,
                'description': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP (Colas Project)',
                'sequence': 4,
                'baseline_value': 0.0,
                'target_value': 61.86,
                'current_value': 24.00,
                'measurement_unit': 'Km',
            },
            {
                'name': 'No of Pedestrian Bridges constructed under KCRSIP',
                'output_id': outputs[1].id,
                'description': 'No of Pedestrian Bridges constructed under KCRSIP (Colas Project)',
                'sequence': 5,
                'baseline_value': 0.0,
                'target_value': 1.00,
                'current_value': 2.00,
                'measurement_unit': 'Bridges',
            },
            {
                'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP or GMAUUP Phase 2',
                'output_id': outputs[1].id,
                'description': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP or GMAUUP Phase 2',
                'sequence': 6,
                'baseline_value': 0.0,
                'target_value': 15.00,
                'current_value': 15.00,
                'measurement_unit': 'Km',
            },
            {
                'name': 'No of key junctions signalized under JICA Project phase 2',
                'output_id': outputs[1].id,
                'description': 'No of key junctions signalized under JICA Project phase 2',
                'sequence': 7,
                'baseline_value': 30.00,
                'target_value': 10.00,
                'current_value': 10.00,
                'measurement_unit': 'Junctions',
            },
            # For Output 1.2.1.2 - Road improvement projects
            {
                'name': 'Implement the Kampala City Road Rehabilitation Project financed by the AfDB',
                'output_id': outputs[2].id,
                'description': 'Implement the Kampala City Road Rehabilitation Project financed by the AfDB (IBRD: $ 27M)',
                'sequence': 1,
                'baseline_value': 131.56,
                'target_value': 27.0,
                'current_value': 0.0,
                'measurement_unit': 'Million USD',
            },
            {
                'name': 'Implement road improvement projects under the GMAUUP financed by the World Bank',
                'output_id': outputs[2].id,
                'description': 'Implement road improvement projects under the GMAUUP financed by the World Bank (US million $ 3 Junctions)',
                'sequence': 2,
                'baseline_value': 113.96,
                'target_value': 17.66,
                'current_value': 0.0,
                'measurement_unit': 'Million USD',
            },
            {
                'name': 'Implement road improvement projects financed by Government of Uganda',
                'output_id': outputs[2].id,
                'description': 'Implement road improvement projects financed by Government of Uganda (USMIS – JOIT Services Project)',
                'sequence': 3,
                'baseline_value': 15.16,
                'target_value': 130.00,
                'current_value': 110.00,
                'measurement_unit': 'Million USD',
            },
            {
                'name': 'Implement Road improvement under the Kampala City Roads and Bridges Improvement Project',
                'output_id': outputs[2].id,
                'description': 'Implement Road improvement under the Kampala City Roads and Bridges Improvement Project financed by JICA (127Km & 3 Pedestrian bridges UML Kasangati Hospital & Queensway)',
                'sequence': 4,
                'baseline_value': 1.00,
                'target_value': 197.54,
                'current_value': 197.54,
                'measurement_unit': 'Km',
            },
            {
                'name': 'Upgrade & rehabilitate roads in the City under KCRSIP/GMAUUP Project',
                'output_id': outputs[2].id,
                'description': 'Upgrade & rehabilitate roads in the City under KCRSIP/GMAUUP Project (2.0Km) Design, configure & signalize key junctions (25 Junctions – JICA phase 2)',
                'sequence': 5,
                'baseline_value': 0.0,
                'target_value': 75.00,
                'current_value': 78.00,
                'measurement_unit': 'Km',
            },
            {
                'name': 'Modernize and optimize parking in the Capital City',
                'output_id': outputs[2].id,
                'description': 'Modernize and optimize parking in the Capital City (PPP-Multiplex)',
                'sequence': 6,
                'baseline_value': 0.0,
                'target_value': 5.10,
                'current_value': 5.10,
                'measurement_unit': 'Sites',
            },
            {
                'name': 'Implement the OTP Redevelopment Project',
                'output_id': outputs[2].id,
                'description': 'Implement the OTP Redevelopment Project (PPP Arrangement)',
                'sequence': 7,
                'baseline_value': 0.0,
                'target_value': 3.50,
                'current_value': 0.50,
                'measurement_unit': 'Projects',
            },
            {
                'name': 'Ensure that the Statutory instrument for Restriction of Heavy Goods Vehicles is amended',
                'output_id': outputs[2].id,
                'description': 'Ensure that the Statutory instrument for Restriction of Heavy Goods Vehicles is amended, regulations developed and implement',
                'sequence': 8,
                'baseline_value': 0.0,
                'target_value': 1.10,
                'current_value': 0.00,
                'measurement_unit': 'Instruments',
            },
            # For Output 1.3.1.1 - Road safety
            {
                'name': 'Number of Fatalities on City Road',
                'output_id': outputs[3].id,
                'description': 'Number of Fatalities on City Road',
                'sequence': 1,
                'baseline_value': 411.0,
                'target_value': 275.0,
                'current_value': 362.0,
                'measurement_unit': 'Fatalities',
            },
            {
                'name': 'Number of road traffic Accidents conducted',
                'output_id': outputs[3].id,
                'description': 'Number of road traffic Accidents conducted',
                'sequence': 2,
                'baseline_value': 0.0,
                'target_value': 331.0,
                'current_value': 305.0,
                'measurement_unit': 'Accidents',
            },
            {
                'name': 'Number of Street Lights Installed Under AFD Funding',
                'output_id': outputs[3].id,
                'description': 'Number of Street Lights Installed Under AFD Funding',
                'sequence': 3,
                'baseline_value': 7558.0,
                'target_value': 15000.0,
                'current_value': 2500.0,
                'measurement_unit': 'Street Lights',
            },
            {
                'name': 'Number of Street Lights Installed Under PPP Arrangement',
                'output_id': outputs[3].id,
                'description': 'Number of Street Lights Installed Under PPP Arrangement',
                'sequence': 4,
                'baseline_value': 0.0,
                'target_value': 10000.0,
                'current_value': 2500.0,
                'measurement_unit': 'Street Lights',
            },
        ]
        
        print("Creating PIAP Actions with master table data...")
        piap_actions = []
        for action_data in piap_actions_data:
            action = env['piap.action'].create(action_data)
            piap_actions.append(action)
            print(f"  Created: {action.name}")

        # Create Indicators based on master table
        indicators_data = [
            # Intermediate Outcome Indicators
            {
                'name': 'Average Travel time (Min/Km) on KCCA Road Links',
                'outcome_id': outcomes[0].id,
                'description': 'Average Travel time (Min/Km) on KCCA Road Links',
                'baseline_value': 4.2,
                'target_value': 3.5,
                'current_value': 3.5,
                'measurement_unit': 'Min/Km',
                'sequence': 1,
            },
            {
                'name': 'Proportion of Commuters using mass public transport (Rail & BRT)',
                'outcome_id': outcomes[1].id,
                'description': 'Proportion of Commuters using mass public transport (Rail & BRT)',
                'baseline_value': 2.0,
                'target_value': 10.0,
                'current_value': 15.0,
                'measurement_unit': '%',
                'sequence': 1,
            },
            # Output Indicators
            {
                'name': 'Km of BRT Network constructed',
                'output_id': outputs[0].id,
                'description': 'Km of BRT Network constructed',
                'baseline_value': 0.0,
                'target_value': 4.4,
                'current_value': 5.0,
                'measurement_unit': 'Km',
                'sequence': 1,
            },
            {
                'name': 'No of Traffic Alleviation Flyovers constructed',
                'output_id': outputs[0].id,
                'description': 'No of Traffic Alleviation Flyovers constructed',
                'baseline_value': 2.0,
                'target_value': 2.0,
                'current_value': 9.0,
                'measurement_unit': 'Flyovers',
                'sequence': 2,
            },
            {
                'name': 'Km of meter gauge commuter rail revamped',
                'output_id': outputs[0].id,
                'description': 'Km of meter gauge commuter rail revamped',
                'baseline_value': 28.5,
                'target_value': 3.0,
                'current_value': 5.0,
                'measurement_unit': 'Km',
                'sequence': 3,
            },
            {
                'name': 'Km of Cable Car System constructed',
                'output_id': outputs[0].id,
                'description': 'Km of Cable Car System constructed',
                'baseline_value': 0.0,
                'target_value': 2.0,
                'current_value': 7.5,
                'measurement_unit': 'Km',
                'sequence': 4,
            },
            {
                'name': 'Completion of Feasibility study & detailed design for LRT',
                'output_id': outputs[0].id,
                'description': 'Completion of Feasibility study & detailed design for LRT',
                'baseline_value': 0.0,
                'target_value': 100.0,
                'current_value': 100.0,
                'measurement_unit': '%',
                'sequence': 5,
            },
            {
                'name': 'Proportion of city road network paved',
                'output_id': outputs[1].id,
                'description': 'Proportion of city road network paved',
                'baseline_value': 37.0,
                'target_value': 46.0,
                'current_value': 51.0,
                'measurement_unit': '%',
                'sequence': 1,
            },
            {
                'name': 'Km of City Roads Paved',
                'output_id': outputs[1].id,
                'description': 'Km of City Roads Paved',
                'baseline_value': 776.50,
                'target_value': 122.24,
                'current_value': 64.60,
                'measurement_unit': 'Km',
                'sequence': 2,
            },
            {
                'name': 'Fatalities per 100,000 persons (Roads)',
                'output_id': outputs[3].id,
                'description': 'Fatalities per 100,000 persons (Roads)',
                'baseline_value': 11.00,
                'target_value': 8.00,
                'current_value': 8.40,
                'measurement_unit': 'Per 100,000',
                'sequence': 1,
            },
            {
                'name': 'Proportion of road network with street lights',
                'output_id': outputs[3].id,
                'description': 'Proportion of road network with street lights',
                'baseline_value': 13.0,
                'target_value': 30.0,
                'current_value': 70.0,
                'measurement_unit': '%',
                'sequence': 2,
            },
        ]

        print("Creating Indicators with master table data...")
        for indicator_data in indicators_data:
            indicator = env['indicator'].create(indicator_data)
            print(f"  Created: {indicator.name}")

        # Commit the transaction
        cr.commit()
        print("\n=== MASTER TABLE DATA IMPORT COMPLETED SUCCESSFULLY ===")

        # Print summary
        outcomes_count = env['intermediate.outcome'].search_count([])
        interventions_count = env['intervention'].search_count([])
        outputs_count = env['output'].search_count([])
        actions_count = env['piap.action'].search_count([])
        indicators_count = env['indicator'].search_count([])

        print(f"\nSUMMARY:")
        print(f"- Intermediate Outcomes: {outcomes_count}")
        print(f"- Interventions: {interventions_count}")
        print(f"- Outputs: {outputs_count}")
        print(f"- PIAP Actions: {actions_count}")
        print(f"- Indicators: {indicators_count}")

if __name__ == "__main__":
    import_master_table_data()
