# -*- coding: utf-8 -*-

from odoo import http, fields, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class KCCAPortalController(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        """Add KCCA PMIS counters to portal home"""
        values = super()._prepare_home_portal_values(counters)
        
        if 'kcca_performance' in counters:
            # Count accessible performance data for portal users
            strategic_goals_count = request.env['strategic.goal'].search_count([('active', '=', True)])
            programmes_count = request.env['kcca.programme'].search_count([('active', '=', True)])
            
            values['kcca_performance_count'] = strategic_goals_count + programmes_count
        
        return values

    @http.route(['/my/kcca_performance'], type='http', auth="public", website=True)
    def portal_kcca_performance(self, page=1, date_begin=None, date_end=None, sortby=None, **kw):
        """KCCA Performance Portal Page"""
        values = self._prepare_portal_layout_values()
        
        # Get public performance data
        strategic_goals = request.env['strategic.goal'].sudo().search([('active', '=', True)])
        directorates = request.env['kcca.directorate'].sudo().search([('active', '=', True)])
        programmes = request.env['kcca.programme'].sudo().search([('active', '=', True)])
        
        # Calculate summary statistics
        total_kpis = request.env['key.performance.indicator'].sudo().search_count([('active', '=', True)])
        
        if strategic_goals:
            avg_goal_progress = sum(goal.progress for goal in strategic_goals) / len(strategic_goals)
        else:
            avg_goal_progress = 0
        
        if programmes:
            avg_programme_performance = sum(prog.overall_performance for prog in programmes) / len(programmes)
        else:
            avg_programme_performance = 0
        
        values.update({
            'strategic_goals': strategic_goals,
            'directorates': directorates,
            'programmes': programmes,
            'summary_stats': {
                'total_goals': len(strategic_goals),
                'total_directorates': len(directorates),
                'total_programmes': len(programmes),
                'total_kpis': total_kpis,
                'avg_goal_progress': avg_goal_progress,
                'avg_programme_performance': avg_programme_performance,
            },
            'page_name': 'kcca_performance',
        })
        
        return request.render("robust_pmis.portal_kcca_performance", values)

    @http.route(['/my/kcca_performance/goal/<int:goal_id>'], type='http', auth="public", website=True)
    def portal_strategic_goal_detail(self, goal_id, **kw):
        """Strategic Goal Detail Page"""
        goal = request.env['strategic.goal'].sudo().browse(goal_id)
        
        if not goal.exists():
            return request.not_found()
        
        values = {
            'goal': goal,
            'page_name': 'strategic_goal_detail',
        }
        
        return request.render("robust_pmis.portal_strategic_goal_detail", values)

    @http.route(['/my/kcca_performance/directorate/<int:directorate_id>'], type='http', auth="public", website=True)
    def portal_directorate_detail(self, directorate_id, **kw):
        """Directorate Detail Page"""
        directorate = request.env['kcca.directorate'].sudo().browse(directorate_id)
        
        if not directorate.exists():
            return request.not_found()
        
        values = {
            'directorate': directorate,
            'page_name': 'directorate_detail',
        }
        
        return request.render("robust_pmis.portal_directorate_detail", values)

    @http.route(['/my/kcca_performance/programme/<int:programme_id>'], type='http', auth="public", website=True)
    def portal_programme_detail(self, programme_id, **kw):
        """Programme Detail Page"""
        programme = request.env['kcca.programme'].sudo().browse(programme_id)
        
        if not programme.exists():
            return request.not_found()
        
        values = {
            'programme': programme,
            'page_name': 'programme_detail',
        }
        
        return request.render("robust_pmis.portal_programme_detail", values)

    @http.route(['/kcca_performance/public_dashboard'], type='http', auth="public", website=True)
    def public_performance_dashboard(self, **kw):
        """Public Performance Dashboard"""
        # Get aggregated public data
        strategic_goals = request.env['strategic.goal'].sudo().search([('active', '=', True)])
        directorates = request.env['kcca.directorate'].sudo().search([('active', '=', True)])
        
        # Calculate public metrics
        total_kpis = request.env['key.performance.indicator'].sudo().search_count([('active', '=', True)])
        total_programmes = request.env['kcca.programme'].sudo().search_count([('active', '=', True)])
        
        # Overall performance metrics
        if strategic_goals:
            overall_strategic_progress = sum(goal.progress for goal in strategic_goals) / len(strategic_goals)
        else:
            overall_strategic_progress = 0
        
        if directorates:
            overall_directorate_performance = sum(d.overall_performance for d in directorates) / len(directorates)
        else:
            overall_directorate_performance = 0
        
        values = {
            'strategic_goals': strategic_goals,
            'directorates': directorates,
            'metrics': {
                'total_goals': len(strategic_goals),
                'total_directorates': len(directorates),
                'total_programmes': total_programmes,
                'total_kpis': total_kpis,
                'overall_strategic_progress': overall_strategic_progress,
                'overall_directorate_performance': overall_directorate_performance,
            },
            'page_name': 'public_dashboard',
        }
        
        return request.render("robust_pmis.public_performance_dashboard", values)
