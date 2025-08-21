# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class KCCADivision(models.Model):
    _name = 'kcca.division'
    _description = 'KCCA Division'
    _order = 'directorate_id, sequence, name'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Division Name',
        required=True,
        tracking=True,
        help="Name of the division"
    )
    
    code = fields.Char(
        string='Division Code',
        help="Short code for the division"
    )
    
    description = fields.Html(
        string='Description',
        help="Detailed description of the division"
    )
    
    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Sequence for ordering divisions within directorate"
    )
    
    active = fields.Boolean(
        string='Active',
        default=True,
        tracking=True
    )
    
    # Relationships
    directorate_id = fields.Many2one(
        'kcca.directorate',
        string='Directorate',
        required=False,
        ondelete='set null',
        tracking=True,
        help="Parent directorate (optional for territorial divisions)"
    )

    # Legacy direct link kept for backwards compatibility but counts/actions rely on intermediary
    programme_ids = fields.One2many(
        'kcca.programme',
        'division_id',
        string='Devolved Programmes (legacy)',
        help="Deprecated: use Division-Programme relationships with 'Devolved Programme' flag"
    )

    # Division-owned KPIs (direct KPIs managed at division level)
    kpi_ids = fields.One2many(
        'key.performance.indicator',
        'division_id',
        string='Division KPIs',
        help='KPIs that are directly owned by this division'
    )

    # Many-to-many relationship with programmes through intermediate model
    division_programme_rel_ids = fields.One2many(
        'division.programme.rel',
        'division_id',
        string='Programme Relationships',
        help="All programme relationships for this division"
    )

    implementing_programme_ids = fields.Many2many(
        'kcca.programme',
        string='Implementing Programmes',
        compute='_compute_implementing_programmes',
        help="All programmes this division implements (via relationships)"
    )
    implementing_programme_count = fields.Integer(
        string='Implementing Programmes Count',
        compute='_compute_implementing_programme_count',
        store=False,
        help='Number of programmes this division implements via relationships'
    )
    
    # Leadership
    head_id = fields.Many2one(
        'res.users',
        string='Division Head',
        help="Head of this division"
    )
    
    deputy_head_id = fields.Many2one(
        'res.users',
        string='Deputy Head',
        help="Deputy head of this division"
    )
    
    # Contact Information
    email = fields.Char(string='Email')
    phone = fields.Char(string='Phone')
    office_location = fields.Char(string='Office Location')
    
    # Computed fields
    programme_count = fields.Integer(
        string='Programmes Count',
        compute='_compute_counts',
        store=True
    )
    
    performance_indicator_count = fields.Integer(
        string='Performance Indicators Count',
        compute='_compute_counts',
        store=True
    )

    division_kpi_count = fields.Integer(
        string='Division KPI Count',
        compute='_compute_counts',
        store=True,
        help='Number of KPIs directly owned by this division'
    )
    
    overall_performance = fields.Float(
        string='Overall Performance (%)',
        compute='_compute_performance',
        store=True,
        help="Overall performance based on programme performance indicators"
    )

    implementation_coverage_percent = fields.Float(
        string='Implementation Coverage (%)',
        compute='_compute_implementation_coverage',
        store=False,
        help='Percentage of programmes this division implements (of all programmes)'
    )

    # Programme KPI performance (via implementing programmes)
    programme_pi_count = fields.Integer(
        string='Programme KPI Count',
        compute='_compute_pi_stats',
        store=False,
        help='Count of programme performance indicators under programmes this division implements'
    )
    programme_pi_avg = fields.Float(
        string='Programme KPI Achievement Avg (%)',
        compute='_compute_pi_stats',
        store=False,
        help='Average achievement (%) of programme indicators for implementing programmes'
    )

    # Direct/owned KPI performance (indicators owned by this division)
    direct_pi_count = fields.Integer(
        string='Direct KPI Count',
        compute='_compute_pi_stats',
        store=False,
        help='Count of performance indicators owned by this division'
    )
    direct_pi_avg = fields.Float(
        string='Direct KPI Achievement Avg (%)',
        compute='_compute_pi_stats',
        store=False,
        help='Average achievement (%) of indicators owned by this division'
    )

    # Status distribution across all relevant programme indicators
    pi_high_count = fields.Integer(
        string='High (≥80%)',
        compute='_compute_pi_stats',
        store=False
    )
    pi_medium_count = fields.Integer(
        string='Medium (50–79%)',
        compute='_compute_pi_stats',
        store=False
    )
    pi_low_count = fields.Integer(
        string='Low (<50%)',
        compute='_compute_pi_stats',
        store=False
    )
    pi_none_count = fields.Integer(
        string='Not Started (0%)',
        compute='_compute_pi_stats',
        store=False
    )
    
    @api.depends('division_programme_rel_ids',
                 'division_programme_rel_ids.is_direct',
                 'division_programme_rel_ids.programme_id')
    def _compute_implementing_programmes(self):
        """Compute non-devolved programmes this division implements.

        Implementing = relationships where is_direct is False. Devolved programmes are
        represented separately via the Devolved Programmes smart button.
        """
        for record in self:
            non_direct = record.division_programme_rel_ids.filtered(lambda r: not r.is_direct)
            record.implementing_programme_ids = non_direct.mapped('programme_id')

    @api.depends('division_programme_rel_ids', 'division_programme_rel_ids.is_direct', 'division_programme_rel_ids.programme_id',
                 'division_programme_rel_ids.programme_id.performance_indicator_ids',
                 'kpi_ids')
    def _compute_counts(self):
        for record in self:
            # Devolved programmes via intermediary flag
            direct_rels = record.division_programme_rel_ids.filtered(lambda r: r.is_direct)
            direct_programmes = direct_rels.mapped('programme_id')
            record.programme_count = len(direct_programmes)
            # KPIs attached to devolved programmes contribute to division KPI pool
            all_indicators = direct_programmes.mapped('performance_indicator_ids')
            record.performance_indicator_count = len(all_indicators)
            record.division_kpi_count = len(record.kpi_ids)

    @api.depends('division_programme_rel_ids', 'division_programme_rel_ids.is_direct')
    def _compute_implementing_programme_count(self):
        """Compute count from non-direct relationships only.

        Decoupled from _compute_counts to avoid mixed stored/non-stored warnings
        and to ensure this value always reflects the latest relationship state.
        """
        for record in self:
            # Count unique programmes linked as non-direct (implementing)
            non_direct = record.division_programme_rel_ids.filtered(lambda r: not r.is_direct)
            record.implementing_programme_count = len(set(non_direct.mapped('programme_id').ids))
    
    @api.depends('programme_ids.overall_performance',
                 'division_programme_rel_ids.performance_score',
                 'kpi_ids.achievement_percentage')
    def _compute_performance(self):
        def _pct(val):
            try:
                v = float(val or 0.0)
            except Exception:
                v = 0.0
            # clamp to 0..100
            return max(0.0, min(100.0, v))

        for record in self:
            # Aggregate components in 0..100 space and clamp to avoid outliers
            direct_performance = 0.0
            relationship_performance = 0.0
            division_kpi_perf = 0.0

            if record.programme_ids:
                vals = [p.overall_performance for p in record.programme_ids]
                if vals:
                    direct_performance = sum(_pct(v) for v in vals) / len(vals)

            if record.division_programme_rel_ids:
                vals = [r.performance_score for r in record.division_programme_rel_ids]
                if vals:
                    relationship_performance = sum(_pct(v) for v in vals) / len(vals)

            if record.kpi_ids:
                vals = [v for v in record.kpi_ids.mapped('achievement_percentage')]
                if vals:
                    division_kpi_perf = sum(_pct(v) for v in vals) / len(vals)

            # Include zeros; only drop Nones
            components = [c for c in [direct_performance, relationship_performance, division_kpi_perf] if c is not None]
            if components:
                blended = sum(components) / len(components)
                record.overall_performance = _pct(blended)
            else:
                record.overall_performance = 0.0
    
    def action_view_programmes(self):
        """Open division-programme relationships filtered to devolved programmes"""
        self.ensure_one()
        # Try standard action; fallback to a safe act_window if not found
        action = None
        try:
            action = self.env.ref('robust_pmis.action_division_programme_performance').sudo().read()[0]
        except Exception:
            action = {
                'type': 'ir.actions.act_window',
                'name': _('Devolved Programmes'),
                'res_model': 'division.programme.rel',
                'view_mode': 'kanban,list,form,graph,pivot',
            }
        action['domain'] = [('division_id', '=', self.id), ('is_direct', '=', True)]
        action.setdefault('context', {})
        action['context'].update({
            'default_division_id': self.id,
            'search_default_is_direct': 1,
            # Force a safe grouping for Graph view (avoid boolean category errors)
            'group_by': 'programme_id',
            'search_default_group_by_programme': 1,
            'search_default_active': 1,
        })
        action['name'] = _('Devolved Programmes')
        return action

    def action_view_division_performance(self):
        """Action to view division performance across programmes"""
        self.ensure_one()
        action = None
        # Prefer the dashboard action if available
        try:
            action = self.env.ref('robust_pmis.action_division_performance_dashboard').sudo().read()[0]
        except Exception:
            try:
                action = self.env.ref('robust_pmis.action_division_programme_performance').sudo().read()[0]
            except Exception:
                action = {
                    'type': 'ir.actions.act_window',
                    'name': _('Division Performance'),
                    'res_model': 'division.programme.rel',
                    'view_mode': 'kanban,list,form,graph,pivot',
                }
        action['domain'] = [('division_id', '=', self.id)]
        action.setdefault('context', {})
        action['context'].update({
            'default_division_id': self.id,
            'search_default_active': 1,
            'search_default_group_by_division': 1,
            'searchpanel_default_division_id': self.id,
            # Ensure graphs default to a supported category
            'group_by': 'division_id',
        })
        action['name'] = _('Division Performance')
        return action

    def action_view_implementing_programmes(self):
        """Open division-programme relationships filtered to non-direct (implementing)"""
        self.ensure_one()
        action = None
        try:
            action = self.env.ref('robust_pmis.action_division_programme_performance').sudo().read()[0]
        except Exception:
            action = {
                'type': 'ir.actions.act_window',
                'name': _('Implementing Programmes'),
                'res_model': 'division.programme.rel',
                'view_mode': 'kanban,list,form,graph,pivot',
            }
        action['domain'] = [('division_id', '=', self.id), ('is_direct', '=', False)]
        action.setdefault('context', {})
        action['context'].update({
            'default_division_id': self.id,
            # Force a safe grouping for Graph view (avoid boolean category errors)
            'group_by': 'programme_id',
            'search_default_group_by_programme': 1,
            'search_default_active': 1,
        })
        action['name'] = _('Implementing Programmes')
        return action

    # Utility: Ensure each division implements only the canonical 16 programmes
    def ensure_all_programmes_implemented(self):
        """
        Ensure that each division has implementing relationships only for the
        allowed set of 16 KCCA programmes. This prevents noise from DEMO or
        legacy programme codes being (re)added by maintenance jobs.

        Notes
        - Implementing relationships are created only when missing.
        - Ownership-derived 'is_direct' remains unchanged and is set by the
          division-programme relation model itself.
        - Allowed programme codes: AGRO, PSD, ITIS, SUH, DT, HCD, LOR, RRP,
          WME, PHE, DRC, UPD, AOJ, GS, PST, SED.

        Returns a dict {division_id: created_count} for logging.
        """
        Programme = self.env['kcca.programme']
        Rel = self.env['division.programme.rel']
        allowed_codes = self.env['res.config.settings'].get_allowed_programme_codes()
        # Fetch only allowed programmes; this automatically excludes DEMO codes
        # like KD-DP01, etc., and any legacy non-allowed codes.
        allowed_programmes = Programme.search([('code', 'in', allowed_codes)])
        results = {}
        for division in self:
            existing_prog_ids = set(division.division_programme_rel_ids.mapped('programme_id').ids)
            # Create links only for allowed programmes that are missing
            to_create = [
                {'division_id': division.id, 'programme_id': pid}
                for pid in allowed_programmes.ids if pid not in existing_prog_ids
            ]
            if to_create:
                Rel.create(to_create)
            results[division.id] = len(to_create)
        return results

    def enforce_allowed_implementing_relations(self):
        """Cleanup utility to enforce only allowed implementing relations.

        Rules applied:
        - Keep implementing (is_direct = False) only for the canonical 16 programme codes.
        - For DEMO programmes (codes like 'CD-DP01', 'KD-DP02', etc.), keep only the
          relation to their owner division and mark those relations as direct.
        - Remove any other non-direct relations pointing to DEMO or legacy codes.

        Returns a dict with simple counters for logging.
        """
        Rel = self.env['division.programme.rel'].sudo()
        Programme = self.env['kcca.programme'].sudo()

        allowed = set(self.env['res.config.settings'].get_allowed_programme_codes())

        # 1) Remove non-allowed implementing relations (non-direct only)
        rem1 = Rel.search([('is_direct', '=', False), ('programme_id.code', 'not in', list(allowed))])
        removed_non_allowed = len(rem1)
        if rem1:
            rem1.unlink()

        # 2) Normalize DEMO programmes: only direct to owner division
        demo_programmes = Programme.search([('code', 'like', '%-DP%')])
        removed_demo_cross = 0
        marked_demo_direct = 0
        if demo_programmes:
            demo_rels = Rel.search([('programme_id', 'in', demo_programmes.ids)])
            # Remove cross-division relations for DEMO programmes
            to_remove = demo_rels.filtered(lambda r: r.programme_id.division_id and r.division_id != r.programme_id.division_id)
            removed_demo_cross = len(to_remove)
            if to_remove:
                to_remove.unlink()
            # Ensure owner relations are marked direct
            owners = Rel.search([('programme_id', 'in', demo_programmes.ids)])
            if owners:
                owners.write({'is_direct': True})
                marked_demo_direct = len(owners)

        # 3) Verify per-division counts after cleanup (optional summary)
        summary = {}
        for division in self.env['kcca.division'].search([]):
            codes = set(division.division_programme_rel_ids.filtered(lambda r: not r.is_direct).mapped('programme_id.code'))
            summary[division.name] = {
                'implementing_count': len(codes),
                'extras': sorted(list(codes - allowed)),
                'missing': sorted(list(allowed - codes)),
            }

        return {
            'removed_non_allowed': removed_non_allowed,
            'removed_demo_cross': removed_demo_cross,
            'marked_demo_direct': marked_demo_direct,
            'summary': summary,
        }

    @api.depends('implementing_programme_ids')
    def _compute_implementation_coverage(self):
        """Compute coverage as percentage of all available programmes implemented by this division."""
        Programme = self.env['kcca.programme']
        total_programmes = Programme.search_count([])
        for rec in self:
            if total_programmes:
                rec.implementation_coverage_percent = round((rec.implementing_programme_count / total_programmes) * 100.0, 2)
            else:
                rec.implementation_coverage_percent = 0.0

    def _compute_pi_stats(self):
        """Compute direct and programme indicator stats and a simple status distribution.

        - direct: performance.indicator with responsible_division_id == division
        - programme: performance.indicator whose parent_programme_id is in implementing_programme_ids
        Status distribution considers programme indicators as the broader performance picture.
        """
        Indicator = self.env['performance.indicator']
        for rec in self:
            # Direct KPIs owned by division
            direct_inds = Indicator.search([('responsible_division_id', '=', rec.id)])
            rec.direct_pi_count = len(direct_inds)
            if direct_inds:
                rec.direct_pi_avg = round(sum(direct_inds.mapped('achievement_percentage')) / len(direct_inds), 2)
            else:
                rec.direct_pi_avg = 0.0

            # Programme KPIs across implementing programmes
            prog_inds = Indicator.browse()
            if rec.implementing_programme_ids:
                prog_inds = Indicator.search([('parent_programme_id', 'in', rec.implementing_programme_ids.ids)])
            rec.programme_pi_count = len(prog_inds)
            if prog_inds:
                rec.programme_pi_avg = round(sum(prog_inds.mapped('achievement_percentage')) / len(prog_inds), 2)
            else:
                rec.programme_pi_avg = 0.0

            # Status distribution (using programme indicators to reflect overall picture)
            high = medium = low = none = 0
            for ind in prog_inds:
                ach = ind.achievement_percentage or 0.0
                if ach == 0:
                    none += 1
                elif ach >= 80:
                    high += 1
                elif ach >= 50:
                    medium += 1
                else:
                    low += 1
            rec.pi_high_count = high
            rec.pi_medium_count = medium
            rec.pi_low_count = low
            rec.pi_none_count = none

    # --- Maintenance utilities ---
    @api.model
    def recompute_all_performance(self):
        """Recompute and clamp stored performance fields across PMIS models.

        This addresses stale values persisted before clamps were introduced.
        """
        # Programmes
        progs = self.env['kcca.programme'].sudo().search([])
        if progs:
            progs._compute_performance()
            progs.flush_recordset()

        # Division-Programme relationships
        rels = self.env['division.programme.rel'].sudo().search([])
        if rels:
            rels._compute_budget_utilization()
            rels._compute_beneficiary_achievement()
            rels._compute_completion_percentage()
            rels._compute_performance_score()
            rels._compute_status_indicators()
            rels.flush_recordset()

        # Divisions
        divs = self.sudo().search([])
        if divs:
            divs._compute_counts()
            divs._compute_performance()
            divs._compute_pi_stats()
            divs.flush_recordset()

        return {
            'programmes': len(progs),
            'relations': len(rels),
            'divisions': len(divs),
        }
