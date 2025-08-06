#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to upload the complete transport infrastructure data
This script can be run from the Odoo shell to upload all the analyzed data
"""

def upload_transport_infrastructure_data(env):
    """Upload the complete transport infrastructure data"""
    
    print("Starting transport infrastructure data upload...")
    
    # Create the transport data import wizard
    wizard = env['transport.data.import.wizard'].create({
        'name': 'Complete Transport Infrastructure Data Upload',
        'import_type': 'full',
        'overwrite_existing': True,
        'validate_only': False,
    })
    
    print(f"Created wizard: {wizard.name}")
    
    # Execute the complete data upload
    try:
        result = wizard.action_upload_complete_data()
        print("✓ Data upload completed successfully!")
        print(f"Import log:\n{wizard.import_log}")
        
        # Get the created programme
        programme = env['kcca.programme'].search([('code', '=', 'ITIS')], limit=1)
        if programme:
            print(f"\n✓ Programme created: {programme.name}")
            print(f"  - Objectives: {len(programme.objective_ids)}")
            print(f"  - Intermediate Outcomes: {len(programme.objective_ids.mapped('outcome_ids'))}")
            print(f"  - Interventions: {len(programme.objective_ids.mapped('outcome_ids.intervention_ids'))}")
            print(f"  - Outputs: {len(programme.objective_ids.mapped('outcome_ids.intervention_ids.output_ids'))}")
            print(f"  - PIAP Actions: {len(programme.objective_ids.mapped('outcome_ids.intervention_ids.output_ids.piap_action_ids'))}")
            print(f"  - Performance Indicators: {len(programme.performance_indicator_ids)}")
            
            # Calculate total budget
            piap_actions = programme.objective_ids.mapped('outcome_ids.intervention_ids.output_ids.piap_action_ids')
            total_budget = sum(piap_actions.mapped('total_budget'))
            print(f"  - Total Budget: {total_budget:.2f} UGX Billion")
            
            # Budget breakdown by fiscal year
            budget_breakdown = {
                'FY2022/23': sum(piap_actions.mapped('budget_fy2022_23')),
                'FY2023/24': sum(piap_actions.mapped('budget_fy2023_24')),
                'FY2024/25': sum(piap_actions.mapped('budget_fy2024_25')),
                'FY2025/26': sum(piap_actions.mapped('budget_fy2025_26')),
                'FY2026/27': sum(piap_actions.mapped('budget_fy2026_27')),
            }
            
            print("\n  Budget Breakdown by Fiscal Year:")
            for fy, amount in budget_breakdown.items():
                print(f"    {fy}: {amount:.2f} UGX Billion")
        
        return True
        
    except Exception as e:
        print(f"✗ Data upload failed: {str(e)}")
        print(f"Import log:\n{wizard.import_log}")
        return False

def main():
    """Main function for standalone execution"""
    print("This script should be run from within Odoo shell")
    print("Example usage:")
    print("  python3 odoo-bin shell -d your_database --addons-path=addons")
    print("  >>> exec(open('addons/robust_pmis/data/upload_transport_data.py').read())")
    print("  >>> upload_transport_infrastructure_data(env)")

if __name__ == "__main__":
    main()
