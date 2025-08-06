#!/usr/bin/env python3
"""
Script to add more PIAP Actions to the Transport Programme
"""

def add_more_piap_actions(env):
    """Add additional PIAP Actions to restore the dataset"""
    
    print("🚀 Adding More PIAP Actions...")
    
    # Get the transport programme
    programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
    if not programme:
        print("❌ Transport Programme not found!")
        return False
    
    # Get the first objective (to avoid the singleton error)
    objectives = env['programme.objective'].search([('programme_id', '=', programme.id)])
    if not objectives:
        print("❌ No objectives found!")
        return False
    
    objective = objectives[0]  # Use the first objective
    print(f"Using objective: {objective.name}")
    
    # Get outcomes
    outcomes = env['intermediate.outcome'].search([('objective_id', '=', objective.id)])
    if not outcomes:
        print("❌ No outcomes found!")
        return False
    
    # Get an existing output to attach actions to
    outputs = env['output'].search([('intervention_id.outcome_id', 'in', [o.id for o in outcomes])])
    if not outputs:
        print("❌ No outputs found!")
        return False
    
    output = outputs[0]
    print(f"Using output: {output.name}")
    
    # Additional PIAP Actions to create
    additional_actions = [
        {
            'name': 'Complete detailed design & Construct BRT Pilot Corridor (Clock Tower to Major Transport Infrastructure Projects)',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'total_budget': 125.0
        },
        {
            'name': 'Complete Kampala Flyover Phase 2 (Mukwano-Kabuusu)',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'total_budget': 200.0
        },
        {
            'name': 'Railway services improvement (Kampala-Mukono)',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Project',
            'total_budget': 75.0
        },
        {
            'name': 'Light rail feasibility studies',
            'baseline_value': 0.0,
            'target_value': 1.0,
            'measurement_unit': 'Study',
            'total_budget': 15.0
        },
        {
            'name': 'AIDS Road Rehabilitation - 8.77 km',
            'baseline_value': 0.0,
            'target_value': 8.77,
            'measurement_unit': 'Km',
            'total_budget': 60.0
        },
        {
            'name': 'Construct Traffic Diversion Flyovers',
            'baseline_value': 0.0,
            'target_value': 3.0,
            'measurement_unit': 'Number',
            'total_budget': 150.0
        },
        {
            'name': 'Upgrade meter gauge commuter rail',
            'baseline_value': 0.0,
            'target_value': 25.0,
            'measurement_unit': 'Km',
            'total_budget': 300.0
        },
        {
            'name': 'Construct Cable Car System',
            'baseline_value': 0.0,
            'target_value': 5.0,
            'measurement_unit': 'Km',
            'total_budget': 250.0
        },
        {
            'name': 'Feasibility study & detailed design for LRT',
            'baseline_value': 0.0,
            'target_value': 100.0,
            'measurement_unit': 'Percentage',
            'total_budget': 50.0
        },
        {
            'name': 'Pave KCCA Road Network',
            'baseline_value': 0.0,
            'target_value': 100.0,
            'measurement_unit': 'Km',
            'total_budget': 500.0
        }
    ]
    
    # Create the additional PIAP Actions
    created_count = 0
    for action_data in additional_actions:
        try:
            piap_action = env['piap.action'].create({
                'name': action_data['name'],
                'output_id': output.id,
                'intervention_id': output.intervention_id.id,
                'outcome_id': output.intervention_id.outcome_id.id,
                'objective_id': objective.id,
                'programme_id': programme.id,
                'baseline_value': action_data['baseline_value'],
                'target_value': action_data['target_value'],
                'measurement_unit': action_data['measurement_unit'],
                'total_budget': action_data['total_budget'],
                'status': 'not_started',
                'progress': 0.0,
                'responsible_user_id': 1
            })
            created_count += 1
            print(f"✅ Created PIAP Action: {piap_action.name}")
        except Exception as e:
            print(f"❌ Failed to create action '{action_data['name']}': {e}")
    
    print(f"\n🎉 Successfully created {created_count} additional PIAP Actions!")
    return True

if __name__ == "__main__":
    print("This script should be run from within Odoo shell")
    print("Usage: exec(open('add_more_piap_actions.py').read())")
    print("Then: result = add_more_piap_actions(env)")
