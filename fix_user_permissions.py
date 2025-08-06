#!/usr/bin/env python3

import sys
import os

# Add Odoo to Python path
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

def fix_user_permissions():
    """Fix user permissions for PMIS module"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config([
        '-d', 'test_db', 
        '--addons-path=/home/richards/Dev/odoo18/addons'
    ])
    
    with odoo.registry('test_db').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("🔧 Fixing User Permissions for PMIS...")
        
        # Find or create a regular user (not system user)
        regular_users = env['res.users'].search([
            ('login', '!=', '__system__'),
            ('active', '=', True)
        ], limit=1)
        
        if not regular_users:
            print("📝 Creating a regular user...")
            user = env['res.users'].create({
                'name': 'PMIS Admin User',
                'login': 'pmis_admin',
                'email': 'pmis_admin@kcca.go.ug',
                'password': 'admin123',
                'active': True,
            })
        else:
            user = regular_users[0]
            
        print(f"👤 Working with user: {user.name} (Login: {user.login})")
        
        # Get PMIS groups
        pmis_admin_group = env.ref('robust_pmis.group_kcca_pmis_admin', raise_if_not_found=False)
        pmis_manager_group = env.ref('robust_pmis.group_kcca_pmis_manager', raise_if_not_found=False)
        pmis_officer_group = env.ref('robust_pmis.group_kcca_pmis_officer', raise_if_not_found=False)
        pmis_user_group = env.ref('robust_pmis.group_kcca_pmis_user', raise_if_not_found=False)
        
        # First ensure user is Internal User type
        internal_user_group = env.ref('base.group_user', raise_if_not_found=False)
        portal_group = env.ref('base.group_portal', raise_if_not_found=False)
        public_group = env.ref('base.group_public', raise_if_not_found=False)

        # Remove portal/public groups if present
        groups_to_remove = []
        if portal_group and portal_group.id in user.groups_id.ids:
            groups_to_remove.append(portal_group.id)
        if public_group and public_group.id in user.groups_id.ids:
            groups_to_remove.append(public_group.id)

        if groups_to_remove:
            user.write({
                'groups_id': [(3, group_id) for group_id in groups_to_remove]
            })
            print(f"🗑️ Removed portal/public groups")

        # Add Internal User group
        if internal_user_group and internal_user_group.id not in user.groups_id.ids:
            user.write({
                'groups_id': [(4, internal_user_group.id)]
            })
            print(f"✅ Added Internal User group")

        # Add user to PMIS Admin group for full access
        groups_to_add = []
        if pmis_admin_group:
            groups_to_add.append(pmis_admin_group.id)
            print(f"✅ Adding user to PMIS Admin group")
        if pmis_manager_group:
            groups_to_add.append(pmis_manager_group.id)
            print(f"✅ Adding user to PMIS Manager group")
        if pmis_officer_group:
            groups_to_add.append(pmis_officer_group.id)
            print(f"✅ Adding user to PMIS Officer group")
        if pmis_user_group:
            groups_to_add.append(pmis_user_group.id)
            print(f"✅ Adding user to PMIS User group")

        if groups_to_add:
            user.write({
                'groups_id': [(4, group_id) for group_id in groups_to_add]
            })
            
        # Test access to performance indicators
        print(f"\n🧪 Testing Performance Indicator Access...")
        try:
            # Switch to the user context
            user_env = env(user=user.id)
            indicators = user_env['performance.indicator'].search([], limit=5)
            print(f"✅ Can read {len(indicators)} performance indicators")
            
            if indicators:
                indicator = indicators[0]
                print(f"📊 Sample indicator: {indicator.name}")
                
                # Test write access
                try:
                    original_value = indicator.current_value
                    indicator.write({'current_value': original_value + 0.01})
                    indicator.write({'current_value': original_value})  # Restore
                    print(f"✅ Can write to performance indicators")
                except Exception as e:
                    print(f"❌ Cannot write to performance indicators: {e}")
            else:
                print(f"⚠️ No performance indicators found to test")
                
        except Exception as e:
            print(f"❌ Cannot access performance indicators: {e}")
            
        # Show final user groups
        print(f"\n📋 Final User Groups for {user.name}:")
        for group in user.groups_id:
            if 'pmis' in group.name.lower() or 'user' in group.name.lower():
                print(f"  ✅ {group.name} ({group.full_name})")
                
        print(f"\n🎉 User permissions setup complete!")
        print(f"🔑 Login credentials:")
        print(f"   Username: {user.login}")
        print(f"   Password: admin123 (if new user created)")
        print(f"   URL: http://localhost:8069")
        
        cr.commit()

if __name__ == '__main__':
    fix_user_permissions()
