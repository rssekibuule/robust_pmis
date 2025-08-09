#!/usr/bin/env python3
"""
Script to identify and remove KCCA divisions with zero programmes
This should be run from the Odoo directory
"""

import psycopg2
import sys

def cleanup_divisions_with_zero_programmes():
    """Clean up divisions that have no programmes assigned"""
    
    # Database connection parameters
    DB_HOST = 'localhost'
    DB_PORT = 5432
    DB_NAME = 'robust_pmis'
    DB_USER = 'richards'
    DB_PASS = ''  # assuming no password for local connection
    
    try:
        # Connect to database
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        cur = conn.cursor()
        
        print("=== ANALYZING DIVISIONS WITH ZERO PROGRAMMES ===")
        
        # Find divisions with zero programmes
        query = """
        SELECT d.id, d.name, d.code, COUNT(dpr.programme_id) as programme_count
        FROM kcca_division d
        LEFT JOIN division_programme_rel dpr ON d.id = dpr.division_id
        GROUP BY d.id, d.name, d.code
        HAVING COUNT(dpr.programme_id) = 0
        ORDER BY d.name;
        """
        
        cur.execute(query)
        zero_divisions = cur.fetchall()
        
        if not zero_divisions:
            print("✅ No divisions with zero programmes found.")
            return
        
        print(f"Found {len(zero_divisions)} divisions with zero programmes:")
        print()
        
        for div_id, name, code, count in zero_divisions:
            print(f"❌ {name} ({code}) - ID: {div_id}")
        
        # Confirm deletion
        print(f"\n⚠️  This will DELETE {len(zero_divisions)} divisions from the database.")
        response = input("Do you want to proceed? (yes/no): ").strip().lower()
        
        if response != 'yes':
            print("❌ Operation cancelled.")
            return
        
        print("\n=== REMOVING DIVISIONS ===")
        
        # Delete divisions with zero programmes
        division_ids = [str(div[0]) for div in zero_divisions]
        delete_query = f"DELETE FROM kcca_division WHERE id IN ({','.join(division_ids)});"
        
        cur.execute(delete_query)
        deleted_count = cur.rowcount
        
        # Commit changes
        conn.commit()
        
        print(f"✅ Successfully removed {deleted_count} divisions with zero programmes")
        
        # Verify remaining divisions
        cur.execute("SELECT COUNT(*) FROM kcca_division;")
        remaining_count = cur.fetchone()[0]
        print(f"📊 Remaining divisions in database: {remaining_count}")
        
        # Show remaining divisions with programme counts
        print("\n=== REMAINING DIVISIONS ===")
        query = """
        SELECT d.name, d.code, COUNT(dpr.programme_id) as programme_count
        FROM kcca_division d
        LEFT JOIN division_programme_rel dpr ON d.id = dpr.division_id
        GROUP BY d.id, d.name, d.code
        ORDER BY d.name;
        """
        cur.execute(query)
        remaining_divisions = cur.fetchall()
        
        for name, code, count in remaining_divisions:
            print(f"✅ {name} ({code}) - {count} programmes")
        
        print(f"\n🎉 Cleanup completed successfully!")
        print(f"Removed: {deleted_count} divisions")
        print(f"Remaining: {remaining_count} divisions")
        
    except psycopg2.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
        
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()

if __name__ == '__main__':
    cleanup_divisions_with_zero_programmes()
