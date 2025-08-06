#!/usr/bin/env python3
"""
Add missing PIAP Actions to existing structure
"""

import sys
import os

# Add Odoo to path
sys.path.append('/home/richards/Dev/odoo18')
import odoo
from odoo import api, SUPERUSER_ID

def add_missing_piap_actions():
    """Add missing PIAP Actions to existing structure"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config(['-d', 'robust_pmis'])
    
    with odoo.registry('robust_pmis').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("=== ADDING MISSING PIAP ACTIONS ===")
        print(f"Database: {cr.dbname}")
        
        # Get existing outputs
        outputs = env['output'].search([], order='sequence')
        
        if len(outputs) < 4:
            print("Required outputs not found!")
            return
        
        print(f"Found {len(outputs)} outputs")
        for i, output in enumerate(outputs):
            print(f"  Output {i}: {output.name}")
        
        # Clear existing PIAP Actions
        print("Clearing existing PIAP Actions...")
        env['piap.action'].search([]).unlink()
        
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
        
        # Commit the transaction
        cr.commit()
        print("\n=== PIAP ACTIONS IMPORT COMPLETED SUCCESSFULLY ===")
        
        # Print final summary
        final_actions_count = env['piap.action'].search_count([])
        
        print(f"\nFINAL SUMMARY:")
        print(f"- PIAP Actions: {final_actions_count}")

if __name__ == "__main__":
    add_missing_piap_actions()
