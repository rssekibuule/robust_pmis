#!/usr/bin/env python3
"""
Script to move KRAs from the newly created objective (33) to the empty objective (8)
that the user wants to populate.
"""

import psycopg2
import sys

def move_kras_to_objective_8():
    """Move all KRAs from objective 33 to objective 8"""
    try:
        # Connect to database
        conn = psycopg2.connect(
            host="localhost",
            database="robust_pmis",
            user="richards",
            password=""
        )
        cur = conn.cursor()
        
        print("Moving KRAs from objective 33 to objective 8...")
        
        # Move KRAs from objective 33 to objective 8
        cur.execute("""
            UPDATE key_result_area 
            SET strategic_objective_id = 8 
            WHERE strategic_objective_id = 33
        """)
        
        kras_moved = cur.rowcount
        print(f"Moved {kras_moved} KRAs from objective 33 to objective 8")
        
        # Update XML ID reference to point to objective 8
        cur.execute("""
            UPDATE ir_model_data 
            SET res_id = 8 
            WHERE name = 'strategic_objective_infrastructure_development_main' 
            AND model = 'strategic.objective'
        """)
        
        print("Updated XML ID to point to objective 8")
        
        # Delete the now-empty objective 33
        cur.execute("DELETE FROM strategic_objective WHERE id = 33")
        print("Deleted empty objective 33")
        
        # Commit changes
        conn.commit()
        print("✅ Successfully moved demo data to objective 8!")
        
        # Verify the result
        cur.execute("""
            SELECT so.id, so.name, COUNT(kra.id) as kra_count,
                   (SELECT COUNT(kpi.id) FROM key_performance_indicator kpi 
                    JOIN key_result_area k ON kpi.kra_id = k.id 
                    WHERE k.strategic_objective_id = so.id) as kpi_count
            FROM strategic_objective so 
            LEFT JOIN key_result_area kra ON kra.strategic_objective_id = so.id 
            WHERE so.id = 8
            GROUP BY so.id, so.name
        """)
        
        result = cur.fetchone()
        if result:
            print(f"Final result: Objective {result[0]} '{result[1]}' now has {result[2]} KRAs and {result[3]} KPIs")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        if conn:
            conn.rollback()
        sys.exit(1)
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    move_kras_to_objective_8()
