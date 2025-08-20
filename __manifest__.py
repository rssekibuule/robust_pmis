# -*- coding: utf-8 -*-
{
    'name': 'KCCA Performance Management Information System',
    'version': '18.0.1.0.8',
    'category': 'Human Resources/Performance',
    'summary': 'Comprehensive Performance Management System for KCCA',
    'description': """
KCCA Performance Management Information System
=============================================

A comprehensive performance management system for Kampala Capital City Authority (KCCA)
with the strategic goal "A well planned, inclusive and resilient capital city".

Key Features:
* Strategic Goals and Objectives Management
* Key Result Areas (KRAs) and Key Performance Indicators (KPIs)
* Programme and Project Management
* Organizational Structure (Directorates and Divisions)
* Performance Tracking and Scoring
* Action-based Performance Updates
* Comprehensive Reporting and Dashboards

Hierarchical Structure:
* Strategic Goals → Key Result Areas (KRAs) → Key Performance Indicators (KPIs)
* Strategic Goals → Strategic Objectives → Key Result Areas (KRAs) → Key Performance Indicators (KPIs)
* Programmes → Programme Objectives → Intermediate Outcomes → Performance Indicators
* Directorates → Divisions → Programmes
* Actions → Performance Indicators (for scoring and progress updates)
    """,
    'author': 'KCCA IT Department',
    'website': 'https://www.kcca.go.ug',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'hr',
        'project',
        'mail',
        'web',
        'portal',
    ],
    'data': [
        # Security
        'security/kcca_pmis_security.xml',
        # Note: ir.model.access.csv will be added after models are loaded

        # Data
        'data/strategic_goal_data.xml',
        'data/directorate_data.xml',
        'data/kcca_divisions_data.xml',
        'data/remove_territorial_directorate.xml',
        'data/programme_data.xml',
        'data/strategic_objective_master_table.xml',
        'data/kra_kpi_data.xml',
        'data/programme_directorate_relationships.xml',
        'data/division_programme_relationships.xml',
        'data/division_programme_relationships_part2.xml',
        'data/division_programme_relationships_part3.xml',
        'data/admin_user_setup.xml',
        'data/cleanup_old_actions.xml',
        'data/remove_dashboard_references.xml',
        'data/financial_strategy_data.xml',
        'data/financial_strategy_mtef_data.xml',
        'data/programme_budget_data.xml',
        'data/financial_strategy_sample_data.xml',
        'data/kpi_thematic_classification.xml',
        'data/sample_kpi_linkages.xml',
    'data/ensure_all_divisions_have_all_programmes.xml',
    'data/enforce_allowed_implementing_relations.xml',

        # Infrastructure strategic goal and objective
        'data/infrastructure_strategic_goal.xml',

        # Single, de-duplicated demo dataset for Infrastructure Development objective
        'data/infrastructure_development_complete_demo.xml',

        # Views - Strategic Management
        'views/strategic_goal_views.xml',
        'views/strategic_objective_views.xml',
        'views/key_result_area_views.xml',
        'views/key_performance_indicator_views.xml',
        'views/kra_kpi_dashboard.xml',

        # Views - Organizational Structure
        'views/kcca_directorate_views.xml',
        'views/kcca_division_views.xml',

        # Views - Programme Management
        'views/kcca_programme_views.xml',
        'views/programme_objective_views.xml',
        'views/intermediate_outcome_views.xml',
        'views/intervention_views.xml',
        'views/output_views.xml',
        'views/piap_action_views.xml',
        'views/performance_indicator_views.xml',
        'views/programme_directorate_rel_views.xml',
        'views/master_table_dashboard.xml',

        # Views - Division Performance
        'views/division_programme_rel_views.xml',
        'views/division_performance_dashboard.xml',

        # Views - Directorate Performance
        'views/directorate_performance_dashboard.xml',

        # Views - Performance Tracking
        'views/performance_action_views.xml',
        'views/performance_score_views.xml',

        # Views - Advanced Features
        'views/performance_analytics_views.xml',
        'views/performance_workflow_views.xml',
        'views/performance_alerts_views.xml',
        'views/audit_log_views.xml',
        'views/financial_strategy_views.xml',
        'views/financial_analysis_views.xml',
        'views/financial_integration_views.xml',
        'views/financial_dashboard_views.xml',
        'views/programme_budget_views.xml',
    'views/res_config_settings_views.xml',

        # Dashboard and Analytics
        'views/kpi_linkage_dashboard.xml',
        'views/strategic_programme_analytics_views.xml',

        # Unified KPI Management
        'views/unified_kpi_views.xml',

        # Wizards
        'wizards/kpi_linkage_wizard_views.xml',
        'wizards/strategic_programme_report_wizard_views.xml',

        # Wizards
        'views/wizard_views.xml',

        # Portal Templates
        'views/portal_templates.xml',

        # Email Templates and Cron Jobs
        'data/email_templates.xml',
        'data/cron_jobs.xml',
        

        # Reports
        'reports/performance_report_templates.xml',
        'reports/performance_reports.xml',

        # Unified Performance Dashboard
        'data/performance_dashboard_data.xml',
        'views/performance_dashboard_views.xml',
        # Main Menus (loaded after all views and actions are defined)
        'views/kcca_pmis_menus.xml',
        'views/programme_directorate_rel_menus.xml',
        'views/division_performance_menus.xml',
        'views/directorate_performance_menus.xml',
        # Security (loaded after models)
        'security/ir.model.access.csv',
        # Dashboard data - commented out due to method signature issues
        # 'data/performance_dashboard_data.xml',
    ],
    'demo': [
        # No demo data - using real data only
    ],
    'assets': {
        'web.assets_backend': [
            'robust_pmis/static/src/css/kcca_pmis.css',
            'robust_pmis/static/src/css/financial_strategy.css',
            'robust_pmis/static/src/css/dashboard_clean.css',
            'robust_pmis/static/src/js/form_layout_override.js',
            # Ensure Chart.js is loaded before any charts code
            'web/static/lib/Chart/Chart.js',
            # Normalize legacy tree->list in hash before the client boots
            'robust_pmis/static/src/js/legacy_view_alias.js',
            'robust_pmis/static/src/js/kcca_directorate_charts.js',
            # Updated dashboard for Odoo 18 compatibility
            'robust_pmis/static/src/js/performance_dashboard_form.js',
            'robust_pmis/static/src/xml/kcca_directorate_charts.xml',
            # KPI Linkage Dashboard client action
            'robust_pmis/static/src/js/kpi_linkage_dashboard.js',
            'robust_pmis/static/src/xml/kpi_linkage_dashboard.xml',

        ],
        'web.assets_frontend': [
            'robust_pmis/static/src/css/portal.css',
        ],
        # Ensure QWeb templates are always picked up by the client
        'web.assets_qweb': [
            'robust_pmis/static/src/xml/kpi_linkage_dashboard.xml',
        ],
    },
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'sequence': 10,
    'post_init_hook': 'post_init_hook',
}
