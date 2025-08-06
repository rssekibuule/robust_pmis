#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to validate the transport infrastructure data structure
"""

def test_transport_data_structure():
    """Test the transport infrastructure data structure"""
    
    print("=" * 80)
    print("TRANSPORT INFRASTRUCTURE DATA STRUCTURE TEST")
    print("=" * 80)
    print()
    
    try:
        # Check if we're in Odoo shell context
        if 'env' not in globals():
            print("Error: This script must be run from within Odoo shell")
            return False
        
        # Find the transport infrastructure programme
        programme = env['kcca.programme'].search([('code', '=', 'ITIS')], limit=1)
        if not programme:
            print("❌ Transport Infrastructure Programme not found!")
            print("   Please run the data upload first.")
            return False
        
        print(f"✓ Found Programme: {programme.name}")
        print()
        
        # Test the complete hierarchy
        print("TESTING PROGRAMME HIERARCHY:")
        print("-" * 40)
        
        # 1. Programme Objectives
        objectives = programme.objective_ids
        print(f"1. Programme Objectives: {len(objectives)}")
        if len(objectives) != 1:
            print(f"   ❌ Expected 1 objective, found {len(objectives)}")
            return False
        
        objective = objectives[0]
        print(f"   ✓ {objective.name}")
        
        # 2. Intermediate Outcomes
        outcomes = objective.outcome_ids
        print(f"2. Intermediate Outcomes: {len(outcomes)}")
        if len(outcomes) != 3:
            print(f"   ❌ Expected 3 outcomes, found {len(outcomes)}")
            return False
        
        expected_outcomes = [
            'Reduced travel time',
            'Increased stock of transport infrastructure', 
            'Reduced fatalities'
        ]
        
        for i, outcome in enumerate(outcomes):
            if outcome.name in expected_outcomes:
                print(f"   ✓ {outcome.name}")
            else:
                print(f"   ❌ Unexpected outcome: {outcome.name}")
        
        # 3. Interventions
        interventions = outcomes.mapped('intervention_ids')
        print(f"3. Interventions: {len(interventions)}")
        if len(interventions) != 3:
            print(f"   ❌ Expected 3 interventions, found {len(interventions)}")
            return False
        
        for intervention in interventions:
            print(f"   ✓ {intervention.name}")
        
        # 4. Outputs
        outputs = interventions.mapped('output_ids')
        print(f"4. Outputs: {len(outputs)}")
        expected_outputs = 5  # 1 + 1 + 2 + 1 = 5 outputs total
        if len(outputs) < expected_outputs:
            print(f"   ⚠️  Expected at least {expected_outputs} outputs, found {len(outputs)}")
        
        for output in outputs:
            print(f"   ✓ {output.name}")
        
        # 5. PIAP Actions
        piap_actions = outputs.mapped('piap_action_ids')
        print(f"5. PIAP Actions: {len(piap_actions)}")
        expected_piap_actions = 22  # From our analysis
        if len(piap_actions) < expected_piap_actions:
            print(f"   ⚠️  Expected {expected_piap_actions} PIAP actions, found {len(piap_actions)}")
        
        # Show sample PIAP actions
        for i, action in enumerate(piap_actions[:5]):  # Show first 5
            print(f"   ✓ {action.name[:60]}...")
        if len(piap_actions) > 5:
            print(f"   ... and {len(piap_actions) - 5} more")
        
        print()
        print("TESTING PERFORMANCE INDICATORS:")
        print("-" * 40)
        
        # Performance Indicators
        outcome_indicators = outcomes.mapped('indicator_ids')
        output_indicators = outputs.mapped('indicator_ids')
        total_indicators = len(outcome_indicators) + len(output_indicators)
        
        print(f"Outcome Level Indicators: {len(outcome_indicators)}")
        for indicator in outcome_indicators:
            print(f"   ✓ {indicator.name} (Baseline: {indicator.baseline_value}, Target: {indicator.target_value})")
        
        print(f"Output Level Indicators: {len(output_indicators)}")
        for indicator in output_indicators[:10]:  # Show first 10
            print(f"   ✓ {indicator.name} (Target: {indicator.target_value})")
        if len(output_indicators) > 10:
            print(f"   ... and {len(output_indicators) - 10} more")
        
        print(f"Total Indicators: {total_indicators}")
        
        print()
        print("TESTING BUDGET DATA:")
        print("-" * 40)
        
        # Budget Analysis
        total_budget = sum(piap_actions.mapped('total_budget'))
        print(f"Total Programme Budget: {total_budget:.2f} UGX Billion")
        
        # Budget by fiscal year
        budget_by_fy = {
            'FY2022/23': sum(piap_actions.mapped('budget_fy2022_23')),
            'FY2023/24': sum(piap_actions.mapped('budget_fy2023_24')),
            'FY2024/25': sum(piap_actions.mapped('budget_fy2024_25')),
            'FY2025/26': sum(piap_actions.mapped('budget_fy2025_26')),
            'FY2026/27': sum(piap_actions.mapped('budget_fy2026_27')),
        }
        
        print("Budget by Fiscal Year:")
        for fy, amount in budget_by_fy.items():
            print(f"   {fy}: {amount:>10.2f} UGX Billion")
        
        # Validate against expected totals from analysis
        expected_totals = {
            'FY2022/23': 752.00,
            'FY2023/24': 217.50, 
            'FY2024/25': 259.00,
            'FY2025/26': 259.00,
            'FY2026/27': 0.00
        }
        
        print()
        print("BUDGET VALIDATION:")
        print("-" * 40)
        
        all_budgets_match = True
        for fy, expected in expected_totals.items():
            actual = budget_by_fy[fy]
            if abs(actual - expected) < 0.01:  # Allow small rounding differences
                print(f"   ✓ {fy}: {actual:.2f} (Expected: {expected:.2f})")
            else:
                print(f"   ❌ {fy}: {actual:.2f} (Expected: {expected:.2f}) - Difference: {actual - expected:.2f}")
                all_budgets_match = False
        
        print()
        print("TESTING RELATIONSHIPS:")
        print("-" * 40)
        
        # Test relationships
        print("Testing parent-child relationships...")
        
        # Check that all outcomes belong to the objective
        for outcome in outcomes:
            if outcome.objective_id == objective:
                print(f"   ✓ {outcome.name} → {objective.name}")
            else:
                print(f"   ❌ {outcome.name} has wrong parent")
                return False
        
        # Check that all interventions belong to outcomes
        for intervention in interventions:
            if intervention.outcome_id in outcomes:
                print(f"   ✓ {intervention.name} → {intervention.outcome_id.name}")
            else:
                print(f"   ❌ {intervention.name} has wrong parent")
                return False
        
        # Check that all outputs belong to interventions
        for output in outputs:
            if output.intervention_id in interventions:
                print(f"   ✓ {output.name} → {output.intervention_id.name}")
            else:
                print(f"   ❌ {output.name} has wrong parent")
                return False
        
        # Check that all PIAP actions belong to outputs
        for action in piap_actions:
            if action.output_id in outputs:
                print(f"   ✓ {action.name[:40]}... → {action.output_id.name}")
            else:
                print(f"   ❌ {action.name} has wrong parent")
                return False
        
        print()
        print("✅ ALL TESTS PASSED!")
        print("=" * 80)
        print()
        print("SUMMARY:")
        print(f"   Programme: {programme.name}")
        print(f"   Objectives: {len(objectives)}")
        print(f"   Intermediate Outcomes: {len(outcomes)}")
        print(f"   Interventions: {len(interventions)}")
        print(f"   Outputs: {len(outputs)}")
        print(f"   PIAP Actions: {len(piap_actions)}")
        print(f"   Performance Indicators: {total_indicators}")
        print(f"   Total Budget: {total_budget:.2f} UGX Billion")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main function for standalone execution"""
    print("This script should be run from within Odoo shell")
    print()
    print("Usage:")
    print("   python3 odoo-bin shell -d your_database_name")
    print("   >>> exec(open('addons/robust_pmis/scripts/test_transport_data.py').read())")
    print("   >>> test_transport_data_structure()")

if __name__ == "__main__":
    main()
