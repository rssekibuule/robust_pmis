#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config
from odoo.modules.registry import Registry

def cleanup_zero_programme_divisions():
    """Remove divisions that have zero programmes"""
    
    # Configure Odoo
    config.parse_config(['-d', 'robust_pmis'])
    registry = Registry.new('robust_pmis')
    
    with api.Environment.manage():
        env = api.Environment(registry, SUPERUSER_ID, {})
        
        # Get all divisions
        divisions = env['kcca.division'].search([])
        zero_prog_divisions = []
        
        print('=== DIVISION PROGRAMME COUNT ANALYSIS ===')
        print(f'Total divisions found: {len(divisions)}')
        print()
        
        for division in divisions:
            try:
                prog_count = len(division.programme_ids) if division.programme_ids else 0
                if prog_count == 0:
                    zero_prog_divisions.append(division)
                    print(f'❌ {division.name} ({division.code}) - {prog_count} programmes - MARKED FOR REMOVAL')
                else:
                    print(f'✅ {division.name} ({division.code}) - {prog_count} programmes')
            except Exception as e:
                print(f'⚠️  Error checking {division.name}: {str(e)}')
        
        print()
        print(f'Summary: {len(zero_prog_divisions)} divisions with zero programmes will be removed')
        print(f'Remaining: {len(divisions) - len(zero_prog_divisions)} divisions with programmes')
        
        if zero_prog_divisions:
            print()
            print('=== REMOVING DIVISIONS WITH ZERO PROGRAMMES ===')
            for division in zero_prog_divisions:
                try:
                    print(f'Removing: {division.name} ({division.code})')
                    division.unlink()
                    print(f'✅ Successfully removed {division.name}')
                except Exception as e:
                    print(f'❌ Error removing {division.name}: {str(e)}')
            
            print()
            print('=== CLEANUP COMPLETED ===')
            
            # Verify final count
            remaining_divisions = env['kcca.division'].search([])
            print(f'Final division count: {len(remaining_divisions)}')
            
            # Update dashboard counters
            try:
                dashboard = env['performance.dashboard'].search([], limit=1)
                if dashboard:
                    dashboard._compute_total_divisions()
                    print(f'Updated dashboard division count: {dashboard.total_divisions}')
            except Exception as e:
                print(f'Warning: Could not update dashboard: {str(e)}')
        
        else:
            print('No divisions with zero programmes found. No cleanup needed.')

if __name__ == '__main__':
    cleanup_zero_programme_divisions()
