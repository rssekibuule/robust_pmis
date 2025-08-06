#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to force recomputation of stored computed fields for Strategic Objectives
"""

import sys
import os
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

def force_recompute():
    """Force recomputation of strategic objective counts"""
    
    # Initialize Odoo environment
    db_name = 'robust_pmis'
    odoo.tools.config.parse_config(['-d', db_name])
    registry = odoo.registry(db_name)
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("🔄 Forcing recomputation of Strategic Objective fields...")
        
        # Get all strategic objectives
        objectives = env['strategic.objective'].search([])
        print(f"Found {len(objectives)} strategic objectives")
        
        # Force recomputation of counts for all objectives
        for obj in objectives:
            print(f"Processing: {obj.name}")
            
            # Manually trigger computation
            obj._compute_counts()
            obj._compute_progress()
            
        # Force flush to database
        env.flush_all()
            
        # Also recompute KRA counts
        print("\n🔄 Forcing recomputation of KRA fields...")
        kras = env['key.result.area'].search([])
        print(f"Found {len(kras)} KRAs")
        
        for kra in kras:
            kra._compute_counts()
            kra._compute_progress()
        
        # Force flush to database again
        env.flush_all()
        
        # Commit all changes
        cr.commit()
        
        print("\n✅ Recomputation completed!")
        
        # Show results for infrastructure objectives
        print("\n📊 Infrastructure Development Results:")
        infra_objectives = env['strategic.objective'].search([('name', 'ilike', 'infrastructure')])
        for obj in infra_objectives:
            print(f"  - {obj.name}: KRAs={obj.kra_count}, KPIs={obj.kpi_count}, Progress={obj.progress}%")

if __name__ == '__main__':
    force_recompute()
