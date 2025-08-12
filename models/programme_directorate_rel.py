# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ProgrammeDirectorateRel(models.Model):
    """Intermediate model for Programme-Directorate relationships

    This model manages the many-to-many relationships between programmes and directorates
    as defined in the master table structure, allowing for better control and tracking
    of implementation responsibilities.
    """
    _name = 'programme.directorate.rel'
    _description = 'Programme-Directorate Relationship'
    _table = 'programme_directorate_relationship'  # Use different table name to avoid conflict
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'strategic_objective_sequence, programme_sequence, directorate_sequence'
    _rec_name = 'display_name'

    # Core relationship fields
    programme_id = fields.Many2one(
        'kcca.programme',
        string='Programme',
        required=True,
        ondelete='cascade',
        help="Programme being implemented"
    )

    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Implementing Directorate',
        required=True,
        ondelete='cascade',
        help="Directorate implementing the programme"
    )

    # Strategic context
    strategic_objective_id = fields.Many2one(
        'strategic.objective',
        string='Strategic Objective',
        compute='_compute_strategic_objective',
        store=True,
        help="Strategic objective this relationship belongs to (computed from master table row)"
    )

    # Master table context
    master_table_row = fields.Integer(
        string='Master Table Row',
        help="Row number in the master table (1-5)"
    )

    # Sequencing for proper ordering
    strategic_objective_sequence = fields.Integer(
        string='Strategic Objective Sequence',
        related='strategic_objective_id.sequence',
        store=True
    )

    programme_sequence = fields.Integer(
        string='Programme Sequence',
        related='programme_id.sequence',
        store=True
    )

    directorate_sequence = fields.Integer(
        string='Directorate Sequence',
        related='directorate_id.sequence',
        store=True
    )

    # Implementation details
    implementation_role = fields.Selection([
        ('primary', 'Primary Implementer'),
        ('supporting', 'Supporting Implementer'),
        ('coordinating', 'Coordinating Role'),
        ('monitoring', 'Monitoring Role')
    ], string='Implementation Role', default='primary',
       help="Role of the directorate in implementing this programme")

    responsibility_percentage = fields.Float(
        string='Responsibility %',
        help="Percentage of responsibility for this programme implementation"
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help="Whether this relationship is currently active"
    )

    # Computed fields
    display_name = fields.Char(
        string='Display Name',
        compute='_compute_display_name',
        store=True
    )

    programme_name = fields.Char(
        string='Programme Name',
        related='programme_id.name',
        store=True
    )

    directorate_name = fields.Char(
        string='Directorate Name',
        related='directorate_id.name',
        store=True
    )

    strategic_objective_name = fields.Char(
        string='Strategic Objective Name',
        related='strategic_objective_id.name',
        store=True
    )

    # Smart button counts
    performance_indicator_count = fields.Integer(
        string='Performance Indicators Count',
        compute='_compute_smart_button_counts',
        help="Number of performance indicators for this programme"
    )

    piap_action_count = fields.Integer(
        string='PIAP Actions Count',
        compute='_compute_smart_button_counts',
        help="Number of PIAP actions for this programme"
    )

    output_count = fields.Integer(
        string='Outputs Count',
        compute='_compute_smart_button_counts',
        help="Number of outputs for this programme"
    )

    intervention_count = fields.Integer(
        string='Interventions Count',
        compute='_compute_smart_button_counts',
        help="Number of interventions for this programme"
    )

    intermediate_outcome_count = fields.Integer(
        string='Intermediate Outcomes Count',
        compute='_compute_smart_button_counts',
        help="Number of intermediate outcomes for this programme"
    )

    # Computed lists of indicators for this relation
    contributing_indicator_ids = fields.Many2many(
        'performance.indicator',
        string='Directorate-Owned Indicators',
        compute='_compute_contributing_indicators',
        search='_search_contributing_indicator_ids',
        help="Programme indicators attributed to this directorate under the selected programme"
    )
    all_programme_indicator_ids = fields.Many2many(
        'performance.indicator',
        string='All Programme Indicators',
        compute='_compute_contributing_indicators',
        help="All programme indicators under the selected programme (irrespective of directorate)"
    )

    # Summary counts (searchable)
    owned_indicator_count = fields.Integer(
        string='Owned KPI Count',
        compute='_compute_indicator_counts',
        search='_search_owned_indicator_count'
    )
    all_indicator_count = fields.Integer(
        string='All KPI Count',
        compute='_compute_indicator_counts',
        search='_search_all_indicator_count'
    )

    # Aggregated normalized performance (from contributing indicators)
    normalized_target_percent = fields.Float(
        string='Normalized Target (%)',
        compute='_compute_normalized_performance',
        store=False,
        help='Target expressed as normalized percentage (100% if indicators exist, else 0%)'
    )

    normalized_achievement_percent = fields.Float(
        string='Achievement (%)',
        compute='_compute_normalized_performance',
        store=True,
        aggregator='avg',
        help='Weighted average achievement (%) of contributing indicators'
    )

    performance_status = fields.Selection([
        ('none', 'Not Started (0%)'),
        ('low', 'Low (<50%)'),
        ('medium', 'Medium (50-79%)'),
        ('high', 'High (≥80%)'),
        ('achieved', 'Achieved (≥100%)'),
    ], string='Status', compute='_compute_normalized_performance', store=False)

    @api.depends('programme_id.name', 'directorate_id.name', 'implementation_role')
    def _compute_display_name(self):
        for record in self:
            if record.programme_id and record.directorate_id:
                role_text = dict(record._fields['implementation_role'].selection).get(
                    record.implementation_role, record.implementation_role
                )
                record.display_name = f"{record.programme_id.name} → {record.directorate_id.name} ({role_text})"
            else:
                record.display_name = "New Relationship"

    @api.depends('programme_id')
    def _compute_smart_button_counts(self):
        """Compute counts for smart buttons"""
        for record in self:
            if record.programme_id:
                # Get programme hierarchy
                programme = record.programme_id

                # Count intermediate outcomes
                intermediate_outcomes = self.env['intermediate.outcome'].search([
                    ('objective_id.programme_id', '=', programme.id)
                ])
                record.intermediate_outcome_count = len(intermediate_outcomes)

                # Count interventions
                interventions = self.env['intervention'].search([
                    ('outcome_id', 'in', intermediate_outcomes.ids)
                ])
                record.intervention_count = len(interventions)

                # Count outputs
                outputs = self.env['output'].search([
                    ('intervention_id', 'in', interventions.ids)
                ])
                record.output_count = len(outputs)

                # Count PIAP actions
                piap_actions = self.env['piap.action'].search([
                    ('output_id', 'in', outputs.ids)
                ])
                record.piap_action_count = len(piap_actions)

                # Count performance indicators (from outputs and PIAP actions)
                performance_indicators = self.env['performance.indicator'].search([
                    '|',
                    ('output_id', 'in', outputs.ids),
                    ('piap_action_id', 'in', piap_actions.ids)
                ])
                record.performance_indicator_count = len(performance_indicators)
            else:
                record.intermediate_outcome_count = 0
                record.intervention_count = 0
                record.output_count = 0
                record.piap_action_count = 0
                record.performance_indicator_count = 0

    @api.depends('programme_id', 'directorate_id')
    def _compute_contributing_indicators(self):
        for record in self:
            if not record.programme_id:
                record.contributing_indicator_ids = [(6, 0, [])]
                record.all_programme_indicator_ids = [(6, 0, [])]
                continue
            # Gather full results-chain under the selected programme
            intermediate_outcomes = self.env['intermediate.outcome'].search([
                ('objective_id.programme_id', '=', record.programme_id.id)
            ])
            interventions = self.env['intervention'].search([
                ('outcome_id', 'in', intermediate_outcomes.ids)
            ])
            outputs = self.env['output'].search([
                ('intervention_id', 'in', interventions.ids)
            ])
            piap_actions = self.env['piap.action'].search([
                ('output_id', 'in', outputs.ids)
            ])
            # All programme indicators
            all_indicators = self.env['performance.indicator'].search([
                '|', ('output_id', 'in', outputs.ids), ('piap_action_id', 'in', piap_actions.ids)
            ])
            record.all_programme_indicator_ids = [(6, 0, all_indicators.ids)]
            # Directorate-owned indicators (requires attribution on indicator)
            if record.directorate_id:
                owned = all_indicators.filtered(lambda i: i.responsible_directorate_id.id == record.directorate_id.id)
            else:
                owned = all_indicators
            record.contributing_indicator_ids = [(6, 0, owned.ids)]
    def _compute_indicator_counts(self):
        for rec in self:
            rec.owned_indicator_count = len(rec.contributing_indicator_ids)
            rec.all_indicator_count = len(rec.all_programme_indicator_ids)

    def _search_owned_indicator_count(self, operator, value):
        # Relations with at least one owned KPI
        if operator in ('>', '>=') and value <= 0:
            return [('id', 'in', self.search([]).filtered(lambda r: len(r.contributing_indicator_ids) > 0).ids)]
        if operator in ('=', '==') and value == 0:
            return [('id', 'in', self.search([]).filtered(lambda r: len(r.contributing_indicator_ids) == 0).ids)]
        return []

    def _search_all_indicator_count(self, operator, value):
        # Relations with at least one programme KPI
        if operator in ('>', '>=') and value <= 0:
            return [('id', 'in', self.search([]).filtered(lambda r: len(r.all_programme_indicator_ids) > 0).ids)]
        if operator in ('=', '==') and value == 0:
            return [('id', 'in', self.search([]).filtered(lambda r: len(r.all_programme_indicator_ids) == 0).ids)]
        return []

    def _search_contributing_indicator_ids(self, operator, value):
        """Search method to support dependencies and domains on computed Many2many.
        Expected usage is mainly [('contributing_indicator_ids', 'in', [indicator_id])].
        Returns programme.directorate.rel records where the given indicators would
        appear in the computed contributing_indicator_ids list.
        """
        Indicator = self.env['performance.indicator']
        if operator in ('in', '='):
            ids = value
            if isinstance(ids, models.BaseModel):
                ids = ids.ids
            if not isinstance(ids, (list, tuple)):
                ids = [ids]
            ids = [int(i) for i in ids if i]
            if not ids:
                return [('id', '=', 0)]
            indicators = Indicator.browse(ids)
            rel_domain = []
            combos = set()
            for ind in indicators:
                # Determine programme for the indicator through its linkage
                programme_id = False
                if ind.programme_id:
                    programme_id = ind.programme_id.id
                elif ind.outcome_id and getattr(ind.outcome_id, 'objective_id', False):
                    programme_id = ind.outcome_id.objective_id.programme_id.id or False
                elif ind.output_id and getattr(ind.output_id, 'intervention_id', False):
                    outcome = ind.output_id.intervention_id.outcome_id
                    programme_id = outcome.objective_id.programme_id.id if outcome and outcome.objective_id else False
                elif ind.piap_action_id and getattr(ind.piap_action_id, 'output_id', False):
                    out = ind.piap_action_id.output_id
                    if out and out.intervention_id and out.intervention_id.outcome_id and out.intervention_id.outcome_id.objective_id:
                        programme_id = out.intervention_id.outcome_id.objective_id.programme_id.id
                directorate_id = ind.responsible_directorate_id.id if ind.responsible_directorate_id else False
                if programme_id and directorate_id:
                    combos.add((programme_id, directorate_id))
            if not combos:
                # If we cannot resolve combos, no relation would match
                return [('id', '=', 0)]
            # Build a domain that matches any of the (programme, directorate) pairs
            combos = list(combos)
            domain = []
            for i, (p_id, d_id) in enumerate(combos):
                if i:
                    domain.append('|')
                domain += [('programme_id', '=', p_id), ('directorate_id', '=', d_id)]
            return domain
        elif operator in ('not in', '!='):
            # Return inverse domain
            pos_domain = self._search_contributing_indicator_ids('in', value)
            return ['!', pos_domain] if pos_domain else []
        # Fallback: no specific match
        return []

    @api.depends(
        'programme_id',
        'directorate_id',
        'contributing_indicator_ids',
        'contributing_indicator_ids.achievement_percentage',
        'contributing_indicator_ids.contribution_weight'
    )
    def _compute_normalized_performance(self):
        for record in self:
            indicators = record.contributing_indicator_ids
            if not indicators:
                record.normalized_target_percent = 0.0
                record.normalized_achievement_percent = 0.0
                record.performance_status = 'none'
                continue
            # Use contribution_weight if present; otherwise equal weight
            weights = []
            for ind in indicators:
                w = ind.contribution_weight if ind.contribution_weight and ind.contribution_weight > 0 else 0.0
                weights.append(w)
            total_w = sum(weights)
            if total_w == 0:
                # Equal weighting fallback
                avg = sum(indicators.mapped('achievement_percentage')) / len(indicators)
                record.normalized_achievement_percent = round(avg, 2)
            else:
                weighted = 0.0
                for ind, w in zip(indicators, weights):
                    weighted += ind.achievement_percentage * (w / total_w)
                record.normalized_achievement_percent = round(weighted, 2)
            # Target normalization: if there are indicators, target baseline is 100%
            record.normalized_target_percent = 100.0
            # Derive status
            ach = record.normalized_achievement_percent or 0.0
            if ach >= 100:
                record.performance_status = 'achieved'
            elif ach >= 80:
                record.performance_status = 'high'
            elif ach >= 50:
                record.performance_status = 'medium'
            elif ach > 0:
                record.performance_status = 'low'
            else:
                record.performance_status = 'none'

    @api.depends('master_table_row')
    def _compute_strategic_objective(self):
        """Compute strategic objective based on master table row"""
        for record in self:
            if record.master_table_row:
                # Map master table rows to strategic objectives
                strategic_obj = self.env['strategic.objective'].search([
                    ('sequence', '=', record.master_table_row)
                ], limit=1)
                record.strategic_objective_id = strategic_obj.id if strategic_obj else False
            else:
                record.strategic_objective_id = False

    @api.constrains('programme_id', 'directorate_id', 'master_table_row')
    def _check_unique_relationship(self):
        """Ensure no duplicate programme-directorate relationships within the same master table row"""
        for record in self:
            if record.programme_id and record.directorate_id and record.master_table_row:
                existing = self.search([
                    ('programme_id', '=', record.programme_id.id),
                    ('directorate_id', '=', record.directorate_id.id),
                    ('master_table_row', '=', record.master_table_row),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError(_(
                        "A relationship between programme '%s' and directorate '%s' in master table row %s already exists."
                    ) % (record.programme_id.name, record.directorate_id.name, record.master_table_row))

    @api.constrains('responsibility_percentage')
    def _check_responsibility_percentage(self):
        """Validate responsibility percentage"""
        for record in self:
            if record.responsibility_percentage < 0 or record.responsibility_percentage > 100:
                raise ValidationError(_("Responsibility percentage must be between 0 and 100."))

    @api.model
    def create_master_table_relationships(self):
        """Create relationships based on the master table structure"""

        # Clear existing relationships
        self.search([]).unlink()

        # Master table data structure
        master_table_data = {
            1: {  # Row 1: Strategic Objective 1 - 8 programmes → 5 directorates
                'programmes': [
                    'Agro-Industrialization',
                    'Private Sector Development',
                    'Integrated Transport Infrastructure and Services',
                    'Development Plan Implementation',
                    'Tourism Development',
                    'Natural Resources, Environment, Climate Change, Water and Land Management',
                    'Sustainable Urbanization and Housing',
                    'Digital Transformation'
                ],
                'directorates': [
                    'Production and Commercial Services',
                    'Engineering',
                    'Revenue Administration',
                    'Physical Planning',
                    'Information & Communications Technology'
                ]
            },
            2: {  # Row 2: Strategic Objective 2 - 1 programme → 3 directorates
                'programmes': ['Human Capital Development'],
                'directorates': [
                    'Public Health',
                    'Education and Sports',
                    'Gender and Community Services'
                ]
            },
            3: {  # Row 3: Strategic Objective 3 - 3 programmes → 2 directorates
                'programmes': [
                    'Legislation, Oversight and Representation',
                    'Administration of Justice',
                    'Governance and Security'
                ],
                'directorates': [
                    'Legislative and Political Affairs',
                    'Legal Affairs'
                ]
            },
            4: {  # Row 4: Strategic Objective 4 - 2 programmes → 2 directorates
                'programmes': [
                    'Development Plan Implementation',  # This appears in multiple rows
                    'Digital Transformation'  # This appears in multiple rows
                ],
                'directorates': [
                    'Treasury Services',
                    'Human Resource and Organizational Development'
                ]
            },
            5: {  # Row 5: Strategic Objective 5 - 3 programmes → 4 directorates
                'programmes': [
                    'Natural Resources, Environment, Climate Change, Water and Land Management',  # Multi-row
                    'Development Plan Implementation',  # Multi-row
                    'Public Sector Transformation'
                ],
                'directorates': [
                    'Treasury Services',
                    'Human Resource and Organizational Development',
                    'Administration and ICT',
                    'Internal Audit'
                ]
            }
        }

        # Create relationships
        for row_num, row_data in master_table_data.items():
            for programme_name in row_data['programmes']:
                programme = self.env['kcca.programme'].search([('name', '=', programme_name)], limit=1)
                if not programme:
                    continue

                for directorate_name in row_data['directorates']:
                    directorate = self.env['kcca.directorate'].search([('name', '=', directorate_name)], limit=1)
                    if not directorate:
                        continue

                    # Check if relationship already exists
                    existing = self.search([
                        ('programme_id', '=', programme.id),
                        ('directorate_id', '=', directorate.id)
                    ])

                    if not existing:
                        self.create({
                            'programme_id': programme.id,
                            'directorate_id': directorate.id,
                            'master_table_row': row_num,
                            'implementation_role': 'primary'
                        })

        return True

    def action_view_programme(self):
        """Action to view the programme"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Programme',
            'res_model': 'kcca.programme',
            'res_id': self.programme_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_view_directorate(self):
        """Action to view the directorate"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Directorate',
            'res_model': 'kcca.directorate',
            'res_id': self.directorate_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to sync many-to-many relationships"""
        records = super().create(vals_list)

        # Sync the many-to-many field for affected programmes
        programmes = records.mapped('programme_id')
        programmes.sync_directorate_relationships()

        return records

    def write(self, vals):
        """Override write to sync many-to-many relationships"""
        old_programmes = self.mapped('programme_id')
        result = super().write(vals)

        # Sync for both old and potentially new programmes
        new_programmes = self.mapped('programme_id')
        all_programmes = old_programmes | new_programmes
        all_programmes.sync_directorate_relationships()

        return result

    def unlink(self):
        """Override unlink to sync many-to-many relationships"""
        programmes = self.mapped('programme_id')
        result = super().unlink()

        # Sync the many-to-many field for affected programmes
        programmes.sync_directorate_relationships()

        return result

    # Smart button action methods
    def action_view_performance_indicators(self):
        """Open performance indicators for this programme"""
        self.ensure_one()
        if not self.programme_id:
            return

        # Get programme hierarchy
        programme = self.programme_id
        intermediate_outcomes = self.env['intermediate.outcome'].search([
            ('objective_id.programme_id', '=', programme.id)
        ])
        interventions = self.env['intervention'].search([
            ('outcome_id', 'in', intermediate_outcomes.ids)
        ])
        outputs = self.env['output'].search([
            ('intervention_id', 'in', interventions.ids)
        ])
        piap_actions = self.env['piap.action'].search([
            ('output_id', 'in', outputs.ids)
        ])

        # Get performance indicators
        domain = [
            '|',
            ('output_id', 'in', outputs.ids),
            ('piap_action_id', 'in', piap_actions.ids)
        ]

        return {
            'name': f'Performance Indicators - {programme.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'performance.indicator',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'default_programme_id': programme.id,
                'search_default_active': 1,
            },
            'target': 'current',
        }

    def action_view_piap_actions(self):
        """Open PIAP actions for this programme"""
        self.ensure_one()
        if not self.programme_id:
            return

        # Get programme hierarchy
        programme = self.programme_id
        intermediate_outcomes = self.env['intermediate.outcome'].search([
            ('objective_id.programme_id', '=', programme.id)
        ])
        interventions = self.env['intervention'].search([
            ('outcome_id', 'in', intermediate_outcomes.ids)
        ])
        outputs = self.env['output'].search([
            ('intervention_id', 'in', interventions.ids)
        ])

        domain = [('output_id', 'in', outputs.ids)]

        return {
            'name': f'PIAP Actions - {programme.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'piap.action',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'default_programme_id': programme.id,
                'search_default_active': 1,
            },
            'target': 'current',
        }

    def action_view_outputs(self):
        """Open outputs for this programme"""
        self.ensure_one()
        if not self.programme_id:
            return

        # Get programme hierarchy
        programme = self.programme_id
        intermediate_outcomes = self.env['intermediate.outcome'].search([
            ('objective_id.programme_id', '=', programme.id)
        ])
        interventions = self.env['intervention'].search([
            ('outcome_id', 'in', intermediate_outcomes.ids)
        ])

        domain = [('intervention_id', 'in', interventions.ids)]

        return {
            'name': f'Outputs - {programme.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'output',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'default_programme_id': programme.id,
                'search_default_active': 1,
            },
            'target': 'current',
        }

    def action_view_interventions(self):
        """Open interventions for this programme"""
        self.ensure_one()
        if not self.programme_id:
            return

        # Get programme hierarchy
        programme = self.programme_id
        intermediate_outcomes = self.env['intermediate.outcome'].search([
            ('objective_id.programme_id', '=', programme.id)
        ])

        domain = [('outcome_id', 'in', intermediate_outcomes.ids)]

        return {
            'name': f'Interventions - {programme.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'intervention',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'default_programme_id': programme.id,
                'search_default_active': 1,
            },
            'target': 'current',
        }

    def action_view_intermediate_outcomes(self):
        """Open intermediate outcomes for this programme"""
        self.ensure_one()
        if not self.programme_id:
            return

        programme = self.programme_id
        domain = [('objective_id.programme_id', '=', programme.id)]

        return {
            'name': f'Intermediate Outcomes - {programme.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'intermediate.outcome',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {
                'default_programme_id': programme.id,
                'search_default_active': 1,
            },
            'target': 'current',
        }
