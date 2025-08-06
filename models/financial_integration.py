# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
import json
import logging

_logger = logging.getLogger(__name__)


class FinancialIntegration(models.Model):
    _name = 'financial.integration'
    _description = 'Financial Integration Hub - Connecting Financial Strategy with Performance'
    _order = 'integration_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Integration Name',
        required=True,
        tracking=True,
        help="Name of the financial integration"
    )
    
    # Core relationships
    financial_strategy_id = fields.Many2one(
        'financial.strategy',
        string='Financial Strategy',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Primary financial strategy"
    )
    
    integration_type = fields.Selection([
        ('budget_performance', 'Budget-Performance Integration'),
        ('programme_financial', 'Programme-Financial Integration'),
        ('directorate_budget', 'Directorate-Budget Integration'),
        ('kpi_financial', 'KPI-Financial Integration'),
        ('strategic_financial', 'Strategic-Financial Integration'),
        ('mtef_strategic', 'MTEF-Strategic Integration'),
    ], string='Integration Type', required=True, tracking=True)
    
    integration_date = fields.Date(
        string='Integration Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True
    )
    
    # Integration scope
    scope = fields.Selection([
        ('full_strategy', 'Full Strategy'),
        ('selected_programmes', 'Selected Programmes'),
        ('selected_directorates', 'Selected Directorates'),
        ('fiscal_year', 'Specific Fiscal Year'),
        ('custom', 'Custom Scope'),
    ], string='Integration Scope', required=True)
    
    fiscal_year_focus = fields.Selection([
        ('2025_26', 'FY2025/26'),
        ('2026_27', 'FY2026/27'),
        ('2027_28', 'FY2027/28'),
        ('2028_29', 'FY2028/29'),
        ('2029_30', 'FY2029/30'),
        ('all_years', 'All Years'),
    ], string='Fiscal Year Focus', default='all_years')
    
    # Integration results
    total_budget_integrated = fields.Float(
        string='Total Budget Integrated (UGX Bns)',
        help="Total budget amount in this integration"
    )
    
    performance_score = fields.Float(
        string='Integrated Performance Score (%)',
        help="Overall performance score from integration"
    )
    
    efficiency_ratio = fields.Float(
        string='Cost-Performance Efficiency Ratio',
        help="Ratio of performance to cost (higher is better)"
    )
    
    integration_completeness = fields.Float(
        string='Integration Completeness (%)',
        help="Percentage of complete data integration"
    )
    
    # Relationships
    programme_ids = fields.Many2many(
        'kcca.programme',
        'financial_integration_programme_rel',
        'integration_id',
        'programme_id',
        string='Integrated Programmes',
        help="Programmes included in this integration"
    )
    
    directorate_ids = fields.Many2many(
        'kcca.directorate',
        'financial_integration_directorate_rel',
        'integration_id',
        'directorate_id',
        string='Integrated Directorates',
        help="Directorates included in this integration"
    )
    
    programme_budget_ids = fields.Many2many(
        'programme.budget',
        'financial_integration_budget_rel',
        'integration_id',
        'budget_id',
        string='Programme Budgets',
        help="Programme budgets in this integration"
    )
    
    performance_indicator_ids = fields.Many2many(
        'performance.indicator',
        'financial_integration_indicator_rel',
        'integration_id',
        'indicator_id',
        string='Performance Indicators',
        help="Performance indicators integrated"
    )
    
    kpi_ids = fields.Many2many(
        'key.performance.indicator',
        'financial_integration_kpi_rel',
        'integration_id',
        'kpi_id',
        string='KPIs',
        help="KPIs integrated with financial data"
    )
    
    # Integration data
    integration_data = fields.Text(
        string='Integration Data (JSON)',
        help="Detailed integration data in JSON format"
    )
    
    mapping_rules = fields.Text(
        string='Mapping Rules',
        help="Rules used for data mapping and integration"
    )
    
    # Integration summary
    executive_summary = fields.Html(
        string='Integration Summary',
        help="Executive summary of integration results"
    )
    
    key_insights = fields.Html(
        string='Key Insights',
        help="Key insights from the integration"
    )
    
    recommendations = fields.Html(
        string='Integration Recommendations',
        help="Recommendations based on integration analysis"
    )
    
    # Status and quality
    state = fields.Selection([
        ('draft', 'Draft'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('validated', 'Validated'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True)
    
    data_quality_score = fields.Float(
        string='Data Quality Score (%)',
        help="Quality score of integrated data"
    )
    
    validation_status = fields.Selection([
        ('pending', 'Pending Validation'),
        ('passed', 'Validation Passed'),
        ('failed', 'Validation Failed'),
        ('partial', 'Partial Validation'),
    ], string='Validation Status', default='pending')
    
    # Computed fields
    programme_count = fields.Integer(
        string='Programmes Count',
        compute='_compute_counts',
        help="Number of programmes integrated"
    )
    
    directorate_count = fields.Integer(
        string='Directorates Count',
        compute='_compute_counts',
        help="Number of directorates integrated"
    )
    
    indicator_count = fields.Integer(
        string='Indicators Count',
        compute='_compute_counts',
        help="Total number of indicators integrated"
    )
    
    budget_count = fields.Integer(
        string='Budget Items Count',
        compute='_compute_counts',
        help="Number of budget items integrated"
    )
    
    @api.depends('programme_ids', 'directorate_ids', 'performance_indicator_ids', 'kpi_ids', 'programme_budget_ids')
    def _compute_counts(self):
        for record in self:
            record.programme_count = len(record.programme_ids)
            record.directorate_count = len(record.directorate_ids)
            record.indicator_count = len(record.performance_indicator_ids) + len(record.kpi_ids)
            record.budget_count = len(record.programme_budget_ids)
    
    # Integration methods
    def execute_budget_performance_integration(self):
        """Execute budget-performance integration"""
        self.ensure_one()
        self.state = 'processing'
        
        integration_data = {
            'integration_type': 'budget_performance',
            'programmes': {},
            'summary': {},
            'performance_budget_mapping': {}
        }
        
        total_budget = 0
        total_performance = 0
        programme_count = 0
        
        # Get programme budgets from financial strategy
        programme_budgets = self.financial_strategy_id.programme_budget_ids
        
        for budget in programme_budgets:
            programme = budget.programme_id
            programme_total = budget.total_budget
            total_budget += programme_total
            programme_count += 1
            
            # Get performance indicators for this programme
            indicators = programme.performance_indicator_ids
            avg_performance = 0
            
            if indicators:
                total_achievement = sum([ind.achievement_percentage or 0 for ind in indicators])
                avg_performance = total_achievement / len(indicators)
                total_performance += avg_performance
            
            # Calculate cost per performance unit
            cost_per_performance = (programme_total / avg_performance) if avg_performance > 0 else 0
            
            integration_data['programmes'][programme.name] = {
                'budget_total': programme_total,
                'performance_avg': avg_performance,
                'cost_per_performance': cost_per_performance,
                'indicator_count': len(indicators),
                'efficiency_score': (avg_performance / programme_total * 100) if programme_total > 0 else 0
            }
            
            # Add to relationships
            if programme not in self.programme_ids:
                self.programme_ids = [(4, programme.id)]
            if budget not in self.programme_budget_ids:
                self.programme_budget_ids = [(4, budget.id)]
            for indicator in indicators:
                if indicator not in self.performance_indicator_ids:
                    self.performance_indicator_ids = [(4, indicator.id)]
        
        # Calculate summary metrics
        avg_performance = total_performance / programme_count if programme_count > 0 else 0
        efficiency_ratio = avg_performance / (total_budget / programme_count) if total_budget > 0 else 0
        
        integration_data['summary'] = {
            'total_budget': total_budget,
            'avg_performance': avg_performance,
            'efficiency_ratio': efficiency_ratio,
            'programme_count': programme_count,
            'integration_completeness': self._calculate_completeness()
        }
        
        # Update integration fields
        self.total_budget_integrated = total_budget
        self.performance_score = avg_performance
        self.efficiency_ratio = efficiency_ratio
        self.integration_data = json.dumps(integration_data)
        self.integration_completeness = integration_data['summary']['integration_completeness']
        
        # Generate summary
        self._generate_integration_summary(integration_data)
        
        self.state = 'completed'
        
    def _calculate_completeness(self):
        """Calculate integration completeness percentage"""
        total_items = 0
        completed_items = 0
        
        # Check programme budgets
        programme_budgets = self.financial_strategy_id.programme_budget_ids
        total_items += len(programme_budgets)
        
        for budget in programme_budgets:
            if budget.total_budget > 0:
                completed_items += 1
                
            # Check if programme has performance indicators
            if budget.programme_id.performance_indicator_ids:
                completed_items += 0.5  # Partial credit for having indicators
        
        return (completed_items / total_items * 100) if total_items > 0 else 0
    
    def _generate_integration_summary(self, integration_data):
        """Generate integration summary"""
        summary_data = integration_data['summary']
        
        summary = f"""
        <h3>Budget-Performance Integration Summary</h3>
        <h4>Integration Overview:</h4>
        <ul>
            <li><strong>Total Budget Integrated:</strong> UGX {summary_data['total_budget']:.2f} Billion</li>
            <li><strong>Average Performance Score:</strong> {summary_data['avg_performance']:.1f}%</li>
            <li><strong>Cost-Performance Efficiency:</strong> {summary_data['efficiency_ratio']:.3f}</li>
            <li><strong>Programmes Integrated:</strong> {summary_data['programme_count']}</li>
            <li><strong>Integration Completeness:</strong> {summary_data['integration_completeness']:.1f}%</li>
        </ul>
        
        <h4>Key Performance-Budget Insights:</h4>
        <ul>
            <li>Budget allocation aligned with performance targets</li>
            <li>Cost efficiency varies significantly across programmes</li>
            <li>Performance data availability: {summary_data['integration_completeness']:.0f}%</li>
        </ul>
        """
        
        self.executive_summary = summary
        
        # Generate recommendations
        recommendations = """
        <h3>Integration Recommendations</h3>
        <ul>
            <li><strong>Data Quality:</strong> Improve performance data collection for better integration</li>
            <li><strong>Budget Alignment:</strong> Align budget allocations with performance priorities</li>
            <li><strong>Monitoring:</strong> Establish regular budget-performance review cycles</li>
            <li><strong>Efficiency:</strong> Focus resources on high-performing programmes</li>
        </ul>
        """
        
        self.recommendations = recommendations
