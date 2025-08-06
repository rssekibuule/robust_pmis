#!/usr/bin/env python3
"""
Complete PIAP Actions Import Script
This script creates the hierarchy and imports all PIAP Actions in one transaction
"""

import subprocess
import sys
import os
import tempfile

def create_complete_script():
    """Create the complete import script"""
    
    script_content = '''
print("🚀 Starting Complete PIAP Actions Import with Hierarchy Setup...")

# Get the transport programme
programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
if not programme:
    print("❌ Transport Programme not found!")
    exit()

print(f"✅ Found programme: {programme.name}")

# Create Programme Objective if it doesn't exist
objectives = env['programme.objective'].search([('programme_id', '=', programme.id)])
if not objectives:
    print("📋 Creating Programme Objective...")
    objective = env['programme.objective'].create({
        'name': 'To develop an inter-modal and seamless transport infrastructure and services',
        'programme_id': programme.id,
        'description': 'Main objective for the Integrated Transport Infrastructure and Services programme',
        'sequence': 1
    })
    print(f"✅ Created objective: {objective.name}")
else:
    objective = objectives[0]
    print(f"✅ Using existing objective: {objective.name}")

# Create Intermediate Outcomes
outcomes_data = [
    {
        'name': '1.1: Reduced travel time',
        'description': 'Reduced travel time for commuters and goods',
        'sequence': 1,
        'key': 'reduced_travel_time'
    },
    {
        'name': '1.2: Increased capacity of existing transport infrastructure and services',
        'description': 'Enhanced capacity of transport infrastructure',
        'sequence': 2,
        'key': 'increased_infrastructure'
    },
    {
        'name': '1.3: Enhanced transport safety',
        'description': 'Improved safety measures in transport systems',
        'sequence': 3,
        'key': 'enhanced_safety'
    }
]

outcome_records = {}
for outcome_data in outcomes_data:
    existing = env['intermediate.outcome'].search([
        ('objective_id', '=', objective.id),
        ('name', '=', outcome_data['name'])
    ])
    
    if not existing:
        print(f"📋 Creating outcome: {outcome_data['name']}")
        outcome = env['intermediate.outcome'].create({
            'name': outcome_data['name'],
            'description': outcome_data['description'],
            'objective_id': objective.id,
            'sequence': outcome_data['sequence']
        })
        print(f"✅ Created outcome: {outcome.name}")
    else:
        outcome = existing[0]
        print(f"✅ Using existing outcome: {outcome.name}")
    
    outcome_records[outcome_data['key']] = outcome

print(f"✅ Setup {len(outcome_records)} outcomes")

# Create Interventions for each outcome
interventions_data = [
    {
        'name': '1.1.1: Construct and upgrade strategic transport infrastructure',
        'outcome_key': 'reduced_travel_time',
        'description': 'Construction and upgrading of strategic transport infrastructure',
        'sequence': 1
    },
    {
        'name': '1.2.1: Increase capacity of existing transport infrastructure and services',
        'outcome_key': 'increased_infrastructure',
        'description': 'Increasing capacity of existing transport infrastructure',
        'sequence': 1
    },
    {
        'name': '1.3.1: Enhance transport safety',
        'outcome_key': 'enhanced_safety',
        'description': 'Enhancement of transport safety measures',
        'sequence': 1
    }
]

intervention_records = {}
for intervention_data in interventions_data:
    outcome_key = intervention_data['outcome_key']
    if outcome_key not in outcome_records:
        print(f"⚠️ Outcome {outcome_key} not found, skipping intervention")
        continue
    
    outcome = outcome_records[outcome_key]
    
    existing = env['intervention'].search([
        ('outcome_id', '=', outcome.id),
        ('name', '=', intervention_data['name'])
    ])
    
    if not existing:
        print(f"📋 Creating intervention: {intervention_data['name']}")
        intervention = env['intervention'].create({
            'name': intervention_data['name'],
            'description': intervention_data['description'],
            'outcome_id': outcome.id,
            'sequence': intervention_data['sequence']
        })
        print(f"✅ Created intervention: {intervention.name}")
    else:
        intervention = existing[0]
        print(f"✅ Using existing intervention: {intervention.name}")
    
    intervention_records[outcome_key] = intervention

print(f"✅ Setup {len(intervention_records)} interventions")

# Create Outputs for each intervention
outputs_data = [
    {
        'name': '1.1.1.1: Strategic transport infrastructure constructed and upgraded',
        'intervention_key': 'reduced_travel_time',
        'description': 'Output for strategic transport infrastructure',
        'sequence': 1
    },
    {
        'name': '1.2.1.1: Capacity of existing transport infrastructure increased',
        'intervention_key': 'increased_infrastructure',
        'description': 'Output for increased infrastructure capacity',
        'sequence': 1
    },
    {
        'name': '1.3.1.1: Transport safety enhanced',
        'intervention_key': 'enhanced_safety',
        'description': 'Output for enhanced transport safety',
        'sequence': 1
    }
]

output_records = {}
for output_data in outputs_data:
    intervention_key = output_data['intervention_key']
    if intervention_key not in intervention_records:
        print(f"⚠️ Intervention {intervention_key} not found, skipping output")
        continue
    
    intervention = intervention_records[intervention_key]
    
    existing = env['output'].search([
        ('intervention_id', '=', intervention.id),
        ('name', '=', output_data['name'])
    ])
    
    if not existing:
        print(f"📋 Creating output: {output_data['name']}")
        output = env['output'].create({
            'name': output_data['name'],
            'description': output_data['description'],
            'intervention_id': intervention.id,
            'sequence': output_data['sequence']
        })
        print(f"✅ Created output: {output.name}")
    else:
        output = existing[0]
        print(f"✅ Using existing output: {output.name}")
    
    output_records[intervention_key] = output

print(f"✅ Setup {len(output_records)} outputs")

# Clear existing PIAP Actions
existing_piap = env['piap.action'].search([('programme_id', '=', programme.id)])
if existing_piap:
    print(f"🗑️ Removing {len(existing_piap)} existing PIAP Actions")
    existing_piap.unlink()

# PIAP Actions data from master table (first batch)
piap_actions_data = [
    # Outcome 1.1: Reduced travel time
    {
        'name': 'Average Travel time (Minutes) on KCCA Road Links',
        'outcome_key': 'reduced_travel_time',
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
        'outcome_key': 'reduced_travel_time',
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
        'outcome_key': 'reduced_travel_time',
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
        'outcome_key': 'reduced_travel_time',
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
        'outcome_key': 'reduced_travel_time',
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

# Create PIAP Actions
created_count = 0
for action_data in piap_actions_data:
    try:
        outcome_key = action_data['outcome_key']
        if outcome_key not in outcome_records:
            print(f"⚠️ Outcome {outcome_key} not found, skipping {action_data['name']}")
            continue
        
        outcome = outcome_records[outcome_key]
        intervention = intervention_records[outcome_key]
        output = output_records[outcome_key]
        
        piap_action = env['piap.action'].create({
            'name': action_data['name'],
            'programme_id': programme.id,
            'objective_id': objective.id,
            'outcome_id': outcome.id,
            'intervention_id': intervention.id,
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

print(f"\\n🎉 Import Complete!")
print(f"📊 Created {created_count} PIAP Actions out of {len(piap_actions_data)}")

# Verification
total_piap = env['piap.action'].search_count([('programme_id', '=', programme.id)])
print(f"🔍 Total PIAP Actions in database: {total_piap}")

print("\\n✅ PIAP Actions Import Completed Successfully!")
print("📋 This was the first batch (5 actions). More can be added following the same pattern.")

exit()
'''
    
    return script_content

def run_complete_import():
    """Run the complete import using Odoo shell"""
    
    print("🚀 Starting Complete PIAP Actions Import...")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_complete_script())
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
        
        print(f"🔧 Command: {' '.join(cmd)}")
        
        # Execute the complete import script
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
    success = run_complete_import()
    if success:
        print("\\n🎉 Complete import completed successfully!")
    else:
        print("\\n❌ Complete import failed!")
        sys.exit(1)
