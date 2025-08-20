#!/usr/bin/env python3
# Verify clamped performance fields are within [0, 100]
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

        def count_out_of_bounds(model, field):
            over = env[model].search_count([(field, '>', 100)])
            under = env[model].search_count([(field, '<', 0)])
            return over, under

        checks = [
            ('kcca.programme', 'overall_performance'),
            ('division.programme.rel', 'performance_score'),
            ('division.programme.rel', 'budget_utilization'),
            ('division.programme.rel', 'beneficiary_achievement'),
            ('division.programme.rel', 'completion_percentage'),
            ('kcca.division', 'overall_performance'),
        ]

        print('Out-of-bounds counts (over>100, under<0):')
        for model, field in checks:
            over, under = count_out_of_bounds(model, field)
            print(f"{model}.{field}: over={over}, under={under}")

if __name__ == '__main__':
    main()
