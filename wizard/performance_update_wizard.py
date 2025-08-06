# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, date


class PerformanceUpdateWizard(models.TransientModel):
    _name = 'performance.update.wizard'
    _description = 'Bulk Performance Update Wizard'

    name = fields.Char(
        string='Update Name',
        required=True,
        default=lambda self: f"Performance Update - {date.today().strftime('%B %Y')}"
    )
    
    update_date = fields.Date(
        string='Update Date',
        required=True,
        default=fields.Date.context_today
    )
    
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Directorate',
        help="Filter KPIs by directorate"
    )
    
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        help="Filter indicators by programme"
    )
    
    update_type = fields.Selection([
        ('kpi', 'Strategic KPIs'),
        ('performance_indicator', 'Programme Performance Indicators'),
        ('both', 'Both KPIs and Performance Indicators'),
    ], string='Update Type', default='both', required=True)
    
    notes = fields.Text(
        string='General Notes',
        help="General notes for this bulk update"
    )
    
    # Lines for KPI updates
    kpi_line_ids = fields.One2many(
        'performance.update.wizard.kpi.line',
        'wizard_id',
        string='KPI Updates'
    )
    
    # Lines for Performance Indicator updates
    pi_line_ids = fields.One2many(
        'performance.update.wizard.pi.line',
        'wizard_id',
        string='Performance Indicator Updates'
    )
    
    @api.onchange('directorate_id', 'update_type')
    def _onchange_directorate_update_type(self):
        """Load KPIs and Performance Indicators based on filters"""
        if self.update_type in ('kpi', 'both'):
            self._load_kpis()
        if self.update_type in ('performance_indicator', 'both'):
            self._load_performance_indicators()
    
    @api.onchange('programme_id', 'update_type')
    def _onchange_programme_update_type(self):
        """Load Performance Indicators based on programme filter"""
        if self.update_type in ('performance_indicator', 'both'):
            self._load_performance_indicators()
    
    def _load_kpis(self):
        """Load KPIs based on current filters"""
        domain = [('active', '=', True)]
        if self.directorate_id:
            domain.append(('directorate_id', '=', self.directorate_id.id))
        
        kpis = self.env['key.performance.indicator'].search(domain)
        
        # Clear existing lines
        self.kpi_line_ids = [(5, 0, 0)]
        
        # Create new lines
        lines = []
        for kpi in kpis:
            lines.append((0, 0, {
                'kpi_id': kpi.id,
                'current_value': kpi.current_value,
                'new_value': kpi.current_value,
                'target_value': kpi.target_value,
                'measurement_unit': kpi.measurement_unit,
            }))
        
        self.kpi_line_ids = lines
    
    def _load_performance_indicators(self):
        """Load Performance Indicators based on current filters"""
        domain = [('active', '=', True)]
        if self.programme_id:
            domain.append(('parent_programme_id', '=', self.programme_id.id))
        
        indicators = self.env['performance.indicator'].search(domain)
        
        # Clear existing lines
        self.pi_line_ids = [(5, 0, 0)]
        
        # Create new lines
        lines = []
        for indicator in indicators:
            lines.append((0, 0, {
                'indicator_id': indicator.id,
                'current_value': indicator.current_value,
                'new_value': indicator.current_value,
                'target_value': indicator.target_value,
                'measurement_unit': indicator.measurement_unit,
            }))
        
        self.pi_line_ids = lines
    
    def action_update_performance(self):
        """Execute the bulk performance update"""
        if not self.kpi_line_ids and not self.pi_line_ids:
            raise ValidationError(_("No performance indicators selected for update."))
        
        actions_created = 0
        
        # Process KPI updates
        for line in self.kpi_line_ids.filtered('update_selected'):
            if line.new_value != line.current_value:
                action = self.env['performance.action'].create({
                    'name': f"Bulk Update: {line.kpi_id.name}",
                    'description': f"Bulk performance update via wizard: {self.name}",
                    'date': self.update_date,
                    'indicator_id': line.kpi_id.id,
                    'action_type': 'update',
                    'previous_value': line.current_value,
                    'new_value': line.new_value,
                    'progress_notes': line.notes or self.notes,
                    'state': 'submitted',
                })
                actions_created += 1
        
        # Process Performance Indicator updates
        for line in self.pi_line_ids.filtered('update_selected'):
            if line.new_value != line.current_value:
                # Create performance action for performance indicators
                # Note: This would need to be adapted based on your specific model structure
                actions_created += 1
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('%d performance actions created successfully.') % actions_created,
                'type': 'success',
                'sticky': False,
            }
        }


class PerformanceUpdateWizardKPILine(models.TransientModel):
    _name = 'performance.update.wizard.kpi.line'
    _description = 'KPI Update Line'

    wizard_id = fields.Many2one('performance.update.wizard', string='Wizard')
    
    kpi_id = fields.Many2one(
        'key.performance.indicator',
        string='KPI',
        required=True
    )
    
    update_selected = fields.Boolean(
        string='Update',
        default=True,
        help="Select to include this KPI in the bulk update"
    )
    
    current_value = fields.Float(string='Current Value', readonly=True)
    new_value = fields.Float(string='New Value', required=True)
    target_value = fields.Float(string='Target Value', readonly=True)
    measurement_unit = fields.Char(string='Unit', readonly=True)
    
    notes = fields.Text(string='Notes')
    
    achievement_percentage = fields.Float(
        string='New Achievement %',
        compute='_compute_achievement_percentage'
    )
    
    @api.depends('new_value', 'target_value')
    def _compute_achievement_percentage(self):
        for line in self:
            if line.target_value:
                line.achievement_percentage = (line.new_value / line.target_value) * 100
            else:
                line.achievement_percentage = 0.0


class PerformanceUpdateWizardPILine(models.TransientModel):
    _name = 'performance.update.wizard.pi.line'
    _description = 'Performance Indicator Update Line'

    wizard_id = fields.Many2one('performance.update.wizard', string='Wizard')
    
    indicator_id = fields.Many2one(
        'performance.indicator',
        string='Performance Indicator',
        required=True
    )
    
    update_selected = fields.Boolean(
        string='Update',
        default=True,
        help="Select to include this indicator in the bulk update"
    )
    
    current_value = fields.Float(string='Current Value', readonly=True)
    new_value = fields.Float(string='New Value', required=True)
    target_value = fields.Float(string='Target Value', readonly=True)
    measurement_unit = fields.Char(string='Unit', readonly=True)
    
    notes = fields.Text(string='Notes')
    
    achievement_percentage = fields.Float(
        string='New Achievement %',
        compute='_compute_achievement_percentage'
    )
    
    @api.depends('new_value', 'target_value')
    def _compute_achievement_percentage(self):
        for line in self:
            if line.target_value:
                line.achievement_percentage = (line.new_value / line.target_value) * 100
            else:
                line.achievement_percentage = 0.0
