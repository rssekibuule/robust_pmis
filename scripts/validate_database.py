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
    
    print("=== ODOO DATABASE VALIDATION ===\n")
    
    # 1. Validate Strategic Goals
    Strategic = env['strategic.goal']
    goals = Strategic.search([])
    print(f"📊 STRATEGIC GOALS ({len(goals)} total):")
    for goal in goals:
        print(f"  • {goal.name} (ID: {goal.id})")
        print(f"    - Objectives: {goal.objective_count}")
        print(f"    - KRAs: {goal.kra_count}")
        print(f"    - KPIs: {goal.kpi_count}")
        print(f"    - Programmes: {goal.programme_count}")
        print(f"    - Directorates: {goal.directorate_count}")
        print(f"    - Divisions: {goal.division_count}")
    
    # 2. Validate KPIs
    KPI = env['key.performance.indicator']
    kpis = KPI.search([])
    print(f"\n🎯 KEY PERFORMANCE INDICATORS ({len(kpis)} total):")
    for kpi in kpis[:10]:  # Show first 10
        print(f"  • {kpi.name}")
        print(f"    - Target: {kpi.target_value}, Current: {kpi.current_value}")
        print(f"    - Achievement: {kpi.achievement_percentage:.1f}%")
    if len(kpis) > 10:
        print(f"    ... and {len(kpis) - 10} more KPIs")
    
    # 3. Validate Programmes
    Programme = env['kcca.programme']
    programmes = Programme.search([])
    print(f"\n📋 PROGRAMMES ({len(programmes)} total):")
    infrastructure_programmes = Programme.search([
        '|', '|', '|',
        ('name', 'ilike', 'road'),
        ('name', 'ilike', 'infrastructure'),
        ('name', 'ilike', 'urban'),
        ('name', 'ilike', 'transport')
    ])
    print(f"  Infrastructure Programmes ({len(infrastructure_programmes)}):")
    for prog in infrastructure_programmes:
        print(f"    • {prog.name} (Performance: {prog.overall_performance:.1f}%)")
    
    # 4. Validate Directorates
    Directorate = env['kcca.directorate']
    directorates = Directorate.search([])
    print(f"\n🏢 DIRECTORATES ({len(directorates)} total):")
    for directorate in directorates:
        print(f"  • {directorate.name} (Performance: {directorate.overall_performance:.1f}%)")
    
    # 5. Validate Divisions
    Division = env['kcca.division']
    divisions = Division.search([])
    print(f"\n🌍 DIVISIONS ({len(divisions)} total):")
    for division in divisions:
        print(f"  • {division.name} under {division.directorate_id.name}")
        print(f"    - Performance: {division.overall_performance:.1f}%")
    
    # 6. Validate Performance Dashboard
    Dashboard = env['performance.dashboard']
    dashboards = Dashboard.search([])
    print(f"\n📈 PERFORMANCE DASHBOARD ({len(dashboards)} records):")
    for dashboard in dashboards:
        print(f"  • {dashboard.name}")
        print(f"    - Strategic Goals: {dashboard.total_goals}")
        print(f"    - KPIs: {dashboard.total_kpis} (Avg Performance: {dashboard.avg_kpi_performance:.1f}%)")
        print(f"    - Programmes: {dashboard.total_programmes} (Avg Performance: {dashboard.avg_programme_performance:.1f}%)")
        print(f"    - Directorates: {dashboard.total_directorates} (Avg Performance: {dashboard.avg_directorate_performance:.1f}%)")
        print(f"    - Divisions: {dashboard.total_divisions} (Avg Performance: {dashboard.avg_division_performance:.1f}%)")
    
    # 7. Validate Relationships
    print(f"\n🔗 RELATIONSHIPS VALIDATION:")
    
    # Strategic Objectives
    StrategicObjective = env['strategic.objective']
    objectives = StrategicObjective.search([])
    print(f"  Strategic Objectives: {len(objectives)}")
    
    # KRAs
    KRA = env['key.result.area']
    kras = KRA.search([])
    print(f"  Key Result Areas: {len(kras)}")
    
    # Programme-Directorate relationships
    ProgDirRel = env['programme.directorate.rel']
    prog_dir_rels = ProgDirRel.search([])
    print(f"  Programme-Directorate Relations: {len(prog_dir_rels)}")
    
    # Division-Programme relationships
    DivProgRel = env['division.programme.rel']
    div_prog_rels = DivProgRel.search([])
    print(f"  Division-Programme Relations: {len(div_prog_rels)}")
    
    # 8. Validate Infrastructure Goal Specifically
    infra_goal = Strategic.search([('name', '=', 'Improve Urban Infrastructure')], limit=1)
    if infra_goal:
        print(f"\n🏗️ INFRASTRUCTURE GOAL VALIDATION:")
        print(f"  Goal: {infra_goal.name}")
        print(f"  Linked Programmes ({len(infra_goal.programme_ids)}):")
        for prog in infra_goal.programme_ids:
            print(f"    • {prog.name}")
        print(f"  Linked Directorates ({len(infra_goal.directorate_ids)}):")
        for dir in infra_goal.directorate_ids:
            print(f"    • {dir.name}")
        print(f"  Linked Divisions ({len(infra_goal.division_ids)}):")
        for div in infra_goal.division_ids:
            print(f"    • {div.name}")
    
    # 9. Database Statistics
    print(f"\n📊 DATABASE STATISTICS:")
    print(f"  Total Records:")
    print(f"    - Strategic Goals: {Strategic.search_count([])}")
    print(f"    - Strategic Objectives: {StrategicObjective.search_count([])}")
    print(f"    - Key Result Areas: {KRA.search_count([])}")
    print(f"    - KPIs: {KPI.search_count([])}")
    print(f"    - Programmes: {Programme.search_count([])}")
    print(f"    - Directorates: {Directorate.search_count([])}")
    print(f"    - Divisions: {Division.search_count([])}")
    print(f"    - Programme-Directorate Relations: {ProgDirRel.search_count([])}")
    print(f"    - Division-Programme Relations: {DivProgRel.search_count([])}")
    
    # 10. Performance Metrics Summary
    print(f"\n🎯 PERFORMANCE METRICS SUMMARY:")
    avg_kpi_perf = sum(kpi.achievement_percentage for kpi in kpis) / len(kpis) if kpis else 0
    avg_prog_perf = sum(programmes.mapped('overall_performance')) / len(programmes) if programmes else 0
    avg_dir_perf = sum(directorates.mapped('overall_performance')) / len(directorates) if directorates else 0
    avg_div_perf = sum(divisions.mapped('overall_performance')) / len(divisions) if divisions else 0
    
    print(f"  Average KPI Achievement: {avg_kpi_perf:.1f}%")
    print(f"  Average Programme Performance: {avg_prog_perf:.1f}%")
    print(f"  Average Directorate Performance: {avg_dir_perf:.1f}%")
    print(f"  Average Division Performance: {avg_div_perf:.1f}%")
    
    print(f"\n✅ DATABASE VALIDATION COMPLETED")
    print(f"   Data is successfully committed and accessible!")
