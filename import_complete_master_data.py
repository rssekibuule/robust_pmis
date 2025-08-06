#!/usr/bin/env python3
"""
Import COMPLETE Programme Structure Data from Master Table into robust_pmis database
This script imports ALL the PIAP Actions and Indicators from the master table
"""

import sys
import os

# Add Odoo to path
sys.path.append('/home/richards/Dev/odoo18')
import odoo
from odoo import api, SUPERUSER_ID

def import_complete_master_data():
    """Import complete programme structure data based on master table"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config(['-d', 'robust_pmis'])
    
    with odoo.registry('robust_pmis').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("=== IMPORTING COMPLETE MASTER TABLE DATA ===")
        print(f"Database: {cr.dbname}")
        
        # Get existing structure
        transport_objective = env['programme.objective'].search([
            ('name', 'ilike', 'develop an inter-modal and seamless transport')
        ], limit=1)
        
        if not transport_objective:
            print("Transport programme objective not found!")
            return
        
        outcomes = env['intermediate.outcome'].search([('objective_id', '=', transport_objective.id)])
        outputs = env['output'].search([])
        
        if len(outcomes) < 3 or len(outputs) < 4:
            print("Required structure not found. Please run the basic import first.")
            return
        
        print(f"Found {len(outcomes)} outcomes and {len(outputs)} outputs")
        
        # Clear existing PIAP Actions and Indicators
        print("Clearing existing PIAP Actions and Indicators...")
        env['piap.action'].search([]).unlink()
        env['performance.indicator'].search([]).unlink()
        
        # Create ALL PIAP Actions from master table
        all_piap_actions = [
            # Output 1.1.1.1 - Strategic transport infrastructure (5 actions)
            {'name': 'Complete detailed design & Construct BRT Pilot Corridor (Busega-Jinja Road)', 'output_idx': 0, 'baseline': 0.0, 'target': 1.0, 'current': 0.0, 'unit': 'Corridor'},
            {'name': 'Complete detailed & implement the Kampala Flyover Phase 2', 'output_idx': 0, 'baseline': 0.0, 'target': 5.0, 'current': 168.75, 'unit': 'Junctions'},
            {'name': 'Support the improvement of passenger railway services by Uganda Railways Corporation', 'output_idx': 0, 'baseline': 0.0, 'target': 1.0, 'current': 0.0, 'unit': 'Railway Line'},
            {'name': 'Undertake feasibility studies and detailed designs for the Kampala Cable Car project', 'output_idx': 0, 'baseline': 0.0, 'target': 1.0, 'current': 0.0, 'unit': 'Project'},
            {'name': 'Undertake feasibility studies and detailed designs for the Kampala light rail system', 'output_idx': 0, 'baseline': 0.0, 'target': 1.0, 'current': 3.75, 'unit': 'System'},
            
            # Output 1.2.1.1 - Capacity increase (7 actions)
            {'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP', 'output_idx': 1, 'baseline': 44.90, 'target': 44.90, 'current': 24.00, 'unit': 'Km'},
            {'name': 'Km of KCCA roads & junctions upgraded/reconstructed under GMAUUP', 'output_idx': 1, 'baseline': 0.0, 'target': 25.00, 'current': 21.34, 'unit': 'Km'},
            {'name': 'Km of KCCA roads & junctions upgraded/reconstructed under GMAUUP services Project', 'output_idx': 1, 'baseline': 0.0, 'target': 25.00, 'current': 24.00, 'unit': 'Km'},
            {'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP (Colas Project)', 'output_idx': 1, 'baseline': 0.0, 'target': 61.86, 'current': 24.00, 'unit': 'Km'},
            {'name': 'No of Pedestrian Bridges constructed under KCRSIP', 'output_idx': 1, 'baseline': 0.0, 'target': 1.00, 'current': 2.00, 'unit': 'Bridges'},
            {'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KCRSIP or GMAUUP Phase 2', 'output_idx': 1, 'baseline': 0.0, 'target': 15.00, 'current': 15.00, 'unit': 'Km'},
            {'name': 'No of key junctions signalized under JICA Project phase 2', 'output_idx': 1, 'baseline': 30.00, 'target': 10.00, 'current': 10.00, 'unit': 'Junctions'},
            
            # Output 1.2.1.2 - Road improvement projects (8 actions)
            {'name': 'Implement the Kampala City Road Rehabilitation Project financed by the AfDB', 'output_idx': 2, 'baseline': 131.56, 'target': 27.0, 'current': 0.0, 'unit': 'Million USD'},
            {'name': 'Implement road improvement projects under the GMAUUP financed by the World Bank', 'output_idx': 2, 'baseline': 113.96, 'target': 17.66, 'current': 0.0, 'unit': 'Million USD'},
            {'name': 'Implement road improvement projects financed by Government of Uganda (USMIS – JOIT Services Project)', 'output_idx': 2, 'baseline': 15.16, 'target': 130.00, 'current': 110.00, 'unit': 'Million USD'},
            {'name': 'Implement Road improvement under the Kampala City Roads and Bridges Improvement Project', 'output_idx': 2, 'baseline': 1.00, 'target': 197.54, 'current': 197.54, 'unit': 'Km'},
            {'name': 'Upgrade & rehabilitate roads in the City under KCRSIP/GMAUUP Project (2.0Km)', 'output_idx': 2, 'baseline': 0.0, 'target': 75.00, 'current': 78.00, 'unit': 'Km'},
            {'name': 'Modernize and optimize parking in the Capital City (PPP-Multiplex)', 'output_idx': 2, 'baseline': 0.0, 'target': 5.10, 'current': 5.10, 'unit': 'Sites'},
            {'name': 'Implement the OTP Redevelopment Project (PPP Arrangement)', 'output_idx': 2, 'baseline': 0.0, 'target': 3.50, 'current': 0.50, 'unit': 'Projects'},
            {'name': 'Ensure that the Statutory instrument for Restriction of Heavy Goods Vehicles is amended', 'output_idx': 2, 'baseline': 0.0, 'target': 1.10, 'current': 0.00, 'unit': 'Instruments'},
            
            # Output 1.3.1.1 - Road safety (4 actions)
            {'name': 'Number of Fatalities on City Road', 'output_idx': 3, 'baseline': 411.0, 'target': 275.0, 'current': 362.0, 'unit': 'Fatalities'},
            {'name': 'Number of road traffic Accidents conducted', 'output_idx': 3, 'baseline': 0.0, 'target': 331.0, 'current': 305.0, 'unit': 'Accidents'},
            {'name': 'Number of Street Lights Installed Under AFD Funding', 'output_idx': 3, 'baseline': 7558.0, 'target': 15000.0, 'current': 2500.0, 'unit': 'Street Lights'},
            {'name': 'Number of Street Lights Installed Under PPP Arrangement', 'output_idx': 3, 'baseline': 0.0, 'target': 10000.0, 'current': 2500.0, 'unit': 'Street Lights'},
        ]
        
        print(f"Creating {len(all_piap_actions)} PIAP Actions...")
        created_actions = 0
        for i, action_data in enumerate(all_piap_actions):
            try:
                piap_action = env['piap.action'].create({
                    'name': action_data['name'],
                    'output_id': outputs[action_data['output_idx']].id,
                    'description': action_data['name'],
                    'sequence': i + 1,
                    'baseline_value': action_data['baseline'],
                    'target_value': action_data['target'],
                    'current_value': action_data['current'],
                    'measurement_unit': action_data['unit'],
                })
                created_actions += 1
                print(f"  ✓ Created PIAP Action {created_actions}: {piap_action.name}")
            except Exception as e:
                print(f"  ✗ Failed to create PIAP Action: {action_data['name']} - {e}")
        
        # Create ALL Indicators from master table
        all_indicators = [
            # Intermediate Outcome Indicators
            {'name': 'Average Travel time (Min/Km) on KCCA Road Links', 'type': 'outcome', 'idx': 0, 'baseline': 4.2, 'target': 3.5, 'current': 3.5, 'unit': 'Min/Km'},
            {'name': 'Proportion of Commuters using mass public transport (Rail & BRT)', 'type': 'outcome', 'idx': 1, 'baseline': 2.0, 'target': 10.0, 'current': 15.0, 'unit': '%'},
            
            # Output Indicators
            {'name': 'Km of BRT Network constructed', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 4.4, 'current': 5.0, 'unit': 'Km'},
            {'name': 'No of Traffic Alleviation Flyovers constructed', 'type': 'output', 'idx': 0, 'baseline': 2.0, 'target': 2.0, 'current': 9.0, 'unit': 'Flyovers'},
            {'name': 'Km of meter gauge commuter rail revamped', 'type': 'output', 'idx': 0, 'baseline': 28.5, 'target': 3.0, 'current': 5.0, 'unit': 'Km'},
            {'name': 'Km of Cable Car System constructed', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 2.0, 'current': 7.5, 'unit': 'Km'},
            {'name': 'Completion of Feasibility study & detailed design for LRT', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 100.0, 'current': 100.0, 'unit': '%'},
            {'name': 'Proportion of city road network paved', 'type': 'output', 'idx': 1, 'baseline': 37.0, 'target': 46.0, 'current': 51.0, 'unit': '%'},
            {'name': 'Km of City Roads Paved', 'type': 'output', 'idx': 1, 'baseline': 776.50, 'target': 122.24, 'current': 64.60, 'unit': 'Km'},
            {'name': 'Fatalities per 100,000 persons (Roads)', 'type': 'output', 'idx': 3, 'baseline': 11.00, 'target': 8.00, 'current': 8.40, 'unit': 'Per 100,000'},
            {'name': 'Proportion of road network with street lights', 'type': 'output', 'idx': 3, 'baseline': 13.0, 'target': 30.0, 'current': 70.0, 'unit': '%'},
        ]
        
        print(f"Creating {len(all_indicators)} Indicators...")
        created_indicators = 0
        for i, indicator_data in enumerate(all_indicators):
            try:
                if indicator_data['type'] == 'outcome':
                    parent_id = outcomes[indicator_data['idx']].id
                    parent_field = 'outcome_id'
                else:
                    parent_id = outputs[indicator_data['idx']].id
                    parent_field = 'output_id'
                
                indicator = env['performance.indicator'].create({
                    'name': indicator_data['name'],
                    parent_field: parent_id,
                    'description': indicator_data['name'],
                    'sequence': i + 1,
                    'baseline_value': indicator_data['baseline'],
                    'target_value': indicator_data['target'],
                    'current_value': indicator_data['current'],
                    'measurement_unit': indicator_data['unit'],
                })
                created_indicators += 1
                print(f"  ✓ Created Indicator {created_indicators}: {indicator.name}")
            except Exception as e:
                print(f"  ✗ Failed to create Indicator: {indicator_data['name']} - {e}")
        
        # Commit the transaction
        cr.commit()
        print("\n=== COMPLETE MASTER TABLE DATA IMPORT COMPLETED SUCCESSFULLY ===")
        
        # Print final summary
        final_actions_count = env['piap.action'].search_count([])
        final_indicators_count = env['performance.indicator'].search_count([])
        
        print(f"\nFINAL SUMMARY:")
        print(f"- PIAP Actions: {final_actions_count}")
        print(f"- Indicators: {final_indicators_count}")
        print(f"- Total Records: {final_actions_count + final_indicators_count}")

if __name__ == "__main__":
    import_complete_master_data()
