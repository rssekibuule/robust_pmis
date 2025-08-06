#!/usr/bin/env python3
"""
Script to link programmes, directorates, and indicators to financial analysis records
"""

# Get the Q1 Budget Variance Analysis record
analysis1 = env['financial.analysis'].search([('name', '=', 'Q1 FY2025/26 Budget Variance Analysis')])

if analysis1:
    print(f"Linking data to {analysis1.name}...")
    
    # Get some programmes to link
    programmes = env['kcca.programme'].search([], limit=3)
    if programmes:
        analysis1.programme_ids = [(6, 0, programmes.ids)]
        print(f"Linked {len(programmes)} programmes: {', '.join(programmes.mapped('name'))}")

    # Get some directorates to link
    directorates = env['kcca.directorate'].search([], limit=2)
    if directorates:
        analysis1.directorate_ids = [(6, 0, directorates.ids)]
        print(f"Linked {len(directorates)} directorates: {', '.join(directorates.mapped('name'))}")

    # Get some performance indicators to link
    indicators = env['performance.indicator'].search([], limit=5)
    if indicators:
        analysis1.performance_indicator_ids = [(6, 0, indicators.ids)]
        print(f"Linked {len(indicators)} performance indicators")

    # Get some KPIs to link
    kpis = env['key.performance.indicator'].search([], limit=3)
    if kpis:
        analysis1.kpi_ids = [(6, 0, kpis.ids)]
        print(f"Linked {len(kpis)} KPIs")
    
    print(f"Updated counts - Programmes: {analysis1.programme_count}, Directorates: {analysis1.directorate_count}, Indicators: {analysis1.indicator_count}")

else:
    print("Q1 Budget Variance Analysis not found!")

# Get the Transport Analysis record
analysis2 = env['financial.analysis'].search([('name', '=', 'Programme Cost Efficiency Analysis - Transport')])

if analysis2:
    print(f"\nLinking data to {analysis2.name}...")
    
    # Get transport-related programmes
    transport_programmes = env['kcca.programme'].search([('name', 'ilike', 'transport')], limit=2)
    if not transport_programmes:
        # If no transport programmes, get any programmes
        transport_programmes = env['kcca.programme'].search([], limit=2)

    if transport_programmes:
        analysis2.programme_ids = [(6, 0, transport_programmes.ids)]
        print(f"Linked {len(transport_programmes)} programmes: {', '.join(transport_programmes.mapped('name'))}")

    # Get some directorates
    directorates = env['kcca.directorate'].search([], limit=1)
    if directorates:
        analysis2.directorate_ids = [(6, 0, directorates.ids)]
        print(f"Linked {len(directorates)} directorates: {', '.join(directorates.mapped('name'))}")
    
    # Get some indicators
    indicators = env['performance.indicator'].search([], limit=3)
    if indicators:
        analysis2.performance_indicator_ids = [(6, 0, indicators.ids)]
        print(f"Linked {len(indicators)} performance indicators")
    
    print(f"Updated counts - Programmes: {analysis2.programme_count}, Directorates: {analysis2.directorate_count}, Indicators: {analysis2.indicator_count}")

else:
    print("Programme Cost Efficiency Analysis - Transport not found!")

# Commit the changes
env.cr.commit()
print("\nAll analysis data linking completed successfully!")

# Show available data counts for reference
print(f"\n=== AVAILABLE DATA ===")
print(f"Total Programmes: {env['kcca.programme'].search_count([])}")
print(f"Total Directorates: {env['kcca.directorate'].search_count([])}")
print(f"Total Performance Indicators: {env['performance.indicator'].search_count([])}")
print(f"Total KPIs: {env['key.performance.indicator'].search_count([])}")

print("Analysis data linking completed!")
