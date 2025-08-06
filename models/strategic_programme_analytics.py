# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools, _
from odoo.exceptions import UserError
import json
from datetime import datetime, timedelta
from collections import defaultdict


class StrategicProgrammeAnalytics(models.Model):
    _name = 'strategic.programme.analytics'
    _description = 'Strategic-Programme Performance Analytics'
    _auto = False  # This is a reporting model

    # Strategic KPI Fields
    strategic_kpi_id = fields.Many2one('key.performance.indicator', string='Strategic KPI')
    strategic_kpi_name = fields.Char(string='Strategic KPI Name')
    kra_name = fields.Char(string='Key Result Area')
    thematic_area = fields.Selection([
        ('infrastructure', 'Infrastructure & Transport'),
        ('health', 'Health Services'),
        ('education', 'Education Services'),
        ('economic', 'Economic Development'),
        ('environment', 'Environmental Management'),
        ('governance', 'Governance & Legal'),
        ('finance', 'Revenue & Finance'),
        ('climate', 'Climate & Resilience'),
        ('citizen', 'Citizen Satisfaction'),
        ('organizational', 'Organizational Performance')
    ], string='Thematic Area')
    
    # Strategic Performance
    strategic_target = fields.Float(string='Strategic Target')
    strategic_current = fields.Float(string='Strategic Current Value')
    strategic_achievement = fields.Float(string='Strategic Achievement %')
    
    # Programme Indicator Fields
    programme_indicator_id = fields.Many2one('performance.indicator', string='Programme Indicator')
    programme_indicator_name = fields.Char(string='Programme Indicator Name')
    programme_name = fields.Char(string='Programme Name')
    
    # Programme Performance
    programme_target = fields.Float(string='Programme Target')
    programme_current = fields.Float(string='Programme Current Value')
    programme_achievement = fields.Float(string='Programme Achievement %')
    
    # Linkage Analysis
    contribution_weight = fields.Float(string='Contribution Weight %')
    impact_relationship = fields.Selection([
        ('direct', 'Direct Impact'),
        ('indirect', 'Indirect Impact'),
        ('supporting', 'Supporting Impact')
    ], string='Impact Relationship')
    
    # Performance Gap Analysis
    performance_gap = fields.Float(string='Performance Gap', help="Difference between target and current achievement")
    contribution_impact = fields.Float(string='Contribution Impact', help="Weighted contribution to strategic KPI")
    
    # Directorate Information
    responsible_directorate = fields.Char(string='Responsible Directorate')
    
    # Time Analysis
    last_update_date = fields.Datetime(string='Last Update Date')
    days_since_update = fields.Integer(string='Days Since Update')

    def init(self):
        """Create the view for strategic-programme analytics"""
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""
            CREATE OR REPLACE VIEW %s AS (
                SELECT 
                    ROW_NUMBER() OVER() AS id,
                    
                    -- Strategic KPI Information
                    kpi.id AS strategic_kpi_id,
                    kpi.name AS strategic_kpi_name,
                    kra.name AS kra_name,
                    kpi.thematic_area,
                    kpi.target_value AS strategic_target,
                    kpi.current_value AS strategic_current,
                    kpi.achievement_percentage AS strategic_achievement,
                    
                    -- Programme Indicator Information
                    pi.id AS programme_indicator_id,
                    pi.name AS programme_indicator_name,
                    prog.name AS programme_name,
                    pi.target_value AS programme_target,
                    pi.current_value AS programme_current,
                    pi.achievement_percentage AS programme_achievement,
                    
                    -- Linkage Information
                    pi.contribution_weight,
                    pi.impact_relationship,
                    
                    -- Performance Analysis
                    (pi.target_value - pi.current_value) AS performance_gap,
                    (pi.achievement_percentage * pi.contribution_weight / 100) AS contribution_impact,
                    
                    -- Directorate Information
                    dir.name AS responsible_directorate,
                    
                    -- Time Analysis
                    pi.write_date AS last_update_date,
                    EXTRACT(DAY FROM (NOW() - pi.write_date)) AS days_since_update
                    
                FROM key_performance_indicator kpi
                JOIN key_result_area kra ON kpi.kra_id = kra.id
                JOIN kpi_programme_indicator_rel rel ON kpi.id = rel.strategic_kpi_id
                JOIN performance_indicator pi ON rel.programme_indicator_id = pi.id
                LEFT JOIN kcca_programme prog ON pi.parent_programme_id = prog.id
                LEFT JOIN kcca_directorate dir ON prog.directorate_id = dir.id
                
                WHERE kpi.auto_calculate = TRUE
                ORDER BY kpi.thematic_area, kpi.name, pi.name
            )
        """ % self._table)

    @api.model
    def get_thematic_performance_summary(self):
        """Get performance summary by thematic area"""
        query = """
            SELECT 
                thematic_area,
                COUNT(DISTINCT strategic_kpi_id) as strategic_kpis_count,
                COUNT(DISTINCT programme_indicator_id) as programme_indicators_count,
                AVG(strategic_achievement) as avg_strategic_achievement,
                AVG(programme_achievement) as avg_programme_achievement,
                SUM(CASE WHEN strategic_achievement >= 80 THEN 1 ELSE 0 END) as on_track_strategic,
                SUM(CASE WHEN programme_achievement >= 80 THEN 1 ELSE 0 END) as on_track_programme
            FROM %s
            WHERE thematic_area IS NOT NULL
            GROUP BY thematic_area
            ORDER BY avg_strategic_achievement DESC
        """ % self._table
        
        self.env.cr.execute(query)
        results = self.env.cr.dictfetchall()
        
        # Calculate percentages
        for result in results:
            if result['strategic_kpis_count'] > 0:
                result['strategic_on_track_pct'] = (result['on_track_strategic'] / result['strategic_kpis_count']) * 100
            else:
                result['strategic_on_track_pct'] = 0
                
            if result['programme_indicators_count'] > 0:
                result['programme_on_track_pct'] = (result['on_track_programme'] / result['programme_indicators_count']) * 100
            else:
                result['programme_on_track_pct'] = 0
        
        return results

    @api.model
    def get_linkage_effectiveness_analysis(self):
        """Analyze the effectiveness of strategic-programme linkages"""
        query = """
            SELECT 
                strategic_kpi_name,
                thematic_area,
                strategic_achievement,
                COUNT(programme_indicator_id) as linked_indicators_count,
                AVG(programme_achievement) as avg_programme_achievement,
                SUM(contribution_impact) as total_contribution_impact,
                CASE 
                    WHEN strategic_achievement >= 80 AND AVG(programme_achievement) >= 80 THEN 'Aligned High Performance'
                    WHEN strategic_achievement >= 80 AND AVG(programme_achievement) < 80 THEN 'Strategic Success, Programme Gaps'
                    WHEN strategic_achievement < 80 AND AVG(programme_achievement) >= 80 THEN 'Programme Success, Strategic Gaps'
                    ELSE 'Performance Gaps'
                END as alignment_status
            FROM %s
            GROUP BY strategic_kpi_id, strategic_kpi_name, thematic_area, strategic_achievement
            ORDER BY strategic_achievement DESC
        """ % self._table
        
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    @api.model
    def get_contribution_analysis(self):
        """Analyze contribution weights and their effectiveness"""
        query = """
            SELECT 
                strategic_kpi_name,
                programme_indicator_name,
                programme_name,
                contribution_weight,
                programme_achievement,
                contribution_impact,
                impact_relationship,
                CASE 
                    WHEN contribution_weight > 30 THEN 'High Impact'
                    WHEN contribution_weight > 15 THEN 'Medium Impact'
                    ELSE 'Low Impact'
                END as impact_level,
                CASE 
                    WHEN programme_achievement >= 80 THEN 'Performing'
                    WHEN programme_achievement >= 50 THEN 'At Risk'
                    ELSE 'Underperforming'
                END as performance_status
            FROM %s
            WHERE contribution_weight > 0
            ORDER BY strategic_kpi_name, contribution_weight DESC
        """ % self._table
        
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    @api.model
    def get_performance_trends_data(self):
        """Get data for performance trends analysis"""
        # This would typically involve historical data
        # For now, we'll provide current snapshot data
        query = """
            SELECT 
                thematic_area,
                strategic_kpi_name,
                strategic_achievement,
                programme_indicator_name,
                programme_achievement,
                days_since_update,
                CASE 
                    WHEN days_since_update <= 7 THEN 'Recent'
                    WHEN days_since_update <= 30 THEN 'Current'
                    WHEN days_since_update <= 90 THEN 'Outdated'
                    ELSE 'Stale'
                END as data_freshness
            FROM %s
            ORDER BY thematic_area, strategic_achievement DESC
        """ % self._table
        
        self.env.cr.execute(query)
        return self.env.cr.dictfetchall()

    @api.model
    def generate_strategic_programme_report(self):
        """Generate comprehensive strategic-programme linkage report"""
        report_data = {
            'generation_date': fields.Datetime.now(),
            'thematic_summary': self.get_thematic_performance_summary(),
            'linkage_effectiveness': self.get_linkage_effectiveness_analysis(),
            'contribution_analysis': self.get_contribution_analysis(),
            'performance_trends': self.get_performance_trends_data(),
        }
        
        # Calculate overall statistics
        all_records = self.search([])
        if all_records:
            report_data['overall_stats'] = {
                'total_strategic_kpis': len(set(all_records.mapped('strategic_kpi_id.id'))),
                'total_programme_indicators': len(set(all_records.mapped('programme_indicator_id.id'))),
                'avg_strategic_achievement': sum(all_records.mapped('strategic_achievement')) / len(all_records),
                'avg_programme_achievement': sum(all_records.mapped('programme_achievement')) / len(all_records),
                'total_linkages': len(all_records),
                'thematic_areas_covered': len(set(all_records.mapped('thematic_area')))
            }
        else:
            report_data['overall_stats'] = {
                'total_strategic_kpis': 0,
                'total_programme_indicators': 0,
                'avg_strategic_achievement': 0,
                'avg_programme_achievement': 0,
                'total_linkages': 0,
                'thematic_areas_covered': 0
            }
        
        return report_data

    @api.model
    def get_dashboard_data(self):
        """Get data for the strategic-programme dashboard"""
        dashboard_data = self.generate_strategic_programme_report()
        
        # Add chart data
        thematic_data = dashboard_data['thematic_summary']
        dashboard_data['charts'] = {
            'thematic_performance': {
                'labels': [item['thematic_area'].replace('_', ' ').title() for item in thematic_data],
                'strategic_achievement': [item['avg_strategic_achievement'] for item in thematic_data],
                'programme_achievement': [item['avg_programme_achievement'] for item in thematic_data]
            },
            'alignment_analysis': {
                'aligned_high': len([item for item in dashboard_data['linkage_effectiveness'] if item['alignment_status'] == 'Aligned High Performance']),
                'strategic_success': len([item for item in dashboard_data['linkage_effectiveness'] if item['alignment_status'] == 'Strategic Success, Programme Gaps']),
                'programme_success': len([item for item in dashboard_data['linkage_effectiveness'] if item['alignment_status'] == 'Programme Success, Strategic Gaps']),
                'performance_gaps': len([item for item in dashboard_data['linkage_effectiveness'] if item['alignment_status'] == 'Performance Gaps'])
            }
        }
        
        return dashboard_data
