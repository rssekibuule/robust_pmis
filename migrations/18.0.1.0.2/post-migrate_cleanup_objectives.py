# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    SO = env['strategic.objective']

    def dedupe(goal_xmlid, keep_xmlid, name):
        try:
            goal = env.ref(goal_xmlid)
        except Exception:
            return 0
        try:
            keep = env.ref(keep_xmlid)
        except Exception:
            keep = SO.search([
                ('strategic_goal_id', '=', goal.id), ('name', '=', name)
            ], limit=1)
            if not keep:
                return 0
        dups = SO.search([
            ('strategic_goal_id', '=', goal.id), ('name', '=', name), ('id', '!=', keep.id)
        ])
        moved = 0
        deleted = 0
        for dup in dups:
            if dup.kra_ids:
                dup.kra_ids.write({'strategic_objective_id': keep.id})
                moved += len(dup.kra_ids)
            dup.unlink()
            deleted += 1
        if deleted:
            print(f"[migration objective] Goal '{goal.name}': kept {keep.id}, moved {moved} KRAs, deleted {deleted} dup(s)")
        return deleted

    removed = 0
    removed += dedupe('robust_pmis.strategic_goal_improve_urban_infrastructure',
                      'robust_pmis.strategic_objective_infrastructure_development_main',
                      'Infrastructure Development')
    print('[migration] Duplicate objective cleanup complete. Removed', removed)

