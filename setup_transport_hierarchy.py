#!/usr/bin/env python3
"""
Setup Transport Programme Hierarchy Script
This creates the complete hierarchy: Programme → Objective → Outcomes → Interventions → Outputs
"""

import subprocess
import sys
import os
import tempfile

def create_hierarchy_script():
    """Create the hierarchy setup script"""
    
    script_content = '''
print("🚀 Setting up Transport Programme Hierarchy...")

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
        'sequence': 1
    },
    {
        'name': '1.2: Increased capacity of existing transport infrastructure and services',
        'description': 'Enhanced capacity of transport infrastructure',
        'sequence': 2
    },
    {
        'name': '1.3: Enhanced transport safety',
        'description': 'Improved safety measures in transport systems',
        'sequence': 3
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
    
    # Store for later use
    if 'travel time' in outcome.name.lower():
        outcome_records['reduced_travel_time'] = outcome
    elif 'infrastructure' in outcome.name.lower():
        outcome_records['increased_infrastructure'] = outcome
    elif 'safety' in outcome.name.lower():
        outcome_records['enhanced_safety'] = outcome

print(f"✅ Created/found {len(outcome_records)} outcomes")

# Create Interventions for each outcome
interventions_data = [
    {
        'name': '1.1.1: Construct and upgrade strategic transport infrastructure',
        'outcome': 'reduced_travel_time',
        'description': 'Construction and upgrading of strategic transport infrastructure',
        'sequence': 1
    },
    {
        'name': '1.2.1: Increase capacity of existing transport infrastructure and services',
        'outcome': 'increased_infrastructure',
        'description': 'Increasing capacity of existing transport infrastructure',
        'sequence': 1
    },
    {
        'name': '1.3.1: Enhance transport safety',
        'outcome': 'enhanced_safety',
        'description': 'Enhancement of transport safety measures',
        'sequence': 1
    }
]

intervention_records = {}
for intervention_data in interventions_data:
    outcome_key = intervention_data['outcome']
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

print(f"✅ Created/found {len(intervention_records)} interventions")

# Create Outputs for each intervention
outputs_data = [
    {
        'name': '1.1.1.1: Strategic transport infrastructure constructed and upgraded',
        'intervention': 'reduced_travel_time',
        'description': 'Output for strategic transport infrastructure',
        'sequence': 1
    },
    {
        'name': '1.2.1.1: Capacity of existing transport infrastructure increased',
        'intervention': 'increased_infrastructure',
        'description': 'Output for increased infrastructure capacity',
        'sequence': 1
    },
    {
        'name': '1.3.1.1: Transport safety enhanced',
        'intervention': 'enhanced_safety',
        'description': 'Output for enhanced transport safety',
        'sequence': 1
    }
]

output_records = {}
for output_data in outputs_data:
    intervention_key = output_data['intervention']
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

print(f"✅ Created/found {len(output_records)} outputs")

print("\\n🎉 Transport Programme Hierarchy Setup Complete!")
print(f"📊 Summary:")
print(f"   • Programme: {programme.name}")
print(f"   • Objective: {objective.name}")
print(f"   • Outcomes: {len(outcome_records)}")
print(f"   • Interventions: {len(intervention_records)}")
print(f"   • Outputs: {len(output_records)}")

print("\\n✅ Ready for PIAP Actions import!")

exit()
'''
    
    return script_content

def run_hierarchy_setup():
    """Run the hierarchy setup using Odoo shell"""
    
    print("🚀 Starting Transport Programme Hierarchy Setup...")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_hierarchy_script())
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
        
        # Execute the hierarchy setup script
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send the setup commands
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
    success = run_hierarchy_setup()
    if success:
        print("\\n🎉 Hierarchy setup completed successfully!")
    else:
        print("\\n❌ Hierarchy setup failed!")
        sys.exit(1)
