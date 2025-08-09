#!/usr/bin/env python3
"""
Simple verification of Infrastructure Development data entries
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

def verify_data():
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
            _logger.info("=== INFRASTRUCTURE DEVELOPMENT DATA VERIFICATION ===")
            
            # Find all Infrastructure Development objectives
            all_objectives = env['strategic.objective'].search([('name', '=', 'Infrastructure Development')])
            _logger.info(f"Found {len(all_objectives)} Infrastructure Development objectives:")
            
            for obj in all_objectives:
                goal_name = obj.strategic_goal_id.name if obj.strategic_goal_id else "No Goal"
                _logger.info(f"\n🎯 Objective ID {obj.id}: {obj.name}")
                _logger.info(f"   Strategic Goal: {goal_name}")
                _logger.info(f"   KRAs: {obj.kra_count}, KPIs: {obj.kpi_count}")
                
                # Show KRAs
                kras = env['key.result.area'].search([('strategic_objective_id', '=', obj.id)])
                if kras:
                    _logger.info(f"   📋 KRAs:")
                    for kra in kras:
                        kpis = env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
                        _logger.info(f"     • {kra.name}: {len(kpis)} KPIs")
            
            # Focus on the objective with 5 KRAs and 17 KPIs (our target)
            target_obj = all_objectives.filtered(lambda x: x.kra_count >= 5 and x.kpi_count >= 17)
            
            if target_obj:
                _logger.info(f"\n🎉 DETAILED VIEW OF TARGET OBJECTIVE(S):")
                for obj in target_obj:
                    _logger.info(f"\n🔍 Objective {obj.id}: {obj.name} ({obj.kra_count} KRAs, {obj.kpi_count} KPIs)")
                    _logger.info(f"   Strategic Goal: {obj.strategic_goal_id.name}")
                    
                    kras = env['key.result.area'].search([('strategic_objective_id', '=', obj.id)])
                    for kra in kras:
                        kpis = env['key.performance.indicator'].search([('kra_id', '=', kra.id)])
                        _logger.info(f"\n   📋 KRA: {kra.name} ({len(kpis)} KPIs)")
                        
                        for kpi in kpis:
                            unit = kpi.measurement_unit or ""
                            _logger.info(f"     • {kpi.name}: {kpi.current_value}/{kpi.target_value} {unit} ({kpi.achievement_percentage:.1f}%)")
            
            else:
                _logger.warning("⚠️  No objective found with 5+ KRAs and 17+ KPIs")
            
            _logger.info("\n=== VERIFICATION COMPLETE ===")
            
        except Exception as e:
            _logger.error(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    verify_data()
