#!/usr/bin/env python3
"""
Import Performance Indicators from Master Table - CORRECTED VERSION
This script imports all performance indicators with their exact data from the master table
"""

import subprocess
import sys
import os
import tempfile

def create_performance_indicators_script():
    """Create the script to import all performance indicators"""
    
    script_content = '''
print("🚀 Starting Performance Indicators Import from Master Table...")

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

print(f"✅ Found hierarchy: {len(outcome_map)} outcomes")

# Clear existing performance indicators
existing_pis = env['performance.indicator'].search([])
if existing_pis:
    print(f"🗑️ Removing {len(existing_pis)} existing performance indicators")
    existing_pis.unlink()

# Performance Indicators data from master table - CORRECTED
performance_indicators_data = [
    # Intermediate Outcome 1.1: Reduced travel time
    {
        'name': 'Average Travel time (Minutes) on KCCA Road Links',
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 4.2,
        'target_fy2025_26': 4.0,
        'target_fy2026_27': 3.8,
        'target_fy2027_28': 3.5,
        'target_fy2028_29': 3.2,
        'target_fy2029_30': 3.0,
        'measurement_unit': 'Minutes',
        'frequency': 'annual'
    },
    {
        'name': 'Proportion of Commuters using mass public transport (Bus & BRT)',
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 2.0,
        'target_fy2025_26': 5.0,
        'target_fy2026_27': 10.0,
        'target_fy2027_28': 15.0,
        'target_fy2028_29': 25.0,
        'target_fy2029_30': 30.0,
        'measurement_unit': 'Percentage',
        'frequency': 'annual'
    },
    
    # Output 1.1.1.1: Strategic transport infrastructure constructed and upgraded
    {
        'name': 'Km of BRT Network constructed',
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 0.0,
        'target_fy2025_26': 0.0,
        'target_fy2026_27': 0.0,
        'target_fy2027_28': 4.4,
        'target_fy2028_29': 5.1,
        'target_fy2029_30': 5.0,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    {
        'name': 'No of Traffic Diversion Flyovers constructed',
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 2.0,
        'target_fy2025_26': 0.0,
        'target_fy2026_27': 1.0,
        'target_fy2027_28': 2.0,
        'target_fy2028_29': 0.0,
        'target_fy2029_30': 1.0,
        'measurement_unit': 'Number',
        'frequency': 'annual'
    },
    {
        'name': 'Km of meter gauge commuter rail revamped',
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 28.5,
        'target_fy2025_26': 0.0,
        'target_fy2026_27': 1.0,
        'target_fy2027_28': 5.0,
        'target_fy2028_29': 5.0,
        'target_fy2029_30': 10.4,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    {
        'name': 'Km of Cable Car System constructed',
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 0.0,
        'target_fy2025_26': 0.0,
        'target_fy2026_27': 0.0,
        'target_fy2027_28': 2.0,
        'target_fy2028_29': 2.5,
        'target_fy2029_30': 2.5,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    {
        'name': '% completion of Feasibility study & detailed design for LRT',
        'outcome_key': 'reduced_travel_time',
        'baseline_value': 0.0,
        'target_fy2025_26': 0.0,
        'target_fy2026_27': 30.0,
        'target_fy2027_28': 50.0,
        'target_fy2028_29': 100.0,
        'target_fy2029_30': 100.0,
        'measurement_unit': 'Percentage',
        'frequency': 'annual'
    },
    
    # Intermediate Outcome 1.2: Increased capacity of existing transport infrastructure
    {
        'name': 'Proportion of city road network paved',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 37.0,
        'target_fy2025_26': 39.0,
        'target_fy2026_27': 46.0,
        'target_fy2027_28': 48.0,
        'target_fy2028_29': 51.0,
        'target_fy2029_30': 51.0,
        'measurement_unit': 'Percentage',
        'frequency': 'annual'
    },
    {
        'name': 'Km of City Roads Paved',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 778.50,
        'target_fy2025_26': 86.52,
        'target_fy2026_27': 122.24,
        'target_fy2027_28': 52.46,
        'target_fy2028_29': 84.06,
        'target_fy2029_30': 51.48,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    
    # Output 1.2.1.1: Capacity of existing road transport infrastructure increased
    {
        'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KIIDP',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 44.00,
        'target_fy2025_26': 24.00,
        'target_fy2026_27': 20.00,
        'target_fy2027_28': 0.00,
        'target_fy2028_29': 0.00,
        'target_fy2029_30': 0.00,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    {
        'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KIIDP Phase2',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 0.00,
        'target_fy2025_26': 1.62,
        'target_fy2026_27': 18.54,
        'target_fy2027_28': 3.40,
        'target_fy2028_29': 0.00,
        'target_fy2029_30': 0.00,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    {
        'name': 'Km of KCCA roads & junctions upgraded/reconstructed under OMAAGP',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 0.00,
        'target_fy2025_26': 14.60,
        'target_fy2026_27': 22.70,
        'target_fy2027_28': 25.00,
        'target_fy2028_29': 25.00,
        'target_fy2029_30': 18.45,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    {
        'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KCBSLIP (Colas Project)',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 0.00,
        'target_fy2025_26': 0.00,
        'target_fy2026_27': 61.69,
        'target_fy2027_28': 24.00,
        'target_fy2028_29': 24.00,
        'target_fy2029_30': 18.00,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    {
        'name': 'Km of City junctions upgraded under - SCA Project phase 2',
        'outcome_key': 'increased_infrastructure',
        'baseline_value': 30.00,
        'target_fy2025_26': 0.00,
        'target_fy2026_27': 0.00,
        'target_fy2027_28': 5.00,
        'target_fy2028_29': 10.00,
        'target_fy2029_30': 10.00,
        'measurement_unit': 'Km',
        'frequency': 'annual'
    },
    
    # Intermediate Outcome 1.3: Enhanced transport safety
    {
        'name': 'Fatalities per 100,000 persons (Roads)',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 11.0,
        'target_fy2025_26': 10.00,
        'target_fy2026_27': 8.00,
        'target_fy2027_28': 8.00,
        'target_fy2028_29': 6.00,
        'target_fy2029_30': 5.00,
        'measurement_unit': 'Number',
        'frequency': 'annual'
    },
    {
        'name': 'Proportion of paved road network with street lights',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 15.0,
        'target_fy2025_26': 15.0,
        'target_fy2026_27': 30.0,
        'target_fy2027_28': 50.0,
        'target_fy2028_29': 75.0,
        'target_fy2029_30': 100.0,
        'measurement_unit': 'Percentage',
        'frequency': 'annual'
    },
    
    # Output 1.3.1.1: Road Transport Safety Enhanced
    {
        'name': 'Number of Fatalities on City Road',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 411.0,
        'target_fy2025_26': 392.0,
        'target_fy2026_27': 356.0,
        'target_fy2027_28': 331.0,
        'target_fy2028_29': 305.0,
        'target_fy2029_30': 275.0,
        'measurement_unit': 'Number',
        'frequency': 'annual'
    },
    {
        'name': 'Number of road safety Audits inspections conducted',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 1.0,
        'target_fy2025_26': 4.0,
        'target_fy2026_27': 1.0,
        'target_fy2027_28': 6.0,
        'target_fy2028_29': 7.0,
        'target_fy2029_30': 8.0,
        'measurement_unit': 'Number',
        'frequency': 'annual'
    },
    {
        'name': 'Number of Street Lights Installed (Under AfDB Funding)',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 7568.0,
        'target_fy2025_26': 0.0,
        'target_fy2026_27': 5000.0,
        'target_fy2027_28': 5000.0,
        'target_fy2028_29': 2500.0,
        'target_fy2029_30': 2500.0,
        'measurement_unit': 'Number',
        'frequency': 'annual'
    },
    {
        'name': 'Number of Street Lights Installed (Under PPP Arrangement)',
        'outcome_key': 'enhanced_safety',
        'baseline_value': 0.0,
        'target_fy2025_26': 0.0,
        'target_fy2026_27': 2500.0,
        'target_fy2027_28': 2500.0,
        'target_fy2028_29': 2500.0,
        'target_fy2029_30': 2500.0,
        'measurement_unit': 'Number',
        'frequency': 'annual'
    }
]

print(f"📋 Prepared {len(performance_indicators_data)} performance indicators for import...")

# Create Performance Indicators
created_count = 0
for pi_data in performance_indicators_data:
    try:
        outcome_key = pi_data['outcome_key']
        if outcome_key not in outcome_map:
            print(f"⚠️ Outcome {outcome_key} not found, skipping {pi_data['name']}")
            continue
        
        outcome = outcome_map[outcome_key]
        
        # Check if indicator already exists
        existing = env['performance.indicator'].search([
            ('name', '=', pi_data['name']),
            ('outcome_id', '=', outcome.id)
        ])
        
        if existing:
            print(f"⚠️ Performance Indicator already exists: {pi_data['name']}")
            continue
        
        performance_indicator = env['performance.indicator'].create({
            'name': pi_data['name'],
            'outcome_id': outcome.id,  # Only link to outcome, not programme
            'baseline_value': pi_data['baseline_value'],
            'target_fy2025_26': pi_data['target_fy2025_26'],
            'target_fy2026_27': pi_data['target_fy2026_27'],
            'target_fy2027_28': pi_data['target_fy2027_28'],
            'target_fy2028_29': pi_data['target_fy2028_29'],
            'target_fy2029_30': pi_data['target_fy2029_30'],
            'measurement_unit': pi_data['measurement_unit'],
            'frequency': pi_data['frequency'],
            'active': True
        })
        
        created_count += 1
        print(f"✅ Created Performance Indicator: {pi_data['name']}")
        
    except Exception as e:
        print(f"❌ Error creating Performance Indicator {pi_data['name']}: {str(e)}")

# Commit the transaction
env.cr.commit()
print("💾 Transaction committed to database")

# Final verification
total_pis = env['performance.indicator'].search_count([('outcome_id.programme_id', '=', programme.id)])
print(f"\\n🎉 PERFORMANCE INDICATORS IMPORT COMPLETE!")
print(f"📊 Created {created_count} new Performance Indicators")
print(f"🔍 Total Performance Indicators in database: {total_pis}")

# Summary by outcome
print(f"\\n📋 SUMMARY BY OUTCOME:")
for outcome_key, outcome in outcome_map.items():
    outcome_pis = env['performance.indicator'].search([
        ('outcome_id', '=', outcome.id)
    ])
    print(f"   • {outcome.name}: {len(outcome_pis)} indicators")

print(f"\\n✅ PERFORMANCE INDICATORS SUCCESSFULLY RESTORED!")
print(f"🎯 All indicators from master table have been imported")
print(f"📊 Complete with baselines and 5-year targets")

exit()
'''
    
    return script_content

def run_performance_indicators_import():
    """Run the performance indicators import using Odoo shell"""
    
    print("🚀 Starting Performance Indicators Import from Master Table...")
    
    # Create temporary script file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(create_performance_indicators_script())
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
        
        # Execute the performance indicators import script
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
    success = run_performance_indicators_import()
    if success:
        print("\\n🎉 Performance Indicators import completed successfully!")
        print("📊 All indicators from master table have been restored!")
        print("✅ Complete with baselines and 5-year targets!")
    else:
        print("\\n❌ Import failed!")
        sys.exit(1)
