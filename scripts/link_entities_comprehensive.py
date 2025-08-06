#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import random

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
    
    # Create strategic objective to link programmes
    StrategicObjective = env['strategic.objective']
    
    objective = StrategicObjective.search([
        ('strategic_goal_id', '=', goal.id),
        ('name', 'ilike', 'infrastructure')
    ], limit=1)
    
    if not objective:
        objective = StrategicObjective.create({
            'name': 'Infrastructure Development',
            'description': 'Develop and maintain urban infrastructure systems',
            'strategic_goal_id': goal.id,
        })
        print(f"Created strategic objective: {objective.name}")
    else:
        print(f"Found existing strategic objective: {objective.name}")
    
    # Link programmes to the strategic objective
    existing_programme_ids = objective.programme_ids.ids
    new_programme_ids = list(set(infrastructure_programmes.ids + existing_programme_ids))
    
    objective.write({
        'programme_ids': [(6, 0, new_programme_ids)]
    })
    print(f"Linked {len(infrastructure_programmes)} programmes to strategic objective")
    
    # Link programmes to engineering directorates
    ProgrammeDirectorateRel = env['programme.directorate.rel']
    
    for programme in infrastructure_programmes:
        for directorate in engineering_directorates[:2]:  # Link to first 2 directorates
            existing_rel = ProgrammeDirectorateRel.search([
                ('programme_id', '=', programme.id),
                ('directorate_id', '=', directorate.id)
            ])
            
            if not existing_rel:
                rel = ProgrammeDirectorateRel.create({
                    'programme_id': programme.id,
                    'directorate_id': directorate.id,
                    'implementation_role': 'primary',
                    'responsibility_percentage': 80.0 + random.uniform(0, 20),
                })
                print(f"Created programme-directorate relationship: {programme.name} <-> {directorate.name}")
    
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
                score = 75.0 + random.uniform(0, 20)  # Random score 75-95
                rel = DivisionProgrammeRel.create({
                    'division_id': division.id,
                    'programme_id': programme.id,
                    'performance_score': score,
                    'implementation_status': 'implementing',
                    'start_date': '2024-01-01',
                    'end_date': '2025-12-31',
                    'allocated_budget': 100000 + random.randint(0, 500000),
                    'utilized_budget': 50000 + random.randint(0, 150000),
                    'target_beneficiaries': 500 + random.randint(0, 2000),
                    'actual_beneficiaries': 300 + random.randint(0, 1000),
                    'completion_percentage': 40.0 + random.uniform(0, 40),
                })
                print(f"Created relationship: {division.name} <-> {programme.name} (Score: {rel.performance_score:.1f}%)")
    
    # Force recomputation of strategic goal metrics
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
    
    # Show the actual related entities
    print(f"\nProgrammes linked via objectives: {len(goal.programme_ids)}")
    for prog in goal.programme_ids:
        print(f"  - {prog.name}")
    
    print(f"\nDirectorates: {len(goal.directorate_ids)}")
    for dir in goal.directorate_ids:
        print(f"  - {dir.name}")
    
    print(f"\nDivisions: {len(goal.division_ids)}")
    for div in goal.division_ids:
        print(f"  - {div.name}")
    
    # Commit the transaction
    cr.commit()
    
    print("\nLinking completed successfully!")
