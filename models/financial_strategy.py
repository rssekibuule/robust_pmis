# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FinancialStrategy(models.Model):
    _name = 'financial.strategy'
    _description = 'Financial Strategy - Strategic Plan Budget'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Strategy Name',
        required=True,
        tracking=True,
        help="Name of the financial strategy"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the financial strategy"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering financial strategies"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Strategy period
    start_date = fields.Date(
        string='Start Date',
        tracking=True,
        help="Strategy start date"
    )
    
    end_date = fields.Date(
        string='End Date',
        tracking=True,
        help="Strategy end date"
    )
    
    # Currency
    currency_id = fields.Many2one(
        'res.currency',
        string='Currency',
        default=lambda self: self.env.company.currency_id,
        help="Currency for budget amounts"
    )
    
    # Budget Categories - FY2025/26 (Approved)
    wage_fy2025_26 = fields.Float(
        string='Wage FY2025/26 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Wage budget for FY2025/26 (Approved). Enter amount in billions of UGX."
    )

    non_wage_recurrent_fy2025_26 = fields.Float(
        string='Non-Wage Recurrent FY2025/26 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Non-wage recurrent budget for FY2025/26. Enter amount in billions of UGX."
    )

    total_development_fy2025_26 = fields.Float(
        string='Total Development FY2025/26 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Total development budget for FY2025/26. Enter amount in billions of UGX."
    )
    
    # Budget Categories - FY2026/27
    wage_fy2026_27 = fields.Float(
        string='Wage FY2026/27 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Wage budget for FY2026/27. Enter amount in billions of UGX."
    )

    non_wage_recurrent_fy2026_27 = fields.Float(
        string='Non-Wage Recurrent FY2026/27 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Non-wage recurrent budget for FY2026/27. Enter amount in billions of UGX."
    )

    total_development_fy2026_27 = fields.Float(
        string='Total Development FY2026/27 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Total development budget for FY2026/27. Enter amount in billions of UGX."
    )
    
    # Budget Categories - FY2027/28
    wage_fy2027_28 = fields.Float(
        string='Wage FY2027/28 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Wage budget for FY2027/28. Enter amount in billions of UGX."
    )

    non_wage_recurrent_fy2027_28 = fields.Float(
        string='Non-Wage Recurrent FY2027/28 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Non-wage recurrent budget for FY2027/28. Enter amount in billions of UGX."
    )

    total_development_fy2027_28 = fields.Float(
        string='Total Development FY2027/28 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Total development budget for FY2027/28. Enter amount in billions of UGX."
    )

    # Budget Categories - FY2028/29
    wage_fy2028_29 = fields.Float(
        string='Wage FY2028/29 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Wage budget for FY2028/29. Enter amount in billions of UGX."
    )

    non_wage_recurrent_fy2028_29 = fields.Float(
        string='Non-Wage Recurrent FY2028/29 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Non-wage recurrent budget for FY2028/29. Enter amount in billions of UGX."
    )

    total_development_fy2028_29 = fields.Float(
        string='Total Development FY2028/29 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Total development budget for FY2028/29. Enter amount in billions of UGX."
    )

    # Budget Categories - FY2029/30
    wage_fy2029_30 = fields.Float(
        string='Wage FY2029/30 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Wage budget for FY2029/30. Enter amount in billions of UGX."
    )

    non_wage_recurrent_fy2029_30 = fields.Float(
        string='Non-Wage Recurrent FY2029/30 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Non-wage recurrent budget for FY2029/30. Enter amount in billions of UGX."
    )

    total_development_fy2029_30 = fields.Float(
        string='Total Development FY2029/30 (UGX Bns)',
        tracking=True,
        digits=(16, 2),
        help="Total development budget for FY2029/30. Enter amount in billions of UGX."
    )

    # ===== MTEF (Medium-Term Expenditure Framework) Fields =====

    # MTEF - FY2025/26 (Approved)
    mtef_wage_fy2025_26 = fields.Float(
        string='MTEF Wage FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF Wage budget for FY2025/26 (Approved)"
    )

    mtef_non_wage_recurrent_fy2025_26 = fields.Float(
        string='MTEF Non-Wage Recurrent FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF Non-wage recurrent budget for FY2025/26"
    )

    mtef_gou_devt_fy2025_26 = fields.Float(
        string='MTEF GoU Dev\'t FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF Government of Uganda Development budget for FY2025/26"
    )

    mtef_gou_total_excl_ext_fin_fy2025_26 = fields.Float(
        string='MTEF GoU Total (Excl Ext Fin) FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF GoU Total excluding External Financing for FY2025/26"
    )

    mtef_external_financing_fy2025_26 = fields.Float(
        string='MTEF External Financing FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF External Financing for FY2025/26"
    )

    mtef_total_gou_ext_fin_fy2025_26 = fields.Float(
        string='MTEF Total GoU+Ext Fin FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF Total GoU plus External Financing for FY2025/26"
    )

    mtef_arrears_fy2025_26 = fields.Float(
        string='MTEF Arrears FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF Arrears for FY2025/26"
    )

    mtef_total_budget_fy2025_26 = fields.Float(
        string='MTEF Total Budget FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF Total Budget for FY2025/26"
    )

    mtef_total_vote_budget_excl_arrears_fy2025_26 = fields.Float(
        string='MTEF Total Vote Budget Excl Arrears FY2025/26 (UGX Bns)',
        tracking=True,
        help="MTEF Total Vote Budget excluding Arrears for FY2025/26"
    )

    # MTEF - FY2026/27
    mtef_wage_fy2026_27 = fields.Float(
        string='MTEF Wage FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF Wage budget for FY2026/27"
    )

    mtef_non_wage_recurrent_fy2026_27 = fields.Float(
        string='MTEF Non-Wage Recurrent FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF Non-wage recurrent budget for FY2026/27"
    )

    mtef_gou_devt_fy2026_27 = fields.Float(
        string='MTEF GoU Dev\'t FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF Government of Uganda Development budget for FY2026/27"
    )

    mtef_gou_total_excl_ext_fin_fy2026_27 = fields.Float(
        string='MTEF GoU Total (Excl Ext Fin) FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF GoU Total excluding External Financing for FY2026/27"
    )

    mtef_external_financing_fy2026_27 = fields.Float(
        string='MTEF External Financing FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF External Financing for FY2026/27"
    )

    mtef_total_gou_ext_fin_fy2026_27 = fields.Float(
        string='MTEF Total GoU+Ext Fin FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF Total GoU plus External Financing for FY2026/27"
    )

    mtef_arrears_fy2026_27 = fields.Float(
        string='MTEF Arrears FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF Arrears for FY2026/27"
    )

    mtef_total_budget_fy2026_27 = fields.Float(
        string='MTEF Total Budget FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF Total Budget for FY2026/27"
    )

    mtef_total_vote_budget_excl_arrears_fy2026_27 = fields.Float(
        string='MTEF Total Vote Budget Excl Arrears FY2026/27 (UGX Bns)',
        tracking=True,
        help="MTEF Total Vote Budget excluding Arrears for FY2026/27"
    )

    # MTEF - FY2027/28
    mtef_wage_fy2027_28 = fields.Float(
        string='MTEF Wage FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF Wage budget for FY2027/28"
    )

    mtef_non_wage_recurrent_fy2027_28 = fields.Float(
        string='MTEF Non-Wage Recurrent FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF Non-wage recurrent budget for FY2027/28"
    )

    mtef_gou_devt_fy2027_28 = fields.Float(
        string='MTEF GoU Dev\'t FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF Government of Uganda Development budget for FY2027/28"
    )

    mtef_gou_total_excl_ext_fin_fy2027_28 = fields.Float(
        string='MTEF GoU Total (Excl Ext Fin) FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF GoU Total excluding External Financing for FY2027/28"
    )

    mtef_external_financing_fy2027_28 = fields.Float(
        string='MTEF External Financing FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF External Financing for FY2027/28"
    )

    mtef_total_gou_ext_fin_fy2027_28 = fields.Float(
        string='MTEF Total GoU+Ext Fin FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF Total GoU plus External Financing for FY2027/28"
    )

    mtef_arrears_fy2027_28 = fields.Float(
        string='MTEF Arrears FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF Arrears for FY2027/28"
    )

    mtef_total_budget_fy2027_28 = fields.Float(
        string='MTEF Total Budget FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF Total Budget for FY2027/28"
    )

    mtef_total_vote_budget_excl_arrears_fy2027_28 = fields.Float(
        string='MTEF Total Vote Budget Excl Arrears FY2027/28 (UGX Bns)',
        tracking=True,
        help="MTEF Total Vote Budget excluding Arrears for FY2027/28"
    )

    # MTEF - FY2028/29
    mtef_wage_fy2028_29 = fields.Float(
        string='MTEF Wage FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF Wage budget for FY2028/29"
    )

    mtef_non_wage_recurrent_fy2028_29 = fields.Float(
        string='MTEF Non-Wage Recurrent FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF Non-wage recurrent budget for FY2028/29"
    )

    mtef_gou_devt_fy2028_29 = fields.Float(
        string='MTEF GoU Dev\'t FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF Government of Uganda Development budget for FY2028/29"
    )

    mtef_gou_total_excl_ext_fin_fy2028_29 = fields.Float(
        string='MTEF GoU Total (Excl Ext Fin) FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF GoU Total excluding External Financing for FY2028/29"
    )

    mtef_external_financing_fy2028_29 = fields.Float(
        string='MTEF External Financing FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF External Financing for FY2028/29"
    )

    mtef_total_gou_ext_fin_fy2028_29 = fields.Float(
        string='MTEF Total GoU+Ext Fin FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF Total GoU plus External Financing for FY2028/29"
    )

    mtef_arrears_fy2028_29 = fields.Float(
        string='MTEF Arrears FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF Arrears for FY2028/29"
    )

    mtef_total_budget_fy2028_29 = fields.Float(
        string='MTEF Total Budget FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF Total Budget for FY2028/29"
    )

    mtef_total_vote_budget_excl_arrears_fy2028_29 = fields.Float(
        string='MTEF Total Vote Budget Excl Arrears FY2028/29 (UGX Bns)',
        tracking=True,
        help="MTEF Total Vote Budget excluding Arrears for FY2028/29"
    )

    # MTEF - FY2029/30
    mtef_wage_fy2029_30 = fields.Float(
        string='MTEF Wage FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF Wage budget for FY2029/30"
    )

    mtef_non_wage_recurrent_fy2029_30 = fields.Float(
        string='MTEF Non-Wage Recurrent FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF Non-wage recurrent budget for FY2029/30"
    )

    mtef_gou_devt_fy2029_30 = fields.Float(
        string='MTEF GoU Dev\'t FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF Government of Uganda Development budget for FY2029/30"
    )

    mtef_gou_total_excl_ext_fin_fy2029_30 = fields.Float(
        string='MTEF GoU Total (Excl Ext Fin) FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF GoU Total excluding External Financing for FY2029/30"
    )

    mtef_external_financing_fy2029_30 = fields.Float(
        string='MTEF External Financing FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF External Financing for FY2029/30"
    )

    mtef_total_gou_ext_fin_fy2029_30 = fields.Float(
        string='MTEF Total GoU+Ext Fin FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF Total GoU plus External Financing for FY2029/30"
    )

    mtef_arrears_fy2029_30 = fields.Float(
        string='MTEF Arrears FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF Arrears for FY2029/30"
    )

    mtef_total_budget_fy2029_30 = fields.Float(
        string='MTEF Total Budget FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF Total Budget for FY2029/30"
    )

    mtef_total_vote_budget_excl_arrears_fy2029_30 = fields.Float(
        string='MTEF Total Vote Budget Excl Arrears FY2029/30 (UGX Bns)',
        tracking=True,
        help="MTEF Total Vote Budget excluding Arrears for FY2029/30"
    )
    
    # Computed fields for totals
    total_recurrent_fy2025_26 = fields.Float(
        string='Total Recurrent FY2025/26 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total recurrent budget for FY2025/26 (Wage + Non-Wage Recurrent)"
    )
    
    total_budget_fy2025_26 = fields.Float(
        string='Total Budget FY2025/26 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total budget for FY2025/26 (Total Recurrent + Total Development)"
    )
    
    total_recurrent_fy2026_27 = fields.Float(
        string='Total Recurrent FY2026/27 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total recurrent budget for FY2026/27"
    )
    
    total_budget_fy2026_27 = fields.Float(
        string='Total Budget FY2026/27 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total budget for FY2026/27"
    )
    
    total_recurrent_fy2027_28 = fields.Float(
        string='Total Recurrent FY2027/28 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total recurrent budget for FY2027/28"
    )
    
    total_budget_fy2027_28 = fields.Float(
        string='Total Budget FY2027/28 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total budget for FY2027/28"
    )
    
    total_recurrent_fy2028_29 = fields.Float(
        string='Total Recurrent FY2028/29 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total recurrent budget for FY2028/29"
    )
    
    total_budget_fy2028_29 = fields.Float(
        string='Total Budget FY2028/29 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total budget for FY2028/29"
    )
    
    total_recurrent_fy2029_30 = fields.Float(
        string='Total Recurrent FY2029/30 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total recurrent budget for FY2029/30"
    )
    
    total_budget_fy2029_30 = fields.Float(
        string='Total Budget FY2029/30 (UGX Bns)',
        compute='_compute_totals',
        store=True,
        help="Total budget for FY2029/30"
    )
    
    # Grand totals across all years
    total_wage_all_years = fields.Float(
        string='Total Wage (All Years)',
        compute='_compute_grand_totals',
        store=True,
        help="Total wage budget across all fiscal years"
    )
    
    total_non_wage_recurrent_all_years = fields.Float(
        string='Total Non-Wage Recurrent (All Years)',
        compute='_compute_grand_totals',
        store=True,
        help="Total non-wage recurrent budget across all fiscal years"
    )
    
    total_recurrent_all_years = fields.Float(
        string='Total Recurrent (All Years)',
        compute='_compute_grand_totals',
        store=True,
        help="Total recurrent budget across all fiscal years"
    )
    
    total_development_all_years = fields.Float(
        string='Total Development (All Years)',
        compute='_compute_grand_totals',
        store=True,
        help="Total development budget across all fiscal years"
    )
    
    total_budget_all_years = fields.Float(
        string='Total Budget (All Years)',
        compute='_compute_grand_totals',
        store=True,
        help="Total budget across all fiscal years"
    )

    # MTEF Grand totals across all years
    mtef_total_wage_all_years = fields.Float(
        string='MTEF Total Wage (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total wage budget across all fiscal years"
    )

    mtef_total_non_wage_recurrent_all_years = fields.Float(
        string='MTEF Total Non-Wage Recurrent (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total non-wage recurrent budget across all fiscal years"
    )

    mtef_total_gou_devt_all_years = fields.Float(
        string='MTEF Total GoU Dev\'t (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total GoU Development budget across all fiscal years"
    )

    mtef_total_gou_total_excl_ext_fin_all_years = fields.Float(
        string='MTEF Total GoU Total Excl Ext Fin (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total GoU Total excluding External Financing across all fiscal years"
    )

    mtef_total_external_financing_all_years = fields.Float(
        string='MTEF Total External Financing (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total External Financing across all fiscal years"
    )

    mtef_total_gou_ext_fin_all_years = fields.Float(
        string='MTEF Total GoU+Ext Fin (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total GoU plus External Financing across all fiscal years"
    )

    mtef_total_arrears_all_years = fields.Float(
        string='MTEF Total Arrears (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total Arrears across all fiscal years"
    )

    mtef_total_budget_all_years = fields.Float(
        string='MTEF Total Budget (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total Budget across all fiscal years"
    )

    mtef_total_vote_budget_excl_arrears_all_years = fields.Float(
        string='MTEF Total Vote Budget Excl Arrears (All Years)',
        compute='_compute_mtef_grand_totals',
        store=True,
        help="MTEF Total Vote Budget excluding Arrears across all fiscal years"
    )

    # Programme budget allocations
    programme_budget_ids = fields.One2many(
        'programme.budget',
        'financial_strategy_id',
        string='Programme Budget Allocations',
        help="Budget allocations by programme for this financial strategy"
    )

    # Financial analysis relationships
    financial_analysis_ids = fields.One2many(
        'financial.analysis',
        'financial_strategy_id',
        string='Financial Analyses',
        help="Financial analyses conducted for this strategy"
    )

    financial_integration_ids = fields.One2many(
        'financial.integration',
        'financial_strategy_id',
        string='Financial Integrations',
        help="Financial integrations for this strategy"
    )

    financial_dashboard_ids = fields.One2many(
        'financial.dashboard',
        'financial_strategy_id',
        string='Financial Dashboards',
        help="Financial dashboards for this strategy"
    )

    # Analysis counts
    analysis_count = fields.Integer(
        string='Analyses Count',
        compute='_compute_analysis_counts',
        help="Number of financial analyses"
    )

    integration_count = fields.Integer(
        string='Integrations Count',
        compute='_compute_analysis_counts',
        help="Number of financial integrations"
    )

    dashboard_count = fields.Integer(
        string='Dashboards Count',
        compute='_compute_analysis_counts',
        help="Number of financial dashboards"
    )

    programme_budget_count = fields.Integer(
        string='Programme Budget Count',
        compute='_compute_programme_budget_count',
        help="Number of programme budget allocations"
    )

    # Responsible person
    responsible_user_id = fields.Many2one(
        'res.users',
        string='Responsible Person',
        tracking=True,
        help="Person responsible for this financial strategy"
    )

    # Status
    status = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # Computed methods
    @api.depends('wage_fy2025_26', 'non_wage_recurrent_fy2025_26', 'total_development_fy2025_26',
                 'wage_fy2026_27', 'non_wage_recurrent_fy2026_27', 'total_development_fy2026_27',
                 'wage_fy2027_28', 'non_wage_recurrent_fy2027_28', 'total_development_fy2027_28',
                 'wage_fy2028_29', 'non_wage_recurrent_fy2028_29', 'total_development_fy2028_29',
                 'wage_fy2029_30', 'non_wage_recurrent_fy2029_30', 'total_development_fy2029_30')
    def _compute_totals(self):
        for record in self:
            # FY2025/26 totals
            record.total_recurrent_fy2025_26 = record.wage_fy2025_26 + record.non_wage_recurrent_fy2025_26
            record.total_budget_fy2025_26 = record.total_recurrent_fy2025_26 + record.total_development_fy2025_26

            # FY2026/27 totals
            record.total_recurrent_fy2026_27 = record.wage_fy2026_27 + record.non_wage_recurrent_fy2026_27
            record.total_budget_fy2026_27 = record.total_recurrent_fy2026_27 + record.total_development_fy2026_27

            # FY2027/28 totals
            record.total_recurrent_fy2027_28 = record.wage_fy2027_28 + record.non_wage_recurrent_fy2027_28
            record.total_budget_fy2027_28 = record.total_recurrent_fy2027_28 + record.total_development_fy2027_28

            # FY2028/29 totals
            record.total_recurrent_fy2028_29 = record.wage_fy2028_29 + record.non_wage_recurrent_fy2028_29
            record.total_budget_fy2028_29 = record.total_recurrent_fy2028_29 + record.total_development_fy2028_29

            # FY2029/30 totals
            record.total_recurrent_fy2029_30 = record.wage_fy2029_30 + record.non_wage_recurrent_fy2029_30
            record.total_budget_fy2029_30 = record.total_recurrent_fy2029_30 + record.total_development_fy2029_30

    @api.depends('wage_fy2025_26', 'wage_fy2026_27', 'wage_fy2027_28', 'wage_fy2028_29', 'wage_fy2029_30',
                 'non_wage_recurrent_fy2025_26', 'non_wage_recurrent_fy2026_27', 'non_wage_recurrent_fy2027_28',
                 'non_wage_recurrent_fy2028_29', 'non_wage_recurrent_fy2029_30',
                 'total_development_fy2025_26', 'total_development_fy2026_27', 'total_development_fy2027_28',
                 'total_development_fy2028_29', 'total_development_fy2029_30')
    def _compute_grand_totals(self):
        for record in self:
            # Total wage across all years
            record.total_wage_all_years = (
                record.wage_fy2025_26 + record.wage_fy2026_27 + record.wage_fy2027_28 +
                record.wage_fy2028_29 + record.wage_fy2029_30
            )

            # Total non-wage recurrent across all years
            record.total_non_wage_recurrent_all_years = (
                record.non_wage_recurrent_fy2025_26 + record.non_wage_recurrent_fy2026_27 +
                record.non_wage_recurrent_fy2027_28 + record.non_wage_recurrent_fy2028_29 +
                record.non_wage_recurrent_fy2029_30
            )

            # Total recurrent across all years
            record.total_recurrent_all_years = (
                record.total_wage_all_years + record.total_non_wage_recurrent_all_years
            )

            # Total development across all years
            record.total_development_all_years = (
                record.total_development_fy2025_26 + record.total_development_fy2026_27 +
                record.total_development_fy2027_28 + record.total_development_fy2028_29 +
                record.total_development_fy2029_30
            )

            # Total budget across all years
            record.total_budget_all_years = (
                record.total_recurrent_all_years + record.total_development_all_years
            )

    @api.depends('mtef_wage_fy2025_26', 'mtef_wage_fy2026_27', 'mtef_wage_fy2027_28', 'mtef_wage_fy2028_29', 'mtef_wage_fy2029_30',
                 'mtef_non_wage_recurrent_fy2025_26', 'mtef_non_wage_recurrent_fy2026_27', 'mtef_non_wage_recurrent_fy2027_28',
                 'mtef_non_wage_recurrent_fy2028_29', 'mtef_non_wage_recurrent_fy2029_30',
                 'mtef_gou_devt_fy2025_26', 'mtef_gou_devt_fy2026_27', 'mtef_gou_devt_fy2027_28',
                 'mtef_gou_devt_fy2028_29', 'mtef_gou_devt_fy2029_30',
                 'mtef_gou_total_excl_ext_fin_fy2025_26', 'mtef_gou_total_excl_ext_fin_fy2026_27', 'mtef_gou_total_excl_ext_fin_fy2027_28',
                 'mtef_gou_total_excl_ext_fin_fy2028_29', 'mtef_gou_total_excl_ext_fin_fy2029_30',
                 'mtef_external_financing_fy2025_26', 'mtef_external_financing_fy2026_27', 'mtef_external_financing_fy2027_28',
                 'mtef_external_financing_fy2028_29', 'mtef_external_financing_fy2029_30',
                 'mtef_total_gou_ext_fin_fy2025_26', 'mtef_total_gou_ext_fin_fy2026_27', 'mtef_total_gou_ext_fin_fy2027_28',
                 'mtef_total_gou_ext_fin_fy2028_29', 'mtef_total_gou_ext_fin_fy2029_30',
                 'mtef_arrears_fy2025_26', 'mtef_arrears_fy2026_27', 'mtef_arrears_fy2027_28',
                 'mtef_arrears_fy2028_29', 'mtef_arrears_fy2029_30',
                 'mtef_total_budget_fy2025_26', 'mtef_total_budget_fy2026_27', 'mtef_total_budget_fy2027_28',
                 'mtef_total_budget_fy2028_29', 'mtef_total_budget_fy2029_30',
                 'mtef_total_vote_budget_excl_arrears_fy2025_26', 'mtef_total_vote_budget_excl_arrears_fy2026_27', 'mtef_total_vote_budget_excl_arrears_fy2027_28',
                 'mtef_total_vote_budget_excl_arrears_fy2028_29', 'mtef_total_vote_budget_excl_arrears_fy2029_30')
    def _compute_mtef_grand_totals(self):
        for record in self:
            # MTEF Total wage across all years
            record.mtef_total_wage_all_years = (
                record.mtef_wage_fy2025_26 + record.mtef_wage_fy2026_27 + record.mtef_wage_fy2027_28 +
                record.mtef_wage_fy2028_29 + record.mtef_wage_fy2029_30
            )

            # MTEF Total non-wage recurrent across all years
            record.mtef_total_non_wage_recurrent_all_years = (
                record.mtef_non_wage_recurrent_fy2025_26 + record.mtef_non_wage_recurrent_fy2026_27 +
                record.mtef_non_wage_recurrent_fy2027_28 + record.mtef_non_wage_recurrent_fy2028_29 +
                record.mtef_non_wage_recurrent_fy2029_30
            )

            # MTEF Total GoU Development across all years
            record.mtef_total_gou_devt_all_years = (
                record.mtef_gou_devt_fy2025_26 + record.mtef_gou_devt_fy2026_27 +
                record.mtef_gou_devt_fy2027_28 + record.mtef_gou_devt_fy2028_29 +
                record.mtef_gou_devt_fy2029_30
            )

            # MTEF Total GoU Total excluding External Financing across all years
            record.mtef_total_gou_total_excl_ext_fin_all_years = (
                record.mtef_gou_total_excl_ext_fin_fy2025_26 + record.mtef_gou_total_excl_ext_fin_fy2026_27 +
                record.mtef_gou_total_excl_ext_fin_fy2027_28 + record.mtef_gou_total_excl_ext_fin_fy2028_29 +
                record.mtef_gou_total_excl_ext_fin_fy2029_30
            )

            # MTEF Total External Financing across all years
            record.mtef_total_external_financing_all_years = (
                record.mtef_external_financing_fy2025_26 + record.mtef_external_financing_fy2026_27 +
                record.mtef_external_financing_fy2027_28 + record.mtef_external_financing_fy2028_29 +
                record.mtef_external_financing_fy2029_30
            )

            # MTEF Total GoU plus External Financing across all years
            record.mtef_total_gou_ext_fin_all_years = (
                record.mtef_total_gou_ext_fin_fy2025_26 + record.mtef_total_gou_ext_fin_fy2026_27 +
                record.mtef_total_gou_ext_fin_fy2027_28 + record.mtef_total_gou_ext_fin_fy2028_29 +
                record.mtef_total_gou_ext_fin_fy2029_30
            )

            # MTEF Total Arrears across all years
            record.mtef_total_arrears_all_years = (
                record.mtef_arrears_fy2025_26 + record.mtef_arrears_fy2026_27 +
                record.mtef_arrears_fy2027_28 + record.mtef_arrears_fy2028_29 +
                record.mtef_arrears_fy2029_30
            )

            # MTEF Total Budget across all years
            record.mtef_total_budget_all_years = (
                record.mtef_total_budget_fy2025_26 + record.mtef_total_budget_fy2026_27 +
                record.mtef_total_budget_fy2027_28 + record.mtef_total_budget_fy2028_29 +
                record.mtef_total_budget_fy2029_30
            )

            # MTEF Total Vote Budget excluding Arrears across all years
            record.mtef_total_vote_budget_excl_arrears_all_years = (
                record.mtef_total_vote_budget_excl_arrears_fy2025_26 + record.mtef_total_vote_budget_excl_arrears_fy2026_27 +
                record.mtef_total_vote_budget_excl_arrears_fy2027_28 + record.mtef_total_vote_budget_excl_arrears_fy2028_29 +
                record.mtef_total_vote_budget_excl_arrears_fy2029_30
            )

    @api.depends('programme_budget_ids')
    def _compute_programme_budget_count(self):
        for record in self:
            record.programme_budget_count = len(record.programme_budget_ids)

    @api.depends('financial_analysis_ids', 'financial_integration_ids', 'financial_dashboard_ids')
    def _compute_analysis_counts(self):
        for record in self:
            record.analysis_count = len(record.financial_analysis_ids)
            record.integration_count = len(record.financial_integration_ids)
            record.dashboard_count = len(record.financial_dashboard_ids)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for record in self:
            if record.start_date and record.end_date and record.start_date > record.end_date:
                raise ValidationError(_("Start date cannot be later than end date."))

    @api.constrains('wage_fy2025_26', 'wage_fy2026_27', 'wage_fy2027_28', 'wage_fy2028_29', 'wage_fy2029_30',
                    'non_wage_recurrent_fy2025_26', 'non_wage_recurrent_fy2026_27', 'non_wage_recurrent_fy2027_28',
                    'non_wage_recurrent_fy2028_29', 'non_wage_recurrent_fy2029_30',
                    'total_development_fy2025_26', 'total_development_fy2026_27', 'total_development_fy2027_28',
                    'total_development_fy2028_29', 'total_development_fy2029_30')
    def _check_budget_amounts(self):
        """Validate that budget amounts are not negative"""
        for record in self:
            budget_fields = [
                'wage_fy2025_26', 'wage_fy2026_27', 'wage_fy2027_28', 'wage_fy2028_29', 'wage_fy2029_30',
                'non_wage_recurrent_fy2025_26', 'non_wage_recurrent_fy2026_27', 'non_wage_recurrent_fy2027_28',
                'non_wage_recurrent_fy2028_29', 'non_wage_recurrent_fy2029_30',
                'total_development_fy2025_26', 'total_development_fy2026_27', 'total_development_fy2027_28',
                'total_development_fy2028_29', 'total_development_fy2029_30'
            ]

            for field_name in budget_fields:
                field_value = getattr(record, field_name, 0)
                if field_value < 0:
                    field_label = record._fields[field_name].string
                    raise ValidationError(_("Budget amount for '%s' cannot be negative.") % field_label)

    def action_approve(self):
        """Approve the financial strategy"""
        self.write({'status': 'approved'})
        return True

    def action_activate(self):
        """Activate the financial strategy"""
        self.write({'status': 'active'})
        return True

    def action_complete(self):
        """Mark the financial strategy as completed"""
        self.write({'status': 'completed'})
        return True

    def action_cancel(self):
        """Cancel the financial strategy"""
        self.write({'status': 'cancelled'})
        return True

    # Financial Analysis Actions
    def action_create_budget_variance_analysis(self):
        """Create budget variance analysis"""
        analysis = self.env['financial.analysis'].create({
            'name': f'Budget Variance Analysis - {self.name}',
            'financial_strategy_id': self.id,
            'analysis_type': 'budget_variance',
            'scope': 'strategic',
            'fiscal_year': 'all_years',
        })
        analysis.generate_budget_variance_analysis()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Budget Variance Analysis',
            'res_model': 'financial.analysis',
            'res_id': analysis.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_create_funding_analysis(self):
        """Create funding source analysis"""
        analysis = self.env['financial.analysis'].create({
            'name': f'Funding Source Analysis - {self.name}',
            'financial_strategy_id': self.id,
            'analysis_type': 'funding_analysis',
            'scope': 'strategic',
            'fiscal_year': 'all_years',
        })
        analysis.generate_funding_source_analysis()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Funding Source Analysis',
            'res_model': 'financial.analysis',
            'res_id': analysis.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_create_programme_efficiency_analysis(self):
        """Create programme efficiency analysis"""
        analysis = self.env['financial.analysis'].create({
            'name': f'Programme Efficiency Analysis - {self.name}',
            'financial_strategy_id': self.id,
            'analysis_type': 'programme_efficiency',
            'scope': 'programme',
            'fiscal_year': 'all_years',
        })
        analysis.generate_programme_efficiency_analysis()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Programme Efficiency Analysis',
            'res_model': 'financial.analysis',
            'res_id': analysis.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_create_budget_performance_integration(self):
        """Create budget-performance integration"""
        integration = self.env['financial.integration'].create({
            'name': f'Budget-Performance Integration - {self.name}',
            'financial_strategy_id': self.id,
            'integration_type': 'budget_performance',
            'scope': 'full_strategy',
            'fiscal_year_focus': 'all_years',
        })
        integration.execute_budget_performance_integration()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Budget-Performance Integration',
            'res_model': 'financial.integration',
            'res_id': integration.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_create_executive_dashboard(self):
        """Create executive financial dashboard"""
        dashboard = self.env['financial.dashboard'].create({
            'name': f'Executive Dashboard - {self.name}',
            'financial_strategy_id': self.id,
            'dashboard_type': 'executive',
            'refresh_frequency': 'daily',
        })
        dashboard.generate_executive_dashboard()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Executive Financial Dashboard',
            'res_model': 'financial.dashboard',
            'res_id': dashboard.id,
            'view_mode': 'form',
            'target': 'current',
        }
