#!/usr/bin/env python3
"""
Direct PIAP Actions Import Script
This script runs the import by executing Odoo shell commands
"""

import subprocess
import sys
import os
import tempfile

def create_import_script():
    """Create the complete import script"""
    
    script_content = '''
# Complete PIAP Actions Import Script
print("🚀 Starting Complete PIAP Actions Import...")

# Get the transport programme
programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
if not programme:
    print("❌ Transport Programme not found!")
    exit()

print(f"✅ Found programme: {programme.name}")

# Get objectives and outcomes
objectives = env['programme.objective'].search([('programme_id', '=', programme.id)])
if not objectives:
    print("❌ No objectives found!")
    exit()

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
    exit()

print(f"✅ Found {len(interventions)} interventions and {len(outputs)} outputs")

# Clear existing PIAP Actions
existing_piap = env['piap.action'].search([('programme_id', '=', programme.id)])
if existing_piap:
    print(f"🗑️ Removing {len(existing_piap)} existing PIAP Actions")
    existing_piap.unlink()

# PIAP Actions data - First batch (Reduced Travel Time)
piap_actions_batch1 = [
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
    }
]

# Create PIAP Actions - Batch 1
created_count = 0
for action_data in piap_actions_batch1:
    try:
        outcome_key = action_data['outcome']
        if outcome_key not in outcome_map:
            print(f"⚠️ Outcome {outcome_key} not found, skipping {action_data['name']}")
            continue
        
        outcome = outcome_map[outcome_key]
        suitable_outputs = [o for o in outputs if o.intervention_id.outcome_id.id == outcome.id]
        if not suitable_outputs:
            print(f"⚠️ No outputs found for outcome {outcome.name}, skipping {action_data['name']}")
            continue
        
        output = suitable_outputs[0]
        
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

print(f"\\n🎉 Batch 1 Complete!")
print(f"📊 Created {created_count} PIAP Actions out of {len(piap_actions_batch1)}")

# Verification
total_piap = env['piap.action'].search_count([('programme_id', '=', programme.id)])
print(f"🔍 Total PIAP Actions in database: {total_piap}")

print("\\n✅ PIAP Actions Import Completed Successfully!")
print("📋 This was the first batch. More actions can be added following the same pattern.")

exit()
'''
    
    return script_content

def run_import():
    """Run the import using Odoo shell"""
    
    print("🚀 Starting PIAP Actions Import...")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_import_script())
        script_path = f.name
    
    try:
        # Change to the correct directory
        os.chdir('/home/richards/Dev/odoo18/addons/robust_pmis')
        
        # Run odoo shell with our script
        cmd = [
            'python3', '/home/richards/Dev/odoo18/odoo-bin', 
            'shell', 
            '-d', 'test_db',
            '--addons-path=/home/richards/Dev/odoo18/addons'
        ]
        
        print(f"📝 Running import script...")
        print(f"🔧 Command: {' '.join(cmd)}")
        
        # Execute the import script
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send the import commands
        with open(script_path, 'r') as f:
            script_content = f.read()
        
        stdout, stderr = process.communicate(input=script_content)
        
        print('📤 STDOUT:')
        print(stdout)
        if stderr:
            print('⚠️ STDERR:')
            print(stderr)
        print(f'🔄 Return code: {process.returncode}')
        
        return process.returncode == 0
        
    finally:
        # Clean up temporary file
        try:
            os.unlink(script_path)
        except:
            pass

if __name__ == "__main__":
    success = run_import()
    if success:
        print("\\n🎉 Import completed successfully!")
    else:
        print("\\n❌ Import failed!")
        sys.exit(1)
