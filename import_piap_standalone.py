#!/usr/bin/env python3
"""
Standalone PIAP Actions Import Script
Run this with: python3 import_piap_standalone.py
"""

import os
import sys
import psycopg2
from psycopg2.extras import RealDictCursor

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'database': 'test_db',
    'user': 'richards',
    'password': '',  # Adjust if needed
    'port': 5432
}

def get_db_connection():
    """Get database connection"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def import_piap_actions():
    """Import PIAP Actions directly to database"""
    
    print("🚀 Starting Direct PIAP Actions Import...")
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Get the transport programme ID
        cursor.execute("""
            SELECT id FROM kcca_programme 
            WHERE name = 'Integrated Transport Infrastructure and Services'
        """)
        programme_result = cursor.fetchone()
        if not programme_result:
            print("❌ Transport Programme not found!")
            return False
        
        programme_id = programme_result['id']
        print(f"✅ Found programme ID: {programme_id}")
        
        # Get objective ID
        cursor.execute("""
            SELECT id FROM programme_objective 
            WHERE programme_id = %s
            LIMIT 1
        """, (programme_id,))
        objective_result = cursor.fetchone()
        if not objective_result:
            print("❌ No objectives found!")
            return False
        
        objective_id = objective_result['id']
        print(f"✅ Found objective ID: {objective_id}")
        
        # Get outcomes
        cursor.execute("""
            SELECT id, name FROM intermediate_outcome 
            WHERE objective_id = %s
        """, (objective_id,))
        outcomes = cursor.fetchall()
        
        outcome_map = {}
        for outcome in outcomes:
            name_lower = outcome['name'].lower()
            if 'travel time' in name_lower:
                outcome_map['reduced_travel_time'] = outcome['id']
            elif 'infrastructure' in name_lower:
                outcome_map['increased_infrastructure'] = outcome['id']
            elif 'safety' in name_lower:
                outcome_map['enhanced_safety'] = outcome['id']
        
        print(f"✅ Found outcomes: {list(outcome_map.keys())}")
        
        # Get interventions and outputs
        cursor.execute("""
            SELECT i.id as intervention_id, o.id as output_id, i.outcome_id
            FROM intervention i
            JOIN output o ON o.intervention_id = i.id
            WHERE i.outcome_id IN %s
        """, (tuple(outcome_map.values()),))
        
        outputs = cursor.fetchall()
        if not outputs:
            print("❌ No outputs found!")
            return False
        
        print(f"✅ Found {len(outputs)} outputs")
        
        # Clear existing PIAP Actions
        cursor.execute("DELETE FROM piap_action WHERE programme_id = %s", (programme_id,))
        deleted_count = cursor.rowcount
        print(f"🗑️ Removed {deleted_count} existing PIAP Actions")
        
        # PIAP Actions data (first batch)
        piap_actions_data = [
            # Outcome 1.1: Reduced travel time
            {
                'name': 'Average Travel time (Minutes) on KCCA Road Links',
                'outcome_key': 'reduced_travel_time',
                'baseline_value': 4.2,
                'target_value': 3.0,
                'measurement_unit': 'Minutes',
                'budget_fy2025_26': 0.0,
                'budget_fy2026_27': 0.0,
                'budget_fy2027_28': 0.0,
                'budget_fy2028_29': 0.0,
                'budget_fy2029_30': 0.0,
                'total_budget': 0.0
            },
            {
                'name': 'Proportion of Commuters using mass public transport (Bus & BRT)',
                'outcome_key': 'reduced_travel_time',
                'baseline_value': 2.0,
                'target_value': 30.0,
                'measurement_unit': 'Percentage',
                'budget_fy2025_26': 0.0,
                'budget_fy2026_27': 0.0,
                'budget_fy2027_28': 0.0,
                'budget_fy2028_29': 0.0,
                'budget_fy2029_30': 0.0,
                'total_budget': 0.0
            },
            {
                'name': 'Km of BRT Network constructed',
                'outcome_key': 'reduced_travel_time',
                'baseline_value': 0.0,
                'target_value': 14.7,
                'measurement_unit': 'Km',
                'budget_fy2025_26': 0.0,
                'budget_fy2026_27': 0.0,
                'budget_fy2027_28': 4.4,
                'budget_fy2028_29': 5.1,
                'budget_fy2029_30': 5.0,
                'total_budget': 14.7
            },
            {
                'name': 'No of Traffic Diversion Flyovers constructed',
                'outcome_key': 'reduced_travel_time',
                'baseline_value': 2.0,
                'target_value': 4.0,
                'measurement_unit': 'Number',
                'budget_fy2025_26': 0.0,
                'budget_fy2026_27': 1.0,
                'budget_fy2027_28': 2.0,
                'budget_fy2028_29': 0.0,
                'budget_fy2029_30': 1.0,
                'total_budget': 4.0
            },
            {
                'name': 'Km of meter gauge commuter rail revamped',
                'outcome_key': 'reduced_travel_time',
                'baseline_value': 28.5,
                'target_value': 29.0,
                'measurement_unit': 'Km',
                'budget_fy2025_26': 0.0,
                'budget_fy2026_27': 0.0,
                'budget_fy2027_28': 5.0,
                'budget_fy2028_29': 3.0,
                'budget_fy2029_30': 10.4,
                'total_budget': 29.0
            }
        ]
        
        return piap_actions_data, outcome_map, outputs, cursor, conn, programme_id, objective_id
        
    except Exception as e:
        print(f"❌ Error during import: {e}")
        conn.rollback()
        return False

if __name__ == "__main__":
    result = import_piap_actions()
    if result:
        piap_actions_data, outcome_map, outputs, cursor, conn, programme_id, objective_id = result
        print(f"✅ Setup complete. Ready to import {len(piap_actions_data)} PIAP Actions")
        print("Run the full import script next...")
    else:
        print("❌ Setup failed!")
