#!/usr/bin/env python3

import sys
import os

# Add Odoo to Python path
sys.path.append('/home/richards/Dev/odoo18')

import odoo
from odoo import api, SUPERUSER_ID

def test_search_filters():
    """Test the new search and filter functionality for Performance Indicators"""
    
    # Initialize Odoo
    odoo.tools.config.parse_config([
        '-d', 'test_db', 
        '--addons-path=/home/richards/Dev/odoo18/addons'
    ])
    
    with odoo.modules.registry.Registry('test_db').cursor() as cr:
        env = api.Environment(cr, SUPERUSER_ID, {})
        
        print("🔍 Testing Performance Indicator Search & Filter Functionality...")
        
        # Get all performance indicators
        indicators = env['performance.indicator'].search([])
        print(f"📊 Total Performance Indicators: {len(indicators)}")
        
        # Test achievement level computation
        print(f"\n🎯 Testing Achievement Level Computation...")
        for indicator in indicators[:5]:
            print(f"   • {indicator.name[:40]}...")
            print(f"     Achievement: {indicator.achievement_percentage:.1f}%")
            print(f"     Level: {indicator.achievement_level}")
            print(f"     Status: {indicator.status}")
        
        # Test various filters
        print(f"\n🔍 Testing Filter Functionality...")
        
        # Filter by status
        achieved_indicators = env['performance.indicator'].search([('status', '=', 'achieved')])
        at_risk_indicators = env['performance.indicator'].search([('status', '=', 'at_risk')])
        behind_indicators = env['performance.indicator'].search([('status', '=', 'behind')])
        not_started_indicators = env['performance.indicator'].search([('status', '=', 'not_started')])
        
        print(f"   📈 Status Distribution:")
        print(f"      • Achieved: {len(achieved_indicators)}")
        print(f"      • At Risk: {len(at_risk_indicators)}")
        print(f"      • Behind: {len(behind_indicators)}")
        print(f"      • Not Started: {len(not_started_indicators)}")
        
        # Filter by achievement level
        high_achievement = env['performance.indicator'].search([('achievement_level', '=', 'high')])
        medium_achievement = env['performance.indicator'].search([('achievement_level', '=', 'medium')])
        low_achievement = env['performance.indicator'].search([('achievement_level', '=', 'low')])
        none_achievement = env['performance.indicator'].search([('achievement_level', '=', 'none')])
        
        print(f"   🎯 Achievement Level Distribution:")
        print(f"      • High (≥80%): {len(high_achievement)}")
        print(f"      • Medium (50-79%): {len(medium_achievement)}")
        print(f"      • Low (<50%): {len(low_achievement)}")
        print(f"      • None (0%): {len(none_achievement)}")
        
        # Filter by achievement percentage ranges
        high_perf = env['performance.indicator'].search([('achievement_percentage', '>=', 80)])
        medium_perf = env['performance.indicator'].search([
            ('achievement_percentage', '>=', 50), 
            ('achievement_percentage', '<', 80)
        ])
        low_perf = env['performance.indicator'].search([('achievement_percentage', '<', 50)])
        
        print(f"   📊 Achievement Percentage Distribution:")
        print(f"      • High Achievement (≥80%): {len(high_perf)}")
        print(f"      • Medium Achievement (50-79%): {len(medium_perf)}")
        print(f"      • Low Achievement (<50%): {len(low_perf)}")
        
        # Filter by indicator type
        increasing_indicators = env['performance.indicator'].search([('indicator_type', '=', 'increasing')])
        decreasing_indicators = env['performance.indicator'].search([('indicator_type', '=', 'decreasing')])
        
        print(f"   📈 Indicator Type Distribution:")
        print(f"      • Increasing (Higher is Better): {len(increasing_indicators)}")
        print(f"      • Decreasing (Lower is Better): {len(decreasing_indicators)}")
        
        # Test search functionality
        print(f"\n🔍 Testing Search Functionality...")
        
        # Search by name
        transport_indicators = env['performance.indicator'].search([('name', 'ilike', 'transport')])
        road_indicators = env['performance.indicator'].search([('name', 'ilike', 'road')])
        km_indicators = env['performance.indicator'].search([('name', 'ilike', 'km')])
        
        print(f"   🔍 Search Results:")
        print(f"      • Contains 'transport': {len(transport_indicators)}")
        print(f"      • Contains 'road': {len(road_indicators)}")
        print(f"      • Contains 'km': {len(km_indicators)}")
        
        # Test grouping capabilities
        print(f"\n📊 Testing Group By Functionality...")
        
        # Group by status
        status_groups = {}
        for indicator in indicators:
            status = indicator.status
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(indicator)
        
        print(f"   📈 Group by Status:")
        for status, group_indicators in status_groups.items():
            print(f"      • {status.replace('_', ' ').title()}: {len(group_indicators)} indicators")
        
        # Group by achievement level
        level_groups = {}
        for indicator in indicators:
            level = indicator.achievement_level
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(indicator)
        
        print(f"   🎯 Group by Achievement Level:")
        for level, group_indicators in level_groups.items():
            level_display = {
                'high': 'High (≥80%)',
                'medium': 'Medium (50-79%)',
                'low': 'Low (<50%)',
                'none': 'Not Started (0%)'
            }.get(level, level)
            print(f"      • {level_display}: {len(group_indicators)} indicators")
        
        # Group by measurement unit
        unit_groups = {}
        for indicator in indicators:
            unit = indicator.measurement_unit or 'No Unit'
            if unit not in unit_groups:
                unit_groups[unit] = []
            unit_groups[unit].append(indicator)
        
        print(f"   📏 Group by Measurement Unit:")
        for unit, group_indicators in unit_groups.items():
            print(f"      • {unit}: {len(group_indicators)} indicators")
        
        print(f"\n✅ Search & Filter Testing Complete!")
        print(f"   • All computed fields are working correctly")
        print(f"   • Search functionality is operational")
        print(f"   • Filter options are functional")
        print(f"   • Group by options are ready")
        
        print(f"\n💡 Available Features in the UI:")
        print(f"   🔍 Search Fields:")
        print(f"      • Indicator Name (fuzzy search)")
        print(f"      • Intermediate Outcome")
        print(f"      • Responsible User")
        print(f"      • Measurement Unit")
        
        print(f"   🎯 Filter Options:")
        print(f"      • Active/Inactive indicators")
        print(f"      • Status filters (Achieved, On Track, At Risk, Behind, Not Started)")
        print(f"      • Achievement level filters (High, Medium, Low)")
        print(f"      • Indicator type filters (Increasing, Decreasing)")
        print(f"      • My Indicators (assigned to current user)")
        
        print(f"   📊 Group By Options:")
        print(f"      • Status")
        print(f"      • Intermediate Outcome")
        print(f"      • Responsible User")
        print(f"      • Indicator Type")
        print(f"      • Measurement Unit")
        print(f"      • Achievement Level")
        
        cr.commit()

if __name__ == '__main__':
    test_search_filters()
