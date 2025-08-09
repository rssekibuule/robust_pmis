#!/usr/bin/env python3
"""
Script to remove divisions that have zero programmes from the database.
This cleans up divisions that were created by mistake during data import processes.
"""

import sys
import os

# Add Odoo directory to Python path
sys.path.insert(0, '/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config

def cleanup_empty_divisions():
    """Remove divisions that have zero programmes"""
    
    # Initialize Odoo
    config.parse_config(['-d', 'robust_pmis'])
    
    with odoo.registry('robust_pmis').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        # Get all divisions
        divisions = env['kcca.division'].search([])
        print(f"Total divisions found: {len(divisions)}")
        
        divisions_to_delete = []
        divisions_with_programmes = []
        
        for division in divisions:
            # Count programmes for this division using the relationship table
            programme_count = env['division.programme.rel'].search_count([
                ('division_id', '=', division.id)
            ])
            
            if programme_count == 0:
                divisions_to_delete.append(division)
                print(f"Division to delete: {division.name} ({division.code}) - {programme_count} programmes")
            else:
                divisions_with_programmes.append(division)
                print(f"Division to keep: {division.name} ({division.code}) - {programme_count} programmes")
        
        print(f"\nSummary:")
        print(f"Divisions with programmes (to keep): {len(divisions_with_programmes)}")
        print(f"Divisions without programmes (to delete): {len(divisions_to_delete)}")
        
        if divisions_to_delete:
            print(f"\nDivisions that will be deleted:")
            for div in divisions_to_delete:
                print(f"- {div.name} ({div.code})")
            
            # Ask for confirmation
            response = input(f"\nDo you want to delete these {len(divisions_to_delete)} divisions? (yes/no): ").strip().lower()
            
            if response in ['yes', 'y']:
                try:
                    # Convert list to recordset and delete the divisions
                    division_recordset = env['kcca.division'].browse([div.id for div in divisions_to_delete])
                    division_recordset.unlink()
                    cr.commit()
                    print(f"✅ Successfully deleted {len(divisions_to_delete)} divisions with zero programmes")
                    
                    # Verify the deletion
                    remaining_divisions = env['kcca.division'].search([])
                    print(f"✅ Remaining divisions in database: {len(remaining_divisions)}")
                    
                except Exception as e:
                    cr.rollback()
                    print(f"❌ Error deleting divisions: {e}")
            else:
                print("❌ Operation cancelled by user")
        else:
            print("✅ No divisions with zero programmes found. Database is clean.")

if __name__ == '__main__':
    cleanup_empty_divisions()
