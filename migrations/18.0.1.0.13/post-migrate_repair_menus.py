# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    """Repair menus that reference deleted actions and reset user home actions.

    - If a menu's action points to a non-existing record, and the menu name suggests
      dashboards/KPIs/performance, point it to our unified KPI hub client action.
    - Otherwise, clear the action to avoid webclient load_menus crashes.
    - Also reset any user.home action_id that points to a deleted action.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    # Try to retrieve the unified KPI dashboard action
    unified = env.ref('robust_pmis.action_unified_kpi_dashboard', raise_if_not_found=False)

    Menu = env['ir.ui.menu'].sudo()
    broken = []
    for m in Menu.search([('action', '!=', False)]):
        try:
            model, rid = m.action.split(',')
            rid = int(rid)
            rec = env[model].browse(rid)
            if not rec.exists():
                broken.append(m)
        except Exception:
            broken.append(m)

    fixed = 0
    cleared = 0
    for m in broken:
        target = False
        lname = (m.name or '').lower()
        if unified and ('dashboard' in lname or 'kpi' in lname or 'performance' in lname):
            target = f"{unified._name},{unified.id}"
        if target:
            m.write({'action': target})
            fixed += 1
        else:
            m.write({'action': False})
            cleared += 1

    # Reset users pointing to dead actions
    Users = env['res.users'].sudo().search([])
    reset = 0
    for u in Users:
        if u.action_id and not u.action_id.exists():
            u.action_id = False
            reset += 1

    # Log to server output for visibility
    print(f"[migrate 18.0.1.0.13] Menu actions repaired: fixed={fixed}, cleared={cleared}; users reset action_id={reset}")
