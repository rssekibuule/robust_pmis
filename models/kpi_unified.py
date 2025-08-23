# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _


class KPIUnified(models.Model):
    _name = 'kpi.unified'
    _description = 'Unified KPI (Strategic + Programme Indicators)'
    _rec_name = 'name'
    _auto = False  # SQL view

    name = fields.Char(readonly=True)
    kind = fields.Selection([
        ('strategic', 'Strategic KPI'),
        ('programme', 'Programme Indicator'),
    ], string='Type', readonly=True, index=True)
    source_model = fields.Char(string='Source Model', readonly=True)
    source_id = fields.Integer(string='Source ID', readonly=True)
    source_ref = fields.Reference(selection=[
        ('key.performance.indicator', 'Strategic KPI'),
        ('performance.indicator', 'Programme Indicator'),
    ], string='Source Record', compute='_compute_source_ref', readonly=True, store=False)

    achievement_percentage = fields.Float(string='Achievement (%)', readonly=True)
    status = fields.Selection([
        ('not_started', 'Not Started'),
        ('on_track', 'On Track'),
        ('at_risk', 'At Risk'),
        ('behind', 'Behind Schedule'),
        ('achieved', 'Achieved'),
    ], readonly=True)

    start_date = fields.Date(readonly=True)
    end_date = fields.Date(readonly=True)
    measurement_unit = fields.Char(readonly=True)
    target_value = fields.Float(readonly=True)
    current_value = fields.Float(readonly=True)

    kra_id = fields.Many2one('key.result.area', string='KRA', readonly=True)
    programme_id = fields.Many2one('kcca.programme', string='Programme', readonly=True)
    directorate_id = fields.Many2one('kcca.directorate', string='Directorate', readonly=True)
    division_id = fields.Many2one('kcca.division', string='Division', readonly=True)
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
    ], string='Thematic Area', readonly=True)
    responsible_user_id = fields.Many2one('res.users', string='Responsible', readonly=True)

    @api.depends('source_model', 'source_id')
    def _compute_source_ref(self):
        for rec in self:
            if rec.source_model and rec.source_id:
                rec.source_ref = f"{rec.source_model},{rec.source_id}"
            else:
                rec.source_ref = False

    def action_open_source(self):
        self.ensure_one()
        model = self.source_model
        if not model:
            return False
        return {
            'type': 'ir.actions.act_window',
            'name': _('Open Source'),
            'res_model': model,
            'view_mode': 'form',
            'res_id': self.source_id,
            'target': 'current',
        }

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'kpi_unified')
        self.env.cr.execute(
            """
            CREATE OR REPLACE VIEW kpi_unified AS (
                SELECT
                    kpi.id AS id,
                    'strategic'::varchar AS kind,
                    'key.performance.indicator'::varchar AS source_model,
                    kpi.id AS source_id,
                    kpi.name,
                    kpi.achievement_percentage,
                    kpi.status,
                    kpi.start_date,
                    kpi.end_date,
                    kpi.measurement_unit,
                    kpi.target_value,
                    kpi.current_value,
                    kpi.kra_id,
                    kpi.programme_id,
                    kpi.directorate_id,
                    kpi.division_id,
                    kpi.thematic_area,
                    kpi.responsible_user_id
                FROM key_performance_indicator kpi
                UNION ALL
                SELECT
                    -pi.id AS id,
                    'programme'::varchar AS kind,
                    'performance.indicator'::varchar AS source_model,
                    pi.id AS source_id,
                    pi.name,
                    pi.achievement_percentage,
                    pi.status,
                    pi.start_date,
                    pi.end_date,
                    pi.measurement_unit,
                    pi.target_value,
                    pi.current_value,
                    NULL::integer AS kra_id,
                    pi.parent_programme_id AS programme_id,
                    pi.responsible_directorate_id AS directorate_id,
                    pi.responsible_division_id AS division_id,
                    pi.thematic_area,
                    pi.responsible_user_id
                FROM performance_indicator pi
            );
            """
        )
