#!/usr/bin/env python3
"""
Complete All 23+ PIAP Actions Import Script
This script adds all remaining PIAP Actions to reach the target of 23+ actions
"""

import subprocess
import sys
import os
import tempfile

def create_complete_all_actions_script():
    """Create the script to import all remaining PIAP Actions"""
    
    script_content = '''
print("🚀 Starting Complete Import of All Remaining PIAP Actions...")
print("🎯 Target: 23+ PIAP Actions total")

# Get the transport programme
programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
if not programme:
    print("❌ Transport Programme not found!")
    exit()

print(f"✅ Found programme: {programme.name}")

# Get existing hierarchy
objectives = env['programme.objective'].search([('programme_id', '=', programme.id)])
if not objectives:
    print("❌ No objectives found!")
    exit()

objective = objectives[0]
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

interventions = env['intervention'].search([('outcome_id', 'in', [o.id for o in outcomes])])
intervention_map = {}
for intervention in interventions:
    if intervention.outcome_id.id == outcome_map['reduced_travel_time'].id:
        intervention_map['reduced_travel_time'] = intervention
    elif intervention.outcome_id.id == outcome_map['increased_infrastructure'].id:
        intervention_map['increased_infrastructure'] = intervention
    elif intervention.outcome_id.id == outcome_map['enhanced_safety'].id:
        intervention_map['enhanced_safety'] = intervention

outputs = env['output'].search([('intervention_id', 'in', [i.id for i in interventions])])
output_map = {}
for output in outputs:
    if output.intervention_id.id == intervention_map['reduced_travel_time'].id:
        output_map['reduced_travel_time'] = output
    elif output.intervention_id.id == intervention_map['increased_infrastructure'].id:
        output_map['increased_infrastructure'] = output
    elif output.intervention_id.id == intervention_map['enhanced_safety'].id:
        output_map['enhanced_safety'] = output

print(f"✅ Found complete hierarchy: {len(outcome_map)} outcomes, {len(intervention_map)} interventions, {len(output_map)} outputs")

# Check current PIAP Actions
existing_piap = env['piap.action'].search([('programme_id', '=', programme.id)])
print(f"📊 Current PIAP Actions: {len(existing_piap)}")

# Show current actions by outcome
for outcome_key, outcome in outcome_map.items():
    count = env['piap.action'].search_count([
        ('programme_id', '=', programme.id),
        ('outcome_id', '=', outcome.id)
    ])
    print(f"   • {outcome.name}: {count} actions")

print(f"\\n🎯 Target: 23+ PIAP Actions")
print(f"📈 Current: {len(existing_piap)} PIAP Actions")
print(f"🔄 Need to add: {23 - len(existing_piap)} more actions")

# All remaining PIAP Actions from master table
remaining_actions = [
    # Additional actions for Outcome 1.1: Reduced travel time (Major Projects)
    {
        'name': 'Complete detailed design & Construct BRT Pilot Corridor (Busega-Jinja Road)',
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 0.0,
        'target_value': 1.0,
        'measurement_unit': 'Project',
        'budget_fy2025_26': 0.0,
        'budget_fy2026_27': 0.0,
        'budget_fy2027_28': 225.0,
        'budget_fy2028_29': 225.0,
        'budget_fy2029_30': 225.0,
        'total_budget': 675.0
    },
    {
        'name': 'Complete detailed design & Construct BRT Pilot Corridor (Clock Tower to Major Transport Infrastructure)',
        'outcome_key': 'reduced_travel_time',
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
        'outcome_key': 'reduced_travel_time',
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
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 0.0,
        'target_value': 1.0,
        'measurement_unit': 'Project',
        'budget_fy2025_26': 0.0,
        'budget_fy2026_27': 3.00,
        'budget_fy2027_28': 11.25,
        'budget_fy2028_29': 14.06,
        'budget_fy2029_30': 14.06,
        'total_budget': 42.37
    },
    {
        'name': 'Undertake feasibility studies, detailed designs and implement Kampala Light rail system',
        'outcome_key': 'reduced_travel_time',
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
    
    # Outcome 1.2: Increased capacity of existing transport infrastructure
    {
        'name': 'Proportion of city road network paved',
        'outcome_key': 'increased_infrastructure',
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
        'outcome_key': 'increased_infrastructure',
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
    {
        'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KIIDP',
        'outcome_key': 'increased_infrastructure',
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
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 0.00,
        'target_value': 43.85,
        'measurement_unit': 'Km',
        'budget_fy2025_26': 1.62,
        'budget_fy2026_27': 0.00,
        'budget_fy2027_28': 18.54,
        'budget_fy2028_29': 3.40,
        'budget_fy2029_30': 0.00,
        'total_budget': 23.56
    },
    {
        'name': 'Km of KCCA roads & junctions upgraded/reconstructed under OMAAGP',
        'outcome_key': 'increased_infrastructure',
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
        'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KCBSLIP (Colas Project)',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 0.00,
        'target_value': 127.00,
        'measurement_unit': 'Km',
        'budget_fy2025_26': 0.00,
        'budget_fy2026_27': 61.69,
        'budget_fy2027_28': 24.00,
        'budget_fy2028_29': 24.00,
        'budget_fy2029_30': 18.00,
        'total_budget': 127.69
    },
    {
        'name': 'Km of City junctions upgraded under - SCA Project phase 2',
        'outcome_key': 'increased_infrastructure',
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
    {
        'name': 'Implement the Kampala City Road Rehabilitation Project financed by the AfDB (about 8.77 km)',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 0.00,
        'target_value': 8.77,
        'measurement_unit': 'Km',
        'budget_fy2025_26': 131.40,
        'budget_fy2026_27': 85.50,
        'budget_fy2027_28': 0.00,
        'budget_fy2028_29': 0.00,
        'budget_fy2029_30': 0.00,
        'total_budget': 216.90
    },
    {
        'name': 'Implement road improvement projects under the GoUoL/UDP financed by the World Bank and Danida & Junctions',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 0.00,
        'target_value': 1.0,
        'measurement_unit': 'Project',
        'budget_fy2025_26': 113.86,
        'budget_fy2026_27': 96.41,
        'budget_fy2027_28': 17.66,
        'budget_fy2028_29': 0.00,
        'budget_fy2029_30': 0.00,
        'total_budget': 227.93
    },
    
    # Outcome 1.3: Enhanced transport safety
    {
        'name': 'Fatalities per 100,000 persons (Roads)',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 11.00,
        'target_value': 2.0,
        'measurement_unit': 'Number',
        'budget_fy2025_26': 10.20,
        'budget_fy2026_27': 8.00,
        'budget_fy2027_28': 8.00,
        'budget_fy2028_29': 6.00,
        'budget_fy2029_30': 4.00,
        'total_budget': 36.20
    },
    {
        'name': 'Proportion of paved road network with street lights',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 15.0,
        'target_value': 100.0,
        'measurement_unit': 'Percentage',
        'budget_fy2025_26': 15.0,
        'budget_fy2026_27': 30.0,
        'budget_fy2027_28': 50.0,
        'budget_fy2028_29': 75.0,
        'budget_fy2029_30': 100.0,
        'total_budget': 270.0
    },
    {
        'name': 'Number of Fatalities on City Road',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 411.0,
        'target_value': 275.0,
        'measurement_unit': 'Number',
        'budget_fy2025_26': 392.0,
        'budget_fy2026_27': 356.0,
        'budget_fy2027_28': 331.0,
        'budget_fy2028_29': 305.0,
        'budget_fy2029_30': 275.0,
        'total_budget': 1659.0
    },
    {
        'name': 'Number of road safety Audits inspections conducted',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 1.00,
        'target_value': 30.0,
        'measurement_unit': 'Number',
        'budget_fy2025_26': 4.0,
        'budget_fy2026_27': 1.0,
        'budget_fy2027_28': 6.0,
        'budget_fy2028_29': 7.0,
        'budget_fy2029_30': 8.0,
        'total_budget': 26.0
    },
    {
        'name': 'Number of Street Lights Installed (Under AfDB Funding)',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 7568.0,
        'target_value': 15000.0,
        'measurement_unit': 'Number',
        'budget_fy2025_26': 0.30,
        'budget_fy2026_27': 5000.0,
        'budget_fy2027_28': 5000.0,
        'budget_fy2028_29': 2500.0,
        'budget_fy2029_30': 2500.0,
        'total_budget': 15000.30
    },
    {
        'name': 'Number of Street Lights Installed (Under PPP Arrangement)',
        'outcome_key': 'enhanced_safety',
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

print(f"\\n📋 Prepared {len(remaining_actions)} additional PIAP Actions for import...")
print(f"🎯 This will bring total to: {len(existing_piap) + len(remaining_actions)} PIAP Actions")

# Create additional PIAP Actions
created_count = 0
skipped_count = 0

for action_data in remaining_actions:
    try:
        outcome_key = action_data['outcome_key']
        if outcome_key not in outcome_map:
            print(f"⚠️ Outcome {outcome_key} not found, skipping {action_data['name']}")
            skipped_count += 1
            continue
        
        # Check if action already exists
        existing = env['piap.action'].search([
            ('programme_id', '=', programme.id),
            ('name', '=', action_data['name'])
        ])
        
        if existing:
            print(f"⚠️ PIAP Action already exists: {action_data['name']}")
            skipped_count += 1
            continue
        
        outcome = outcome_map[outcome_key]
        intervention = intervention_map[outcome_key]
        output = output_map[outcome_key]
        
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
        skipped_count += 1

# Commit the transaction
env.cr.commit()
print("💾 Transaction committed to database")

# Final verification
total_piap = env['piap.action'].search_count([('programme_id', '=', programme.id)])
print(f"\\n🎉 COMPLETE IMPORT FINISHED!")
print(f"📊 Created {created_count} new PIAP Actions")
print(f"⚠️ Skipped {skipped_count} actions (duplicates or errors)")
print(f"🔍 Total PIAP Actions in database: {total_piap}")

# Final summary by outcome
print(f"\\n📋 FINAL SUMMARY BY OUTCOME:")
total_budget_all = 0.0
for outcome_key, outcome in outcome_map.items():
    actions = env['piap.action'].search([
        ('programme_id', '=', programme.id),
        ('outcome_id', '=', outcome.id)
    ])
    count = len(actions)
    total_budget = sum(action.total_budget for action in actions)
    total_budget_all += total_budget
    print(f"   • {outcome.name}: {count} actions (Budget: {total_budget:,.2f} UGX Billion)")

print(f"\\n💰 TOTAL BUDGET ACROSS ALL PIAP ACTIONS: {total_budget_all:,.2f} UGX Billion")

print(f"\\n✅ MISSION ACCOMPLISHED!")
print(f"🎯 Target: 23+ PIAP Actions")
print(f"📊 Achieved: {total_piap} PIAP Actions")
print(f"✅ Status: {'TARGET EXCEEDED!' if total_piap >= 23 else 'TARGET NOT MET'}")
print(f"🔄 Gap Analysis: {'COMPLETELY RESOLVED!' if total_piap >= 23 else 'STILL EXISTS'}")

if total_piap >= 23:
    print(f"\\n🏆 CONGRATULATIONS!")
    print(f"🎉 Successfully imported {total_piap} PIAP Actions")
    print(f"📈 Exceeded the target of 23+ actions")
    print(f"💪 The gap has been completely resolved!")
else:
    print(f"\\n📊 Progress Report:")
    print(f"🔄 Still need {23 - total_piap} more actions to reach target")

exit()
'''
    
    return script_content

def run_complete_all_actions():
    """Run the complete all actions import using Odoo shell"""
    
    print("🚀 Starting Complete Import of All Remaining PIAP Actions...")
    print("🎯 Target: 23+ PIAP Actions total")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_complete_all_actions_script())
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
        
        # Execute the complete all actions import script
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
    success = run_complete_all_actions()
    if success:
        print("\\n🎉 Complete import of all remaining PIAP Actions completed successfully!")
        print("🏆 Target of 23+ PIAP Actions should now be achieved!")
        print("✅ Gap analysis completely resolved!")
    else:
        print("\\n❌ Import failed!")
        sys.exit(1)
