#!/usr/bin/env python3
"""
Script to create sample data for Financial Strategy modules
Run this script from Odoo shell: python3 odoo-bin shell -d robust_pmis --addons-path=addons
Then execute: exec(open('scripts/create_financial_sample_data.py').read())
"""

def create_financial_sample_data():
    """Create sample data for Financial Analysis, Integration, and Dashboard modules"""
    
    print("Creating Financial Strategy sample data...")
    
    # Get existing financial strategies
    financial_strategies = env['financial.strategy'].search([])
    if not financial_strategies:
        print("No financial strategies found. Creating basic financial strategy...")
        financial_strategy = env['financial.strategy'].create({
            'name': 'KCCA Strategic Financial Plan 2025-2030',
            'description': 'Comprehensive financial strategy for KCCA operations and development programmes',
            'start_date': '2025-07-01',
            'end_date': '2030-06-30',
            'total_budget': 2500.0,  # UGX 2.5 Trillion
            'status': 'active'
        })
    else:
        financial_strategy = financial_strategies[0]
    
    print(f"Using financial strategy: {financial_strategy.name}")
    
    # 1. Create Financial Analysis records
    print("Creating Financial Analysis records...")
    
    financial_analyses = [
        {
            'name': 'Q1 FY2025/26 Budget Variance Analysis',
            'financial_strategy_id': financial_strategy.id,
            'analysis_type': 'budget_variance',
            'scope': 'strategic',
            'fiscal_year': '2025_26',
            'analysis_date': '2025-10-31',
            'total_budget_analyzed': 625.0,  # UGX 625 Billion
            'variance_amount': 45.2,
            'variance_percentage': 7.23,
            'efficiency_score': 85.5,
            'risk_level': 'medium',
            'state': 'published',
            'executive_summary': '<p>Q1 budget execution shows overall positive performance with 92.77% budget utilization. Key programmes performing well include Transport Infrastructure and Human Capital Development.</p>',
            'key_findings': '<p><strong>Key Findings:</strong><ul><li>Transport Infrastructure: 88.7% budget utilization</li><li>Natural Resources: 114.2% budget utilization (over budget)</li><li>Human Capital Development: 95.8% budget utilization</li><li>Digital Transformation: 90.8% budget utilization</li></ul></p>',
            'recommendations': '<p><strong>Recommendations:</strong><ul><li>Review Natural Resources budget allocation for Q2</li><li>Accelerate Transport Infrastructure project implementation</li><li>Maintain current pace for Human Capital programmes</li></ul></p>',
            'confidence_level': 92.5
        },
        {
            'name': 'Programme Cost Efficiency Analysis - Transport',
            'financial_strategy_id': financial_strategy.id,
            'analysis_type': 'programme_efficiency',
            'scope': 'programme',
            'fiscal_year': '2025_26',
            'analysis_date': '2025-11-15',
            'total_budget_analyzed': 163.74,
            'variance_amount': -12.3,
            'variance_percentage': -7.51,
            'efficiency_score': 78.2,
            'risk_level': 'low',
            'state': 'approved',
            'executive_summary': '<p>Transport Infrastructure programme showing good cost efficiency with room for improvement in procurement processes.</p>',
            'key_findings': '<p>Road construction costs 15% below market average. Equipment procurement showing delays affecting project timelines.</p>',
            'recommendations': '<p>Streamline procurement processes and establish framework agreements with suppliers.</p>',
            'confidence_level': 88.0
        },
        {
            'name': 'Multi-Year Trend Analysis FY2023-2025',
            'financial_strategy_id': financial_strategy.id,
            'analysis_type': 'trend_analysis',
            'scope': 'strategic',
            'fiscal_year': 'all_years',
            'analysis_date': '2025-12-01',
            'total_budget_analyzed': 1850.0,
            'variance_amount': 125.8,
            'variance_percentage': 6.8,
            'efficiency_score': 82.1,
            'risk_level': 'medium',
            'state': 'in_review',
            'executive_summary': '<p>Three-year trend analysis shows steady improvement in budget execution and programme delivery efficiency.</p>',
            'key_findings': '<p>Budget utilization improved from 78% (FY2023) to 85% (FY2025). Programme delivery efficiency increased by 12%.</p>',
            'recommendations': '<p>Continue current trajectory with focus on capacity building and system improvements.</p>',
            'confidence_level': 85.5
        },
        {
            'name': 'Financial Risk Assessment - Revenue Streams',
            'financial_strategy_id': financial_strategy.id,
            'analysis_type': 'risk_assessment',
            'scope': 'funding_source',
            'fiscal_year': '2025_26',
            'analysis_date': '2025-09-30',
            'total_budget_analyzed': 450.0,
            'variance_amount': 67.5,
            'variance_percentage': 15.0,
            'efficiency_score': 72.3,
            'risk_level': 'high',
            'state': 'published',
            'executive_summary': '<p>Revenue collection faces significant challenges with property tax and business license collection below targets.</p>',
            'key_findings': '<p>Property tax collection at 68% of target. Mobile money payments showing 15% growth. Market dues collection stable.</p>',
            'recommendations': '<p>Implement digital property tax system and enhance enforcement mechanisms.</p>',
            'confidence_level': 90.0
        }
    ]
    
    for analysis_data in financial_analyses:
        analysis = env['financial.analysis'].create(analysis_data)
        print(f"Created Financial Analysis: {analysis.name}")
    
    # 2. Create Financial Integration records
    print("Creating Financial Integration records...")

    financial_integrations = [
        {
            'name': 'Budget-Performance Integration Analysis',
            'financial_strategy_id': financial_strategy.id,
            'integration_type': 'budget_performance',
            'integration_date': '2025-07-26',
            'scope': 'full_strategy',
            'fiscal_year_focus': '2025_26',
            'total_budget_integrated': 625.0,
            'performance_score': 85.5,
            'efficiency_ratio': 1.23,
            'state': 'published',
            'executive_summary': '<p>Successfully integrated budget data with performance metrics for Q1 FY2025/26. Key findings show strong correlation between budget utilization and programme delivery.</p>',
            'key_insights': '<p><strong>Key Insights:</strong><ul><li>Transport programmes show 88% budget-performance alignment</li><li>Human Capital programmes exceed performance targets by 12%</li><li>Digital transformation showing efficiency gains</li></ul></p>',
            'recommendations': '<p>Continue current integration approach with enhanced real-time monitoring capabilities.</p>'
        },
        {
            'name': 'Programme-Financial Integration Dashboard',
            'financial_strategy_id': financial_strategy.id,
            'integration_type': 'programme_financial',
            'integration_date': '2025-07-25',
            'scope': 'selected_programmes',
            'fiscal_year_focus': '2025_26',
            'total_budget_integrated': 450.0,
            'performance_score': 78.2,
            'efficiency_ratio': 1.15,
            'state': 'published',
            'executive_summary': '<p>Integrated financial tracking for 8 priority programmes with automated variance alerts and performance correlation.</p>',
            'key_insights': '<p>Programme financial integration reveals opportunities for resource reallocation and efficiency improvements.</p>',
            'recommendations': '<p>Implement automated budget reallocation triggers based on performance thresholds.</p>'
        },
        {
            'name': 'Directorate Budget Alignment',
            'financial_strategy_id': financial_strategy.id,
            'integration_type': 'directorate_budget',
            'integration_date': '2025-07-24',
            'scope': 'selected_directorates',
            'fiscal_year_focus': '2025_26',
            'total_budget_integrated': 380.0,
            'performance_score': 82.1,
            'efficiency_ratio': 1.18,
            'state': 'completed',
            'executive_summary': '<p>Aligned directorate budgets with strategic priorities, enabling better resource allocation and accountability.</p>',
            'key_insights': '<p>Directorate budget alignment shows potential for 15% efficiency improvement through better coordination.</p>',
            'recommendations': '<p>Establish quarterly budget review meetings with performance-based adjustments.</p>'
        },
        {
            'name': 'MTEF-Strategic Integration Framework',
            'financial_strategy_id': financial_strategy.id,
            'integration_type': 'mtef_strategic',
            'integration_date': '2025-07-23',
            'scope': 'full_strategy',
            'fiscal_year_focus': 'all_years',
            'total_budget_integrated': 2500.0,
            'performance_score': 79.8,
            'efficiency_ratio': 1.12,
            'state': 'validated',
            'executive_summary': '<p>Full MTEF integration provides 5-year financial planning alignment with strategic objectives and performance targets.</p>',
            'key_insights': '<p>MTEF integration enables predictive budget planning and long-term performance forecasting.</p>',
            'recommendations': '<p>Enhance MTEF integration with quarterly rolling forecasts and scenario planning capabilities.</p>'
        }
    ]
    
    for integration_data in financial_integrations:
        integration = env['financial.integration'].create(integration_data)
        print(f"Created Financial Integration: {integration.name}")
    
    # 3. Create Financial Dashboard records
    print("Creating Financial Dashboard records...")

    financial_dashboards = [
        {
            'name': 'Executive Financial Overview',
            'financial_strategy_id': financial_strategy.id,
            'dashboard_type': 'executive',
            'dashboard_date': '2025-07-26',
            'refresh_frequency': 'daily',
            'last_refresh': '2025-07-26 06:00:00',
            'total_budget': 2500.0,
            'budget_utilization': 78.5,
            'performance_score': 85.2,
            'efficiency_index': 1.23,
            'state': 'active'
        },
        {
            'name': 'Programme Financial Performance',
            'financial_strategy_id': financial_strategy.id,
            'dashboard_type': 'programme',
            'dashboard_date': '2025-07-26',
            'refresh_frequency': 'hourly',
            'last_refresh': '2025-07-26 06:30:00',
            'total_budget': 1850.0,
            'budget_utilization': 82.1,
            'performance_score': 88.7,
            'efficiency_index': 1.15,
            'state': 'active'
        },
        {
            'name': 'Budget Execution Tracking',
            'financial_strategy_id': financial_strategy.id,
            'dashboard_type': 'budget_tracking',
            'dashboard_date': '2025-07-26',
            'refresh_frequency': 'daily',
            'last_refresh': '2025-07-26 05:30:00',
            'total_budget': 2500.0,
            'budget_utilization': 78.5,
            'performance_score': 83.4,
            'efficiency_index': 1.18,
            'state': 'active'
        },
        {
            'name': 'Performance-Financial Integration',
            'financial_strategy_id': financial_strategy.id,
            'dashboard_type': 'performance_financial',
            'dashboard_date': '2025-07-26',
            'refresh_frequency': 'real_time',
            'last_refresh': '2025-07-26 06:45:00',
            'total_budget': 2500.0,
            'budget_utilization': 78.5,
            'performance_score': 86.1,
            'efficiency_index': 1.21,
            'state': 'active'
        }
    ]
    
    for dashboard_data in financial_dashboards:
        dashboard = env['financial.dashboard'].create(dashboard_data)
        print(f"Created Financial Dashboard: {dashboard.name}")
        
        # Create some sample widgets for the first dashboard
        if dashboard.name == 'Executive Financial Overview':
            widgets = [
                {
                    'dashboard_id': dashboard.id,
                    'name': 'Total Budget Utilization',
                    'widget_type': 'metric',
                    'position_x': 0,
                    'position_y': 0,
                    'width': 4,
                    'height': 3,
                    'data_source': 'budget_breakdown',
                    'widget_data': '{"metric": "utilization_percentage", "target": 85, "format": "percentage", "current": 78.5}',
                    'title': 'Budget Utilization',
                    'description': 'Overall budget utilization percentage across all programmes',
                    'color_scheme': 'blue',
                    'is_active': True,
                    'refresh_interval': 300
                },
                {
                    'dashboard_id': dashboard.id,
                    'name': 'Revenue Achievement',
                    'widget_type': 'gauge',
                    'position_x': 4,
                    'position_y': 0,
                    'width': 4,
                    'height': 3,
                    'data_source': 'funding_sources',
                    'widget_data': '{"metric": "revenue_achievement", "target": 100, "current": 92.3, "gauge_type": "arc"}',
                    'title': 'Revenue vs Target',
                    'description': 'Revenue collection achievement against annual targets',
                    'color_scheme': 'green',
                    'is_active': True,
                    'refresh_interval': 300
                },
                {
                    'dashboard_id': dashboard.id,
                    'name': 'Programme Performance Trend',
                    'widget_type': 'chart',
                    'chart_type': 'line',
                    'position_x': 0,
                    'position_y': 3,
                    'width': 8,
                    'height': 4,
                    'data_source': 'programme_performance',
                    'widget_data': '{"period": "12_months", "show_budget_line": true, "programmes": ["transport", "human_capital", "digital"]}',
                    'title': 'Programme Performance Trend',
                    'description': 'Monthly programme performance and budget execution trends',
                    'color_scheme': 'default',
                    'is_active': True,
                    'refresh_interval': 600
                }
            ]

            for widget_data in widgets:
                widget = env['financial.dashboard.widget'].create(widget_data)
                print(f"  Created widget: {widget.name}")
    
    print("\n✅ Financial Strategy sample data created successfully!")
    print(f"Created:")
    print(f"  - {len(financial_analyses)} Financial Analysis records")
    print(f"  - {len(financial_integrations)} Financial Integration records") 
    print(f"  - {len(financial_dashboards)} Financial Dashboard records")
    print(f"  - 3 Dashboard widgets")
    print("\nYou can now access the Financial Strategy menus to see the sample data.")

# Execute the function
if __name__ == '__main__':
    create_financial_sample_data()
