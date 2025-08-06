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
    
    print("Analyzing and fixing division-directorate structure...")
    
    Division = env['kcca.division']
    Directorate = env['kcca.directorate']
    
    # Show all divisions and their directorates
    all_divisions = Division.search([])
    print(f"\nAll Divisions ({len(all_divisions)}):")
    
    division_names = {}
    duplicates = []
    
    for div in all_divisions:
        print(f"  - {div.name} (ID: {div.id}) under {div.directorate_id.name}")
        
        if div.name in division_names:
            # Found duplicate name
            duplicates.append(div)
            print(f"    *** DUPLICATE: {div.name} already exists under {division_names[div.name].directorate_id.name}")
        else:
            division_names[div.name] = div
    
    print(f"\nFound {len(duplicates)} duplicate divisions")
    
    # Show engineering directorates specifically
    engineering_dirs = Directorate.search([
        '|',
        ('name', 'ilike', 'engineering'),
        ('name', 'ilike', 'technical')
    ])
    
    print(f"\nEngineering Directorates ({len(engineering_dirs)}):")
    for dir in engineering_dirs:
        divisions_under = Division.search([('directorate_id', '=', dir.id)])
        print(f"  - {dir.name} (ID: {dir.id})")
        for div in divisions_under:
            print(f"    └─ {div.name} (ID: {div.id})")
    
    # Clean up the strategic goal to only use unique divisions
    Strategic = env['strategic.goal']
    goal = Strategic.search([('name', '=', 'Improve Urban Infrastructure')], limit=1)
    
    if goal:
        print(f"\n=== Fixing Strategic Goal: {goal.name} ===")
        
        # Get the proper divisions - use only the 5 main territorial divisions
        main_divisions = Division.search([
            ('name', 'in', ['Central Division', 'Kawempe Division', 'Makindye Division', 'Nakawa Division', 'Rubaga Division']),
            ('directorate_id.name', '=', 'Territorial Divisions')  # Only territorial divisions
        ])
        
        print(f"Main territorial divisions to use ({len(main_divisions)}):")
        for div in main_divisions:
            print(f"  - {div.name} under {div.directorate_id.name}")
        
        # Clean up division-programme relationships to use only main divisions
        DivisionProgrammeRel = env['division.programme.rel']
        
        # Get infrastructure programmes
        Programme = env['kcca.programme']
        infrastructure_programmes = Programme.search([
            '|', '|', '|',
            ('name', 'ilike', 'road'),
            ('name', 'ilike', 'infrastructure'),
            ('name', 'ilike', 'urban'),
            ('name', 'ilike', 'transport')
        ])
        
        # Remove relationships with duplicate divisions
        duplicate_ids = [dup.id for dup in duplicates]
        duplicate_rels = DivisionProgrammeRel.search([
            ('programme_id', 'in', infrastructure_programmes.ids),
            ('division_id', 'in', duplicate_ids)
        ])
        
        if duplicate_rels:
            print(f"\nRemoving {len(duplicate_rels)} relationships with duplicate divisions")
            duplicate_rels.unlink()
        
        # Ensure main divisions have relationships
        for programme in infrastructure_programmes:
            for division in main_divisions[:3]:  # Use first 3 main divisions
                existing_rel = DivisionProgrammeRel.search([
                    ('division_id', '=', division.id),
                    ('programme_id', '=', programme.id)
                ])
                
                if not existing_rel:
                    rel = DivisionProgrammeRel.create({
                        'division_id': division.id,
                        'programme_id': programme.id,
                        'performance_score': 80.0,
                        'implementation_status': 'implementing',
                        'start_date': '2024-01-01',
                        'end_date': '2025-12-31',
                    })
                    print(f"Created relationship: {division.name} <-> {programme.name}")
        
        # Force recomputation
        goal._compute_counts()
        goal._compute_smart_card_counts() 
        goal._compute_related_entities()
        
        print(f"\n=== Updated Strategic Goal Stats ===")
        print(f"Objectives: {goal.objective_count}")
        print(f"KRAs: {goal.kra_count}")
        print(f"KPIs: {goal.kpi_count}")
        print(f"Related Programmes: {goal.programme_count}")
        print(f"Related Directorates: {goal.directorate_count}")
        print(f"Related Divisions: {goal.division_count}")
        
        print(f"\nFinal Unique Divisions ({len(goal.division_ids)}):")
        for div in goal.division_ids:
            print(f"  - {div.name} (under {div.directorate_id.name})")
        
        print(f"\nFinal Unique Directorates ({len(goal.directorate_ids)}):")
        for dir in goal.directorate_ids:
            print(f"  - {dir.name}")
    
    # Update dashboard
    Dashboard = env['performance.dashboard']
    dashboards = Dashboard.search([])
    for dashboard in dashboards:
        dashboard._compute_metrics()
        
        print(f"\n=== Final Dashboard Metrics ===")
        print(f"Total Divisions: {dashboard.total_divisions}")
        print(f"Total Directorates: {dashboard.total_directorates}")
        print(f"Average Division Performance: {dashboard.avg_division_performance:.1f}%")
        print(f"Average Directorate Performance: {dashboard.avg_directorate_performance:.1f}%")
    
    # Commit the transaction
    cr.commit()
    
    print("\nStructure cleanup completed!")
