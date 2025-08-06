# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date
import json


class PerformanceAlert(models.Model):
    _name = 'performance.alert'
    _description = 'Performance Alert System'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Alert Title',
        required=True,
        tracking=True,
        help="Title of the performance alert"
    )
    
    alert_type = fields.Selection([
        ('performance_decline', 'Performance Decline'),
        ('target_missed', 'Target Missed'),
        ('deadline_approaching', 'Deadline Approaching'),
        ('risk_escalation', 'Risk Escalation'),
        ('anomaly_detected', 'Anomaly Detected'),
        ('milestone_achieved', 'Milestone Achieved'),
        ('system_notification', 'System Notification'),
    ], string='Alert Type', required=True, tracking=True)
    
    severity = fields.Selection([
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('critical', 'Critical'),
        ('urgent', 'Urgent'),
    ], string='Severity', required=True, default='info', tracking=True)
    
    # Related records
    kpi_id = fields.Many2one(
        'key.performance.indicator',
        string='Related KPI',
        help="KPI that triggered the alert"
    )
    
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Related Programme',
        help="Programme that triggered the alert"
    )
    
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Related Directorate',
        help="Directorate that triggered the alert"
    )
    
    workflow_id = fields.Many2one(
        'performance.workflow',
        string='Related Workflow',
        help="Workflow that triggered the alert"
    )
    
    # Alert details
    description = fields.Html(
        string='Description',
        required=True,
        help="Detailed description of the alert"
    )
    
    recommended_actions = fields.Html(
        string='Recommended Actions',
        help="Recommended actions to address the alert"
    )
    
    # Alert status
    state = fields.Selection([
        ('new', 'New'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
    ], string='Status', default='new', tracking=True)
    
    # Assignment and handling
    assigned_user_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        help="User assigned to handle this alert"
    )
    
    acknowledged_by_id = fields.Many2one(
        'res.users',
        string='Acknowledged By',
        help="User who acknowledged the alert"
    )
    
    acknowledged_date = fields.Datetime(
        string='Acknowledged Date',
        help="Date when alert was acknowledged"
    )
    
    resolved_by_id = fields.Many2one(
        'res.users',
        string='Resolved By',
        help="User who resolved the alert"
    )
    
    resolved_date = fields.Datetime(
        string='Resolved Date',
        help="Date when alert was resolved"
    )
    
    resolution_notes = fields.Text(
        string='Resolution Notes',
        help="Notes about how the alert was resolved"
    )
    
    # Alert data
    alert_data = fields.Text(
        string='Alert Data',
        help="JSON data related to the alert"
    )
    
    # Notification settings
    notification_sent = fields.Boolean(
        string='Notification Sent',
        default=False,
        help="Whether notification has been sent"
    )
    
    auto_escalate = fields.Boolean(
        string='Auto Escalate',
        default=True,
        help="Whether to auto-escalate if not handled within time limit"
    )
    
    escalation_hours = fields.Integer(
        string='Escalation Hours',
        default=24,
        help="Hours after which to escalate if not handled"
    )
    
    # Computed fields
    is_overdue = fields.Boolean(
        string='Is Overdue',
        compute='_compute_overdue',
        store=True,
        help="Whether the alert is overdue for handling"
    )
    
    age_hours = fields.Float(
        string='Age (Hours)',
        compute='_compute_age',
        help="Age of the alert in hours"
    )
    
    @api.depends('create_date')
    def _compute_age(self):
        now = datetime.now()
        for record in self:
            if record.create_date:
                age = now - record.create_date
                record.age_hours = age.total_seconds() / 3600
            else:
                record.age_hours = 0
    
    @api.depends('create_date', 'escalation_hours', 'state')
    def _compute_overdue(self):
        now = datetime.now()
        for record in self:
            if record.state in ['new', 'acknowledged'] and record.create_date:
                escalation_time = record.create_date + timedelta(hours=record.escalation_hours)
                record.is_overdue = now > escalation_time
            else:
                record.is_overdue = False
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to send notifications"""
        alerts = super().create(vals_list)
        for alert in alerts:
            alert._send_alert_notification()
        return alerts
    
    def _send_alert_notification(self):
        """Send alert notification to relevant users"""
        if self.notification_sent:
            return
        
        # Determine recipients based on alert context
        recipients = self._get_alert_recipients()
        
        if not recipients:
            return
        
        # Prepare notification content
        subject = f"[{self.severity.upper()}] {self.name}"
        
        body = f"""
        <div style="font-family: Arial, sans-serif;">
            <h3 style="color: {self._get_severity_color()};">{self.name}</h3>
            
            <table style="border-collapse: collapse; width: 100%;">
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>Alert Type:</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{dict(self._fields['alert_type'].selection)[self.alert_type]}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>Severity:</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{self.severity.upper()}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd; background-color: #f9f9f9;"><strong>Date:</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{self.create_date.strftime('%Y-%m-%d %H:%M:%S')}</td>
                </tr>
            </table>
            
            <h4>Description:</h4>
            <div style="background-color: #f8f9fa; padding: 10px; border-left: 4px solid {self._get_severity_color()};">
                {self.description}
            </div>
            
            {f'<h4>Recommended Actions:</h4><div>{self.recommended_actions}</div>' if self.recommended_actions else ''}
            
            <p style="margin-top: 20px;">
                <strong>Please acknowledge this alert and take appropriate action.</strong>
            </p>
        </div>
        """
        
        # Send notifications
        for user in recipients:
            self.message_post(
                subject=subject,
                body=body,
                partner_ids=[user.partner_id.id],
                message_type='email'
            )
        
        # Create activities for critical/urgent alerts
        if self.severity in ['critical', 'urgent']:
            for user in recipients:
                self.activity_schedule(
                    'mail.mail_activity_data_todo',
                    user_id=user.id,
                    summary=f"Handle {self.severity} alert: {self.name}",
                    note=self.description,
                    date_deadline=date.today() + timedelta(days=1)
                )
        
        self.notification_sent = True
    
    def _get_alert_recipients(self):
        """Get list of users who should receive this alert"""
        recipients = self.env['res.users']
        
        # Add assigned user if any
        if self.assigned_user_id:
            recipients |= self.assigned_user_id
        
        # Add directorate leadership if directorate-related
        if self.directorate_id:
            if self.directorate_id.director_id:
                recipients |= self.directorate_id.director_id
            if self.directorate_id.deputy_director_id:
                recipients |= self.directorate_id.deputy_director_id
        
        # Add programme manager if programme-related
        if self.programme_id and self.programme_id.programme_manager_id:
            recipients |= self.programme_id.programme_manager_id
        
        # Add KPI responsible person if KPI-related
        if self.kpi_id and self.kpi_id.responsible_user_id:
            recipients |= self.kpi_id.responsible_user_id
        
        # Add workflow participants if workflow-related
        if self.workflow_id:
            recipients |= self.workflow_id.reviewer_ids
            recipients |= self.workflow_id.approver_ids
        
        # For critical/urgent alerts, also notify PMIS admins
        if self.severity in ['critical', 'urgent']:
            admin_group = self.env.ref('robust_pmis.group_kcca_pmis_admin', raise_if_not_found=False)
            if admin_group:
                recipients |= admin_group.users
        
        return recipients
    
    def _get_severity_color(self):
        """Get color code for severity level"""
        colors = {
            'info': '#17a2b8',
            'warning': '#ffc107',
            'critical': '#dc3545',
            'urgent': '#6f42c1',
        }
        return colors.get(self.severity, '#6c757d')
    
    def action_acknowledge(self):
        """Acknowledge the alert"""
        self.write({
            'state': 'acknowledged',
            'acknowledged_by_id': self.env.user.id,
            'acknowledged_date': fields.Datetime.now(),
        })
    
    def action_assign(self):
        """Open wizard to assign alert to user"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Assign Alert',
            'res_model': 'performance.alert.assign.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_alert_id': self.id}
        }
    
    def action_resolve(self):
        """Mark alert as resolved"""
        self.write({
            'state': 'resolved',
            'resolved_by_id': self.env.user.id,
            'resolved_date': fields.Datetime.now(),
        })
    
    def action_dismiss(self):
        """Dismiss the alert"""
        self.write({'state': 'dismissed'})
    
    @api.model
    def cron_check_performance_alerts(self):
        """Cron job to check for performance issues and create alerts"""
        # Check for KPIs with declining performance
        self._check_kpi_performance_decline()
        
        # Check for missed targets
        self._check_missed_targets()
        
        # Check for approaching deadlines
        self._check_approaching_deadlines()
        
        # Check for overdue alerts that need escalation
        self._check_alert_escalation()
        
        return True
    
    def _check_kpi_performance_decline(self):
        """Check for KPIs with declining performance"""
        # Get KPIs that have shown decline in last 30 days
        thirty_days_ago = date.today() - timedelta(days=30)
        
        kpis = self.env['key.performance.indicator'].search([
            ('active', '=', True),
            ('status', 'in', ['behind', 'at_risk'])
        ])
        
        for kpi in kpis:
            # Check if alert already exists for this KPI in last 7 days
            existing_alert = self.search([
                ('kpi_id', '=', kpi.id),
                ('alert_type', '=', 'performance_decline'),
                ('create_date', '>=', datetime.now() - timedelta(days=7))
            ], limit=1)
            
            if not existing_alert:
                # Create performance decline alert
                self.create({
                    'name': f'Performance Decline: {kpi.name}',
                    'alert_type': 'performance_decline',
                    'severity': 'critical' if kpi.status == 'behind' else 'warning',
                    'kpi_id': kpi.id,
                    'directorate_id': kpi.directorate_id.id if kpi.directorate_id else False,
                    'description': f"""
                    <p>KPI <strong>{kpi.name}</strong> is showing declining performance:</p>
                    <ul>
                        <li><strong>Current Status:</strong> {dict(kpi._fields['status'].selection)[kpi.status]}</li>
                        <li><strong>Current Value:</strong> {kpi.current_value} {kpi.measurement_unit}</li>
                        <li><strong>Target Value:</strong> {kpi.target_value} {kpi.measurement_unit}</li>
                        <li><strong>Achievement:</strong> {kpi.achievement_percentage:.1f}%</li>
                    </ul>
                    """,
                    'recommended_actions': """
                    <ul>
                        <li>Review current strategies and interventions</li>
                        <li>Identify root causes of performance decline</li>
                        <li>Develop corrective action plan</li>
                        <li>Increase monitoring frequency</li>
                        <li>Consider resource reallocation</li>
                    </ul>
                    """,
                    'assigned_user_id': kpi.responsible_user_id.id if kpi.responsible_user_id else False,
                })
    
    def _check_missed_targets(self):
        """Check for missed targets"""
        # Implementation for checking missed targets
        pass
    
    def _check_approaching_deadlines(self):
        """Check for approaching deadlines"""
        # Check for KPIs with end dates approaching
        seven_days_from_now = date.today() + timedelta(days=7)
        
        kpis_approaching_deadline = self.env['key.performance.indicator'].search([
            ('active', '=', True),
            ('end_date', '<=', seven_days_from_now),
            ('end_date', '>=', date.today()),
            ('status', '!=', 'achieved')
        ])
        
        for kpi in kpis_approaching_deadline:
            # Check if alert already exists
            existing_alert = self.search([
                ('kpi_id', '=', kpi.id),
                ('alert_type', '=', 'deadline_approaching'),
                ('create_date', '>=', datetime.now() - timedelta(days=3))
            ], limit=1)
            
            if not existing_alert:
                days_remaining = (kpi.end_date - date.today()).days
                self.create({
                    'name': f'Deadline Approaching: {kpi.name}',
                    'alert_type': 'deadline_approaching',
                    'severity': 'urgent' if days_remaining <= 3 else 'warning',
                    'kpi_id': kpi.id,
                    'directorate_id': kpi.directorate_id.id if kpi.directorate_id else False,
                    'description': f"""
                    <p>KPI <strong>{kpi.name}</strong> deadline is approaching:</p>
                    <ul>
                        <li><strong>End Date:</strong> {kpi.end_date}</li>
                        <li><strong>Days Remaining:</strong> {days_remaining}</li>
                        <li><strong>Current Achievement:</strong> {kpi.achievement_percentage:.1f}%</li>
                        <li><strong>Status:</strong> {dict(kpi._fields['status'].selection)[kpi.status]}</li>
                    </ul>
                    """,
                    'recommended_actions': """
                    <ul>
                        <li>Accelerate current activities</li>
                        <li>Review and adjust targets if necessary</li>
                        <li>Allocate additional resources</li>
                        <li>Prepare contingency plans</li>
                    </ul>
                    """,
                    'assigned_user_id': kpi.responsible_user_id.id if kpi.responsible_user_id else False,
                })
    
    def _check_alert_escalation(self):
        """Check for alerts that need escalation"""
        overdue_alerts = self.search([
            ('state', 'in', ['new', 'acknowledged']),
            ('auto_escalate', '=', True),
            ('is_overdue', '=', True)
        ])
        
        for alert in overdue_alerts:
            alert._escalate_alert()
    
    def _escalate_alert(self):
        """Escalate overdue alert"""
        # Create escalation alert
        escalation_alert = self.create({
            'name': f'ESCALATED: {self.name}',
            'alert_type': 'risk_escalation',
            'severity': 'urgent',
            'kpi_id': self.kpi_id.id if self.kpi_id else False,
            'programme_id': self.programme_id.id if self.programme_id else False,
            'directorate_id': self.directorate_id.id if self.directorate_id else False,
            'description': f"""
            <p><strong>ESCALATED ALERT:</strong> The following alert has not been handled within the specified time limit:</p>
            <div style="background-color: #fff3cd; padding: 10px; border: 1px solid #ffeaa7;">
                <h4>Original Alert: {self.name}</h4>
                <p><strong>Created:</strong> {self.create_date.strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p><strong>Age:</strong> {self.age_hours:.1f} hours</p>
                <p><strong>Current Status:</strong> {dict(self._fields['state'].selection)[self.state]}</p>
            </div>
            <p>Original Description:</p>
            {self.description}
            """,
            'recommended_actions': """
            <ul>
                <li><strong>IMMEDIATE ACTION REQUIRED</strong></li>
                <li>Review and handle the original alert immediately</li>
                <li>Investigate why the alert was not handled on time</li>
                <li>Implement process improvements to prevent future escalations</li>
            </ul>
            """,
            'auto_escalate': False,  # Don't auto-escalate escalation alerts
        })
        
        # Update original alert
        self.write({
            'state': 'in_progress',
            'assigned_user_id': self.env.user.id,
        })


class PerformanceAlertAssignWizard(models.TransientModel):
    _name = 'performance.alert.assign.wizard'
    _description = 'Assign Performance Alert Wizard'

    alert_id = fields.Many2one(
        'performance.alert',
        string='Alert',
        required=True
    )
    
    assigned_user_id = fields.Many2one(
        'res.users',
        string='Assign To',
        required=True,
        help="User to assign the alert to"
    )
    
    notes = fields.Text(
        string='Assignment Notes',
        help="Notes about the assignment"
    )
    
    def action_assign(self):
        """Assign the alert to selected user"""
        self.alert_id.write({
            'assigned_user_id': self.assigned_user_id.id,
            'state': 'in_progress',
        })
        
        # Send notification to assigned user
        if self.assigned_user_id:
            self.alert_id.message_post(
                subject=f"Alert Assigned: {self.alert_id.name}",
                body=f"""
                <p>You have been assigned to handle the following alert:</p>
                <p><strong>{self.alert_id.name}</strong></p>
                {f'<p><strong>Assignment Notes:</strong> {self.notes}</p>' if self.notes else ''}
                <p>Please review and take appropriate action.</p>
                """,
                partner_ids=[self.assigned_user_id.partner_id.id],
                message_type='email'
            )
        
        return {'type': 'ir.actions.act_window_close'}
