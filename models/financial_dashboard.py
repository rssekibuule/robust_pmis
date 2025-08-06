# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date, timedelta
import json
import logging

_logger = logging.getLogger(__name__)


class FinancialDashboard(models.Model):
    _name = 'financial.dashboard'
    _description = 'Financial Dashboard - Real-time Financial Analytics'
    _order = 'dashboard_date desc, id desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Dashboard Name',
        required=True,
        tracking=True,
        help="Name of the financial dashboard"
    )
    
    # Core configuration
    financial_strategy_id = fields.Many2one(
        'financial.strategy',
        string='Financial Strategy',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Financial strategy for dashboard"
    )
    
    dashboard_type = fields.Selection([
        ('executive', 'Executive Dashboard'),
        ('operational', 'Operational Dashboard'),
        ('programme', 'Programme Dashboard'),
        ('directorate', 'Directorate Dashboard'),
        ('budget_tracking', 'Budget Tracking Dashboard'),
        ('performance_financial', 'Performance-Financial Dashboard'),
    ], string='Dashboard Type', required=True, default='executive')
    
    dashboard_date = fields.Date(
        string='Dashboard Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True
    )
    
    refresh_frequency = fields.Selection([
        ('real_time', 'Real-time'),
        ('hourly', 'Hourly'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ], string='Refresh Frequency', default='daily')
    
    last_refresh = fields.Datetime(
        string='Last Refresh',
        help="Last time dashboard data was refreshed"
    )
    
    # Dashboard metrics
    total_budget = fields.Float(
        string='Total Budget (UGX Bns)',
        help="Total budget amount in dashboard"
    )
    
    budget_utilization = fields.Float(
        string='Budget Utilization (%)',
        help="Percentage of budget utilized"
    )
    
    performance_score = fields.Float(
        string='Overall Performance Score (%)',
        help="Overall performance score"
    )
    
    efficiency_index = fields.Float(
        string='Efficiency Index',
        help="Cost-performance efficiency index"
    )
    
    risk_score = fields.Float(
        string='Risk Score (%)',
        help="Overall financial risk score"
    )
    
    # Key Performance Indicators (KPIs) for Dashboard
    kpi_budget_variance = fields.Float(
        string='Budget Variance (%)',
        help="Variance from planned budget"
    )
    
    kpi_funding_ratio = fields.Float(
        string='GoU:Donor Funding Ratio',
        help="Ratio of GoU to Donor funding"
    )
    
    kpi_programme_efficiency = fields.Float(
        string='Programme Efficiency Score',
        help="Average programme efficiency score"
    )
    
    kpi_performance_trend = fields.Selection([
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
        ('critical', 'Critical'),
    ], string='Performance Trend', help="Overall performance trend")
    
    # Dashboard data
    dashboard_data = fields.Text(
        string='Dashboard Data (JSON)',
        help="Complete dashboard data in JSON format"
    )

    dashboard_summary = fields.Html(
        string='Dashboard Summary',
        compute='_compute_dashboard_summary',
        help="Formatted dashboard summary for display"
    )
    
    chart_data = fields.Text(
        string='Chart Data (JSON)',
        help="Data for dashboard charts and visualizations"
    )
    
    # Dashboard content
    executive_summary = fields.Html(
        string='Executive Summary',
        help="Executive summary for dashboard"
    )
    
    key_alerts = fields.Html(
        string='Key Alerts',
        help="Important alerts and notifications"
    )
    
    recommendations = fields.Html(
        string='Dashboard Recommendations',
        help="Actionable recommendations"
    )
    
    # Status and access
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('archived', 'Archived'),
    ], string='Status', default='draft', tracking=True)
    
    is_public = fields.Boolean(
        string='Public Dashboard',
        default=False,
        help="Whether dashboard is publicly accessible"
    )
    
    access_level = fields.Selection([
        ('public', 'Public Access'),
        ('internal', 'Internal Access'),
        ('restricted', 'Restricted Access'),
        ('confidential', 'Confidential'),
    ], string='Access Level', default='internal')
    
    # Relationships
    programme_ids = fields.Many2many(
        'kcca.programme',
        'dashboard_programme_rel',
        'dashboard_id',
        'programme_id',
        string='Dashboard Programmes',
        help="Programmes included in dashboard"
    )
    
    directorate_ids = fields.Many2many(
        'kcca.directorate',
        'dashboard_directorate_rel',
        'dashboard_id',
        'directorate_id',
        string='Dashboard Directorates',
        help="Directorates included in dashboard"
    )
    
    # Dashboard widgets/components
    widget_ids = fields.One2many(
        'financial.dashboard.widget',
        'dashboard_id',
        string='Dashboard Widgets',
        help="Widgets/components in this dashboard"
    )
    
    # Computed fields
    widget_count = fields.Integer(
        string='Widgets Count',
        compute='_compute_widget_count',
        help="Number of widgets in dashboard"
    )
    
    @api.depends('widget_ids')
    def _compute_widget_count(self):
        for record in self:
            record.widget_count = len(record.widget_ids)

    @api.depends('dashboard_data', 'total_budget', 'performance_score', 'efficiency_index')
    def _compute_dashboard_summary(self):
        for record in self:
            if not record.dashboard_data:
                record.dashboard_summary = "<p>No dashboard data available. Please refresh the dashboard.</p>"
                continue

            try:
                data = json.loads(record.dashboard_data)

                # Build formatted summary
                summary_html = f"""
                <div class="dashboard-summary">
                    <h4>Dashboard Overview</h4>
                    <div class="row">
                        <div class="col-md-6">
                            <h5>Financial Metrics</h5>
                            <ul>
                                <li><strong>Total Budget:</strong> UGX {record.total_budget:.2f} Billion</li>
                                <li><strong>Budget Utilization:</strong> {record.budget_utilization:.1f}%</li>
                                <li><strong>Performance Score:</strong> {record.performance_score:.1f}%</li>
                                <li><strong>Efficiency Index:</strong> {record.efficiency_index:.2f}</li>
                            </ul>
                        </div>
                        <div class="col-md-6">
                            <h5>Dashboard Information</h5>
                            <ul>
                                <li><strong>Dashboard Type:</strong> {dict(record._fields['dashboard_type'].selection).get(record.dashboard_type, record.dashboard_type)}</li>
                                <li><strong>Last Refresh:</strong> {record.last_refresh.strftime('%Y-%m-%d %H:%M:%S') if record.last_refresh else 'Never'}</li>
                                <li><strong>Widget Count:</strong> {record.widget_count}</li>
                                <li><strong>Access Level:</strong> {dict(record._fields['access_level'].selection).get(record.access_level, record.access_level)}</li>
                            </ul>
                        </div>
                    </div>
                """

                # Add KPIs if available
                if data.get('kpis'):
                    summary_html += """
                    <h5>Key Performance Indicators</h5>
                    <div class="row">
                    """
                    kpis = data['kpis']
                    for kpi_name, kpi_value in kpis.items():
                        if isinstance(kpi_value, (int, float)):
                            summary_html += f"""
                            <div class="col-md-3">
                                <div class="card">
                                    <div class="card-body text-center">
                                        <h6>{kpi_name.replace('_', ' ').title()}</h6>
                                        <h4>{kpi_value:.2f}{'%' if 'percentage' in kpi_name else ''}</h4>
                                    </div>
                                </div>
                            </div>
                            """
                    summary_html += "</div>"

                # Add alerts if available
                if data.get('alerts'):
                    summary_html += """
                    <h5>Active Alerts</h5>
                    <div class="alert-list">
                    """
                    for alert in data['alerts']:
                        alert_class = 'alert-warning' if alert.get('type') == 'warning' else 'alert-info'
                        summary_html += f"""
                        <div class="alert {alert_class}">
                            <strong>{alert.get('priority', '').title()} Priority:</strong> {alert.get('message', '')}
                        </div>
                        """
                    summary_html += "</div>"

                summary_html += "</div>"
                record.dashboard_summary = summary_html

            except (json.JSONDecodeError, KeyError, AttributeError) as e:
                record.dashboard_summary = f"<p class='text-danger'>Error parsing dashboard data: {str(e)}</p>"
    
    # Dashboard generation methods
    def generate_executive_dashboard(self):
        """Generate executive dashboard"""
        self.ensure_one()
        
        # Collect key metrics
        strategy = self.financial_strategy_id
        
        dashboard_data = {
            'dashboard_type': 'executive',
            'generated_at': datetime.now().isoformat(),
            'metrics': {
                'total_budget': strategy.total_budget_all_years,
                'gou_funding': strategy.total_wage_all_years + strategy.total_non_wage_recurrent_all_years,
                'donor_funding': strategy.total_development_all_years - (strategy.total_wage_all_years + strategy.total_non_wage_recurrent_all_years),
                'programme_count': len(strategy.programme_budget_ids),
            },
            'kpis': {},
            'trends': {},
            'alerts': []
        }
        
        # Calculate key ratios
        total_budget = dashboard_data['metrics']['total_budget']
        gou_funding = dashboard_data['metrics']['gou_funding']
        donor_funding = dashboard_data['metrics']['donor_funding']
        
        if total_budget > 0:
            dashboard_data['kpis']['gou_percentage'] = (gou_funding / total_budget) * 100
            dashboard_data['kpis']['donor_percentage'] = (donor_funding / total_budget) * 100
            dashboard_data['kpis']['funding_ratio'] = gou_funding / donor_funding if donor_funding > 0 else 0
        
        # Generate alerts
        if dashboard_data['kpis'].get('donor_percentage', 0) > 70:
            dashboard_data['alerts'].append({
                'type': 'warning',
                'message': 'High dependency on donor funding (>70%)',
                'priority': 'high'
            })
        
        # Update dashboard fields
        self.total_budget = total_budget
        self.kpi_funding_ratio = dashboard_data['kpis'].get('funding_ratio', 0)
        self.dashboard_data = json.dumps(dashboard_data)
        self.last_refresh = datetime.now()
        
        # Generate executive summary
        self._generate_executive_summary(dashboard_data)
        
        # Create default widgets
        self._create_default_widgets()

    def generate_programme_dashboard(self):
        """Generate programme-specific dashboard"""
        self.ensure_one()

        # For now, use executive dashboard logic as base
        # TODO: Implement programme-specific metrics
        self.generate_executive_dashboard()

        # Update dashboard type
        dashboard_data = json.loads(self.dashboard_data or '{}')
        dashboard_data['dashboard_type'] = 'programme'
        self.dashboard_data = json.dumps(dashboard_data)

    def generate_operational_dashboard(self):
        """Generate operational dashboard"""
        self.ensure_one()

        # For now, use executive dashboard logic as base
        # TODO: Implement operational-specific metrics
        self.generate_executive_dashboard()

        # Update dashboard type
        dashboard_data = json.loads(self.dashboard_data or '{}')
        dashboard_data['dashboard_type'] = 'operational'
        self.dashboard_data = json.dumps(dashboard_data)

    def generate_directorate_dashboard(self):
        """Generate directorate-specific dashboard"""
        self.ensure_one()

        # For now, use executive dashboard logic as base
        # TODO: Implement directorate-specific metrics
        self.generate_executive_dashboard()

        # Update dashboard type
        dashboard_data = json.loads(self.dashboard_data or '{}')
        dashboard_data['dashboard_type'] = 'directorate'
        self.dashboard_data = json.dumps(dashboard_data)

    def generate_budget_tracking_dashboard(self):
        """Generate budget tracking dashboard"""
        self.ensure_one()

        # For now, use executive dashboard logic as base
        # TODO: Implement budget tracking-specific metrics
        self.generate_executive_dashboard()

        # Update dashboard type
        dashboard_data = json.loads(self.dashboard_data or '{}')
        dashboard_data['dashboard_type'] = 'budget_tracking'
        self.dashboard_data = json.dumps(dashboard_data)
    
    def _generate_executive_summary(self, dashboard_data):
        """Generate executive summary"""
        metrics = dashboard_data['metrics']
        kpis = dashboard_data['kpis']
        
        summary = f"""
        <h3>Financial Strategy Executive Summary</h3>
        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4>📊 Key Financial Metrics</h4>
            <ul>
                <li><strong>Total Strategic Budget:</strong> UGX {metrics['total_budget']:.2f} Billion</li>
                <li><strong>GoU Funding:</strong> UGX {metrics['gou_funding']:.2f} Billion ({kpis.get('gou_percentage', 0):.1f}%)</li>
                <li><strong>Donor Funding:</strong> UGX {metrics['donor_funding']:.2f} Billion ({kpis.get('donor_percentage', 0):.1f}%)</li>
                <li><strong>Programme Count:</strong> {metrics['programme_count']} programmes</li>
            </ul>
        </div>
        
        <div style="background-color: #E8F5E8; padding: 15px; border-radius: 8px; margin: 10px 0;">
            <h4>🎯 Strategic Highlights</h4>
            <ul>
                <li>5-year strategic plan covering FY2025/26 to FY2029/30</li>
                <li>Balanced funding approach with government and donor support</li>
                <li>Focus on sustainable development and service delivery</li>
                <li>Integrated performance and financial management</li>
            </ul>
        </div>
        """
        
        self.executive_summary = summary
        
        # Generate alerts if any
        alerts = dashboard_data.get('alerts', [])
        if alerts:
            alert_html = "<h4>🚨 Key Alerts</h4><ul>"
            for alert in alerts:
                alert_html += f"<li><strong>{alert['type'].title()}:</strong> {alert['message']}</li>"
            alert_html += "</ul>"
            self.key_alerts = alert_html
    
    def _create_default_widgets(self):
        """Create default dashboard widgets"""
        # Clear existing widgets
        self.widget_ids.unlink()
        
        # Budget Overview Widget
        self.env['financial.dashboard.widget'].create({
            'dashboard_id': self.id,
            'name': 'Budget Overview',
            'widget_type': 'chart',
            'chart_type': 'pie',
            'position_x': 0,
            'position_y': 0,
            'width': 6,
            'height': 4,
            'data_source': 'budget_breakdown',
            'is_active': True,
        })
        
        # Funding Sources Widget
        self.env['financial.dashboard.widget'].create({
            'dashboard_id': self.id,
            'name': 'Funding Sources',
            'widget_type': 'chart',
            'chart_type': 'bar',
            'position_x': 6,
            'position_y': 0,
            'width': 6,
            'height': 4,
            'data_source': 'funding_sources',
            'is_active': True,
        })
        
        # Performance Metrics Widget
        self.env['financial.dashboard.widget'].create({
            'dashboard_id': self.id,
            'name': 'Performance Metrics',
            'widget_type': 'metric',
            'position_x': 0,
            'position_y': 4,
            'width': 4,
            'height': 3,
            'data_source': 'performance_metrics',
            'is_active': True,
        })
        
        # Budget Trend Widget
        self.env['financial.dashboard.widget'].create({
            'dashboard_id': self.id,
            'name': 'Budget Trend',
            'widget_type': 'chart',
            'chart_type': 'line',
            'position_x': 4,
            'position_y': 4,
            'width': 8,
            'height': 3,
            'data_source': 'budget_trend',
            'is_active': True,
        })
    
    def refresh_dashboard(self):
        """Refresh dashboard data"""
        self.ensure_one()

        if self.dashboard_type == 'executive':
            self.generate_executive_dashboard()
        elif self.dashboard_type == 'programme':
            self.generate_programme_dashboard()
        elif self.dashboard_type == 'operational':
            self.generate_operational_dashboard()
        elif self.dashboard_type == 'directorate':
            self.generate_directorate_dashboard()
        elif self.dashboard_type == 'budget_tracking':
            self.generate_budget_tracking_dashboard()
        else:
            # Fallback to executive dashboard for unknown types
            self.generate_executive_dashboard()
        
        self.last_refresh = datetime.now()
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Dashboard Refreshed',
                'message': f'Dashboard "{self.name}" has been refreshed successfully.',
                'type': 'success',
            }
        }


class FinancialDashboardWidget(models.Model):
    _name = 'financial.dashboard.widget'
    _description = 'Financial Dashboard Widget'
    _order = 'position_y, position_x'

    name = fields.Char(
        string='Widget Name',
        required=True,
        help="Name of the dashboard widget"
    )
    
    dashboard_id = fields.Many2one(
        'financial.dashboard',
        string='Dashboard',
        required=True,
        ondelete='cascade',
        help="Dashboard this widget belongs to"
    )
    
    widget_type = fields.Selection([
        ('chart', 'Chart'),
        ('metric', 'Metric'),
        ('table', 'Table'),
        ('gauge', 'Gauge'),
        ('text', 'Text'),
        ('alert', 'Alert'),
    ], string='Widget Type', required=True, default='chart')
    
    chart_type = fields.Selection([
        ('bar', 'Bar Chart'),
        ('line', 'Line Chart'),
        ('pie', 'Pie Chart'),
        ('doughnut', 'Doughnut Chart'),
        ('area', 'Area Chart'),
        ('scatter', 'Scatter Plot'),
    ], string='Chart Type', help="Type of chart (if widget_type is chart)")
    
    # Position and size
    position_x = fields.Integer(
        string='X Position',
        default=0,
        help="Horizontal position in grid"
    )
    
    position_y = fields.Integer(
        string='Y Position',
        default=0,
        help="Vertical position in grid"
    )
    
    width = fields.Integer(
        string='Width',
        default=4,
        help="Widget width in grid units"
    )
    
    height = fields.Integer(
        string='Height',
        default=3,
        help="Widget height in grid units"
    )
    
    # Data configuration
    data_source = fields.Selection([
        ('budget_breakdown', 'Budget Breakdown'),
        ('funding_sources', 'Funding Sources'),
        ('performance_metrics', 'Performance Metrics'),
        ('budget_trend', 'Budget Trend'),
        ('programme_performance', 'Programme Performance'),
        ('directorate_budget', 'Directorate Budget'),
        ('custom_query', 'Custom Query'),
    ], string='Data Source', required=True)
    
    widget_data = fields.Text(
        string='Widget Data (JSON)',
        help="Widget-specific data in JSON format"
    )
    
    # Display configuration
    title = fields.Char(
        string='Widget Title',
        help="Display title for the widget"
    )
    
    description = fields.Text(
        string='Widget Description',
        help="Description of what the widget shows"
    )
    
    color_scheme = fields.Selection([
        ('default', 'Default'),
        ('blue', 'Blue'),
        ('green', 'Green'),
        ('orange', 'Orange'),
        ('red', 'Red'),
        ('purple', 'Purple'),
    ], string='Color Scheme', default='default')
    
    # Status
    is_active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether widget is active and visible"
    )
    
    refresh_interval = fields.Integer(
        string='Refresh Interval (seconds)',
        default=300,
        help="How often to refresh widget data (in seconds)"
    )
