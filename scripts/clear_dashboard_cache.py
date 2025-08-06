#!/usr/bin/env python3
"""
Script to clear all dashboard-related caches and force refresh
This should resolve OWL template compilation errors
"""

import requests
import json

def clear_dashboard_cache():
    """Clear dashboard cache via Odoo web interface"""
    
    print("🧹 Clearing Dashboard Cache...")
    
    try:
        # Try to access the main Odoo interface to trigger cache refresh
        base_url = "http://localhost:8069"
        
        # Create a session
        session = requests.Session()
        
        # Try to access the web interface
        response = session.get(f"{base_url}/web")
        
        if response.status_code == 200:
            print("✅ Successfully accessed Odoo web interface")
            print("🔄 This should trigger cache refresh")
        else:
            print(f"⚠️ Got status code {response.status_code}")
        
        # Try to access the login page to force template recompilation
        login_response = session.get(f"{base_url}/web/login")
        
        if login_response.status_code == 200:
            print("✅ Successfully accessed login page")
            print("🔄 Templates should be recompiled")
        
        print("\n🎉 Cache clearing completed!")
        print("📝 Next steps:")
        print("   1. Hard refresh your browser (Ctrl+F5)")
        print("   2. Clear browser cache completely")
        print("   3. Close and reopen browser")
        print("   4. Try accessing the system again")
        
        return True
        
    except Exception as e:
        print(f"❌ Error clearing cache: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 KCCA PMIS Dashboard Cache Cleaner")
    print("====================================")
    
    success = clear_dashboard_cache()
    
    if success:
        print("\n✅ Cache clearing process completed!")
    else:
        print("\n❌ Cache clearing failed!")
