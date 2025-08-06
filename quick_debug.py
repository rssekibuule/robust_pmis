#!/usr/bin/env python3

import sys
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

# Configure Odoo
odoo.tools.config.parse_config(['-d', 'robust_pmis'])

def quick_debug():
    with odoo.api.Environment.manage():
        with odoo.registry('robust_pmis').cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            
            # Get the strategic goal
            goal = env['strategic.goal'].search([('name', 'ilike', 'well planned')], limit=1)
            if not goal:
                print("❌ No strategic goal found!")
                return
                
            print(f"🎯 Strategic Goal: {goal.name}")
            print(f"   Current counts: P={goal.programme_count}, D={goal.directorate_count}, Div={goal.division_count}")
            
            # Check strategic objectives
            objectives = goal.strategic_objective_ids
            print(f"   Strategic Objectives: {len(objectives)}")
            
            if not objectives:
                print("❌ No strategic objectives linked to goal!")
                return
                
            # Check programmes
            all_programmes = objectives.mapped('programme_ids')
            print(f"   Total programmes from objectives: {len(all_programmes)}")
            
            if all_programmes:
                print("   Programme names:")
                for prog in all_programmes[:5]:  # Show first 5
                    print(f"     - {prog.name}")
                    
                # Check directorates
                directorates = all_programmes.mapped('implementing_directorate_ids')
                print(f"   Directorates from programmes: {len(directorates)}")
                
                # Force recompute
                print("\n🔄 Forcing recomputation...")
                goal._compute_smart_card_counts()
                
                print(f"   After recompute: P={goal.programme_count}, D={goal.directorate_count}, Div={goal.division_count}")
                
                # Save the changes
                cr.commit()
                print("✅ Changes committed!")
            else:
                print("❌ No programmes found in strategic objectives!")

if __name__ == '__main__':
    quick_debug()
