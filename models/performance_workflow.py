# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta, date


class PerformanceWorkflow(models.Model):
    _name = 'performance.workflow'
    _description = 'Performance Review Workflow'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Workflow Name',
        required=True,
        tracking=True,
        help="Name of the performance workflow"
    )
    
    workflow_type = fields.Selection([
        ('monthly_review', 'Monthly Performance Review'),
        ('quarterly_review', 'Quarterly Performance Review'),
        ('annual_review', 'Annual Performance Review'),
        ('ad_hoc_review', 'Ad-hoc Performance Review'),
        ('risk_escalation', 'Risk Escalation Workflow'),
    ], string='Workflow Type', required=True, default='monthly_review', tracking=True)
    
    # Scope and targets
    scope = fields.Selection([
        ('organization', 'Organization-wide'),
        ('directorate', 'Directorate-specific'),
        ('programme', 'Programme-specific'),
        ('kpi', 'KPI-specific'),
    ], string='Review Scope', required=True, default='organization')
    
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Target Directorate',
        help="Directorate for review (if scope is directorate-specific)"
    )
    
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Target Programme',
        help="Programme for review (if scope is programme-specific)"
    )
    
    kpi_id = fields.Many2one(
        'key.performance.indicator',
        string='Target KPI',
        help="KPI for review (if scope is KPI-specific)"
    )
    
    # Workflow timing
    review_period_start = fields.Date(
        string='Review Period Start',
        required=True,
        help="Start date of the review period"
    )
    
    review_period_end = fields.Date(
        string='Review Period End',
        required=True,
        help="End date of the review period"
    )
    
    due_date = fields.Date(
        string='Review Due Date',
        required=True,
        help="Date when review should be completed"
    )
    
    # Workflow participants
    initiator_id = fields.Many2one(
        'res.users',
        string='Workflow Initiator',
        default=lambda self: self.env.user,
        required=True,
        tracking=True
    )
    
    reviewer_ids = fields.Many2many(
        'res.users',
        'workflow_reviewer_rel',
        'workflow_id',
        'user_id',
        string='Reviewers',
        help="Users responsible for conducting the review"
    )
    
    approver_ids = fields.Many2many(
        'res.users',
        'workflow_approver_rel',
        'workflow_id',
        'user_id',
        string='Approvers',
        help="Users responsible for approving the review"
    )
    
    # Workflow status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('initiated', 'Initiated'),
        ('in_review', 'In Review'),
        ('pending_approval', 'Pending Approval'),
        ('approved', 'Approved'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    
    # Review results
    review_summary = fields.Html(
        string='Review Summary',
        help="Summary of the performance review"
    )
    
    key_findings = fields.Html(
        string='Key Findings',
        help="Key findings from the review"
    )
    
    action_items = fields.Html(
        string='Action Items',
        help="Action items identified during the review"
    )
    
    overall_rating = fields.Selection([
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('satisfactory', 'Satisfactory'),
        ('needs_improvement', 'Needs Improvement'),
        ('unsatisfactory', 'Unsatisfactory'),
    ], string='Overall Rating', help="Overall performance rating")
    
    # Workflow steps
    step_ids = fields.One2many(
        'performance.workflow.step',
        'workflow_id',
        string='Workflow Steps',
        help="Steps in the workflow"
    )
    
    # Computed fields
    progress = fields.Float(
        string='Progress (%)',
        compute='_compute_progress',
        store=True,
        help="Workflow completion progress"
    )
    
    is_overdue = fields.Boolean(
        string='Is Overdue',
        compute='_compute_overdue',
        store=True,
        help="Whether the workflow is overdue"
    )
    
    @api.depends('step_ids.state')
    def _compute_progress(self):
        for record in self:
            if record.step_ids:
                completed_steps = len(record.step_ids.filtered(lambda s: s.state == 'completed'))
                total_steps = len(record.step_ids)
                record.progress = (completed_steps / total_steps) * 100 if total_steps > 0 else 0
            else:
                record.progress = 0
    
    @api.depends('due_date', 'state')
    def _compute_overdue(self):
        today = date.today()
        for record in self:
            record.is_overdue = (record.due_date < today and record.state not in ['completed', 'cancelled'])
    
    @api.model_create_multi
    def create(self, vals_list):
        """Override create to auto-generate workflow steps"""
        workflows = super().create(vals_list)
        for workflow in workflows:
            workflow._generate_workflow_steps()
        return workflows
    
    def _generate_workflow_steps(self):
        """Generate workflow steps based on workflow type"""
        steps_data = self._get_workflow_steps_template()
        
        sequence = 10
        for step_data in steps_data:
            step_data.update({
                'workflow_id': self.id,
                'sequence': sequence,
            })
            self.env['performance.workflow.step'].create(step_data)
            sequence += 10
    
    def _get_workflow_steps_template(self):
        """Get workflow steps template based on workflow type"""
        if self.workflow_type == 'monthly_review':
            return [
                {
                    'name': 'Data Collection',
                    'description': 'Collect performance data for the review period',
                    'step_type': 'data_collection',
                    'estimated_duration': 2,  # days
                },
                {
                    'name': 'Performance Analysis',
                    'description': 'Analyze collected performance data',
                    'step_type': 'analysis',
                    'estimated_duration': 3,
                },
                {
                    'name': 'Review Meeting',
                    'description': 'Conduct performance review meeting',
                    'step_type': 'meeting',
                    'estimated_duration': 1,
                },
                {
                    'name': 'Action Planning',
                    'description': 'Develop action plans based on review findings',
                    'step_type': 'planning',
                    'estimated_duration': 2,
                },
                {
                    'name': 'Approval',
                    'description': 'Get approval for review results and action plans',
                    'step_type': 'approval',
                    'estimated_duration': 1,
                },
            ]
        elif self.workflow_type == 'quarterly_review':
            return [
                {
                    'name': 'Quarterly Data Compilation',
                    'description': 'Compile quarterly performance data',
                    'step_type': 'data_collection',
                    'estimated_duration': 3,
                },
                {
                    'name': 'Trend Analysis',
                    'description': 'Analyze performance trends over the quarter',
                    'step_type': 'analysis',
                    'estimated_duration': 5,
                },
                {
                    'name': 'Stakeholder Consultation',
                    'description': 'Consult with key stakeholders',
                    'step_type': 'consultation',
                    'estimated_duration': 3,
                },
                {
                    'name': 'Report Preparation',
                    'description': 'Prepare quarterly performance report',
                    'step_type': 'reporting',
                    'estimated_duration': 4,
                },
                {
                    'name': 'Executive Review',
                    'description': 'Executive review and approval',
                    'step_type': 'approval',
                    'estimated_duration': 2,
                },
            ]
        elif self.workflow_type == 'risk_escalation':
            return [
                {
                    'name': 'Risk Assessment',
                    'description': 'Assess the identified performance risk',
                    'step_type': 'assessment',
                    'estimated_duration': 1,
                },
                {
                    'name': 'Impact Analysis',
                    'description': 'Analyze potential impact of the risk',
                    'step_type': 'analysis',
                    'estimated_duration': 1,
                },
                {
                    'name': 'Mitigation Planning',
                    'description': 'Develop risk mitigation plan',
                    'step_type': 'planning',
                    'estimated_duration': 2,
                },
                {
                    'name': 'Implementation',
                    'description': 'Implement mitigation measures',
                    'step_type': 'implementation',
                    'estimated_duration': 5,
                },
                {
                    'name': 'Monitoring',
                    'description': 'Monitor effectiveness of mitigation measures',
                    'step_type': 'monitoring',
                    'estimated_duration': 7,
                },
            ]
        else:
            return []
    
    def action_initiate(self):
        """Initiate the workflow"""
        self.write({'state': 'initiated'})
        
        # Start the first step
        first_step = self.step_ids.sorted('sequence')[0] if self.step_ids else False
        if first_step:
            first_step.action_start()
        
        # Send notifications to reviewers
        self._send_workflow_notification('initiated')
    
    def action_complete(self):
        """Complete the workflow"""
        # Check if all steps are completed
        incomplete_steps = self.step_ids.filtered(lambda s: s.state != 'completed')
        if incomplete_steps:
            raise ValidationError(_("Cannot complete workflow. The following steps are not completed: %s") % 
                                ', '.join(incomplete_steps.mapped('name')))
        
        self.write({'state': 'completed'})
        self._send_workflow_notification('completed')
    
    def action_cancel(self):
        """Cancel the workflow"""
        self.write({'state': 'cancelled'})
        # Cancel all pending steps
        self.step_ids.filtered(lambda s: s.state in ['pending', 'in_progress']).write({'state': 'cancelled'})
    
    def _send_workflow_notification(self, event_type):
        """Send workflow notifications"""
        if event_type == 'initiated':
            subject = f"Performance Review Workflow Initiated: {self.name}"
            body = f"""
            <p>A new performance review workflow has been initiated:</p>
            <ul>
                <li><strong>Workflow:</strong> {self.name}</li>
                <li><strong>Type:</strong> {dict(self._fields['workflow_type'].selection)[self.workflow_type]}</li>
                <li><strong>Review Period:</strong> {self.review_period_start} to {self.review_period_end}</li>
                <li><strong>Due Date:</strong> {self.due_date}</li>
            </ul>
            <p>Please complete your assigned steps on time.</p>
            """
            recipients = self.reviewer_ids | self.approver_ids
        elif event_type == 'completed':
            subject = f"Performance Review Workflow Completed: {self.name}"
            body = f"""
            <p>The performance review workflow has been completed:</p>
            <ul>
                <li><strong>Workflow:</strong> {self.name}</li>
                <li><strong>Overall Rating:</strong> {dict(self._fields['overall_rating'].selection)[self.overall_rating] if self.overall_rating else 'Not Rated'}</li>
                <li><strong>Completion Date:</strong> {date.today()}</li>
            </ul>
            """
            recipients = self.reviewer_ids | self.approver_ids | self.env['res.users'].browse([self.initiator_id.id])
        else:
            return
        
        # Send email notifications
        for user in recipients:
            self.message_post(
                subject=subject,
                body=body,
                partner_ids=[user.partner_id.id],
                message_type='email'
            )
    
    @api.model
    def cron_check_overdue_workflows(self):
        """Check for overdue workflows and send alerts"""
        overdue_workflows = self.search([
            ('due_date', '<', date.today()),
            ('state', 'not in', ['completed', 'cancelled'])
        ])
        
        for workflow in overdue_workflows:
            workflow._send_overdue_alert()
        
        return True
    
    def _send_overdue_alert(self):
        """Send overdue workflow alert"""
        subject = f"OVERDUE: Performance Review Workflow - {self.name}"
        body = f"""
        <p><strong>ALERT:</strong> The following performance review workflow is overdue:</p>
        <ul>
            <li><strong>Workflow:</strong> {self.name}</li>
            <li><strong>Due Date:</strong> {self.due_date}</li>
            <li><strong>Days Overdue:</strong> {(date.today() - self.due_date).days}</li>
            <li><strong>Current Status:</strong> {dict(self._fields['state'].selection)[self.state]}</li>
        </ul>
        <p>Please take immediate action to complete this workflow.</p>
        """
        
        # Send to reviewers, approvers, and initiator
        recipients = self.reviewer_ids | self.approver_ids | self.env['res.users'].browse([self.initiator_id.id])
        
        for user in recipients:
            self.message_post(
                subject=subject,
                body=body,
                partner_ids=[user.partner_id.id],
                message_type='email'
            )


class PerformanceWorkflowStep(models.Model):
    _name = 'performance.workflow.step'
    _description = 'Performance Workflow Step'
    _order = 'workflow_id, sequence'

    name = fields.Char(
        string='Step Name',
        required=True,
        help="Name of the workflow step"
    )
    
    description = fields.Text(
        string='Description',
        help="Description of what needs to be done in this step"
    )
    
    workflow_id = fields.Many2one(
        'performance.workflow',
        string='Workflow',
        required=True,
        ondelete='cascade'
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Order of execution"
    )
    
    step_type = fields.Selection([
        ('data_collection', 'Data Collection'),
        ('analysis', 'Analysis'),
        ('meeting', 'Meeting'),
        ('consultation', 'Consultation'),
        ('planning', 'Planning'),
        ('reporting', 'Reporting'),
        ('approval', 'Approval'),
        ('assessment', 'Assessment'),
        ('implementation', 'Implementation'),
        ('monitoring', 'Monitoring'),
    ], string='Step Type', required=True)
    
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending')
    
    assigned_user_id = fields.Many2one(
        'res.users',
        string='Assigned To',
        help="User assigned to complete this step"
    )
    
    estimated_duration = fields.Integer(
        string='Estimated Duration (Days)',
        help="Estimated number of days to complete this step"
    )
    
    start_date = fields.Date(
        string='Start Date',
        help="Date when step was started"
    )
    
    completion_date = fields.Date(
        string='Completion Date',
        help="Date when step was completed"
    )
    
    notes = fields.Text(
        string='Notes',
        help="Notes about the step completion"
    )
    
    def action_start(self):
        """Start the workflow step"""
        self.write({
            'state': 'in_progress',
            'start_date': date.today(),
        })
    
    def action_complete(self):
        """Complete the workflow step"""
        self.write({
            'state': 'completed',
            'completion_date': date.today(),
        })
        
        # Check if this was the last step and auto-advance workflow
        workflow = self.workflow_id
        remaining_steps = workflow.step_ids.filtered(lambda s: s.state != 'completed')
        
        if not remaining_steps:
            # All steps completed, advance workflow
            if workflow.state == 'in_review':
                workflow.write({'state': 'pending_approval'})
        else:
            # Start next step if it's pending
            next_step = remaining_steps.sorted('sequence')[0]
            if next_step.state == 'pending':
                next_step.action_start()
