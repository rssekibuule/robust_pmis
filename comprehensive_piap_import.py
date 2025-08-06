#!/usr/bin/env python3
"""
Comprehensive PIAP Actions Import Script
Based on the detailed master table analysis showing ~23 PIAP Actions
"""

def import_comprehensive_piap_actions(env):
    """Import all PIAP Actions from the master table with proper data"""
    
    print("🚀 Starting Comprehensive PIAP Actions Import...")
    print("📊 Analyzing master table data for complete import")
    
    # Get the transport programme
    programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
    if not programme:
        print("❌ Transport Programme not found!")
        return False
    
    # Get objectives and outcomes
    objectives = env['programme.objective'].search([('programme_id', '=', programme.id)])
    if not objectives:
        print("❌ No objectives found!")
        return False
    
    objective = objectives[0]  # Use the first objective
    print(f"✅ Using objective: {objective.name}")
    
    # Get outcomes
    outcomes = env['intermediate.outcome'].search([('objective_id', '=', objective.id)])
    outcome_map = {}
    for outcome in outcomes:
        if 'travel time' in outcome.name.lower():
            outcome_map['reduced_travel_time'] = outcome
        elif 'transport infrastructure' in outcome.name.lower() or 'infrastructure' in outcome.name.lower():
            outcome_map['increased_infrastructure'] = outcome
        elif 'transport safety' in outcome.name.lower() or 'safety' in outcome.name.lower():
            outcome_map['enhanced_safety'] = outcome
    
    print(f"✅ Found {len(outcomes)} outcomes: {list(outcome_map.keys())}")
    
    # Get interventions and outputs
    interventions = env['intervention'].search([('outcome_id', 'in', [o.id for o in outcomes])])
    outputs = env['output'].search([('intervention_id', 'in', [i.id for i in interventions])])
    
    if not outputs:
        print("❌ No outputs found!")
        return False
    
    print(f"✅ Found {len(interventions)} interventions and {len(outputs)} outputs")
    
    # Clear existing PIAP Actions to avoid duplicates
    existing_piap = env['piap.action'].search([('programme_id', '=', programme.id)])
    if existing_piap:
        print(f"🗑️ Removing {len(existing_piap)} existing PIAP Actions to avoid duplicates")
        existing_piap.unlink()
    
    # Comprehensive PIAP Actions from the master table
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
        # Intervention 1.1.1: Construct and upgrade strategic transport infrastructure
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
        # Major Infrastructure Projects
        {
            'name': 'Complete detailed design & Construct BRT Pilot Corridor (Busega-Jinja Road, Kampala-Jinja Road, Kampala-Entebbe Road)',
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
            'name': 'Complete detailed design & Construct BRT Pilot Corridor (Clock Tower to Major Transport Infrastructure Projects)',
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
            'name': 'Complete detailed & Implement the Kampala Flyover Phase 2 comprising of Mukwano-Kabuusu Flyover, Africana, Plaza House and Garden City Junctions',
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
            'name': 'Undertake feasibility studies, detailed designs and implement the Kampala Light rail system',
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
        },
        # Intermediate Outcome 1.2: Increased stock of transport infrastructure
        {
            'name': 'Proportion of city road network paved',
            'outcome': 'increased_infrastructure',
            'baseline_value': 37.0,
            'target_value': 51.0,
            'measurement_unit': 'Percentage',
            'budget_fy2025_26': 39.0,
            'budget_fy2026_27': 46.0,
            'budget_fy2027_28': 48.0,
            'budget_fy2028_29': 51.0,
            'budget_fy2029_30': 51.0,
            'total_budget': 51.0
        },
        {
            'name': 'Km of City Roads Paved',
            'outcome': 'increased_infrastructure',
            'baseline_value': 778.50,
            'target_value': 1394.18,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 86.52,
            'budget_fy2026_27': 122.24,
            'budget_fy2027_28': 52.46,
            'budget_fy2028_29': 84.06,
            'budget_fy2029_30': 51.48,
            'total_budget': 1394.18
        },
        # Intervention 1.2.1: Increase capacity of existing transport infrastructure and services
        {
            'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KIIDP',
            'outcome': 'increased_infrastructure',
            'baseline_value': 44.03,
            'target_value': 44.03,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 24.00,
            'budget_fy2026_27': 20.00,
            'budget_fy2027_28': 0.00,
            'budget_fy2028_29': 0.00,
            'budget_fy2029_30': 0.00,
            'total_budget': 44.03
        },
        {
            'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KIIDP Phase2',
            'outcome': 'increased_infrastructure',
            'baseline_value': 0.00,
            'target_value': 43.85,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 1.62,
            'budget_fy2027_28': 18.54,
            'budget_fy2028_29': 3.40,
            'budget_fy2029_30': 0.00,
            'total_budget': 43.85
        },
        {
            'name': 'Km of KCCA roads & junctions upgraded/ reconstructed under OMAAGP',
            'outcome': 'increased_infrastructure',
            'baseline_value': 0.00,
            'target_value': 105.75,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 14.60,
            'budget_fy2026_27': 22.70,
            'budget_fy2027_28': 25.00,
            'budget_fy2028_29': 25.00,
            'budget_fy2029_30': 18.45,
            'total_budget': 105.75
        },
        {
            'name': 'Km of KCCA roads & junctions upgraded/ reconstructed under KCBSLIP (Colas Project)',
            'outcome': 'increased_infrastructure',
            'baseline_value': 0.00,
            'target_value': 127.00,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 0.00,
            'budget_fy2026_27': 61.69,
            'budget_fy2027_28': 24.00,
            'budget_fy2028_29': 24.00,
            'budget_fy2029_30': 18.00,
            'total_budget': 127.00
        },
        {
            'name': 'Km of KCCA roads & junctions upgraded/ reconstructed under KCBSLIP (Colas Project)',
            'outcome': 'increased_infrastructure',
            'baseline_value': 0.00,
            'target_value': 1.50,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 0.00,
            'budget_fy2026_27': 0.00,
            'budget_fy2027_28': 1.00,
            'budget_fy2028_29': 2.00,
            'budget_fy2029_30': 0.00,
            'total_budget': 1.50
        },
        {
            'name': 'Km of KCCA roads & junctions upgraded/ reconstructed under HCBSLIP (Colas Project)',
            'outcome': 'increased_infrastructure',
            'baseline_value': 0.00,
            'target_value': 30.00,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 0.00,
            'budget_fy2026_27': 0.00,
            'budget_fy2027_28': 0.00,
            'budget_fy2028_29': 15.00,
            'budget_fy2029_30': 15.00,
            'total_budget': 30.00
        },
        {
            'name': 'Km of City junctions upgraded under - SCA Project phase 2',
            'outcome': 'increased_infrastructure',
            'baseline_value': 30.00,
            'target_value': 25.00,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 0.00,
            'budget_fy2026_27': 0.00,
            'budget_fy2027_28': 5.00,
            'budget_fy2028_29': 10.00,
            'budget_fy2029_30': 10.00,
            'total_budget': 25.00
        },
        # PIAP Actions from the detailed table
        {
            'name': 'Implement the Kampala City Road Rehabilitation Project financed by the AfDB (about 8.77 km/USD)',
            'outcome': 'increased_infrastructure',
            'baseline_value': 0.00,
            'target_value': 8.77,
            'measurement_unit': 'Km',
            'budget_fy2025_26': 131.40,
            'budget_fy2026_27': 85.50,
            'budget_fy2027_28': 0.00,
            'budget_fy2028_29': 0.00,
            'budget_fy2029_30': 0.00,
            'total_budget': 217.67
        },
        {
            'name': 'Implement road improvement projects under the GoUoL/UDP financed by the World Bank and Danida & Junctuons',
            'outcome': 'increased_infrastructure',
            'baseline_value': 0.00,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'budget_fy2025_26': 113.86,
            'budget_fy2026_27': 96.41,
            'budget_fy2027_28': 17.66,
            'budget_fy2028_29': 0.00,
            'budget_fy2029_30': 0.00,
            'total_budget': 228.12
        },
        # Intermediate Outcome 1.3: Enhanced transport safety
        {
            'name': 'Fatalities per 100,000 persons (Roads)',
            'outcome': 'enhanced_safety',
            'baseline_value': 11.00,
            'target_value': 2.0,
            'measurement_unit': 'Number',
            'budget_fy2025_26': 10.20,
            'budget_fy2026_27': 8.00,
            'budget_fy2027_28': 8.00,
            'budget_fy2028_29': 6.00,
            'budget_fy2029_30': 4.00,
            'total_budget': 2.0
        },
        {
            'name': 'Proportion of paved road network with street lights',
            'outcome': 'enhanced_safety',
            'baseline_value': 15.0,
            'target_value': 100.0,
            'measurement_unit': 'Percentage',
            'budget_fy2025_26': 15.0,
            'budget_fy2026_27': 30.0,
            'budget_fy2027_28': 50.0,
            'budget_fy2028_29': 75.0,
            'budget_fy2029_30': 100.0,
            'total_budget': 100.0
        },
        # Intervention 1.3.1: Enhance transport safety
        {
            'name': 'Number of Fatalities on City Road',
            'outcome': 'enhanced_safety',
            'baseline_value': 411.0,
            'target_value': 275.0,
            'measurement_unit': 'Number',
            'budget_fy2025_26': 392.0,
            'budget_fy2026_27': 356.0,
            'budget_fy2027_28': 331.0,
            'budget_fy2028_29': 305.0,
            'budget_fy2029_30': 275.0,
            'total_budget': 275.0
        },
        {
            'name': 'Number of road safety Audits inspections conducted',
            'outcome': 'enhanced_safety',
            'baseline_value': 1.00,
            'target_value': 30.0,
            'measurement_unit': 'Number',
            'budget_fy2025_26': 4.0,
            'budget_fy2026_27': 1.0,
            'budget_fy2027_28': 6.0,
            'budget_fy2028_29': 7.0,
            'budget_fy2029_30': 8.0,
            'total_budget': 30.0
        },
        {
            'name': 'Number of Street Lights Installed (Under AfDB Funding)',
            'outcome': 'enhanced_safety',
            'baseline_value': 7568.0,
            'target_value': 15000.0,
            'measurement_unit': 'Number',
            'budget_fy2025_26': 0.30,
            'budget_fy2026_27': 5000.0,
            'budget_fy2027_28': 5000.0,
            'budget_fy2028_29': 2500.0,
            'budget_fy2029_30': 2500.0,
            'total_budget': 15000.0
        },
        {
            'name': 'Number of Street Lights Installed (Under PPP Arrangement)',
            'outcome': 'enhanced_safety',
            'baseline_value': 0.00,
            'target_value': 10000.0,
            'measurement_unit': 'Number',
            'budget_fy2025_26': 0.00,
            'budget_fy2026_27': 2500.0,
            'budget_fy2027_28': 2500.0,
            'budget_fy2028_29': 2500.0,
            'budget_fy2029_30': 2500.0,
            'total_budget': 10000.0
        }
    ]

    # Create PIAP Actions
    created_count = 0
    for action_data in piap_actions_data:
        try:
            # Find appropriate output based on outcome
            outcome_key = action_data['outcome']
            if outcome_key not in outcome_map:
                print(f"⚠️ Outcome {outcome_key} not found, skipping {action_data['name']}")
                continue

            outcome = outcome_map[outcome_key]

            # Find an appropriate output for this outcome
            suitable_outputs = [o for o in outputs if o.intervention_id.outcome_id.id == outcome.id]
            if not suitable_outputs:
                print(f"⚠️ No outputs found for outcome {outcome.name}, skipping {action_data['name']}")
                continue

            output = suitable_outputs[0]  # Use the first suitable output

            # Create PIAP Action
            piap_action = env['piap.action'].create({
                'name': action_data['name'],
                'programme_id': programme.id,
                'objective_id': objective.id,
                'outcome_id': outcome.id,
                'intervention_id': output.intervention_id.id,
                'output_id': output.id,
                'baseline_value': action_data['baseline_value'],
                'target_value': action_data['target_value'],
                'measurement_unit': action_data['measurement_unit'],
                'budget_fy2025_26': action_data['budget_fy2025_26'],
                'budget_fy2026_27': action_data['budget_fy2026_27'],
                'budget_fy2027_28': action_data['budget_fy2027_28'],
                'budget_fy2028_29': action_data['budget_fy2028_29'],
                'budget_fy2029_30': action_data['budget_fy2029_30'],
                'total_budget': action_data['total_budget'],
            })

            created_count += 1
            print(f"✅ Created PIAP Action: {action_data['name']}")

        except Exception as e:
            print(f"❌ Error creating PIAP Action {action_data['name']}: {str(e)}")

    print(f"\n🎉 Import Complete!")
    print(f"📊 Created {created_count} PIAP Actions out of {len(piap_actions_data)} total")

    # Verification
    total_piap = env['piap.action'].search_count([('programme_id', '=', programme.id)])
    print(f"🔍 Total PIAP Actions in database: {total_piap}")

    return True

def verify_import(env):
    """Verify the imported PIAP Actions"""
    print("\n🔍 Verifying PIAP Actions Import...")

    programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
    if not programme:
        print("❌ Programme not found!")
        return

    piap_actions = env['piap.action'].search([('programme_id', '=', programme.id)])
    print(f"📊 Found {len(piap_actions)} PIAP Actions")

    # Group by outcome
    outcomes = {}
    for action in piap_actions:
        outcome_name = action.outcome_id.name if action.outcome_id else 'No Outcome'
        if outcome_name not in outcomes:
            outcomes[outcome_name] = []
        outcomes[outcome_name].append(action.name)

    for outcome, actions in outcomes.items():
        print(f"\n📋 {outcome}: {len(actions)} actions")
        for action in actions[:3]:  # Show first 3
            print(f"   • {action}")
        if len(actions) > 3:
            print(f"   ... and {len(actions) - 3} more")

    # Check budget totals
    total_budget = sum(action.total_budget for action in piap_actions)
    print(f"\n💰 Total Budget across all PIAP Actions: {total_budget:,.2f}")

if __name__ == "__main__":
    print("This script should be run from within Odoo shell")
    print("Usage: exec(open('comprehensive_piap_import.py').read())")
    print("Then: import_comprehensive_piap_actions(env)")
    print("Then: verify_import(env)")
