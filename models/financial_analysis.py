# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
import json
import logging

_logger = logging.getLogger(__name__)


class FinancialAnalysis(models.Model):
    _name = 'financial.analysis'
    _description = 'Financial Analysis and Integration Hub'
    _order = 'analysis_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Analysis Name',
        required=True,
        tracking=True,
        help="Name of the financial analysis"
    )
    
    # Core relationships
    financial_strategy_id = fields.Many2one(
        'financial.strategy',
        string='Financial Strategy',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Financial strategy being analyzed"
    )
    
    analysis_type = fields.Selection([
        ('budget_variance', 'Budget Variance Analysis'),
        ('funding_analysis', 'Funding Source Analysis'),
        ('programme_efficiency', 'Programme Cost Efficiency'),
        ('trend_analysis', 'Multi-Year Trend Analysis'),
        ('risk_assessment', 'Financial Risk Assessment'),
        ('performance_cost', 'Performance vs Cost Analysis'),
        ('comparative', 'Comparative Analysis'),
        ('forecast', 'Financial Forecast'),
    ], string='Analysis Type', required=True, tracking=True)
    
    scope = fields.Selection([
        ('strategic', 'Strategic Level'),
        ('programme', 'Programme Level'),
        ('directorate', 'Directorate Level'),
        ('fiscal_year', 'Fiscal Year'),
        ('funding_source', 'Funding Source'),
    ], string='Analysis Scope', required=True)
    
    # Analysis period
    analysis_date = fields.Date(
        string='Analysis Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True
    )
    
    fiscal_year = fields.Selection([
        ('2025_26', 'FY2025/26'),
        ('2026_27', 'FY2026/27'),
        ('2027_28', 'FY2027/28'),
        ('2028_29', 'FY2028/29'),
        ('2029_30', 'FY2029/30'),
        ('all_years', 'All Years'),
    ], string='Fiscal Year Focus', default='all_years')
    
    # Analysis results
    total_budget_analyzed = fields.Float(
        string='Total Budget Analyzed (UGX Bns)',
        help="Total budget amount included in this analysis"
    )
    
    variance_amount = fields.Float(
        string='Variance Amount (UGX Bns)',
        help="Budget variance identified in analysis"
    )
    
    variance_percentage = fields.Float(
        string='Variance Percentage (%)',
        help="Percentage variance from planned budget"
    )
    
    efficiency_score = fields.Float(
        string='Efficiency Score (%)',
        help="Overall efficiency score (0-100%)"
    )
    
    risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ], string='Risk Level', help="Financial risk assessment")
    
    # Analysis content
    executive_summary = fields.Html(
        string='Executive Summary',
        help="High-level summary of analysis findings"
    )
    
    key_findings = fields.Html(
        string='Key Findings',
        help="Detailed findings from the analysis"
    )
    
    recommendations = fields.Html(
        string='Recommendations',
        help="Recommended actions based on analysis"
    )
    
    methodology = fields.Text(
        string='Analysis Methodology',
        help="Methodology used for this analysis"
    )
    
    # Data and metrics
    analysis_data = fields.Text(
        string='Analysis Data (JSON)',
        help="Raw analysis data in JSON format"
    )
    
    data_sources = fields.Text(
        string='Data Sources',
        help="Sources of data used in analysis"
    )
    
    confidence_level = fields.Float(
        string='Confidence Level (%)',
        default=85.0,
        help="Confidence level of analysis results"
    )
    
    # Status and workflow
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True)
    
    # Relationships to other financial components
    programme_budget_ids = fields.Many2many(
        'programme.budget',
        string='Programme Budgets',
        help="Programme budgets included in this analysis"
    )
    
    directorate_ids = fields.Many2many(
        'kcca.directorate',
        string='Directorates',
        help="Directorates covered in this analysis"
    )
    
    programme_ids = fields.Many2many(
        'kcca.programme',
        string='Programmes',
        help="Programmes included in this analysis"
    )
    
    # Performance integration
    performance_indicator_ids = fields.Many2many(
        'performance.indicator',
        string='Performance Indicators',
        help="Performance indicators linked to this financial analysis"
    )
    
    kpi_ids = fields.Many2many(
        'key.performance.indicator',
        string='KPIs',
        help="KPIs related to this financial analysis"
    )
    
    # Analysis attachments
    chart_attachments = fields.Many2many(
        'ir.attachment',
        'financial_analysis_chart_rel',
        'analysis_id',
        'attachment_id',
        string='Charts and Graphs',
        help="Charts and graphs generated for this analysis"
    )
    
    report_attachments = fields.Many2many(
        'ir.attachment',
        'financial_analysis_report_rel',
        'analysis_id',
        'attachment_id',
        string='Analysis Reports',
        help="Detailed analysis reports"
    )
    
    # Computed fields
    programme_count = fields.Integer(
        string='Programmes Count',
        compute='_compute_counts',
        help="Number of programmes in analysis"
    )
    
    directorate_count = fields.Integer(
        string='Directorates Count',
        compute='_compute_counts',
        help="Number of directorates in analysis"
    )
    
    indicator_count = fields.Integer(
        string='Indicators Count',
        compute='_compute_counts',
        help="Number of performance indicators in analysis"
    )
    
    @api.depends('programme_ids', 'directorate_ids', 'performance_indicator_ids', 'kpi_ids')
    def _compute_counts(self):
        for record in self:
            record.programme_count = len(record.programme_ids)
            record.directorate_count = len(record.directorate_ids)
            record.indicator_count = len(record.performance_indicator_ids) + len(record.kpi_ids)
    
    # Analysis generation methods
    def generate_budget_variance_analysis(self):
        """Generate budget variance analysis"""
        self.ensure_one()
        
        # Get programme budgets
        programme_budgets = self.financial_strategy_id.programme_budget_ids
        
        analysis_data = {
            'total_programmes': len(programme_budgets),
            'fiscal_years': ['2025_26', '2026_27', '2027_28', '2028_29', '2029_30'],
            'variances': {},
            'summary': {}
        }
        
        total_budget = 0
        total_variance = 0
        
        for budget in programme_budgets:
            programme_name = budget.programme_id.name
            programme_total = budget.total_budget
            total_budget += programme_total
            
            # Calculate variance (placeholder - would use actual vs planned)
            variance = 0  # Would calculate actual variance here
            total_variance += variance
            
            analysis_data['variances'][programme_name] = {
                'budget': programme_total,
                'variance': variance,
                'variance_pct': (variance / programme_total * 100) if programme_total > 0 else 0
            }
        
        self.total_budget_analyzed = total_budget
        self.variance_amount = total_variance
        self.variance_percentage = (total_variance / total_budget * 100) if total_budget > 0 else 0
        self.analysis_data = json.dumps(analysis_data)
        
        # Generate findings
        self._generate_variance_findings()
    
    def _generate_variance_findings(self):
        """Generate findings for variance analysis"""
        findings = f"""
        <h3>Budget Variance Analysis Findings</h3>
        <ul>
            <li><strong>Total Budget Analyzed:</strong> UGX {self.total_budget_analyzed:.2f} Billion</li>
            <li><strong>Overall Variance:</strong> UGX {self.variance_amount:.2f} Billion ({self.variance_percentage:.1f}%)</li>
            <li><strong>Analysis Date:</strong> {self.analysis_date}</li>
        </ul>
        """
        
        self.key_findings = findings

    def generate_funding_source_analysis(self):
        """Generate funding source analysis"""
        self.ensure_one()

        strategy = self.financial_strategy_id

        # Calculate GoU vs Donor funding by year
        funding_analysis = {
            'fiscal_years': {},
            'totals': {
                'gou_total': 0,
                'donor_total': 0,
                'grand_total': 0
            },
            'trends': {}
        }

        # FY2025/26
        fy2025_gou = strategy.wage_fy2025_26 + strategy.non_wage_recurrent_fy2025_26 + 221.619
        fy2025_donor = 1036.181
        fy2025_total = fy2025_gou + fy2025_donor

        funding_analysis['fiscal_years']['2025_26'] = {
            'gou': fy2025_gou,
            'donor': fy2025_donor,
            'total': fy2025_total,
            'gou_pct': (fy2025_gou / fy2025_total * 100) if fy2025_total > 0 else 0,
            'donor_pct': (fy2025_donor / fy2025_total * 100) if fy2025_total > 0 else 0
        }

        # Similar calculations for other years...
        # FY2026/27
        fy2026_gou = strategy.wage_fy2026_27 + strategy.non_wage_recurrent_fy2026_27 + 254.862
        fy2026_donor = 1220.518
        fy2026_total = fy2026_gou + fy2026_donor

        funding_analysis['fiscal_years']['2026_27'] = {
            'gou': fy2026_gou,
            'donor': fy2026_donor,
            'total': fy2026_total,
            'gou_pct': (fy2026_gou / fy2026_total * 100) if fy2026_total > 0 else 0,
            'donor_pct': (fy2026_donor / fy2026_total * 100) if fy2026_total > 0 else 0
        }

        # Calculate totals
        total_gou = sum([year_data['gou'] for year_data in funding_analysis['fiscal_years'].values()])
        total_donor = sum([year_data['donor'] for year_data in funding_analysis['fiscal_years'].values()])
        grand_total = total_gou + total_donor

        funding_analysis['totals'] = {
            'gou_total': total_gou,
            'donor_total': total_donor,
            'grand_total': grand_total,
            'gou_pct': (total_gou / grand_total * 100) if grand_total > 0 else 0,
            'donor_pct': (total_donor / grand_total * 100) if grand_total > 0 else 0
        }

        self.total_budget_analyzed = grand_total
        self.analysis_data = json.dumps(funding_analysis)

        # Generate findings
        self._generate_funding_findings(funding_analysis)

    def _generate_funding_findings(self, funding_data):
        """Generate findings for funding source analysis"""
        totals = funding_data['totals']

        findings = f"""
        <h3>Funding Source Analysis</h3>
        <h4>Overall Funding Distribution:</h4>
        <ul>
            <li><strong>Government of Uganda (GoU):</strong> UGX {totals['gou_total']:.2f} Billion ({totals['gou_pct']:.1f}%)</li>
            <li><strong>Donor Funding:</strong> UGX {totals['donor_total']:.2f} Billion ({totals['donor_pct']:.1f}%)</li>
            <li><strong>Total Budget:</strong> UGX {totals['grand_total']:.2f} Billion</li>
        </ul>

        <h4>Key Observations:</h4>
        <ul>
            <li>Development projects heavily dependent on donor funding</li>
            <li>Recurrent costs (wage and non-wage) fully funded by GoU</li>
            <li>Donor funding averages {totals['donor_pct']:.0f}% of total budget</li>
        </ul>
        """

        self.key_findings = findings

        # Generate recommendations
        recommendations = """
        <h3>Funding Strategy Recommendations</h3>
        <ul>
            <li><strong>Diversification:</strong> Explore additional funding sources to reduce donor dependency</li>
            <li><strong>Sustainability:</strong> Develop plans for transitioning donor-funded projects to GoU funding</li>
            <li><strong>Capacity Building:</strong> Strengthen local revenue generation capabilities</li>
            <li><strong>Risk Management:</strong> Establish contingency plans for potential donor funding reductions</li>
        </ul>
        """

        self.recommendations = recommendations

    def generate_programme_efficiency_analysis(self):
        """Generate programme cost efficiency analysis"""
        self.ensure_one()

        programme_budgets = self.financial_strategy_id.programme_budget_ids
        efficiency_data = {
            'programmes': {},
            'rankings': [],
            'averages': {}
        }

        total_budget = 0
        programme_count = 0

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

            # Calculate cost per performance point
            cost_efficiency = (programme_total / avg_performance) if avg_performance > 0 else float('inf')

            efficiency_data['programmes'][programme.name] = {
                'budget': programme_total,
                'performance': avg_performance,
                'efficiency': cost_efficiency,
                'indicator_count': len(indicators)
            }

            efficiency_data['rankings'].append({
                'programme': programme.name,
                'efficiency_score': avg_performance / (programme_total / 100) if programme_total > 0 else 0
            })

        # Sort by efficiency score
        efficiency_data['rankings'].sort(key=lambda x: x['efficiency_score'], reverse=True)

        # Calculate averages
        avg_budget = total_budget / programme_count if programme_count > 0 else 0
        avg_performance = sum([p['performance'] for p in efficiency_data['programmes'].values()]) / programme_count if programme_count > 0 else 0

        efficiency_data['averages'] = {
            'avg_budget': avg_budget,
            'avg_performance': avg_performance,
            'total_budget': total_budget,
            'programme_count': programme_count
        }

        self.total_budget_analyzed = total_budget
        self.efficiency_score = avg_performance
        self.analysis_data = json.dumps(efficiency_data)

        # Generate findings
        self._generate_efficiency_findings(efficiency_data)

    def _generate_efficiency_findings(self, efficiency_data):
        """Generate findings for efficiency analysis"""
        averages = efficiency_data['averages']
        top_performers = efficiency_data['rankings'][:3]

        findings = f"""
        <h3>Programme Cost Efficiency Analysis</h3>
        <h4>Overall Statistics:</h4>
        <ul>
            <li><strong>Total Programmes Analyzed:</strong> {averages['programme_count']}</li>
            <li><strong>Total Budget:</strong> UGX {averages['total_budget']:.2f} Billion</li>
            <li><strong>Average Performance:</strong> {averages['avg_performance']:.1f}%</li>
            <li><strong>Average Budget per Programme:</strong> UGX {averages['avg_budget']:.2f} Billion</li>
        </ul>

        <h4>Top Performing Programmes (Efficiency):</h4>
        <ol>
        """

        for i, performer in enumerate(top_performers, 1):
            findings += f"<li><strong>{performer['programme']}</strong> - Efficiency Score: {performer['efficiency_score']:.2f}</li>"

        findings += """
        </ol>
        """

        self.key_findings = findings
