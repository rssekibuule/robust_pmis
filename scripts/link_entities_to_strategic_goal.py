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
    
    print("Linking existing entities to Strategic Goal: Improve Urban Infrastructure")
    
    # Find the strategic goal
    Strategic = env['strategic.goal']
    goal = Strategic.search([('name', '=', 'Improve Urban Infrastructure')], limit=1)
    
    if not goal:
        print("Strategic goal 'Improve Urban Infrastructure' not found!")
        exit(1)
    
    print(f"Found strategic goal: {goal.name}")
    
    # Get existing entities
    Programme = env['kcca.programme']
    Directorate = env['kcca.directorate']
    Division = env['kcca.division']
    
    # Find infrastructure-related programmes
    infrastructure_programmes = Programme.search([
        '|', '|', '|',
        ('name', 'ilike', 'road'),
        ('name', 'ilike', 'infrastructure'),
        ('name', 'ilike', 'urban'),
        ('name', 'ilike', 'transport')
    ])
    
    print(f"\nFound {len(infrastructure_programmes)} infrastructure-related programmes:")
    for prog in infrastructure_programmes:
        print(f"  - {prog.name}")
    
    # Find Engineering & Technical Services directorate
    engineering_directorates = Directorate.search([
        '|',
        ('name', 'ilike', 'engineering'),
        ('name', 'ilike', 'technical')
    ])
    
    print(f"\nFound {len(engineering_directorates)} engineering-related directorates:")
    for dir in engineering_directorates:
        print(f"  - {dir.name}")
    
    # Find divisions under engineering directorates
    engineering_divisions = Division.search([
        ('directorate_id', 'in', engineering_directorates.ids)
    ])
    
    print(f"\nFound {len(engineering_divisions)} divisions under engineering directorates:")
    for div in engineering_divisions:
        print(f"  - {div.name} (under {div.directorate_id.name})")
    
    # Link programmes to the strategic goal through implementing directorates
    for programme in infrastructure_programmes:
        if engineering_directorates:
            # Link the first engineering directorate to this programme
            programme.write({
                'implementing_directorate_ids': [(6, 0, [engineering_directorates[0].id])]
            })
            print(f"Linked programme '{programme.name}' to directorate '{engineering_directorates[0].name}'")
    
    # Create relationships between programmes and divisions
    DivisionProgrammeRel = env['division.programme.rel']
    
    for programme in infrastructure_programmes:
        for division in engineering_divisions:
            # Check if relationship already exists
            existing_rel = DivisionProgrammeRel.search([
                ('division_id', '=', division.id),
                ('programme_id', '=', programme.id)
            ])
            
            if not existing_rel:
                rel = DivisionProgrammeRel.create({
                    'division_id': division.id,
                    'programme_id': programme.id,
                    'performance_score': 75.0 + (hash(f"{division.id}-{programme.id}") % 20),  # Random score 75-95
                    'implementation_status': 'implementing',
                    'start_date': '2024-01-01',
                    'end_date': '2025-12-31',
                })
                print(f"Created relationship: {division.name} <-> {programme.name} (Score: {rel.performance_score:.1f})")
    
    # Force recomputation of strategic goal metrics
    goal._compute_counts()
    goal._compute_related_entities()
    
    print(f"\n=== Updated Strategic Goal Stats ===")
    print(f"Objectives: {goal.objective_count}")
    print(f"KRAs: {goal.kra_count}")
    print(f"KPIs: {goal.kpi_count}")
    print(f"Related Programmes: {goal.programme_count}")
    print(f"Related Directorates: {goal.directorate_count}")
    print(f"Related Divisions: {goal.division_count}")
    
    # Commit the transaction
    cr.commit()
    
    print("\nLinking completed successfully!")
