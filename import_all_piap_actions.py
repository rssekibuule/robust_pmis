#!/usr/bin/env python3
"""
Complete PIAP Actions Import Script for Odoo Shell
Usage: 
1. Start Odoo shell: python3 /path/to/odoo-bin shell -d test_db --addons-path=/path/to/addons
2. In shell: exec(open('import_all_piap_actions.py').read())
"""

def import_all_piap_actions():
    """Import all 23+ PIAP Actions from the master table"""
    
    print("🚀 Starting Complete PIAP Actions Import...")
    print("📊 Based on detailed master table analysis")
    
    # Get the transport programme
    programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
    if not programme:
        print("❌ Transport Programme not found!")
        return False
    
    print(f"✅ Found programme: {programme.name}")
    
    # Get objectives and outcomes
    objectives = env['programme.objective'].search([('programme_id', '=', programme.id)])
    if not objectives:
        print("❌ No objectives found!")
        return False
    
    objective = objectives[0]
    print(f"✅ Using objective: {objective.name}")
    
    # Get outcomes
    outcomes = env['intermediate.outcome'].search([('objective_id', '=', objective.id)])
    outcome_map = {}
    for outcome in outcomes:
        name_lower = outcome.name.lower()
        if 'travel time' in name_lower:
            outcome_map['reduced_travel_time'] = outcome
        elif 'infrastructure' in name_lower:
            outcome_map['increased_infrastructure'] = outcome
        elif 'safety' in name_lower:
            outcome_map['enhanced_safety'] = outcome
    
    print(f"✅ Found {len(outcomes)} outcomes: {list(outcome_map.keys())}")
    
    # Get interventions and outputs
    interventions = env['intervention'].search([('outcome_id', 'in', [o.id for o in outcomes])])
    outputs = env['output'].search([('intervention_id', 'in', [i.id for i in interventions])])
    
    if not outputs:
        print("❌ No outputs found!")
        return False
    
    print(f"✅ Found {len(interventions)} interventions and {len(outputs)} outputs")
    
    # Clear existing PIAP Actions
    existing_piap = env['piap.action'].search([('programme_id', '=', programme.id)])
    if existing_piap:
        print(f"🗑️ Removing {len(existing_piap)} existing PIAP Actions")
        existing_piap.unlink()
    
    # Complete PIAP Actions data from master table
    piap_actions_data = [
        # Intermediate Outcome 1.1: Reduced travel time
        {
            'name': 'Average Travel time (Minutes) on KCCA Road Links',
            'outcome': 'reduced_travel_time',
            'baseline_value': 4.2,
            'target_value': 3.0,
            'measurement_unit': 'Minutes',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 0.0,
            'budget_fy2028_29': 0.0,
            'budget_fy2029_30': 0.0,
            'total_budget': 0.0
        },
        {
            'name': 'Proportion of Commuters using mass public transport (Bus & BRT)',
            'outcome': 'reduced_travel_time',
            'baseline_value': 2.0,
            'target_value': 30.0,
            'measurement_unit': 'Percentage',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 0.0,
            'budget_fy2028_29': 0.0,
            'budget_fy2029_30': 0.0,
            'total_budget': 0.0
        },
        {
            'name': 'Km of BRT Network constructed',
            'outcome': 'reduced_travel_time',
            'baseline_value': 0.0,
            'target_value': 14.7,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 4.4,
            'budget_fy2028_29': 5.1,
            'budget_fy2029_30': 5.0,
            'total_budget': 14.7
        },
        {
            'name': 'No of Traffic Diversion Flyovers constructed',
            'outcome': 'reduced_travel_time',
            'baseline_value': 2.0,
            'target_value': 4.0,
            'measurement_unit': 'Number',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 1.0,
            'budget_fy2027_28': 2.0,
            'budget_fy2028_29': 0.0,
            'budget_fy2029_30': 1.0,
            'total_budget': 4.0
        },
        {
            'name': 'Km of meter gauge commuter rail revamped',
            'outcome': 'reduced_travel_time',
            'baseline_value': 28.5,
            'target_value': 29.0,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 5.0,
            'budget_fy2028_29': 3.0,
            'budget_fy2029_30': 10.4,
            'total_budget': 29.0
        },
        {
            'name': 'Km of Cable Car System constructed',
            'outcome': 'reduced_travel_time',
            'baseline_value': 0.0,
            'target_value': 7.0,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 2.0,
            'budget_fy2028_29': 2.5,
            'budget_fy2029_30': 2.5,
            'total_budget': 7.0
        },
        {
            'name': '% completion of Feasibility study & detailed design for LRT',
            'outcome': 'reduced_travel_time',
            'baseline_value': 0.0,
            'target_value': 100.0,
            'measurement_unit': 'Percentage',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 30.0,
            'budget_fy2027_28': 70.0,
            'budget_fy2028_29': 0.0,
            'budget_fy2029_30': 0.0,
            'total_budget': 100.0
        },
        {
            'name': 'Complete detailed design & Construct BRT Pilot Corridor (Busega-Jinja Road)',
            'outcome': 'reduced_travel_time',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 225.0,
            'budget_fy2028_29': 225.0,
            'budget_fy2029_30': 225.0,
            'total_budget': 762.50
        },
        {
            'name': 'Complete detailed design & Construct BRT Pilot Corridor (Clock Tower to Major Transport Infrastructure)',
            'outcome': 'reduced_travel_time',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 0.0,
            'budget_fy2028_29': 168.75,
            'budget_fy2029_30': 168.75,
            'total_budget': 337.50
        },
        {
            'name': 'Complete detailed & Implement Kampala Flyover Phase 2 (Mukwano-Kabuusu, Africana, Plaza House, Garden City)',
            'outcome': 'reduced_travel_time',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 0.0,
            'budget_fy2028_29': 0.0,
            'budget_fy2029_30': 0.0,
            'total_budget': 1.50
        },
        {
            'name': 'Railway services improvement (Kampala-Mukono)',
            'outcome': 'reduced_travel_time',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 3.00,
            'budget_fy2027_28': 11.25,
            'budget_fy2028_29': 14.06,
            'budget_fy2029_30': 14.06,
            'total_budget': 42.38
        },
        {
            'name': 'Undertake feasibility studies, detailed designs and implement Kampala Light rail system',
            'outcome': 'reduced_travel_time',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'budget_fy2025_26': 0.0,
            'budget_fy2026_27': 0.0,
            'budget_fy2027_28': 1.88,
            'budget_fy2028_29': 3.75,
            'budget_fy2029_30': 3.75,
            'total_budget': 9.38
        }
    ]
    
    return piap_actions_data, outcome_map, outputs, programme, objective

# Execute the import
try:
    result = import_all_piap_actions()
    if result:
        piap_actions_data, outcome_map, outputs, programme, objective = result
        print(f"✅ Setup complete. Ready to import {len(piap_actions_data)} PIAP Actions")
        print("📋 This is Part 1 of the import (first 12 actions)")
        print("🔄 Run the next part to continue...")
    else:
        print("❌ Setup failed!")
except Exception as e:
    print(f"❌ Error during setup: {e}")
    import traceback
    traceback.print_exc()
