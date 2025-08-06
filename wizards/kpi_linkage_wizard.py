# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class KPILinkageWizard(models.TransientModel):
    _name = 'kpi.linkage.wizard'
    _description = 'KPI Linkage Setup Wizard'

    # Wizard Steps
    step = fields.Selection([
        ('select_strategic_kpi', 'Select Strategic KPI'),
        ('select_programme_indicators', 'Select Programme Indicators'),
        ('configure_weights', 'Configure Contribution Weights'),
        ('setup_cascade', 'Setup Target Cascade'),
        ('review_confirm', 'Review & Confirm')
    ], string='Step', default='select_strategic_kpi', required=True)

    # Strategic KPI Selection
    strategic_kpi_id = fields.Many2one(
        'key.performance.indicator',
        string='Strategic KPI',
        required=True,
        help="Strategic KPI to link with programme indicators"
    )
    
    strategic_kpi_thematic_area = fields.Selection(
        related='strategic_kpi_id.thematic_area',
        string='Thematic Area'
    )

    # Programme Indicator Selection
    programme_indicator_ids = fields.Many2many(
        'performance.indicator',
        'wizard_programme_indicator_rel',
        'wizard_id',
        'indicator_id',
        string='Programme Indicators',
        help="Programme indicators that contribute to the strategic KPI"
    )

    # Linkage Configuration
    linkage_line_ids = fields.One2many(
        'kpi.linkage.wizard.line',
        'wizard_id',
        string='Linkage Configuration'
    )

    # Calculation Method
    calculation_method = fields.Selection([
        ('weighted_average', 'Weighted Average'),
        ('sum', 'Sum of Values'),
        ('percentage_complete', 'Percentage of Targets Met'),
        ('milestone_count', 'Count of Milestones Achieved')
    ], string='Calculation Method', default='weighted_average')

    # Target Cascade Settings
    enable_target_cascade = fields.Boolean(
        string='Enable Target Cascade',
        default=True,
        help="Cascade strategic KPI targets to programme indicators"
    )

    total_allocation_percentage = fields.Float(
        string='Total Allocation %',
        compute='_compute_total_allocation',
        help="Total percentage allocated to programme indicators"
    )

    @api.depends('linkage_line_ids.target_allocation_percentage')
    def _compute_total_allocation(self):
        for wizard in self:
            wizard.total_allocation_percentage = sum(
                wizard.linkage_line_ids.mapped('target_allocation_percentage')
            )

    @api.onchange('strategic_kpi_id')
    def _onchange_strategic_kpi_id(self):
        """Filter programme indicators by thematic area"""
        if self.strategic_kpi_id and self.strategic_kpi_id.thematic_area:
            domain = [('thematic_area', '=', self.strategic_kpi_id.thematic_area)]
            return {'domain': {'programme_indicator_ids': domain}}
        return {'domain': {'programme_indicator_ids': []}}

    @api.onchange('programme_indicator_ids')
    def _onchange_programme_indicator_ids(self):
        """Create linkage lines for selected indicators"""
        if self.programme_indicator_ids:
            lines = []
            for indicator in self.programme_indicator_ids:
                lines.append((0, 0, {
                    'programme_indicator_id': indicator.id,
                    'contribution_weight': 0.0,
                    'target_allocation_percentage': 0.0,
                    'impact_relationship': 'direct'
                }))
            self.linkage_line_ids = lines

    def action_next_step(self):
        """Move to next step in wizard"""
        steps = ['select_strategic_kpi', 'select_programme_indicators', 
                'configure_weights', 'setup_cascade', 'review_confirm']
        current_index = steps.index(self.step)
        
        # Validation for each step
        if self.step == 'select_strategic_kpi' and not self.strategic_kpi_id:
            raise UserError(_("Please select a Strategic KPI"))
        
        if self.step == 'select_programme_indicators' and not self.programme_indicator_ids:
            raise UserError(_("Please select at least one Programme Indicator"))
        
        if self.step == 'configure_weights':
            total_weight = sum(self.linkage_line_ids.mapped('contribution_weight'))
            if total_weight != 100.0:
                raise UserError(_("Total contribution weights must equal 100%%. Current total: %.1f%%") % total_weight)
        
        if self.step == 'setup_cascade' and self.enable_target_cascade:
            if abs(self.total_allocation_percentage - 100.0) > 0.1:
                raise UserError(_("Total target allocation must equal 100%%. Current total: %.1f%%") % self.total_allocation_percentage)

        if current_index < len(steps) - 1:
            self.step = steps[current_index + 1]
        
        return self._return_wizard_action()

    def action_previous_step(self):
        """Move to previous step in wizard"""
        steps = ['select_strategic_kpi', 'select_programme_indicators', 
                'configure_weights', 'setup_cascade', 'review_confirm']
        current_index = steps.index(self.step)
        
        if current_index > 0:
            self.step = steps[current_index - 1]
        
        return self._return_wizard_action()

    def action_auto_distribute_weights(self):
        """Automatically distribute weights equally among indicators"""
        if self.linkage_line_ids:
            weight_per_indicator = 100.0 / len(self.linkage_line_ids)
            for line in self.linkage_line_ids:
                line.contribution_weight = weight_per_indicator

    def action_auto_distribute_targets(self):
        """Automatically distribute target allocation equally"""
        if self.linkage_line_ids:
            allocation_per_indicator = 100.0 / len(self.linkage_line_ids)
            for line in self.linkage_line_ids:
                line.target_allocation_percentage = allocation_per_indicator

    def action_confirm_linkage(self):
        """Create the KPI linkages"""
        if not self.strategic_kpi_id or not self.linkage_line_ids:
            raise UserError(_("Please complete all required fields"))

        # Update Strategic KPI
        self.strategic_kpi_id.write({
            'contributing_programme_indicators': [(6, 0, self.programme_indicator_ids.ids)],
            'auto_calculate': True,
            'calculation_method': self.calculation_method
        })

        # Update Programme Indicators
        for line in self.linkage_line_ids:
            indicator = line.programme_indicator_id
            indicator.write({
                'strategic_kpi_ids': [(4, self.strategic_kpi_id.id)],
                'contribution_weight': line.contribution_weight,
                'impact_relationship': line.impact_relationship,
                'parent_strategic_kpi_id': self.strategic_kpi_id.id if self.enable_target_cascade else False,
                'target_allocation_percentage': line.target_allocation_percentage if self.enable_target_cascade else 0.0
            })

        # Calculate initial strategic KPI value
        self.strategic_kpi_id._calculate_from_programme_indicators()

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('KPI linkage created successfully for %s') % self.strategic_kpi_id.name,
                'type': 'success',
                'sticky': False,
            }
        }

    def _return_wizard_action(self):
        """Return action to keep wizard open"""
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'kpi.linkage.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
            'context': self.env.context
        }


class KPILinkageWizardLine(models.TransientModel):
    _name = 'kpi.linkage.wizard.line'
    _description = 'KPI Linkage Wizard Line'

    wizard_id = fields.Many2one('kpi.linkage.wizard', string='Wizard', required=True, ondelete='cascade')
    
    programme_indicator_id = fields.Many2one(
        'performance.indicator',
        string='Programme Indicator',
        required=True
    )
    
    programme_name = fields.Char(
        related='programme_indicator_id.programme_id.name',
        string='Programme'
    )
    
    current_value = fields.Float(
        related='programme_indicator_id.current_value',
        string='Current Value'
    )
    
    target_value = fields.Float(
        related='programme_indicator_id.target_value',
        string='Target Value'
    )
    
    achievement_percentage = fields.Float(
        related='programme_indicator_id.achievement_percentage',
        string='Achievement %'
    )
    
    contribution_weight = fields.Float(
        string='Contribution Weight (%)',
        help="Weight of this indicator in strategic KPI calculation"
    )
    
    impact_relationship = fields.Selection([
        ('direct', 'Direct Impact'),
        ('indirect', 'Indirect Impact'),
        ('supporting', 'Supporting Impact')
    ], string='Impact Relationship', default='direct')
    
    target_allocation_percentage = fields.Float(
        string='Target Allocation %',
        help="Percentage of strategic target allocated to this indicator"
    )
    
    cascaded_target = fields.Float(
        string='Cascaded Target',
        compute='_compute_cascaded_target',
        help="Target cascaded from strategic KPI"
    )

    @api.depends('wizard_id.strategic_kpi_id.target_value', 'target_allocation_percentage')
    def _compute_cascaded_target(self):
        for line in self:
            if line.wizard_id.strategic_kpi_id and line.target_allocation_percentage:
                line.cascaded_target = (
                    line.wizard_id.strategic_kpi_id.target_value * 
                    line.target_allocation_percentage / 100
                )
            else:
                line.cascaded_target = 0.0


class BulkKPILinkageWizard(models.TransientModel):
    _name = 'bulk.kpi.linkage.wizard'
    _description = 'Bulk KPI Linkage Setup Wizard'

    thematic_area = fields.Selection([
        ('infrastructure', 'Infrastructure & Transport'),
        ('health', 'Health Services'),
        ('education', 'Education Services'),
        ('economic', 'Economic Development'),
        ('environment', 'Environmental Management'),
        ('governance', 'Governance & Legal'),
        ('finance', 'Revenue & Finance'),
        ('climate', 'Climate & Resilience'),
        ('citizen', 'Citizen Satisfaction'),
        ('organizational', 'Organizational Performance')
    ], string='Thematic Area', required=True)

    strategic_kpi_ids = fields.Many2many(
        'key.performance.indicator',
        'bulk_wizard_strategic_kpi_rel',
        'wizard_id',
        'kpi_id',
        string='Strategic KPIs'
    )

    programme_indicator_ids = fields.Many2many(
        'performance.indicator',
        'bulk_wizard_programme_indicator_rel',
        'wizard_id',
        'indicator_id',
        string='Programme Indicators'
    )

    auto_link_by_thematic = fields.Boolean(
        string='Auto-link by Thematic Area',
        default=True,
        help="Automatically link KPIs and indicators with matching thematic areas"
    )

    default_calculation_method = fields.Selection([
        ('weighted_average', 'Weighted Average'),
        ('sum', 'Sum of Values'),
        ('percentage_complete', 'Percentage of Targets Met'),
        ('milestone_count', 'Count of Milestones Achieved')
    ], string='Default Calculation Method', default='weighted_average')

    @api.onchange('thematic_area')
    def _onchange_thematic_area(self):
        """Filter KPIs and indicators by thematic area"""
        if self.thematic_area:
            kpi_domain = [('thematic_area', '=', self.thematic_area)]
            indicator_domain = [('thematic_area', '=', self.thematic_area)]
            return {
                'domain': {
                    'strategic_kpi_ids': kpi_domain,
                    'programme_indicator_ids': indicator_domain
                }
            }
        return {
            'domain': {
                'strategic_kpi_ids': [],
                'programme_indicator_ids': []
            }
        }

    def action_create_bulk_linkages(self):
        """Create bulk KPI linkages"""
        if not self.strategic_kpi_ids or not self.programme_indicator_ids:
            raise UserError(_("Please select both Strategic KPIs and Programme Indicators"))

        linkages_created = 0

        if self.auto_link_by_thematic:
            # Auto-link by thematic area
            for kpi in self.strategic_kpi_ids:
                matching_indicators = self.programme_indicator_ids.filtered(
                    lambda x: x.thematic_area == kpi.thematic_area
                )

                if matching_indicators:
                    # Equal weight distribution
                    weight_per_indicator = 100.0 / len(matching_indicators)

                    # Update Strategic KPI
                    kpi.write({
                        'contributing_programme_indicators': [(6, 0, matching_indicators.ids)],
                        'auto_calculate': True,
                        'calculation_method': self.default_calculation_method
                    })

                    # Update Programme Indicators
                    for indicator in matching_indicators:
                        indicator.write({
                            'strategic_kpi_ids': [(4, kpi.id)],
                            'contribution_weight': weight_per_indicator,
                            'impact_relationship': 'direct'
                        })

                    # Calculate initial value
                    kpi._calculate_from_programme_indicators()
                    linkages_created += 1
        else:
            # Manual linkage - link all indicators to all KPIs
            for kpi in self.strategic_kpi_ids:
                weight_per_indicator = 100.0 / len(self.programme_indicator_ids)

                kpi.write({
                    'contributing_programme_indicators': [(6, 0, self.programme_indicator_ids.ids)],
                    'auto_calculate': True,
                    'calculation_method': self.default_calculation_method
                })

                for indicator in self.programme_indicator_ids:
                    indicator.write({
                        'strategic_kpi_ids': [(4, kpi.id)],
                        'contribution_weight': weight_per_indicator,
                        'impact_relationship': 'direct'
                    })

                kpi._calculate_from_programme_indicators()
                linkages_created += 1

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('%d KPI linkages created successfully') % linkages_created,
                'type': 'success',
                'sticky': False,
            }
        }
