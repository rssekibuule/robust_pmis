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
    
    print("Cleaning up duplicate relationships and verifying counts...")
    
    # Find the strategic goal
    Strategic = env['strategic.goal']
    goal = Strategic.search([('name', '=', 'Improve Urban Infrastructure')], limit=1)
    
    if not goal:
        print("Strategic goal 'Improve Urban Infrastructure' not found!")
        exit(1)
    
    # Clean up duplicate division-programme relationships
    DivisionProgrammeRel = env['division.programme.rel']
    
    # Get all relationships for infrastructure programmes
    Programme = env['kcca.programme']
    infrastructure_programmes = Programme.search([
        '|', '|', '|',
        ('name', 'ilike', 'road'),
        ('name', 'ilike', 'infrastructure'),
        ('name', 'ilike', 'urban'),
        ('name', 'ilike', 'transport')
    ])
    
    all_rels = DivisionProgrammeRel.search([
        ('programme_id', 'in', infrastructure_programmes.ids)
    ])
    
    # Group by division_id and programme_id to find duplicates
    unique_combinations = {}
    duplicates_to_delete = []
    
    for rel in all_rels:
        key = (rel.division_id.id, rel.programme_id.id)
        if key in unique_combinations:
            # This is a duplicate, mark for deletion
            duplicates_to_delete.append(rel.id)
            print(f"Found duplicate: {rel.division_id.name} <-> {rel.programme_id.name}")
        else:
            unique_combinations[key] = rel.id
    
    # Delete duplicates
    if duplicates_to_delete:
        DivisionProgrammeRel.browse(duplicates_to_delete).unlink()
        print(f"Deleted {len(duplicates_to_delete)} duplicate relationships")
    
    # Clean up duplicate programme-directorate relationships
    ProgrammeDirectorateRel = env['programme.directorate.rel']
    
    prog_dir_rels = ProgrammeDirectorateRel.search([
        ('programme_id', 'in', infrastructure_programmes.ids)
    ])
    
    unique_prog_dir = {}
    prog_dir_duplicates = []
    
    for rel in prog_dir_rels:
        key = (rel.programme_id.id, rel.directorate_id.id)
        if key in unique_prog_dir:
            prog_dir_duplicates.append(rel.id)
            print(f"Found duplicate programme-directorate: {rel.programme_id.name} <-> {rel.directorate_id.name}")
        else:
            unique_prog_dir[key] = rel.id
    
    # Delete programme-directorate duplicates
    if prog_dir_duplicates:
        ProgrammeDirectorateRel.browse(prog_dir_duplicates).unlink()
        print(f"Deleted {len(prog_dir_duplicates)} duplicate programme-directorate relationships")
    
    # Verify and show actual counts
    Directorate = env['kcca.directorate']
    Division = env['kcca.division']
    
    # Count actual divisions and directorates
    total_divisions = Division.search_count([])
    total_directorates = Directorate.search_count([])
    
    print(f"\n=== Database Totals ===")
    print(f"Total Divisions in system: {total_divisions}")
    print(f"Total Directorates in system: {total_directorates}")
    print(f"Total Programmes in system: {Programme.search_count([])}")
    
    # Force recomputation of strategic goal metrics
    goal._compute_counts()
    goal._compute_smart_card_counts()
    goal._compute_related_entities()
    
    print(f"\n=== Strategic Goal: {goal.name} ===")
    print(f"Objectives: {goal.objective_count}")
    print(f"KRAs: {goal.kra_count}")
    print(f"KPIs: {goal.kpi_count}")
    print(f"Related Programmes: {goal.programme_count}")
    print(f"Related Directorates: {goal.directorate_count}")
    print(f"Related Divisions: {goal.division_count}")
    
    # Show unique entities linked
    print(f"\nUnique Programmes ({len(goal.programme_ids)}):")
    for prog in goal.programme_ids:
        print(f"  - {prog.name}")
    
    print(f"\nUnique Directorates ({len(goal.directorate_ids)}):")
    unique_directorates = goal.directorate_ids
    for dir in unique_directorates:
        print(f"  - {dir.name}")
    
    print(f"\nUnique Divisions ({len(goal.division_ids)}):")
    unique_divisions = goal.division_ids
    for div in unique_divisions:
        print(f"  - {div.name} (under {div.directorate_id.name})")
    
    # Update dashboard metrics
    Dashboard = env['performance.dashboard']
    dashboards = Dashboard.search([])
    for dashboard in dashboards:
        dashboard._compute_metrics()
        print(f"\n=== Dashboard Metrics Updated ===")
        print(f"Total Strategic Goals: {dashboard.total_goals}")
        print(f"Total KPIs: {dashboard.total_kpis}")
        print(f"Average KPI Performance: {dashboard.avg_kpi_performance:.1f}%")
        print(f"Total Programmes: {dashboard.total_programmes}")
        print(f"Average Programme Performance: {dashboard.avg_programme_performance:.1f}%")
        print(f"Total Directorates: {dashboard.total_directorates}")
        print(f"Average Directorate Performance: {dashboard.avg_directorate_performance:.1f}%")
        print(f"Total Divisions: {dashboard.total_divisions}")
        print(f"Average Division Performance: {dashboard.avg_division_performance:.1f}%")
    
    # Commit the transaction
    cr.commit()
    
    print("\nCleanup completed successfully!")
