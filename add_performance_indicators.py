#!/usr/bin/env python3
"""
Add Performance Indicators to existing structure
"""

import sys
import os

# Add Odoo to path
sys.path.append('/home/richards/Dev/odoo18')
import odoo
from odoo import api, SUPERUSER_ID

def add_performance_indicators():
    """Add Performance Indicators to existing structure"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config(['-d', 'robust_pmis'])
    
    with odoo.registry('robust_pmis').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("=== ADDING PERFORMANCE INDICATORS ===")
        print(f"Database: {cr.dbname}")
        
        # Get existing structure
        outcomes = env['intermediate.outcome'].search([], order='sequence')
        outputs = env['output'].search([], order='sequence')
        
        if len(outcomes) < 3 or len(outputs) < 4:
            print("Required structure not found!")
            return
        
        print(f"Found {len(outcomes)} outcomes and {len(outputs)} outputs")
        for i, outcome in enumerate(outcomes):
            print(f"  Outcome {i}: {outcome.name}")
        for i, output in enumerate(outputs):
            print(f"  Output {i}: {output.name}")
        
        # Clear existing Performance Indicators
        print("Clearing existing Performance Indicators...")
        env['performance.indicator'].search([]).unlink()
        
        # Create ALL Performance Indicators from master table
        all_indicators = [
            # Intermediate Outcome Indicators
            {'name': 'Average Travel time (Min/Km) on KCCA Road Links', 'type': 'outcome', 'idx': 0, 'baseline': 4.2, 'target': 3.5, 'current': 3.5, 'unit': 'Min/Km'},
            {'name': 'Proportion of Commuters using mass public transport (Rail & BRT)', 'type': 'outcome', 'idx': 1, 'baseline': 2.0, 'target': 10.0, 'current': 15.0, 'unit': '%'},
            {'name': 'Fatalities per 100,000 persons (Roads)', 'type': 'outcome', 'idx': 2, 'baseline': 11.00, 'target': 8.00, 'current': 8.40, 'unit': 'Per 100,000'},
            
            # Output Indicators
            {'name': 'Km of BRT Network constructed', 'type': 'output', 'idx': 1, 'baseline': 0.0, 'target': 4.4, 'current': 5.0, 'unit': 'Km'},
            {'name': 'No of Traffic Alleviation Flyovers constructed', 'type': 'output', 'idx': 1, 'baseline': 2.0, 'target': 2.0, 'current': 9.0, 'unit': 'Flyovers'},
            {'name': 'Km of meter gauge commuter rail revamped', 'type': 'output', 'idx': 1, 'baseline': 28.5, 'target': 3.0, 'current': 5.0, 'unit': 'Km'},
            {'name': 'Km of Cable Car System constructed', 'type': 'output', 'idx': 1, 'baseline': 0.0, 'target': 2.0, 'current': 7.5, 'unit': 'Km'},
            {'name': 'Completion of Feasibility study & detailed design for LRT', 'type': 'output', 'idx': 1, 'baseline': 0.0, 'target': 100.0, 'current': 100.0, 'unit': '%'},
            {'name': 'Proportion of city road network paved', 'type': 'output', 'idx': 2, 'baseline': 37.0, 'target': 46.0, 'current': 51.0, 'unit': '%'},
            {'name': 'Km of City Roads Paved', 'type': 'output', 'idx': 2, 'baseline': 776.50, 'target': 122.24, 'current': 64.60, 'unit': 'Km'},
            {'name': 'Proportion of road network with street lights', 'type': 'output', 'idx': 0, 'baseline': 13.0, 'target': 30.0, 'current': 70.0, 'unit': '%'},
            
            # Additional indicators from master table
            {'name': 'Number of Staff trained on Transport safety', 'type': 'output', 'idx': 0, 'baseline': 10.0, 'target': 10.0, 'current': 10.0, 'unit': 'Staff'},
            {'name': 'Number of Stakeholders trained on Transport safety', 'type': 'output', 'idx': 0, 'baseline': 25.0, 'target': 25.0, 'current': 25.0, 'unit': 'Stakeholders'},
            
            # PIAP Action Indicators (from master table)
            {'name': 'Undertake the KCCA Road Safety Unit', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 1.0, 'current': 1.0, 'unit': 'Unit'},
            {'name': 'Undertake Road Safety Audits', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 0.25, 'current': 0.30, 'unit': 'Audits'},
            {'name': 'Construct road safety infrastructure across the city (Humps, signage, zebra-crossings, road marking etc)', 'type': 'output', 'idx': 0, 'baseline': 1.0, 'target': 2.0, 'current': 2.0, 'unit': 'Infrastructure'},
            {'name': 'Conduct road safety campaigns (School & communities, Billboards, Newspaper articles, Radio talk shows)', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 0.50, 'current': 0.50, 'unit': 'Campaigns'},
            {'name': 'Streamline Road Safety Operations (Patrols, Registration, Boda Boda ops, sensitization, Ordinance, operations and implement', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 0.50, 'current': 0.50, 'unit': 'Operations'},
            {'name': 'Develop and maintain a road safety dashboard for the city', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 0.10, 'current': 0.10, 'unit': 'Dashboard'},
            {'name': 'Review and update the Kampala Road Safety Strategy and Action Plan', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 0.10, 'current': 0.10, 'unit': 'Strategy'},
            {'name': 'Publish Annual Road Safety Reports', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 0.40, 'current': 0.40, 'unit': 'Reports'},
            {'name': 'Install Street Lights including crime hotspots under the AFD project (15,000)', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 65.00, 'current': 32.50, 'unit': 'Lights'},
            {'name': 'Install Street Lights under PPP Arrangement (10,000)', 'type': 'output', 'idx': 0, 'baseline': 0.0, 'target': 32.50, 'current': 32.50, 'unit': 'Lights'},
            
            # Transport safety capacity strengthened indicators
            {'name': 'Number of Staff trained on Transport safety', 'type': 'output', 'idx': 0, 'baseline': 10.0, 'target': 10.0, 'current': 10.0, 'unit': 'Staff'},
            {'name': 'Number of Stakeholders trained on Transport safety', 'type': 'output', 'idx': 0, 'baseline': 25.0, 'target': 25.0, 'current': 25.0, 'unit': 'Stakeholders'},
            {'name': 'Year stakeholders on road safety', 'type': 'output', 'idx': 0, 'baseline': 0.05, 'target': 0.05, 'current': 0.05, 'unit': 'Years'},
        ]
        
        print(f"Creating {len(all_indicators)} Performance Indicators...")
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
        print("\n=== PERFORMANCE INDICATORS IMPORT COMPLETED SUCCESSFULLY ===")
        
        # Print final summary
        final_indicators_count = env['performance.indicator'].search_count([])
        
        print(f"\nFINAL SUMMARY:")
        print(f"- Performance Indicators: {final_indicators_count}")

if __name__ == "__main__":
    add_performance_indicators()
