#!/usr/bin/env python3
# Recompute and clamp PMIS performance fields
import sys
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

def main():
    db = 'robust_pmis'
    odoo.tools.config.parse_config(['-d', db])
    registry = odoo.registry(db)
    with registry.cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        res = env['kcca.division'].recompute_all_performance()
        env.cr.commit()
        print(f"Recomputed: {res}")

if __name__ == '__main__':
    main()
