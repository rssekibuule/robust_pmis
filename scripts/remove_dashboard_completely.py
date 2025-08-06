#!/usr/bin/env python3
"""
Script to completely remove all dashboard references from the KCCA PMIS system
Run this script to clean up any remaining dashboard references in the database
"""

import psycopg2
import sys

def remove_dashboard_references():
    """Remove all dashboard references from the database"""
    
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            database="robust_pmis",
            user="odoo",
            password="odoo",
            port="5432"
        )
        
        cur = conn.cursor()
        
        print("🗑️  Removing dashboard references from database...")
        
        # Remove dashboard actions (using correct PostgreSQL table names)
        queries = [
            "DELETE FROM ir_act_window WHERE name ILIKE '%dashboard%' AND name ILIKE '%kcca%';",
            "DELETE FROM ir_act_window WHERE name ILIKE '%strategic performance dashboard%';",
            "DELETE FROM ir_act_client WHERE tag ILIKE '%dashboard%' AND tag ILIKE '%kcca%';",
            "DELETE FROM ir_act_client WHERE name ILIKE '%dashboard%' AND name ILIKE '%kcca%';",
            "DELETE FROM ir_act_client WHERE name ILIKE '%strategic performance dashboard%';",

            # Remove dashboard menu items
            "DELETE FROM ir_ui_menu WHERE name ILIKE '%strategic performance dashboard%';",
            "DELETE FROM ir_ui_menu WHERE name = '📊 Strategic Performance Dashboard';",
            "DELETE FROM ir_ui_menu WHERE name ILIKE '%kcca dashboard%';",

            # Remove user action references
            "UPDATE res_users SET action_id = NULL WHERE action_id IN (SELECT id FROM ir_act_window WHERE name ILIKE '%dashboard%');",
            "UPDATE res_users SET action_id = NULL WHERE action_id IN (SELECT id FROM ir_act_client WHERE name ILIKE '%dashboard%');",

            # Clear caches and attachments
            "DELETE FROM ir_attachment WHERE name ILIKE '%dashboard%' AND res_model ILIKE '%menu%';",
        ]
        
        for query in queries:
            try:
                cur.execute(query)
                affected_rows = cur.rowcount
                if affected_rows > 0:
                    print(f"✅ Executed: {query[:50]}... (affected {affected_rows} rows)")
                else:
                    print(f"ℹ️  No rows affected: {query[:50]}...")
            except Exception as e:
                print(f"⚠️  Error executing query: {query[:50]}... - {str(e)}")
        
        # Commit changes
        conn.commit()
        print("✅ All dashboard references removed successfully!")
        print("🔄 Please refresh your browser and clear browser cache.")
        
    except Exception as e:
        print(f"❌ Error connecting to database: {str(e)}")
        print("Make sure PostgreSQL is running and credentials are correct.")
        return False
    
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
    
    return True

if __name__ == "__main__":
    print("🚀 KCCA PMIS Dashboard Cleanup Script")
    print("=====================================")
    
    confirm = input("This will permanently remove all dashboard references. Continue? (y/N): ")
    if confirm.lower() != 'y':
        print("❌ Operation cancelled.")
        sys.exit(0)
    
    success = remove_dashboard_references()
    
    if success:
        print("\n🎉 Dashboard cleanup completed!")
        print("📝 Next steps:")
        print("   1. Refresh your browser (Ctrl+F5 or Cmd+Shift+R)")
        print("   2. Clear browser cache")
        print("   3. Log out and log back in to Odoo")
    else:
        print("\n❌ Dashboard cleanup failed!")
        sys.exit(1)
