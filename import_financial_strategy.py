#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# Add the Odoo directory to the Python path
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

# Configuration
DB_NAME = 'robust_pmis'
DB_USER = 'odoo'
DB_PASSWORD = 'odoo'
DB_HOST = 'localhost'
DB_PORT = 5432

def import_financial_strategy():
    """Import the Strategic Plan Budget data into Financial Strategy model"""

    # Configure Odoo
    odoo.tools.config.parse_config([
        '--database', DB_NAME,
        '--db_user', DB_USER,
        '--db_password', DB_PASSWORD,
        '--db_host', DB_HOST,
        '--db_port', str(DB_PORT),
    ])

    from odoo.modules.registry import Registry
    with Registry(DB_NAME).cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("=== IMPORTING STRATEGIC PLAN BUDGET - FINANCIAL STRATEGY ===")
        print(f"Database: {cr.dbname}")
        
        # Clear existing Financial Strategy records
        print("Clearing existing Financial Strategy records...")
        existing_strategies = env['financial.strategy'].search([])
        if existing_strategies:
            existing_strategies.unlink()
            print(f"Deleted {len(existing_strategies)} existing records")
        
        # Strategic Plan Budget Data (from the provided table)
        financial_strategy_data = {
            'name': 'KCCA Strategic Plan Budget (FY2025/26 - FY2029/30)',
            'description': '''
                <p><strong>Strategic Plan Budget Overview</strong></p>
                <p>This financial strategy outlines the comprehensive budget allocation for KCCA's strategic plan 
                covering the period from FY2025/26 to FY2029/30.</p>
                
                <p><strong>Budget Categories:</strong></p>
                <ul>
                    <li><strong>Wage:</strong> Personnel costs and salaries</li>
                    <li><strong>Non-Wage Recurrent:</strong> Operational expenses excluding personnel</li>
                    <li><strong>Total Recurrent:</strong> Combined wage and non-wage recurrent costs</li>
                    <li><strong>Total Development:</strong> Capital and development expenditure</li>
                    <li><strong>Total Budget:</strong> Overall budget combining recurrent and development</li>
                </ul>
                
                <p><strong>Currency:</strong> UGX Billions</p>
                <p><strong>Total Strategic Plan Budget:</strong> UGX 9,543.05 Billion over 5 years</p>
            ''',
            'sequence': 10,
            'active': True,
            'status': 'approved',  # FY2025/26 is marked as approved in the table
            'start_date': '2025-07-01',  # FY2025/26 start
            'end_date': '2030-06-30',    # FY2029/30 end
            
            # FY2025/26 (Approved) - Budget data from the table
            'wage_fy2025_26': 182.73,
            'non_wage_recurrent_fy2025_26': 149.14,
            'total_development_fy2025_26': 1257.80,
            
            # FY2026/27 - Budget data from the table
            'wage_fy2026_27': 193.66,
            'non_wage_recurrent_fy2026_27': 166.17,
            'total_development_fy2026_27': 1475.38,
            
            # FY2027/28 - Budget data from the table
            'wage_fy2027_28': 212.20,
            'non_wage_recurrent_fy2027_28': 195.41,
            'total_development_fy2027_28': 1493.13,
            
            # FY2028/29 - Budget data from the table
            'wage_fy2028_29': 213.58,
            'non_wage_recurrent_fy2028_29': 198.80,
            'total_development_fy2028_29': 1511.06,
            
            # FY2029/30 - Budget data from the table
            'wage_fy2029_30': 223.78,
            'non_wage_recurrent_fy2029_30': 204.83,
            'total_development_fy2029_30': 1865.39,
        }
        
        # Create the Financial Strategy record
        print("Creating Strategic Plan Budget Financial Strategy...")
        
        try:
            financial_strategy = env['financial.strategy'].create(financial_strategy_data)
            
            print(f"✅ Successfully created Financial Strategy: {financial_strategy.name}")
            print(f"   ID: {financial_strategy.id}")
            print(f"   Status: {financial_strategy.status}")
            print(f"   Period: {financial_strategy.start_date} to {financial_strategy.end_date}")
            print()
            
            # Display the computed totals to verify calculations
            print("=== BUDGET VERIFICATION ===")
            print("Multi-Year Budget Breakdown (UGX Billions):")
            print()
            
            print("FY2025/26 (Approved):")
            print(f"  Wage: {financial_strategy.wage_fy2025_26:,.2f}")
            print(f"  Non-Wage Recurrent: {financial_strategy.non_wage_recurrent_fy2025_26:,.2f}")
            print(f"  Total Recurrent: {financial_strategy.total_recurrent_fy2025_26:,.2f}")
            print(f"  Total Development: {financial_strategy.total_development_fy2025_26:,.2f}")
            print(f"  Total Budget: {financial_strategy.total_budget_fy2025_26:,.2f}")
            print()
            
            print("FY2026/27:")
            print(f"  Wage: {financial_strategy.wage_fy2026_27:,.2f}")
            print(f"  Non-Wage Recurrent: {financial_strategy.non_wage_recurrent_fy2026_27:,.2f}")
            print(f"  Total Recurrent: {financial_strategy.total_recurrent_fy2026_27:,.2f}")
            print(f"  Total Development: {financial_strategy.total_development_fy2026_27:,.2f}")
            print(f"  Total Budget: {financial_strategy.total_budget_fy2026_27:,.2f}")
            print()
            
            print("FY2027/28:")
            print(f"  Wage: {financial_strategy.wage_fy2027_28:,.2f}")
            print(f"  Non-Wage Recurrent: {financial_strategy.non_wage_recurrent_fy2027_28:,.2f}")
            print(f"  Total Recurrent: {financial_strategy.total_recurrent_fy2027_28:,.2f}")
            print(f"  Total Development: {financial_strategy.total_development_fy2027_28:,.2f}")
            print(f"  Total Budget: {financial_strategy.total_budget_fy2027_28:,.2f}")
            print()
            
            print("FY2028/29:")
            print(f"  Wage: {financial_strategy.wage_fy2028_29:,.2f}")
            print(f"  Non-Wage Recurrent: {financial_strategy.non_wage_recurrent_fy2028_29:,.2f}")
            print(f"  Total Recurrent: {financial_strategy.total_recurrent_fy2028_29:,.2f}")
            print(f"  Total Development: {financial_strategy.total_development_fy2028_29:,.2f}")
            print(f"  Total Budget: {financial_strategy.total_budget_fy2028_29:,.2f}")
            print()
            
            print("FY2029/30:")
            print(f"  Wage: {financial_strategy.wage_fy2029_30:,.2f}")
            print(f"  Non-Wage Recurrent: {financial_strategy.non_wage_recurrent_fy2029_30:,.2f}")
            print(f"  Total Recurrent: {financial_strategy.total_recurrent_fy2029_30:,.2f}")
            print(f"  Total Development: {financial_strategy.total_development_fy2029_30:,.2f}")
            print(f"  Total Budget: {financial_strategy.total_budget_fy2029_30:,.2f}")
            print()
            
            print("=== GRAND TOTALS (All Years) ===")
            print(f"Total Wage: {financial_strategy.total_wage_all_years:,.2f}")
            print(f"Total Non-Wage Recurrent: {financial_strategy.total_non_wage_recurrent_all_years:,.2f}")
            print(f"Total Recurrent: {financial_strategy.total_recurrent_all_years:,.2f}")
            print(f"Total Development: {financial_strategy.total_development_all_years:,.2f}")
            print(f"TOTAL BUDGET: {financial_strategy.total_budget_all_years:,.2f}")
            print()
            
            # Verify against the provided table totals
            expected_totals = {
                'wage': 1025.94,
                'non_wage_recurrent': 914.35,
                'total_recurrent': 1940.29,
                'total_development': 7602.76,
                'total_budget': 9543.05
            }
            
            print("=== VERIFICATION AGAINST PROVIDED TABLE ===")
            print("Expected vs Computed:")
            print(f"Wage: Expected {expected_totals['wage']:,.2f}, Computed {financial_strategy.total_wage_all_years:,.2f}")
            print(f"Non-Wage Recurrent: Expected {expected_totals['non_wage_recurrent']:,.2f}, Computed {financial_strategy.total_non_wage_recurrent_all_years:,.2f}")
            print(f"Total Recurrent: Expected {expected_totals['total_recurrent']:,.2f}, Computed {financial_strategy.total_recurrent_all_years:,.2f}")
            print(f"Total Development: Expected {expected_totals['total_development']:,.2f}, Computed {financial_strategy.total_development_all_years:,.2f}")
            print(f"Total Budget: Expected {expected_totals['total_budget']:,.2f}, Computed {financial_strategy.total_budget_all_years:,.2f}")
            
            # Check if totals match
            tolerance = 0.01  # Allow small rounding differences
            all_match = True
            
            if abs(financial_strategy.total_wage_all_years - expected_totals['wage']) > tolerance:
                print("❌ Wage total mismatch!")
                all_match = False
            if abs(financial_strategy.total_non_wage_recurrent_all_years - expected_totals['non_wage_recurrent']) > tolerance:
                print("❌ Non-Wage Recurrent total mismatch!")
                all_match = False
            if abs(financial_strategy.total_recurrent_all_years - expected_totals['total_recurrent']) > tolerance:
                print("❌ Total Recurrent mismatch!")
                all_match = False
            if abs(financial_strategy.total_development_all_years - expected_totals['total_development']) > tolerance:
                print("❌ Total Development mismatch!")
                all_match = False
            if abs(financial_strategy.total_budget_all_years - expected_totals['total_budget']) > tolerance:
                print("❌ Total Budget mismatch!")
                all_match = False
            
            if all_match:
                print("✅ All totals match the provided table!")
            
            # Commit the transaction
            cr.commit()
            print("\n✅ Financial Strategy import completed successfully!")
            
        except Exception as e:
            print(f"❌ Error creating Financial Strategy: {e}")
            import traceback
            traceback.print_exc()
            cr.rollback()
            return False
    
    return True

if __name__ == '__main__':
    success = import_financial_strategy()
    if success:
        print("\n🎉 Strategic Plan Budget import completed successfully!")
    else:
        print("\n❌ Strategic Plan Budget import failed!")
        sys.exit(1)
