#!/usr/bin/env python3
"""
Script to fix the financial analysis sample data values
"""

# Update the Q1 Budget Variance Analysis record
analysis1 = env['financial.analysis'].search([('name', '=', 'Q1 FY2025/26 Budget Variance Analysis')])
if analysis1:
    print(f"Updating {analysis1.name}...")
    analysis1.write({
        'total_budget_analyzed': 625.0,
        'variance_amount': 45.2,
        'variance_percentage': 7.23,
        'efficiency_score': 85.5,
        'risk_level': 'medium',
        'confidence_level': 92.5,
    })
    print(f"Updated values: Budget={analysis1.total_budget_analyzed}, Variance={analysis1.variance_amount}, Percentage={analysis1.variance_percentage}")
else:
    print("Q1 Budget Variance Analysis not found!")

# Update the Programme Cost Efficiency Analysis record
analysis2 = env['financial.analysis'].search([('name', '=', 'Programme Cost Efficiency Analysis - Transport')])
if analysis2:
    print(f"Updating {analysis2.name}...")
    analysis2.write({
        'total_budget_analyzed': 163.74,
        'variance_amount': -12.3,
        'variance_percentage': -7.51,
        'efficiency_score': 78.2,
        'risk_level': 'low',
        'confidence_level': 88.0,
    })
    print(f"Updated values: Budget={analysis2.total_budget_analyzed}, Variance={analysis2.variance_amount}, Percentage={analysis2.variance_percentage}")
else:
    print("Programme Cost Efficiency Analysis not found!")

# Update financial integration records
integration1 = env['financial.integration'].search([('name', '=', 'Budget-Performance Integration Analysis')])
if integration1:
    print(f"Updating {integration1.name}...")
    integration1.write({
        'total_budget_integrated': 625.0,
        'performance_score': 85.5,
        'efficiency_ratio': 1.23,
    })
    print(f"Updated integration values: Budget={integration1.total_budget_integrated}, Performance={integration1.performance_score}")
else:
    print("Budget-Performance Integration Analysis not found!")

integration2 = env['financial.integration'].search([('name', '=', 'Programme-Financial Integration Dashboard')])
if integration2:
    print(f"Updating {integration2.name}...")
    integration2.write({
        'total_budget_integrated': 450.0,
        'performance_score': 78.2,
        'efficiency_ratio': 1.15,
    })
    print(f"Updated integration values: Budget={integration2.total_budget_integrated}, Performance={integration2.performance_score}")
else:
    print("Programme-Financial Integration Dashboard not found!")

# Update financial dashboard records
dashboard1 = env['financial.dashboard'].search([('name', '=', 'Executive Financial Overview')])
if dashboard1:
    print(f"Updating {dashboard1.name}...")
    dashboard1.write({
        'total_budget': 2500.0,
        'budget_utilization': 78.5,
        'performance_score': 85.2,
        'efficiency_index': 1.23,
    })
    print(f"Updated dashboard values: Budget={dashboard1.total_budget}, Utilization={dashboard1.budget_utilization}%")
else:
    print("Executive Financial Overview not found!")

dashboard2 = env['financial.dashboard'].search([('name', '=', 'Programme Financial Performance')])
if dashboard2:
    print(f"Updating {dashboard2.name}...")
    dashboard2.write({
        'total_budget': 1850.0,
        'budget_utilization': 82.1,
        'performance_score': 88.7,
        'efficiency_index': 1.15,
    })
    print(f"Updated dashboard values: Budget={dashboard2.total_budget}, Utilization={dashboard2.budget_utilization}%")
else:
    print("Programme Financial Performance not found!")

# Commit the changes
env.cr.commit()
print("\nAll financial sample data has been updated successfully!")

# Verify the updates
print("\n=== VERIFICATION ===")
analysis1 = env['financial.analysis'].search([('name', '=', 'Q1 FY2025/26 Budget Variance Analysis')])
if analysis1:
    print(f"Q1 Analysis - Budget: {analysis1.total_budget_analyzed}, Variance: {analysis1.variance_amount}, Percentage: {analysis1.variance_percentage}%")

analysis2 = env['financial.analysis'].search([('name', '=', 'Programme Cost Efficiency Analysis - Transport')])
if analysis2:
    print(f"Transport Analysis - Budget: {analysis2.total_budget_analyzed}, Variance: {analysis2.variance_amount}, Percentage: {analysis2.variance_percentage}%")

print("Financial sample data fix completed!")
