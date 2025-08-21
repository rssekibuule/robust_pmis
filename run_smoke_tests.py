#!/usr/bin/env python3
# Lightweight runner to execute smoke tests within an Odoo environment.
import sys
import os
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID


def main():
    db = os.environ.get('ODOO_DB', 'robust_pmis')
    addons_path = os.environ.get('ODOO_ADDONS_PATH', '/home/richards/Dev/odoo18/addons')
    odoo.tools.config.parse_config(['-d', db, f'--addons-path={addons_path}'])
    with odoo.api.Environment.manage():
        registry = odoo.modules.registry.Registry(db)
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})
            from robust_pmis.tests import test_dashboard_filters
            ok = test_dashboard_filters.run(env)
            cr.commit()
            print('Smoke tests completed:', 'PASS' if ok else 'FAIL')


if __name__ == '__main__':
    main()
