# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Post-migrate hook: ensure no duplicate Strategic Goals seeded by demo scripts.
    Keeps the XML-defined 'Improve Urban Infrastructure' and removes others with same name.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    SG = env['strategic.goal']

    def dedupe(name, xmlid=None):
        keep = False
        if xmlid:
            try:
                keep = env.ref(xmlid)
            except Exception:
                keep = False
        if not keep:
            keep = SG.search([('name', '=', name)], limit=1)
        if not keep:
            return 0
        dups = SG.search([('name', '=', name), ('id', '!=', keep.id)])
        count = len(dups)
        if count:
            dups.unlink()
        return count

    removed = 0
    removed += dedupe('Improve Urban Infrastructure', 'robust_pmis.strategic_goal_improve_urban_infrastructure')
    removed += dedupe('Enhance Service Delivery')
    removed += dedupe('Strengthen Revenue Collection')
    # Log to server output
    print('[migration 18.0.1.0.2] Removed duplicate strategic goals:', removed)

