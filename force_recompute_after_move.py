#!/usr/bin/env python3
"""
Force recomputation of computed fields after moving the demo data
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

def force_recompute_after_move():
    """Force recomputation of computed fields after data move"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config([
        '--addons-path=/home/richards/Dev/odoo18/addons',
        '--data-dir=/home/richards/.local/share/Odoo',
        '-d', 'robust_pmis'
    ])
    
    registry = odoo.registry('robust_pmis')
    
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        try:
            _logger.info("=== FORCE RECOMPUTATION AFTER DATA MOVE ===")
            
            # Get the Infrastructure Development objective (ID 8)
            objective = env['strategic.objective'].browse(8)
            if objective.exists():
                _logger.info(f"Found objective: {objective.name}")
                
                # Force recompute counts
                objective._compute_counts()
                objective.flush_recordset()
                
                _logger.info(f"After recompute - KRA count: {objective.kra_count}, KPI count: {objective.kpi_count}")
                
                # Also recompute the strategic goal
                if objective.strategic_goal_id:
                    goal = objective.strategic_goal_id
                    goal._compute_counts()
                    goal.flush_recordset()
                    _logger.info(f"Strategic Goal '{goal.name}' - Objectives: {goal.objective_count}, KRAs: {goal.kra_count}, KPIs: {goal.kpi_count}")
                
                # Recompute all KRAs under this objective
                kras = env['key.result.area'].search([('strategic_objective_id', '=', 8)])
                for kra in kras:
                    kra._compute_counts()
                    kra._compute_progress()
                    kra.flush_recordset()
                    _logger.info(f"KRA '{kra.name}' - KPI count: {kra.kpi_count}, Progress: {kra.progress}%")
                
                # Commit the changes
                cr.commit()
                _logger.info("✅ Successfully recomputed all fields!")
                
            else:
                _logger.error("Objective with ID 8 not found!")
                
        except Exception as e:
            _logger.error(f"❌ Error during recomputation: {e}")
            cr.rollback()

if __name__ == "__main__":
    force_recompute_after_move()
