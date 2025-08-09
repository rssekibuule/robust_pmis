#!/usr/bin/env python3
"""
Verify Infrastructure Development data entries using Odoo environment
"""

import logging
import sys
import os

# Add Odoo to path
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

# Configure logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

def verify_infrastructure_data():
    """Verify Infrastructure Development data entries"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config([
        '--addons-path=/home/richards/Dev/odoo18/addons',
        '--data-dir=/home/richards/.local/share/Odoo',
        '-d', 'robust_pmis'
    ])
    
    registry = odoo.modules.registry.Registry('robust_pmis')
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        try:
            _logger.info("=== VERIFYING INFRASTRUCTURE DEVELOPMENT DATA ===")
            
            # Find the strategic goal
            strategic_goals = env['strategic.goal'].search([('name', '=', 'Improve Urban Infrastructure')])
            if not strategic_goals:
                _logger.error("Strategic Goal 'Improve Urban Infrastructure' not found!")
                return
            
            _logger.info(f"✅ Found {len(strategic_goals)} Strategic Goal(s) named 'Improve Urban Infrastructure':")
            for sg in strategic_goals:
                _logger.info(f"   Goal ID {sg.id}: {sg.name}")
                _logger.info(f"   Objectives: {sg.objective_count}, KRAs: {sg.kra_count}, KPIs: {sg.kpi_count}")
                
                # Find Infrastructure Development objectives for this goal
                infrastructure_objectives = env['strategic.objective'].search([
                    ('name', '=', 'Infrastructure Development'),
                    ('strategic_goal_id', '=', sg.id)
                ])
                
                _logger.info(f"\n📊 Found {len(infrastructure_objectives)} Infrastructure Development objectives for Goal {sg.id}:")
                
                for obj in infrastructure_objectives:
                _logger.info(f"  🎯 Objective ID {obj.id}: {obj.name}")
                _logger.info(f"     KRAs: {obj.kra_count}, KPIs: {obj.kpi_count}")
                
                # Get KRAs for this objective
                kras = env['key.result.area'].search([('strategic_objective_id', '=', obj.id)])
                
                if kras:
                    _logger.info(f"     📋 KRAs for Objective {obj.id}:")
                    for kra in kras:
                        kpis = env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
                        kpi_count = len(kpis)
                        avg_achievement = sum(kpi.achievement_percentage for kpi in kpis) / kpi_count if kpi_count > 0 else 0
                        
                        _logger.info(f"       • {kra.name}: {kpi_count} KPIs (Avg: {avg_achievement:.1f}%)")
                        
                        # Show first few KPIs as examples
                        for i, kpi in enumerate(kpis[:2]):  # Show first 2 KPIs
                            _logger.info(f"         - {kpi.name}: {kpi.current_value}/{kpi.target_value} ({kpi.achievement_percentage:.1f}%)")
                        
                        if len(kpis) > 2:
                            _logger.info(f"         ... and {len(kpis) - 2} more KPIs")
                
                _logger.info("")  # Empty line for readability
            
            # Check if we have the expected 5 KRAs, 17 KPIs structure
            target_obj = infrastructure_objectives.filtered(lambda x: x.kra_count == 5 and x.kpi_count == 17)
            if target_obj:
                _logger.info(f"🎉 SUCCESS: Found target objective {target_obj.id} with 5 KRAs and 17 KPIs!")
                
                # Detailed verification of the target objective
                _logger.info(f"\n🔍 DETAILED VERIFICATION OF OBJECTIVE {target_obj.id}:")
                
                kras = env['key.result.area'].search([('strategic_objective_id', '=', target_obj.id)])
                expected_kras = [
                    'Transport Infrastructure Development',
                    'Water and Sanitation Infrastructure', 
                    'Digital Infrastructure',
                    'Housing and Settlements',
                    'Green Infrastructure'
                ]
                
                for expected_kra in expected_kras:
                    kra = kras.filtered(lambda x: x.name == expected_kra)
                    if kra:
                        kpis = env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
                        _logger.info(f"  ✅ {expected_kra}: {len(kpis)} KPIs")
                        
                        # Show all KPIs for this KRA
                        for kpi in kpis:
                            _logger.info(f"     • {kpi.name}: {kpi.current_value}/{kpi.target_value} {kpi.measurement_unit} ({kpi.achievement_percentage:.1f}%)")
                    else:
                        _logger.error(f"  ❌ Missing KRA: {expected_kra}")
                
            else:
                _logger.warning("⚠️  No objective found with exactly 5 KRAs and 17 KPIs")
            
            _logger.info("\n=== VERIFICATION COMPLETE ===")
            
        except Exception as e:
            _logger.error(f"❌ Error during verification: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    verify_infrastructure_data()
