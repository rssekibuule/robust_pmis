#!/usr/bin/env python3
"""
Verification Script for Transport Programme Indicators
Verifies that all 24 indicators are properly implemented with correct hierarchy
"""

import subprocess
import sys
import os
import tempfile

def create_verification_script():
    """Create the verification script"""
    
    script_content = '''
print("🔍 Verifying Transport Programme Indicators Implementation...")

# Get the transport programme
programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
if not programme:
    print("❌ Transport Programme not found!")
    exit()

print(f"✅ Found programme: {programme.name}")

# Get programme objective
objective = env['programme.objective'].search([('programme_id', '=', programme.id)])
if not objective:
    print("❌ Programme objective not found!")
    exit()

objective = objective[0]
print(f"✅ Found objective: {objective.name}")

# Get intermediate outcomes
outcomes = env['intermediate.outcome'].search([('objective_id', '=', objective.id)])
print(f"✅ Found {len(outcomes)} intermediate outcomes:")
for outcome in outcomes:
    print(f"   • {outcome.name}")

# Get interventions
interventions = env['intervention'].search([('outcome_id', 'in', outcomes.ids)])
print(f"✅ Found {len(interventions)} interventions:")
for intervention in interventions:
    print(f"   • {intervention.name}")

# Get outputs
outputs = env['output'].search([('intervention_id', 'in', interventions.ids)])
print(f"✅ Found {len(outputs)} outputs:")
for output in outputs:
    print(f"   • {output.name}")

# Get all PIAP Actions/Indicators
piap_actions = env['piap.action'].search([('programme_id', '=', programme.id)])
print(f"\\n📊 TOTAL INDICATORS: {len(piap_actions)}")

if len(piap_actions) != 24:
    print(f"⚠️ Expected 24 indicators, found {len(piap_actions)}")
else:
    print("✅ Correct number of indicators found!")

# Verify indicators by outcome
print("\\n📋 INDICATORS BY OUTCOME:")
for outcome in outcomes:
    outcome_indicators = env['piap.action'].search([
        ('programme_id', '=', programme.id),
        ('outcome_id', '=', outcome.id)
    ])
    print(f"\\n{outcome.name}: {len(outcome_indicators)} indicators")
    for indicator in outcome_indicators:
        print(f"   • {indicator.name}")
        print(f"     Baseline: {indicator.baseline_value} {indicator.measurement_unit}")
        print(f"     Target: {indicator.target_value} {indicator.measurement_unit}")

# Expected distribution
expected_distribution = {
    '1.1: Reduced travel time': 12,
    '1.2: Increased capacity of existing transport infrastructure and services': 10,
    '1.3: Enhanced transport safety': 2
}

print("\\n🎯 VERIFICATION SUMMARY:")
all_correct = True
for outcome in outcomes:
    outcome_count = env['piap.action'].search_count([
        ('programme_id', '=', programme.id),
        ('outcome_id', '=', outcome.id)
    ])
    expected_count = expected_distribution.get(outcome.name, 0)
    
    if outcome_count == expected_count:
        print(f"✅ {outcome.name}: {outcome_count}/{expected_count} indicators")
    else:
        print(f"❌ {outcome.name}: {outcome_count}/{expected_count} indicators")
        all_correct = False

if all_correct and len(piap_actions) == 24:
    print("\\n🎉 ALL VERIFICATIONS PASSED!")
    print("✅ All 24 transport indicators are properly implemented")
    print("✅ Correct distribution across outcomes")
    print("✅ Proper hierarchy structure in place")
else:
    print("\\n⚠️ VERIFICATION ISSUES FOUND!")
    print("Please check the implementation")

# Sample some indicators to verify data integrity
print("\\n🔍 SAMPLE INDICATOR VERIFICATION:")
sample_indicators = [
    'Average Travel time (Minutes) on KCCA Road Links',
    'Proportion of city road network paved',
    'Fatalities per 100,000 persons (Roads)'
]

for indicator_name in sample_indicators:
    indicator = env['piap.action'].search([
        ('programme_id', '=', programme.id),
        ('name', '=', indicator_name)
    ])
    
    if indicator:
        print(f"✅ {indicator_name}")
        print(f"   Outcome: {indicator.outcome_id.name}")
        print(f"   Intervention: {indicator.intervention_id.name}")
        print(f"   Output: {indicator.output_id.name}")
        print(f"   Baseline: {indicator.baseline_value} {indicator.measurement_unit}")
        print(f"   Target: {indicator.target_value} {indicator.measurement_unit}")
    else:
        print(f"❌ {indicator_name} - NOT FOUND")

print("\\n✅ VERIFICATION COMPLETE!")
'''
    
    return script_content

def run_verification():
    """Run the verification using Odoo shell"""
    
    print("🔍 Starting Transport Indicators Verification...")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_verification_script())
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
        
        # Execute the verification script
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send the verification commands
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
    success = run_verification()
    if success:
        print("\\n🎉 Verification completed successfully!")
    else:
        print("\\n❌ Verification failed!")
        sys.exit(1)
