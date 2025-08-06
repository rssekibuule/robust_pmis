# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date
import json
import statistics


class PerformanceAnalytics(models.Model):
    _name = 'performance.analytics'
    _description = 'Performance Analytics and Insights'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'
    _rec_name = 'title'

    title = fields.Char(
        string='Analysis Title',
        required=True,
        help="Title of the performance analysis"
    )
    
    date = fields.Date(
        string='Analysis Date',
        default=fields.Date.context_today,
        required=True
    )
    
    analysis_type = fields.Selection([
        ('trend', 'Trend Analysis'),
        ('comparative', 'Comparative Analysis'),
        ('predictive', 'Predictive Analysis'),
        ('risk', 'Risk Assessment'),
        ('performance_gap', 'Performance Gap Analysis'),
    ], string='Analysis Type', required=True, default='trend')
    
    scope = fields.Selection([
        ('strategic', 'Strategic Level'),
        ('directorate', 'Directorate Level'),
        ('programme', 'Programme Level'),
        ('kpi', 'KPI Level'),
    ], string='Analysis Scope', required=True, default='strategic')
    
    # Related records
    strategic_goal_id = fields.Many2one(
        'strategic.goal',
        string='Strategic Goal',
        help="Strategic goal for analysis"
    )
    
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Directorate',
        help="Directorate for analysis"
    )
    
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        help="Programme for analysis"
    )
    
    kpi_id = fields.Many2one(
        'key.performance.indicator',
        string='KPI',
        help="KPI for analysis"
    )
    
    # Analysis results
    insights = fields.Html(
        string='Key Insights',
        help="Key insights from the analysis"
    )
    
    recommendations = fields.Html(
        string='Recommendations',
        help="Recommended actions based on analysis"
    )
    
    risk_level = fields.Selection([
        ('low', 'Low Risk'),
        ('medium', 'Medium Risk'),
        ('high', 'High Risk'),
        ('critical', 'Critical Risk'),
    ], string='Risk Level', help="Overall risk assessment")
    
    confidence_score = fields.Float(
        string='Confidence Score (%)',
        help="Confidence level of the analysis (0-100%)"
    )
    
    # Data and metrics
    data_points = fields.Integer(
        string='Data Points',
        help="Number of data points used in analysis"
    )
    
    analysis_period_start = fields.Date(
        string='Analysis Period Start',
        help="Start date of analysis period"
    )
    
    analysis_period_end = fields.Date(
        string='Analysis Period End',
        help="End date of analysis period"
    )
    
    # JSON field for storing detailed analysis data
    analysis_data = fields.Text(
        string='Analysis Data',
        help="Detailed analysis data in JSON format"
    )
    
    # Status and workflow
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_review', 'In Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
    ], string='Status', default='draft')
    
    reviewer_id = fields.Many2one(
        'res.users',
        string='Reviewer',
        help="User who reviewed the analysis"
    )
    
    review_date = fields.Datetime(
        string='Review Date',
        help="Date when analysis was reviewed"
    )
    
    # Automated analysis methods
    @api.model
    def cron_generate_weekly_analytics(self):
        """Generate weekly performance analytics"""
        # Generate trend analysis for all active KPIs
        self._generate_kpi_trend_analysis()
        
        # Generate directorate performance comparison
        self._generate_directorate_comparison()
        
        # Generate risk assessment
        self._generate_risk_assessment()
        
        return True
    
    def _generate_kpi_trend_analysis(self):
        """Generate trend analysis for KPIs"""
        kpis = self.env['key.performance.indicator'].search([('active', '=', True)])
        
        for kpi in kpis:
            # Get performance scores for the last 3 months
            three_months_ago = date.today() - timedelta(days=90)
            scores = self.env['performance.score'].search([
                ('indicator_id', '=', kpi.id),
                ('date', '>=', three_months_ago)
            ], order='date')
            
            if len(scores) >= 3:  # Need at least 3 data points
                trend_data = self._analyze_trend(scores)
                
                # Create analytics record
                self.create({
                    'title': f'Trend Analysis: {kpi.name}',
                    'analysis_type': 'trend',
                    'scope': 'kpi',
                    'kpi_id': kpi.id,
                    'directorate_id': kpi.directorate_id.id if kpi.directorate_id else False,
                    'analysis_period_start': three_months_ago,
                    'analysis_period_end': date.today(),
                    'data_points': len(scores),
                    'insights': trend_data['insights'],
                    'recommendations': trend_data['recommendations'],
                    'risk_level': trend_data['risk_level'],
                    'confidence_score': trend_data['confidence'],
                    'analysis_data': json.dumps(trend_data['raw_data']),
                    'state': 'approved',  # Auto-approve system-generated analytics
                })
    
    def _analyze_trend(self, scores):
        """Analyze trend from performance scores"""
        values = [score.achievement_percentage for score in scores]
        dates = [score.date.strftime('%Y-%m-%d') for score in scores]
        
        # Calculate trend direction
        if len(values) >= 2:
            recent_avg = statistics.mean(values[-3:]) if len(values) >= 3 else values[-1]
            earlier_avg = statistics.mean(values[:3]) if len(values) >= 3 else values[0]
            trend_direction = 'improving' if recent_avg > earlier_avg else 'declining' if recent_avg < earlier_avg else 'stable'
        else:
            trend_direction = 'insufficient_data'
        
        # Calculate volatility
        volatility = statistics.stdev(values) if len(values) > 1 else 0
        
        # Generate insights
        insights = f"""
        <h4>Trend Analysis Results</h4>
        <ul>
            <li><strong>Trend Direction:</strong> {trend_direction.title()}</li>
            <li><strong>Current Performance:</strong> {values[-1]:.1f}%</li>
            <li><strong>Average Performance:</strong> {statistics.mean(values):.1f}%</li>
            <li><strong>Performance Volatility:</strong> {volatility:.1f}%</li>
            <li><strong>Data Points Analyzed:</strong> {len(values)}</li>
        </ul>
        """
        
        # Generate recommendations
        if trend_direction == 'declining':
            recommendations = """
            <h4>Recommended Actions</h4>
            <ul>
                <li>Investigate root causes of performance decline</li>
                <li>Implement corrective measures immediately</li>
                <li>Increase monitoring frequency</li>
                <li>Review resource allocation and support</li>
            </ul>
            """
            risk_level = 'high' if recent_avg < 70 else 'medium'
        elif trend_direction == 'improving':
            recommendations = """
            <h4>Recommended Actions</h4>
            <ul>
                <li>Continue current successful strategies</li>
                <li>Document best practices for replication</li>
                <li>Consider scaling successful approaches</li>
            </ul>
            """
            risk_level = 'low'
        else:
            recommendations = """
            <h4>Recommended Actions</h4>
            <ul>
                <li>Monitor for any changes in performance patterns</li>
                <li>Maintain current performance levels</li>
                <li>Look for opportunities for improvement</li>
            </ul>
            """
            risk_level = 'medium' if statistics.mean(values) < 80 else 'low'
        
        # Calculate confidence based on data quality
        confidence = min(100, (len(values) / 12) * 100)  # Higher confidence with more data points
        
        return {
            'insights': insights,
            'recommendations': recommendations,
            'risk_level': risk_level,
            'confidence': confidence,
            'raw_data': {
                'values': values,
                'dates': dates,
                'trend_direction': trend_direction,
                'volatility': volatility,
                'average': statistics.mean(values),
            }
        }
    
    def _generate_directorate_comparison(self):
        """Generate comparative analysis between directorates"""
        directorates = self.env['kcca.directorate'].search([('active', '=', True)])
        
        if len(directorates) < 2:
            return
        
        # Get performance data for each directorate
        directorate_performance = {}
        for directorate in directorates:
            kpis = self.env['key.performance.indicator'].search([
                ('directorate_id', '=', directorate.id),
                ('active', '=', True)
            ])
            
            if kpis:
                avg_performance = sum(kpi.achievement_percentage for kpi in kpis) / len(kpis)
                directorate_performance[directorate.name] = {
                    'performance': avg_performance,
                    'kpi_count': len(kpis),
                    'directorate_id': directorate.id
                }
        
        if len(directorate_performance) >= 2:
            # Create comparative analysis
            sorted_performance = sorted(directorate_performance.items(), key=lambda x: x[1]['performance'], reverse=True)
            
            insights = "<h4>Directorate Performance Comparison</h4><ul>"
            for i, (name, data) in enumerate(sorted_performance):
                insights += f"<li><strong>{i+1}. {name}:</strong> {data['performance']:.1f}% (based on {data['kpi_count']} KPIs)</li>"
            insights += "</ul>"
            
            # Generate recommendations for bottom performers
            bottom_performers = sorted_performance[-2:]  # Bottom 2 performers
            recommendations = "<h4>Improvement Recommendations</h4><ul>"
            for name, data in bottom_performers:
                recommendations += f"<li><strong>{name}:</strong> Focus on performance improvement initiatives</li>"
            recommendations += "</ul>"
            
            self.create({
                'title': f'Directorate Performance Comparison - {date.today().strftime("%B %Y")}',
                'analysis_type': 'comparative',
                'scope': 'directorate',
                'analysis_period_start': date.today() - timedelta(days=30),
                'analysis_period_end': date.today(),
                'data_points': len(directorate_performance),
                'insights': insights,
                'recommendations': recommendations,
                'risk_level': 'medium',
                'confidence_score': 85.0,
                'analysis_data': json.dumps(directorate_performance),
                'state': 'approved',
            })
    
    def _generate_risk_assessment(self):
        """Generate overall risk assessment"""
        # Get all KPIs with low performance
        at_risk_kpis = self.env['key.performance.indicator'].search([
            ('active', '=', True),
            ('status', 'in', ['behind', 'at_risk'])
        ])
        
        if at_risk_kpis:
            # Group by directorate
            directorate_risks = {}
            for kpi in at_risk_kpis:
                if kpi.directorate_id:
                    if kpi.directorate_id.name not in directorate_risks:
                        directorate_risks[kpi.directorate_id.name] = []
                    directorate_risks[kpi.directorate_id.name].append(kpi.name)
            
            insights = "<h4>Risk Assessment Summary</h4>"
            insights += f"<p><strong>Total At-Risk KPIs:</strong> {len(at_risk_kpis)}</p>"
            insights += "<h5>Risks by Directorate:</h5><ul>"
            for directorate, kpis in directorate_risks.items():
                insights += f"<li><strong>{directorate}:</strong> {len(kpis)} at-risk KPIs</li>"
            insights += "</ul>"
            
            recommendations = "<h4>Risk Mitigation Recommendations</h4><ul>"
            recommendations += "<li>Immediate review of all at-risk KPIs</li>"
            recommendations += "<li>Develop action plans for performance improvement</li>"
            recommendations += "<li>Increase monitoring frequency for at-risk areas</li>"
            recommendations += "<li>Allocate additional resources where needed</li>"
            recommendations += "</ul>"
            
            # Determine overall risk level
            risk_percentage = (len(at_risk_kpis) / len(self.env['key.performance.indicator'].search([('active', '=', True)]))) * 100
            if risk_percentage > 30:
                risk_level = 'critical'
            elif risk_percentage > 20:
                risk_level = 'high'
            elif risk_percentage > 10:
                risk_level = 'medium'
            else:
                risk_level = 'low'
            
            self.create({
                'title': f'Organizational Risk Assessment - {date.today().strftime("%B %Y")}',
                'analysis_type': 'risk',
                'scope': 'strategic',
                'analysis_period_start': date.today() - timedelta(days=7),
                'analysis_period_end': date.today(),
                'data_points': len(at_risk_kpis),
                'insights': insights,
                'recommendations': recommendations,
                'risk_level': risk_level,
                'confidence_score': 90.0,
                'analysis_data': json.dumps(directorate_risks),
                'state': 'approved',
            })
    
    def action_approve(self):
        """Approve the analysis"""
        self.write({
            'state': 'approved',
            'reviewer_id': self.env.user.id,
            'review_date': fields.Datetime.now(),
        })
    
    def action_publish(self):
        """Publish the analysis"""
        self.write({'state': 'published'})
        
        # Send notification to relevant stakeholders
        self._send_analysis_notification()
    
    def _send_analysis_notification(self):
        """Send notification about published analysis"""
        # Implementation for sending notifications
        pass
