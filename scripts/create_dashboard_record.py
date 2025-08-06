#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Add the Odoo directory to Python path
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

# Initialize Odoo environment
odoo.tools.config.parse_config(['-d', 'robust_pmis'])

with odoo.registry('robust_pmis').cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    print("Creating performance dashboard record...")
    
    # Create or update the dashboard record
    Dashboard = env['performance.dashboard']
    
    # Check if record already exists
    existing = Dashboard.search([])
    if existing:
        print(f"Updating existing dashboard record: {existing[0].name}")
        existing[0]._compute_metrics()
    else:
        dashboard = Dashboard.create({
            'name': 'KCCA Organization Performance Dashboard'
        })
        print(f"Created new dashboard record: {dashboard.name}")
    
    # Force recomputation of all metrics
    dashboards = Dashboard.search([])
    for dashboard in dashboards:
        dashboard._compute_metrics()
        
    # Print metrics
    for dashboard in dashboards:
        print(f"\n=== {dashboard.name} ===")
        print(f"Strategic Goals: {dashboard.total_goals}")
        print(f"KPIs: {dashboard.total_kpis}")
        print(f"Average KPI Performance: {dashboard.avg_kpi_performance:.1f}%")
        print(f"Programmes: {dashboard.total_programmes}")
        print(f"Average Programme Performance: {dashboard.avg_programme_performance:.1f}%")
        print(f"Directorates: {dashboard.total_directorates}")
        print(f"Average Directorate Performance: {dashboard.avg_directorate_performance:.1f}%")
        print(f"Divisions: {dashboard.total_divisions}")
        print(f"Average Division Performance: {dashboard.avg_division_performance:.1f}%")
    
    # Commit the transaction
    cr.commit()
    
    print("\nDashboard setup completed successfully!")
