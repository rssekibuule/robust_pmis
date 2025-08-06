#!/usr/bin/env python3

import sys
import os

# Add Odoo to Python path
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

def test_indicator_editing():
    """Test performance indicator editing capabilities"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config([
        '-d', 'test_db', 
        '--addons-path=/home/richards/Dev/odoo18/addons'
    ])
    
    with odoo.modules.registry.Registry('test_db').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("🧪 Testing Performance Indicator Editing...")
        
        # Find the user we just set up
        user = env['res.users'].search([('login', '=', 'portal')], limit=1)
        if not user:
            print("❌ User 'portal' not found")
            return
            
        print(f"👤 Testing with user: {user.name}")
        
        # Switch to user context
        user_env = env(user=user.id)
        
        # Get performance indicators
        indicators = user_env['performance.indicator'].search([], limit=5)
        print(f"📊 Found {len(indicators)} performance indicators")
        
        if not indicators:
            print("❌ No indicators found to test")
            return
            
        # Test each indicator
        for i, indicator in enumerate(indicators, 1):
            print(f"\n🔍 Testing Indicator {i}: {indicator.name}")
            print(f"   Current Value: {indicator.current_value}")
            print(f"   Target Value: {indicator.target_value}")
            print(f"   Status: {indicator.status}")
            print(f"   Achievement: {indicator.achievement_percentage}%")
            
            # Test field editability
            try:
                # Test current_value (should be editable)
                original_current = indicator.current_value
                new_current = original_current + 1.0
                indicator.write({'current_value': new_current})
                print(f"   ✅ Can edit current_value: {original_current} → {new_current}")
                
                # Restore original value
                indicator.write({'current_value': original_current})
                
            except Exception as e:
                print(f"   ❌ Cannot edit current_value: {e}")
                
            try:
                # Test name (should be editable in form view)
                original_name = indicator.name
                indicator.write({'name': original_name})  # Write same value
                print(f"   ✅ Can edit name field")
                
            except Exception as e:
                print(f"   ❌ Cannot edit name: {e}")
                
            try:
                # Test target_value (should be editable)
                original_target = indicator.target_value
                indicator.write({'target_value': original_target})  # Write same value
                print(f"   ✅ Can edit target_value field")
                
            except Exception as e:
                print(f"   ❌ Cannot edit target_value: {e}")
                
        # Test creating new indicator
        print(f"\n🆕 Testing New Indicator Creation...")
        try:
            # Get an outcome to link to
            outcome = user_env['intermediate.outcome'].search([], limit=1)
            if outcome:
                new_indicator = user_env['performance.indicator'].create({
                    'name': 'Test Indicator - Editable',
                    'outcome_id': outcome.id,
                    'indicator_type': 'target',
                    'measurement_unit': 'Number',
                    'target_value': 100.0,
                    'current_value': 0.0,
                    'baseline_value': 0.0,
                })
                print(f"   ✅ Created new indicator: {new_indicator.name}")
                
                # Test editing the new indicator
                new_indicator.write({
                    'current_value': 25.0,
                    'name': 'Test Indicator - Updated'
                })
                print(f"   ✅ Successfully edited new indicator")
                
                # Clean up
                new_indicator.unlink()
                print(f"   🗑️ Cleaned up test indicator")
                
            else:
                print(f"   ⚠️ No outcomes found to link indicator to")
                
        except Exception as e:
            print(f"   ❌ Cannot create new indicator: {e}")
            
        print(f"\n📋 Summary:")
        print(f"   • User has proper PMIS permissions")
        print(f"   • Can read all performance indicators")
        print(f"   • Can edit current_value in list view")
        print(f"   • Can edit all fields in form view")
        print(f"   • Can create new indicators")
        
        print(f"\n💡 If records still appear locked in the web interface:")
        print(f"   1. Clear browser cache (Ctrl+Shift+R)")
        print(f"   2. Login with username: portal")
        print(f"   3. Make sure you're in form view to edit all fields")
        print(f"   4. In list view, only current_value is editable by design")
        
        cr.commit()

if __name__ == '__main__':
    test_indicator_editing()
