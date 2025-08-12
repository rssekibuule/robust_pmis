# -*- coding: utf-8 -*-

from odoo import api, models


class IrActionsActWindowCleanup(models.Model):
    _inherit = 'ir.actions.act_window'

    @api.model
    def fix_legacy_tree_view_modes(self):
        """Convert any legacy 'tree' view types to Odoo 18 'list' on actions.
        - Normalize view_mode string
        - Normalize child ir.actions.act_window.view records
        Returns count of actions and views updated.
        """
        updated_actions = 0
        updated_views = 0

        # 1) Fix actions whose view_mode contains 'tree'
        actions = self.search([('view_mode', 'ilike', 'tree')])
        for act in actions:
            modes = [m.strip() for m in (act.view_mode or '').split(',') if m.strip()]
            if not modes:
                continue
            new_modes = []
            seen = set()
            for m in modes:
                nm = 'list' if m == 'tree' else m
                if nm not in seen:
                    seen.add(nm)
                    new_modes.append(nm)
            if new_modes != modes:
                act.view_mode = ','.join(new_modes)
                updated_actions += 1

        # 2) Fix act_window.view children that still have 'tree'
        ViewRel = self.env['ir.actions.act_window.view']
        rels = ViewRel.search([('view_mode', '=', 'tree')])
        for rel in rels:
            rel.view_mode = 'list'
            updated_views += 1

        # 3) Optional: ensure there is at least a list view when expected
        # Do not create new views; rely on existing list views already defined in our module

        return {
            'updated_actions': updated_actions,
            'updated_views': updated_views,
        }

