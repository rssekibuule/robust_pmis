#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

# Configure Odoo
odoo.tools.config.parse_config(['-d', 'robust_pmis'])

def debug_counts():
    with odoo.api.Environment.manage():
        with odoo.registry('robust_pmis').cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            
            print("=== DEBUGGING STRATEGIC GOAL COUNTS ===")
            
            # Get strategic goals
            goals = env['strategic.goal'].search([])
            print(f"\nFound {len(goals)} strategic goals:")
            
            for goal in goals:
                print(f"\n🎯 GOAL: {goal.name}")
                print(f"   ID: {goal.id}")
                
                # Check strategic objectives
                objectives = goal.strategic_objective_ids
                print(f"   Strategic Objectives: {len(objectives)}")
                for obj in objectives:
                    print(f"     - {obj.name} (ID: {obj.id})")
                    
                    # Check programmes for each objective
                    programmes = obj.programme_ids
                    print(f"       Programmes: {len(programmes)}")
                    for prog in programmes[:3]:  # Show first 3
                        print(f"         - {prog.name} (ID: {prog.id})")
                        
                        # Check directorates
                        print(f"           Implementing directorates: {len(prog.implementing_directorate_ids)}")
                        for dir in prog.implementing_directorate_ids:
                            print(f"             - {dir.name}")
                            
                        # Check programme-directorate relationships
                        prog_dir_rels = env['programme.directorate.rel'].search([
                            ('programme_id', '=', prog.id)
                        ])
                        print(f"           Programme-Directorate relationships: {len(prog_dir_rels)}")
                        for rel in prog_dir_rels:
                            print(f"             - {rel.directorate_id.name}")
                
                # Force recompute
                print(f"\n   🔄 FORCING RECOMPUTATION...")
                goal._compute_smart_card_counts()
                
                print(f"   📊 COMPUTED COUNTS:")
                print(f"     Programme count: {goal.programme_count}")
                print(f"     Directorate count: {goal.directorate_count}")
                print(f"     Division count: {goal.division_count}")
                
            print("\n=== CHECKING RELATIONSHIPS DIRECTLY ===")
            
            # Check programme-directorate relationships
            prog_dir_rels = env['programme.directorate.rel'].search([])
            print(f"\nTotal Programme-Directorate relationships: {len(prog_dir_rels)}")
            for rel in prog_dir_rels[:5]:  # Show first 5
                print(f"  - {rel.programme_id.name} → {rel.directorate_id.name}")
                
            # Check division-programme relationships  
            div_prog_rels = env['division.programme.rel'].search([])
            print(f"\nTotal Division-Programme relationships: {len(div_prog_rels)}")
            for rel in div_prog_rels[:5]:  # Show first 5
                print(f"  - {rel.division_id.name} → {rel.programme_id.name}")

if __name__ == '__main__':
    debug_counts()
