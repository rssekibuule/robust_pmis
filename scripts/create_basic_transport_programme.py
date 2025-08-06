#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to create the basic transport infrastructure programme
This creates only the programme and objective using existing models
"""

def create_basic_transport_programme():
    """Create the basic transport infrastructure programme"""
    
    print("=" * 80)
    print("CREATING BASIC TRANSPORT INFRASTRUCTURE PROGRAMME")
    print("=" * 80)
    print()
    
    try:
        # Check if we're in Odoo shell context
        if 'env' not in globals():
            print("Error: This script must be run from within Odoo shell")
            print("Usage:")
            print("  python3 odoo-bin shell -d your_database")
            print("  >>> exec(open('addons/robust_pmis/scripts/create_basic_transport_programme.py').read())")
            print("  >>> create_basic_transport_programme()")
            return False
        
        # Check if programme already exists
        existing_programme = env['kcca.programme'].search([('code', '=', 'ITIS')], limit=1)
        if existing_programme:
            print(f"✓ Programme already exists: {existing_programme.name}")
            programme = existing_programme
        else:
            # Create the transport infrastructure programme
            programme = env['kcca.programme'].create({
                'name': 'Integrated Transport Infrastructure and Services',
                'code': 'ITIS',
                'description': '''<p><strong>Programme Goal:</strong> To have a safe, integrated and sustainable multi-modal transport system</p>
                <p>Programme focused on developing integrated transport infrastructure and services for Kampala.</p>
                <p><strong>Implementation Structure:</strong></p>
                <ul>
                    <li>5 Implementing Directorates</li>
                    <li>5 Implementing Divisions (All KCCA Territorial Divisions)</li>
                    <li>Strategic Objective: Economic Growth (Master Table Row 1)</li>
                </ul>
                <p><strong>Total Budget:</strong> 1,487.50 UGX Billion across FY2022/23 to FY2026/27</p>''',
                'sequence': 1,
            })
            print(f"✓ Created programme: {programme.name}")
        
        # Check if objective already exists
        existing_objective = env['programme.objective'].search([
            ('programme_id', '=', programme.id),
            ('name', '=', 'To develop an inter-modal and seamless transport infrastructure and services')
        ], limit=1)
        
        if existing_objective:
            print(f"✓ Objective already exists: {existing_objective.name}")
            objective = existing_objective
        else:
            # Create the programme objective
            objective = env['programme.objective'].create({
                'name': 'To develop an inter-modal and seamless transport infrastructure and services',
                'programme_id': programme.id,
                'sequence': 1,
                'description': 'Single programme objective under which all intermediate outcomes are organized',
            })
            print(f"✓ Created objective: {objective.name}")
        
        # Create intermediate outcomes
        outcomes_data = [
            {
                'name': 'Reduced travel time',
                'description': 'Achieve reduced travel time through strategic transport infrastructure development',
                'sequence': 1,
            },
            {
                'name': 'Increased stock of transport infrastructure',
                'description': 'Increase the stock of transport infrastructure through capacity enhancement',
                'sequence': 2,
            },
            {
                'name': 'Reduced fatalities',
                'description': 'Reduce road fatalities through enhanced transport safety measures',
                'sequence': 3,
            }
        ]
        
        created_outcomes = []
        for outcome_data in outcomes_data:
            existing_outcome = env['intermediate.outcome'].search([
                ('objective_id', '=', objective.id),
                ('name', '=', outcome_data['name'])
            ], limit=1)
            
            if existing_outcome:
                print(f"✓ Outcome already exists: {existing_outcome.name}")
                created_outcomes.append(existing_outcome)
            else:
                outcome = env['intermediate.outcome'].create({
                    'name': outcome_data['name'],
                    'objective_id': objective.id,
                    'sequence': outcome_data['sequence'],
                    'description': outcome_data['description'],
                })
                print(f"✓ Created outcome: {outcome.name}")
                created_outcomes.append(outcome)
        
        # Create some basic performance indicators for the outcomes
        indicators_data = [
            {
                'name': 'Average Travel time (Min/Km) on KCCA Road',
                'outcome_name': 'Reduced travel time',
                'measurement_unit': 'Minutes per Km',
                'baseline_value': 4.2,
                'target_value': 3.0,
                'indicator_type': 'decreasing',
            },
            {
                'name': 'Proportion of Commuters using mass public transport (Rail & BRT)',
                'outcome_name': 'Reduced travel time',
                'measurement_unit': 'Percentage',
                'baseline_value': 2.0,
                'target_value': 30.0,
                'indicator_type': 'increasing',
            },
            {
                'name': 'Proportion of city road network paved',
                'outcome_name': 'Increased stock of transport infrastructure',
                'measurement_unit': 'Percentage',
                'baseline_value': 37.0,
                'target_value': 52.0,
                'indicator_type': 'increasing',
            },
            {
                'name': 'Km of City Roads Paved',
                'outcome_name': 'Increased stock of transport infrastructure',
                'measurement_unit': 'Kilometers',
                'baseline_value': 770.50,
                'target_value': 1094.00,
                'indicator_type': 'increasing',
            },
            {
                'name': 'Fatalities per 100,000 persons (Roads)',
                'outcome_name': 'Reduced fatalities',
                'measurement_unit': 'Number per 100,000',
                'baseline_value': 11.0,
                'target_value': 5.0,
                'indicator_type': 'decreasing',
            },
            {
                'name': 'Proportion of paved road network with street lights',
                'outcome_name': 'Reduced fatalities',
                'measurement_unit': 'Percentage',
                'baseline_value': 15.0,
                'target_value': 100.0,
                'indicator_type': 'increasing',
            },
        ]
        
        created_indicators = 0
        for indicator_data in indicators_data:
            # Find the outcome
            outcome = next((o for o in created_outcomes if o.name == indicator_data['outcome_name']), None)
            if outcome:
                existing_indicator = env['performance.indicator'].search([
                    ('outcome_id', '=', outcome.id),
                    ('name', '=', indicator_data['name'])
                ], limit=1)
                
                if not existing_indicator:
                    env['performance.indicator'].create({
                        'name': indicator_data['name'],
                        'outcome_id': outcome.id,
                        'measurement_unit': indicator_data['measurement_unit'],
                        'baseline_value': indicator_data['baseline_value'],
                        'target_value': indicator_data['target_value'],
                        'indicator_type': indicator_data['indicator_type'],
                        'sequence': created_indicators + 1,
                    })
                    created_indicators += 1
                    print(f"✓ Created indicator: {indicator_data['name']}")
                else:
                    print(f"✓ Indicator already exists: {indicator_data['name']}")
        
        print()
        print("✅ BASIC TRANSPORT INFRASTRUCTURE PROGRAMME CREATED SUCCESSFULLY!")
        print("=" * 80)
        print()
        print("SUMMARY:")
        print(f"   Programme: {programme.name} ({programme.code})")
        print(f"   Objective: {objective.name}")
        print(f"   Intermediate Outcomes: {len(created_outcomes)}")
        for outcome in created_outcomes:
            print(f"     - {outcome.name}")
        print(f"   Performance Indicators: {created_indicators}")
        print()
        print("You can now view this data in the system:")
        print("   1. Go to Programme Management → Programmes")
        print("   2. Click on 'Integrated Transport Infrastructure and Services'")
        print("   3. Navigate through the objectives and outcomes")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Creation failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function for standalone execution"""
    print("This script should be run from within Odoo shell")
    print()
    print("Steps to run:")
    print("1. Start Odoo shell:")
    print("   python3 odoo-bin shell -d your_database_name")
    print()
    print("2. Execute this script:")
    print("   >>> exec(open('addons/robust_pmis/scripts/create_basic_transport_programme.py').read())")
    print()
    print("3. Run the creation function:")
    print("   >>> create_basic_transport_programme()")
    print()

if __name__ == "__main__":
    main()
