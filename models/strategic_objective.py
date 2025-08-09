# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StrategicObjective(models.Model):
    _name = 'strategic.objective'
    _description = 'Strategic Plan Objective'
    _order = 'sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _sql_constraints = [
        ('unique_objective_per_goal', 'unique(strategic_goal_id, name)',
         'Strategic Objective names must be unique within each Strategic Goal.'),
    ]

    name = fields.Char(
        string='Strategic Objective',
        required=True,
        tracking=True,
        help="Name of the strategic objective"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the strategic objective"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering objectives"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    strategic_goal_id = fields.Many2one(
        'strategic.goal',
        string='Strategic Goal',
        required=True,
        ondelete='cascade',
        tracking=True,
        help="Parent strategic goal"
    )
    
    kra_ids = fields.One2many(
        'key.result.area',
        'strategic_objective_id',
        string='Key Result Areas',
        help="KRAs under this strategic objective"
    )
    
    programme_ids = fields.Many2many(
        'kcca.programme',
        'objective_programme_rel',
        'objective_id',
        'programme_id',
        string='Related Programmes',
        help="Programmes that contribute to this objective"
    )
    
    # Computed fields
    kra_count = fields.Integer(
        string='KRAs Count',
        compute='_compute_counts',
        store=True
    )
    
    kpi_count = fields.Integer(
        string='KPIs Count',
        compute='_compute_counts',
        store=True
    )
    
    programme_count = fields.Integer(
        string='Programmes Count',
        compute='_compute_counts',
        store=True
    )
    
    progress = fields.Float(
        string='Progress (%)',
        compute='_compute_progress',
        store=True,
        help="Progress based on KRAs achievement"
    )
    
    @api.depends('kra_ids', 'kra_ids.kpi_ids', 'programme_ids')
    def _compute_counts(self):
        for record in self:
            record.kra_count = len(record.kra_ids)
            record.kpi_count = len(record.kra_ids.mapped('kpi_ids'))
            record.programme_count = len(record.programme_ids)
    
    @api.depends('kra_ids.progress')
    def _compute_progress(self):
        for record in self:
            if record.kra_ids:
                total_progress = sum(kra.progress for kra in record.kra_ids)
                record.progress = total_progress / len(record.kra_ids)
            else:
                record.progress = 0.0
    
    def action_view_kras(self):
        """Action to view KRAs"""
        action = self.env.ref('robust_pmis.action_key_result_area').read()[0]
        action['domain'] = [('strategic_objective_id', '=', self.id)]
        action['context'] = {'default_strategic_objective_id': self.id}
        return action
    
    def action_view_programmes(self):
        """Action to view related programmes"""
        action = self.env.ref('robust_pmis.action_kcca_programme').read()[0]
        action['domain'] = [('id', 'in', self.programme_ids.ids)]
        return action

    @api.model
    def create_master_table_relationships(self):
        """Create strategic objective-programme relationships based on master table"""
        # Define the relationships based on the master table
        relationships = {
            'strategic_objective_economic_growth': [
                'programme_agro_industrialization',
                'programme_private_sector_dev',
                'programme_transport_infrastructure',
                'programme_dev_plan_implementation',
                'programme_tourism_development',
                'programme_natural_resources',
                'programme_sustainable_urbanization',
                'programme_digital_transformation',
                'programme_sustainable_energy_dev'
            ],
            'strategic_objective_productivity_wellbeing': [
                'programme_human_capital_dev',
                'programme_sustainable_energy_dev'
            ],
            'strategic_objective_governance': [
                'programme_legislation_oversight',
                'programme_admin_justice',
                'programme_governance_security'
            ],
            'strategic_objective_climate_resilience': [
                'programme_natural_resources',
                'programme_dev_plan_implementation',
                'programme_digital_transformation'
            ],
            'strategic_objective_institutional_capacity': [
                'programme_natural_resources',
                'programme_dev_plan_implementation',
                'programme_public_sector_transformation'
            ]
        }

        total_created = 0
        for obj_xml_id, prog_xml_ids in relationships.items():
            # Find the strategic objective
            try:
                strategic_obj = self.env.ref(f'robust_pmis.{obj_xml_id}')
            except:
                continue

            programme_ids = []
            for prog_xml_id in prog_xml_ids:
                try:
                    programme = self.env.ref(f'robust_pmis.{prog_xml_id}')
                    programme_ids.append(programme.id)
                except:
                    continue

            # Create the many-to-many relationships
            if programme_ids:
                strategic_obj.write({
                    'programme_ids': [(6, 0, programme_ids)]
                })
                total_created += len(programme_ids)

        return total_created
