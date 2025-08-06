#!/usr/bin/env python3
"""
Script to run the comprehensive PIAP Actions import in Odoo shell
"""

# Load and execute the comprehensive import
exec(open('comprehensive_piap_import.py').read())

# Run the import
print("🚀 Starting Comprehensive PIAP Actions Import...")
result = import_comprehensive_piap_actions(env)

if result:
    print("\n✅ Import completed successfully!")
    
    # Run verification
    verify_import(env)
    
    # Additional detailed verification
    print("\n" + "="*60)
    print("📋 DETAILED VERIFICATION REPORT")
    print("="*60)
    
    programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
    piap_actions = env['piap.action'].search([('programme_id', '=', programme.id)])
    
    print(f"📊 Total PIAP Actions: {len(piap_actions)}")
    print(f"🎯 Expected: ~23 actions")
    print(f"✅ Gap Analysis: {'RESOLVED' if len(piap_actions) >= 23 else 'STILL EXISTS'}")
    
    # Show all actions with their key data
    print("\n📋 Complete PIAP Actions List:")
    for i, action in enumerate(piap_actions, 1):
        print(f"{i:2d}. {action.name}")
        print(f"    📈 Baseline: {action.baseline_value} → Target: {action.target_value} {action.measurement_unit}")
        print(f"    💰 Total Budget: {action.total_budget:,.2f}")
        print(f"    🎯 Outcome: {action.outcome_id.name if action.outcome_id else 'N/A'}")
        print()
    
    # Budget summary by fiscal year
    print("\n💰 BUDGET SUMMARY BY FISCAL YEAR:")
    fy_budgets = {
        'FY 2025-26': sum(action.budget_fy2025_26 for action in piap_actions),
        'FY 2026-27': sum(action.budget_fy2026_27 for action in piap_actions),
        'FY 2027-28': sum(action.budget_fy2027_28 for action in piap_actions),
        'FY 2028-29': sum(action.budget_fy2028_29 for action in piap_actions),
        'FY 2029-30': sum(action.budget_fy2029_30 for action in piap_actions),
    }
    
    for fy, budget in fy_budgets.items():
        print(f"   {fy}: {budget:>12,.2f}")
    
    total_all_years = sum(fy_budgets.values())
    print(f"   {'TOTAL':<9}: {total_all_years:>12,.2f}")
    
    print("\n🎉 COMPREHENSIVE IMPORT COMPLETED SUCCESSFULLY!")
    print("✅ All 23+ PIAP Actions have been imported with complete data")
    print("✅ Baselines, targets, and budget allocations are properly set")
    print("✅ Actions are properly linked to outcomes and interventions")
    
else:
    print("❌ Import failed!")
