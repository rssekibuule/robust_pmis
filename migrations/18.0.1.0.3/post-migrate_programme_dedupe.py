# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID

def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    P = env['kcca.programme']

    # Build case-insensitive name groups
    groups = {}
    for p in P.search([]):
        key = (p.name or '').strip().lower()
        groups.setdefault(key, []).append(p)

    removed = 0
    rels_migrated = 0
    for key, recs in groups.items():
        if not key or len(recs) == 1:
            continue
        # Choose canonical to keep: prefer record with the most links
        keep = max(recs, key=lambda r: (
            len(r.implementing_directorate_ids) + len(r.implementing_division_ids) +
            len(r.objective_ids) + len(r.performance_indicator_ids) +
            len(r.strategic_objective_ids)
        ))
        for dup in recs:
            if dup.id == keep.id:
                continue
            # Merge M2M links: objectives and directorates/divisions
            if dup.strategic_objective_ids:
                keep.strategic_objective_ids = [(4, oid) for oid in dup.strategic_objective_ids.ids] + keep.strategic_objective_ids._origin
            if dup.implementing_directorate_ids:
                keep.implementing_directorate_ids = [(4, did) for did in dup.implementing_directorate_ids.ids] + keep.implementing_directorate_ids._origin
            # Division links are computed via division_programme_rel_ids, but keep any legacy division_id
            if dup.division_programme_rel_ids:
                # Reassign division rels to keep
                dup.division_programme_rel_ids.write({'programme_id': keep.id})
            if dup.programme_directorate_rel_ids:
                dup.programme_directorate_rel_ids.write({'programme_id': keep.id})
            if dup.objective_ids:
                dup.objective_ids.write({'programme_id': keep.id})
            if dup.performance_indicator_ids:
                dup.performance_indicator_ids.write({'programme_id': keep.id})
            if dup.directorate_id and not keep.directorate_id:
                keep.directorate_id = dup.directorate_id
            if dup.division_id and not keep.division_id:
                keep.division_id = dup.division_id

            rels_migrated += 1
            dup.unlink()
            removed += 1
    print(f"[migration] Programme dedupe complete. Removed {removed} duplicates; migrated relationships for {rels_migrated} records.")

