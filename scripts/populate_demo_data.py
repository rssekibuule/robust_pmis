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
    
    print("Populating KCCA Performance Management System with demo data...")
    
    # 1. Create Strategic Goals
    goal_data = [
        {
            'name': 'Improve Urban Infrastructure',
            'description': 'Enhance road networks, drainage systems, and public facilities',
            'active': True
        },
        {
            'name': 'Enhance Service Delivery',
            'description': 'Improve efficiency and quality of public services',
            'active': True
        },
        {
            'name': 'Strengthen Revenue Collection',
            'description': 'Optimize tax collection and revenue generation',
            'active': True
        }
    ]
    
    Strategic = env['strategic.goal']
    created_goals = []
    for data in goal_data:
        goal = Strategic.create(data)
        created_goals.append(goal)
        print(f"Created Strategic Goal: {goal.name}")
    
    # Create KRAs (Key Result Areas) for each strategic goal
    KRA = env['key.result.area']
    created_kras = []
    
    kra_data = [
        {
            'name': 'Infrastructure Quality Management',
            'description': 'Maintain and improve urban infrastructure standards',
            'strategic_goal_id': created_goals[0].id,  # Improve Urban Infrastructure
        },
        {
            'name': 'Service Excellence',
            'description': 'Enhance quality and efficiency of public services',
            'strategic_goal_id': created_goals[1].id,  # Enhance Service Delivery
        },
        {
            'name': 'Revenue Optimization',
            'description': 'Maximize revenue collection and financial efficiency',
            'strategic_goal_id': created_goals[2].id,  # Strengthen Revenue Collection
        }
    ]
    
    for data in kra_data:
        kra = KRA.create(data)
        created_kras.append(kra)
        print(f"Created KRA: {kra.name}")
    
    # 2. Create Directorates
    directorate_data = [
        {
            'name': 'Engineering & Technical Services',
            'code': 'ETS',
            'description': 'Infrastructure development and maintenance',
            'overall_performance': 85.2,
            'active': True
        },
        {
            'name': 'Health Services',
            'code': 'HS',
            'description': 'Public health services and healthcare delivery',
            'overall_performance': 78.9,
            'active': True
        },
        {
            'name': 'Education Services',
            'code': 'ES',
            'description': 'Educational programs and school management',
            'overall_performance': 92.1,
            'active': True
        },
        {
            'name': 'Revenue & Finance',
            'code': 'RF',
            'description': 'Financial management and revenue collection',
            'overall_performance': 71.4,
            'active': True
        }
    ]
    
    Directorate = env['kcca.directorate']
    created_directorates = []
    for data in directorate_data:
        directorate = Directorate.create(data)
        created_directorates.append(directorate)
        print(f"Created Directorate: {directorate.name}")
    
    # 3. Create Divisions linked to directorates
    division_data = [
        {
            'name': 'Central Division',
            'code': 'CD',
            'description': 'Central business district administration',
            'overall_performance': 88.5,
            'directorate_id': created_directorates[0].id,  # Engineering & Technical Services
            'active': True
        },
        {
            'name': 'Kawempe Division',
            'code': 'KD',
            'description': 'Northern suburban division',
            'overall_performance': 76.3,
            'directorate_id': created_directorates[1].id,  # Health Services
            'active': True
        },
        {
            'name': 'Makindye Division',
            'code': 'MD',
            'description': 'Southern residential division',
            'overall_performance': 82.7,
            'directorate_id': created_directorates[2].id,  # Education Services
            'active': True
        },
        {
            'name': 'Nakawa Division',
            'code': 'ND',
            'description': 'Eastern industrial division',
            'overall_performance': 79.8,
            'directorate_id': created_directorates[0].id,  # Engineering & Technical Services
            'active': True
        },
        {
            'name': 'Rubaga Division',
            'code': 'RD',
            'description': 'Western mixed-use division',
            'overall_performance': 84.1,
            'directorate_id': created_directorates[3].id,  # Revenue & Finance
            'active': True
        }
    ]
    
    Division = env['kcca.division']
    for data in division_data:
        division = Division.create(data)
        print(f"Created Division: {division.name}")
    
    # 4. Create Programmes
    programme_data = [
        {
            'name': 'Road Rehabilitation Programme',
            'code': 'RRP',
            'description': 'Comprehensive road network improvement',
            'overall_performance': 73.6,
            'active': True
        },
        {
            'name': 'Waste Management Enhancement',
            'code': 'WME',
            'description': 'Solid waste collection and disposal improvement',
            'overall_performance': 81.2,
            'active': True
        },
        {
            'name': 'Primary Healthcare Expansion',
            'code': 'PHE',
            'description': 'Expand access to primary healthcare services',
            'overall_performance': 89.4,
            'active': True
        },
        {
            'name': 'Digital Revenue Collection',
            'code': 'DRC',
            'description': 'Modernize tax and fee collection systems',
            'overall_performance': 65.8,
            'active': True
        },
        {
            'name': 'Urban Planning & Development',
            'code': 'UPD',
            'description': 'Strategic urban development planning',
            'overall_performance': 77.9,
            'active': True
        }
    ]
    
    Programme = env['kcca.programme']
    for data in programme_data:
        programme = Programme.create(data)
        print(f"Created Programme: {programme.name}")
    
    # 5. Create KPIs with performance data linked to KRAs
    kpi_data = [
        {
            'name': 'Road Network Quality Index',
            'description': 'Percentage of roads in good condition',
            'target_value': 85.0,
            'current_value': 72.4,
            'measurement_unit': 'percentage',
            'kra_id': created_kras[0].id,  # Infrastructure Quality Management
            'active': True
        },
        {
            'name': 'Waste Collection Coverage',
            'description': 'Percentage of areas with regular waste collection',
            'target_value': 95.0,
            'current_value': 84.7,
            'measurement_unit': 'percentage',
            'kra_id': created_kras[0].id,  # Infrastructure Quality Management
            'active': True
        },
        {
            'name': 'Healthcare Service Accessibility',
            'description': 'Population within 2km of health facility',
            'target_value': 95.0,
            'current_value': 91.2,
            'measurement_unit': 'percentage',
            'kra_id': created_kras[1].id,  # Service Excellence
            'active': True
        },
        {
            'name': 'Revenue Collection Efficiency',
            'description': 'Percentage of targeted revenue collected',
            'target_value': 90.0,
            'current_value': 68.9,
            'measurement_unit': 'percentage',
            'kra_id': created_kras[2].id,  # Revenue Optimization
            'active': True
        },
        {
            'name': 'Citizen Satisfaction Index',
            'description': 'Overall citizen satisfaction with KCCA services',
            'target_value': 85.0,
            'current_value': 76.8,
            'measurement_unit': 'index',
            'kra_id': created_kras[1].id,  # Service Excellence
            'active': True
        }
    ]
    
    KPI = env['key.performance.indicator']
    for data in kpi_data:
        kpi = KPI.create(data)
        print(f"Created KPI: {kpi.name}")
    
    # Commit the transaction
    cr.commit()
    
    print("\nDemo data population completed successfully!")
    print(f"Created {len(goal_data)} Strategic Goals")
    print(f"Created {len(kra_data)} Key Result Areas")
    print(f"Created {len(directorate_data)} Directorates") 
    print(f"Created {len(division_data)} Divisions")
    print(f"Created {len(programme_data)} Programmes")
    print(f"Created {len(kpi_data)} KPIs")
