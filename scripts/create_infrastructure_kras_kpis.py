#!/usr/bin/env python3
import sys
import os
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo.api import Environment

# Initialize Odoo
odoo.tools.config.parse_config([])
odoo.tools.config['db_host'] = 'localhost'
odoo.tools.config['db_port'] = 5432
odoo.tools.config['db_user'] = 'richards'
odoo.tools.config['db_password'] = False
odoo.tools.config['database'] = 'robust_pmis'

with odoo.registry('robust_pmis').cursor() as cr:
    env = Environment(cr, 1, {})  # uid=1 for admin
    
    print("=== CREATING INFRASTRUCTURE DEVELOPMENT DEMO DATA ===")
    
    # Find the Infrastructure Development strategic objective
    objective = env['strategic.objective'].search([
        ('name', 'ilike', 'Infrastructure Development')
    ], limit=1)
    
    if not objective:
        print("❌ Infrastructure Development objective not found!")
        sys.exit(1)
    
    print(f"📋 Found objective: {objective.name}")
    
    # Create 5 KRAs
    kra_data = [
        {
            'name': 'Transport Infrastructure Development',
            'description': 'Develop and maintain efficient transport infrastructure',
            'sequence': 10,
            'target_value': 100.0,
            'current_value': 75.0,
        },
        {
            'name': 'Urban Housing and Settlement Development', 
            'description': 'Promote sustainable housing development',
            'sequence': 20,
            'target_value': 100.0,
            'current_value': 60.0,
        },
        {
            'name': 'Public Infrastructure Maintenance',
            'description': 'Maintain and upgrade existing public infrastructure',
            'sequence': 30,
            'target_value': 100.0,
            'current_value': 85.0,
        },
        {
            'name': 'Smart City Infrastructure',
            'description': 'Develop ICT and digital infrastructure',
            'sequence': 40,
            'target_value': 100.0,
            'current_value': 45.0,
        },
        {
            'name': 'Environmental Infrastructure',
            'description': 'Develop sustainable environmental infrastructure',
            'sequence': 50,
            'target_value': 100.0,
            'current_value': 70.0,
        }
    ]
    
    created_kras = []
    for kra_info in kra_data:
        existing_kra = env['key.result.area'].search([
            ('name', '=', kra_info['name']),
            ('strategic_objective_id', '=', objective.id)
        ])
        
        if not existing_kra:
            kra = env['key.result.area'].create({
                'name': kra_info['name'],
                'description': kra_info['description'],
                'sequence': kra_info['sequence'],
                'strategic_objective_id': objective.id,
                'target_value': kra_info['target_value'],
                'current_value': kra_info['current_value'],
                'active': True,
                'weight': 1.0,
            })
            created_kras.append(kra)
            print(f"✅ Created KRA: {kra.name}")
        else:
            created_kras.append(existing_kra)
            print(f"📌 Using existing KRA: {existing_kra.name}")
    
    # Create KPIs for first KRA as example
    transport_kra = env['key.result.area'].search([
        ('name', '=', 'Transport Infrastructure Development'),
        ('strategic_objective_id', '=', objective.id)
    ], limit=1)
    
    if transport_kra:
        kpi_data = [
            {
                'name': 'Kilometers of Roads Rehabilitated',
                'description': 'Total kilometers of roads rehabilitated annually',
                'target_value': 150.0,
                'current_value': 112.0,
                'unit_of_measure': 'Kilometers',
                'frequency': 'annual',
            },
            {
                'name': 'Bridge Construction and Rehabilitation',
                'description': 'Number of bridges constructed and rehabilitated',
                'target_value': 5.0,
                'current_value': 3.0,
                'unit_of_measure': 'Number',
                'frequency': 'annual',
            },
            {
                'name': 'Public Transport Coverage',
                'description': 'Percentage of city areas covered by public transport',
                'target_value': 80.0,
                'current_value': 65.0,
                'unit_of_measure': 'Percentage',
                'frequency': 'quarterly',
            },
            {
                'name': 'Traffic Flow Efficiency',
                'description': 'Average traffic flow speed during peak hours',
                'target_value': 35.0,
                'current_value': 25.0,
                'unit_of_measure': 'Km/h',
                'frequency': 'monthly',
            },
            {
                'name': 'Transport Infrastructure Budget Utilization',
                'description': 'Percentage of allocated transport budget utilized',
                'target_value': 95.0,
                'current_value': 78.0,
                'unit_of_measure': 'Percentage',
                'frequency': 'quarterly',
            },
        ]
        
        kpis_created = 0
        for kpi_info in kpi_data:
            existing_kpi = env['key.performance.indicator'].search([
                ('name', '=', kpi_info['name']),
                ('kra_id', '=', transport_kra.id)
            ])
            
            if not existing_kpi:
                kpi = env['key.performance.indicator'].create({
                    'name': kpi_info['name'],
                    'description': kpi_info['description'],
                    'target_value': kpi_info['target_value'],
                    'current_value': kpi_info['current_value'],
                    'unit_of_measure': kpi_info['unit_of_measure'],
                    'frequency': kpi_info['frequency'],
                    'kra_id': transport_kra.id,
                    'active': True,
                    'weight': 1.0,
                })
                kpis_created += 1
                achievement = (kpi_info['current_value'] / kpi_info['target_value']) * 100
                print(f"✅ Created KPI: {kpi.name} ({achievement:.1f}% achievement)")
        
        print(f"📊 Created {kpis_created} KPIs for Transport Infrastructure")
    
    # Commit changes
    cr.commit()
    
    # Show final counts
    objective.invalidate_cache()
    print(f"\n📈 FINAL COUNTS:")
    print(f"   KRAs: {len(objective.kra_ids)}")
    print(f"   KPIs: {len(objective.kra_ids.mapped('kpi_ids'))}")
    print(f"   Programmes: {len(objective.programme_ids)}")
    
    print(f"\n✅ Demo data creation completed successfully!")
