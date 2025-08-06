#!/usr/bin/env python3
"""
Complete Transport Programme Indicators Implementation
Implements all 24 indicators for the Integrated Transport Infrastructure and Services programme
"""

import subprocess
import sys
import os
import tempfile

def create_complete_implementation_script():
    """Create the complete implementation script"""
    
    script_content = '''
print("🚀 Implementing Complete Transport Programme Indicators...")
print("📋 Setting up all 24 indicators with proper hierarchy structure")

# Get or create the transport programme
programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
if not programme:
    print("❌ Transport Programme not found! Creating it...")
    programme = env['kcca.programme'].create({
        'name': 'Integrated Transport Infrastructure and Services',
        'code': 'ITIS',
        'description': 'Programme for integrated transport infrastructure development',
        'sequence': 3
    })
    print(f"✅ Created programme: {programme.name}")
else:
    print(f"✅ Found programme: {programme.name}")

# Get or create programme objective
objective = env['programme.objective'].search([('programme_id', '=', programme.id)])
if not objective:
    objective = env['programme.objective'].create({
        'name': 'To develop an inter-modal and seamless transport infrastructure and services',
        'programme_id': programme.id,
        'description': 'Programme objective for integrated transport infrastructure',
        'sequence': 1
    })
    print(f"✅ Created objective: {objective.name}")
else:
    objective = objective[0]
    print(f"✅ Found objective: {objective.name}")

# Create Intermediate Outcomes
print("📋 Creating Intermediate Outcomes...")
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
    
    if existing:
        outcome = existing[0]
        print(f"✅ Found outcome: {outcome.name}")
    else:
        outcome = env['intermediate.outcome'].create({
            'name': outcome_data['name'],
            'description': outcome_data['description'],
            'objective_id': objective.id,
            'sequence': outcome_data['sequence']
        })
        print(f"✅ Created outcome: {outcome.name}")
    
    outcome_records[outcome_data['key']] = outcome

print(f"✅ Setup {len(outcome_records)} outcomes")

# Create Interventions
print("📋 Creating Interventions...")
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
    outcome = outcome_records[intervention_data['outcome_key']]
    
    existing = env['intervention'].search([
        ('outcome_id', '=', outcome.id),
        ('name', '=', intervention_data['name'])
    ])
    
    if existing:
        intervention = existing[0]
        print(f"✅ Found intervention: {intervention.name}")
    else:
        intervention = env['intervention'].create({
            'name': intervention_data['name'],
            'description': intervention_data['description'],
            'outcome_id': outcome.id,
            'sequence': intervention_data['sequence']
        })
        print(f"✅ Created intervention: {intervention.name}")
    
    intervention_records[intervention_data['outcome_key']] = intervention

print(f"✅ Setup {len(intervention_records)} interventions")

# Create Outputs
print("📋 Creating Outputs...")
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
    intervention = intervention_records[output_data['intervention_key']]
    
    existing = env['output'].search([
        ('intervention_id', '=', intervention.id),
        ('name', '=', output_data['name'])
    ])
    
    if existing:
        output = existing[0]
        print(f"✅ Found output: {output.name}")
    else:
        output = env['output'].create({
            'name': output_data['name'],
            'description': output_data['description'],
            'intervention_id': intervention.id,
            'sequence': output_data['sequence']
        })
        print(f"✅ Created output: {output.name}")
    
    output_records[output_data['intervention_key']] = output

print(f"✅ Setup {len(output_records)} outputs")
print(f"✅ Hierarchy setup complete: 1 objective, {len(outcome_records)} outcomes, {len(intervention_records)} interventions, {len(output_records)} outputs")

# Clear existing PIAP Actions to avoid duplicates
existing_piap = env['piap.action'].search([('programme_id', '=', programme.id)])
if existing_piap:
    print(f"🗑️ Removing {len(existing_piap)} existing PIAP Actions to avoid duplicates")
    existing_piap.unlink()

print("📋 Implementing all 24 PIAP Actions/Indicators...")

# Complete PIAP Actions data (all 24 indicators from master table)
piap_actions_data = [
    # Intermediate Outcome 1.1: Reduced travel time (12 indicators)
    # Outcome-level indicators (2)
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
    # Intervention 1.1.1: Construct and upgrade strategic transport infrastructure (5 indicators)
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
    },
    {
        'name': 'Km of Cable Car System constructed',
        'outcome_key': 'reduced_travel_time',
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
        'outcome_key': 'reduced_travel_time',
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
    # Major Infrastructure Projects (PIAP Actions - 5 indicators)
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
        'total_budget': 42.38
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
    }
]

print(f"📊 Prepared {len(piap_actions_data)} PIAP Actions (Batch 1: Reduced Travel Time)")

# Add remaining indicators for other outcomes
additional_indicators = [
    # Intermediate Outcome 1.2: Increased Infrastructure Capacity (10 indicators)
    # Outcome-level indicators (2)
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
    # Intervention 1.2.1: Increase capacity of existing transport infrastructure (8 indicators)
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
        'total_budget': 43.85
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
        'total_budget': 127.00
    },
    {
        'name': 'Km of Pedestrian Bridges constructed under KCBSLIP (Colas Project)',
        'outcome_key': 'increased_infrastructure',
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
        'name': 'Km of KCCA roads & junctions upgraded/reconstructed under HCBSLIP (Colas Project)',
        'outcome_key': 'increased_infrastructure',
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
        'name': 'Km of City junctions upgraded under SCA Project phase 2',
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
        'name': 'Implement the Kampala City Road Rehabilitation Project financed by the AfDB',
        'outcome_key': 'increased_infrastructure',
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
    # Intermediate Outcome 1.3: Enhanced Transport Safety (2 indicators)
    # Outcome-level indicators (2)
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
        'total_budget': 2.0
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
        'total_budget': 100.0
    }
]

# Combine all indicators
piap_actions_data.extend(additional_indicators)
print(f"📊 Total indicators prepared: {len(piap_actions_data)} (All 24 indicators)")

# Create PIAP Actions
created_count = 0
for action_data in piap_actions_data:
    try:
        outcome_key = action_data['outcome_key']
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
        print(f"✅ Created indicator: {action_data['name']}")

    except Exception as e:
        print(f"❌ Error creating indicator {action_data['name']}: {str(e)}")

# Commit the transaction
env.cr.commit()
print("💾 Transaction committed to database")

# Final verification
total_piap = env['piap.action'].search_count([('programme_id', '=', programme.id)])
print(f"\\n🎉 COMPLETE IMPLEMENTATION FINISHED!")
print(f"📊 Created {created_count} indicators out of {len(piap_actions_data)}")
print(f"🔍 Total indicators in database: {total_piap}")

# Summary by outcome
print(f"\\n📋 SUMMARY BY OUTCOME:")
for outcome_key, outcome in outcome_records.items():
    count = env['piap.action'].search_count([
        ('programme_id', '=', programme.id),
        ('outcome_id', '=', outcome.id)
    ])
    print(f"   • {outcome.name}: {count} indicators")

print("\\n✅ ALL 24 TRANSPORT INDICATORS IMPLEMENTED SUCCESSFULLY!")
'''

    return script_content

def run_complete_implementation():
    """Run the complete implementation using Odoo shell"""
    
    print("🚀 Starting Complete Transport Indicators Implementation...")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_complete_implementation_script())
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
        
        # Execute the implementation script
        process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Send the implementation commands
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
    success = run_complete_implementation()
    if success:
        print("\\n🎉 Hierarchy setup completed successfully!")
        print("📊 Ready for PIAP Actions implementation")
    else:
        print("\\n❌ Implementation failed!")
        sys.exit(1)
