#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from odoo import api, SUPERUSER_ID

_logger = logging.getLogger(__name__)

def update_kpi_classifications(cr, registry):
    """
    Update all KPI classification fields based on existing relationships.
    This can be called from the terminal for manual updates.
    """
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Get all KPIs
        kpis = env['key.performance.indicator'].search([])
        _logger.info(f"Found {len(kpis)} KPIs to update classifications for")
        
        # Update classification fields
        count = 0
        for kpi in kpis:
            kpi._compute_classification_fields()
            count += 1
            if count % 100 == 0:
                _logger.info(f"Processed {count}/{len(kpis)} KPIs")
        
        # Log results
        env.cr.execute("""
            SELECT classification_level, parent_type, COUNT(*) 
            FROM key_performance_indicator 
            GROUP BY classification_level, parent_type
        """)
        results = env.cr.fetchall()
        for level, parent_type, count in results:
            _logger.info(f"Updated {count} KPIs with level: {level}, parent_type: {parent_type}")
        
        _logger.info(f"Successfully updated classifications for {len(kpis)} KPIs")
        
        return True

# If this script is run directly
if __name__ == "__main__":
    # This will be run when script is executed directly
    print("This script should be run from the Odoo shell or as a post-install hook")
    print("To run in Odoo shell:")
    print("from odoo.addons.robust_pmis.update_kpi_classifications import update_kpi_classifications")
    print("update_kpi_classifications(cr, registry)")
