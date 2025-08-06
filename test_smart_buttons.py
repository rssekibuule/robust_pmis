#!/usr/bin/env python3
"""
Test Smart Buttons for Programme Objectives
Verifies that all smart buttons work correctly and show proper counts
"""

import subprocess
import sys
import os
import tempfile

def create_test_script():
    """Create the test script"""
    
    script_content = '''
print("🔍 Testing Programme Objective Smart Buttons...")

# Get the transport programme objective
programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
if not programme:
    print("❌ Transport Programme not found!")
    exit()

objective = env['programme.objective'].search([('programme_id', '=', programme.id)])
if not objective:
    print("❌ Programme objective not found!")
    exit()

objective = objective[0]
print(f"✅ Found objective: {objective.name}")

# Test computed fields
print(f"\\n📊 SMART BUTTON COUNTS:")
print(f"   • Outcomes: {objective.outcome_count}")
print(f"   • Interventions: {objective.intervention_count}")
print(f"   • Outputs: {objective.output_count}")
print(f"   • PIAP Actions: {objective.piap_action_count}")
print(f"   • Indicators: {objective.indicator_count}")

# Test action methods
print(f"\\n🔧 TESTING ACTION METHODS:")

# Test outcomes action
try:
    outcomes_action = objective.action_view_outcomes()
    print(f"✅ action_view_outcomes: {outcomes_action['name']}")
    print(f"   Domain: {outcomes_action['domain']}")
except Exception as e:
    print(f"❌ action_view_outcomes failed: {e}")

# Test interventions action
try:
    interventions_action = objective.action_view_interventions()
    print(f"✅ action_view_interventions: {interventions_action['name']}")
    print(f"   Domain: {interventions_action['domain']}")
except Exception as e:
    print(f"❌ action_view_interventions failed: {e}")

# Test outputs action
try:
    outputs_action = objective.action_view_outputs()
    print(f"✅ action_view_outputs: {outputs_action['name']}")
    print(f"   Domain: {outputs_action['domain']}")
except Exception as e:
    print(f"❌ action_view_outputs failed: {e}")

# Test PIAP actions action
try:
    piap_actions_action = objective.action_view_piap_actions()
    print(f"✅ action_view_piap_actions: {piap_actions_action['name']}")
    print(f"   Domain: {piap_actions_action['domain']}")
except Exception as e:
    print(f"❌ action_view_piap_actions failed: {e}")

# Test indicators action
try:
    indicators_action = objective.action_view_indicators()
    print(f"✅ action_view_indicators: {indicators_action['name']}")
    print(f"   Domain: {indicators_action['domain']}")
except Exception as e:
    print(f"❌ action_view_indicators failed: {e}")

# Verify actual counts match computed fields
print(f"\\n🔍 VERIFYING ACTUAL COUNTS:")

# Count outcomes
actual_outcomes = env['intermediate.outcome'].search_count([('objective_id', '=', objective.id)])
print(f"   • Outcomes: {objective.outcome_count} (computed) vs {actual_outcomes} (actual) {'✅' if objective.outcome_count == actual_outcomes else '❌'}")

# Count interventions
actual_interventions = env['intervention'].search_count([('outcome_id', 'in', objective.outcome_ids.ids)])
print(f"   • Interventions: {objective.intervention_count} (computed) vs {actual_interventions} (actual) {'✅' if objective.intervention_count == actual_interventions else '❌'}")

# Count outputs
actual_outputs = env['output'].search_count([('intervention_id.outcome_id', 'in', objective.outcome_ids.ids)])
print(f"   • Outputs: {objective.output_count} (computed) vs {actual_outputs} (actual) {'✅' if objective.output_count == actual_outputs else '❌'}")

# Count PIAP actions
actual_piap_actions = env['piap.action'].search_count([('outcome_id', 'in', objective.outcome_ids.ids)])
print(f"   • PIAP Actions: {objective.piap_action_count} (computed) vs {actual_piap_actions} (actual) {'✅' if objective.piap_action_count == actual_piap_actions else '❌'}")

# Count indicators
actual_indicators = env['performance.indicator'].search_count([('outcome_id', 'in', objective.outcome_ids.ids)])
print(f"   • Indicators: {objective.indicator_count} (computed) vs {actual_indicators} (actual) {'✅' if objective.indicator_count == actual_indicators else '❌'}")

print("\\n✅ SMART BUTTONS TEST COMPLETE!")
'''
    
    return script_content

def run_test():
    """Run the test using Odoo shell"""
    
    print("🔧 Starting Smart Buttons Test...")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_test_script())
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
        
        # Execute the test script
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send the test commands
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
    success = run_test()
    if success:
        print("\\n🎉 Smart buttons test completed successfully!")
    else:
        print("\\n❌ Smart buttons test failed!")
        sys.exit(1)
