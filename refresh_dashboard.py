#!/usr/bin/env python3
# Script to refresh dashboard data

import sys
import os

# Add the Odoo path to sys.path
sys.path.insert(0, '/home/richards/Dev/odoo18')
os.environ['PYTHONPATH'] = '/home/richards/Dev/odoo18'

import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools import config

# Configure Odoo
config['db_host'] = 'localhost'
config['db_user'] = 'richards'
config['db_password'] = ''
config['db_name'] = 'robust_pmis'
config['db_port'] = 5432

# Initialize Odoo
odoo.tools.config.parse_config([])

def refresh_dashboard():
    try:
        # Initialize database connection
        import psycopg2
        
        print("=== Checking data counts via direct database access ===")
        
        # Connect directly to database
        conn = psycopg2.connect(
            host='localhost',
            database='robust_pmis',
            user='richards',
            password=''
        )
        cur = conn.cursor()
        
        # Check actual data counts
        cur.execute("SELECT COUNT(*) FROM strategic_goal;")
        goals_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM key_result_area;")
        kras_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM key_performance_indicator;")
        kpis_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM kcca_programme;")
        programmes_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM kcca_directorate;")
        directorates_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM kcca_division;")
        divisions_count = cur.fetchone()[0]
        
        print(f"Strategic Goals: {goals_count}")
        print(f"KRAs: {kras_count}")
        print(f"KPIs: {kpis_count}")
        print(f"Programmes: {programmes_count}")
        print(f"Directorates: {directorates_count}")
        print(f"Divisions: {divisions_count}")
        
        # Update dashboard record manually
        print("\n=== Updating dashboard record ===")
        
        # Check if dashboard record exists
        cur.execute("SELECT id FROM performance_dashboard LIMIT 1;")
        result = cur.fetchone()
        
        if result:
            dashboard_id = result[0]
            print(f"Found dashboard record with ID: {dashboard_id}")
            
            # Update the dashboard record with actual counts
            cur.execute("""
                UPDATE performance_dashboard 
                SET total_goals = %s,
                    total_strategic_goals = %s,
                    total_kras = %s,
                    total_kpis = %s,
                    total_programmes = %s,
                    total_directorates = %s,
                    total_divisions = %s
                WHERE id = %s
            """, (goals_count, goals_count, kras_count, kpis_count, 
                  programmes_count, directorates_count, divisions_count, dashboard_id))
            
        else:
            print("Creating new dashboard record...")
            cur.execute("""
                INSERT INTO performance_dashboard 
                (name, total_goals, total_strategic_goals, total_kras, total_kpis, 
                 total_programmes, total_directorates, total_divisions, create_date, write_date, create_uid, write_uid)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), 1, 1)
            """, ('KCCA Executive Performance Dashboard', goals_count, goals_count, 
                  kras_count, kpis_count, programmes_count, directorates_count, divisions_count))
        
        # Commit changes
        conn.commit()
        
        # Verify the update
        cur.execute("SELECT * FROM performance_dashboard;")
        dashboard_data = cur.fetchall()
        
        print("\n=== Dashboard record after update ===")
        for row in dashboard_data:
            print(f"Dashboard ID: {row[0]}")
            print(f"Name: {row[1]}")
            print(f"Goals: {row[2] if len(row) > 2 else 'N/A'}")
            print(f"Strategic Goals: {row[3] if len(row) > 3 else 'N/A'}")
            print(f"KRAs: {row[4] if len(row) > 4 else 'N/A'}")
            print(f"KPIs: {row[6] if len(row) > 6 else 'N/A'}")
            print(f"Programmes: {row[7] if len(row) > 7 else 'N/A'}")
            print(f"Directorates: {row[9] if len(row) > 9 else 'N/A'}")
            print(f"Divisions: {row[11] if len(row) > 11 else 'N/A'}")
        
        conn.close()
        print("\nDashboard refresh completed successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    refresh_dashboard()
