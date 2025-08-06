# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import base64
import io
import xlsxwriter
import json


class StrategicProgrammeReportWizard(models.TransientModel):
    _name = 'strategic.programme.report.wizard'
    _description = 'Strategic-Programme Linkage Report Generator'

    # Report Configuration
    report_type = fields.Selection([
        ('comprehensive', 'Comprehensive Analysis Report'),
        ('thematic_summary', 'Thematic Area Summary'),
        ('linkage_effectiveness', 'Linkage Effectiveness Analysis'),
        ('performance_gaps', 'Performance Gap Analysis'),
        ('contribution_analysis', 'Contribution Weight Analysis')
    ], string='Report Type', default='comprehensive', required=True)

    # Filters
    thematic_areas = fields.Selection([
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
    ], string='Thematic Area Filter', help="Leave empty to include all thematic areas")

    strategic_kpi_ids = fields.Many2many(
        'key.performance.indicator',
        string='Strategic KPIs',
        help="Leave empty to include all strategic KPIs"
    )

    programme_ids = fields.Many2many(
        'kcca.programme',
        string='Programmes',
        help="Leave empty to include all programmes"
    )

    directorate_ids = fields.Many2many(
        'kcca.directorate',
        string='Directorates',
        help="Leave empty to include all directorates"
    )

    # Performance Filters
    min_achievement_percentage = fields.Float(
        string='Minimum Achievement %',
        default=0.0,
        help="Filter indicators with achievement percentage above this value"
    )

    max_achievement_percentage = fields.Float(
        string='Maximum Achievement %',
        default=100.0,
        help="Filter indicators with achievement percentage below this value"
    )

    # Output Options
    output_format = fields.Selection([
        ('pdf', 'PDF Report'),
        ('excel', 'Excel Spreadsheet'),
        ('json', 'JSON Data Export')
    ], string='Output Format', default='pdf', required=True)

    include_charts = fields.Boolean(
        string='Include Charts',
        default=True,
        help="Include performance charts in the report"
    )

    include_recommendations = fields.Boolean(
        string='Include Recommendations',
        default=True,
        help="Include performance improvement recommendations"
    )

    # Generated Report
    report_file = fields.Binary(string='Generated Report', readonly=True)
    report_filename = fields.Char(string='Report Filename', readonly=True)

    def action_generate_report(self):
        """Generate the strategic-programme linkage report"""
        # Get analytics data
        analytics_model = self.env['strategic.programme.analytics']
        
        # Build domain based on filters
        domain = []

        if self.thematic_areas:
            domain.append(('thematic_area', '=', self.thematic_areas))

        if self.strategic_kpi_ids:
            domain.append(('strategic_kpi_id', 'in', self.strategic_kpi_ids.ids))
        
        if self.programme_ids:
            # Get programme indicators for selected programmes
            programme_indicators = self.env['performance.indicator'].search([
                ('parent_programme_id', 'in', self.programme_ids.ids)
            ])
            domain.append(('programme_indicator_id', 'in', programme_indicators.ids))
        
        if self.directorate_ids:
            domain.append(('responsible_directorate', 'in', self.directorate_ids.mapped('name')))
        
        if self.min_achievement_percentage > 0:
            domain.append(('strategic_achievement', '>=', self.min_achievement_percentage))
        
        if self.max_achievement_percentage < 100:
            domain.append(('strategic_achievement', '<=', self.max_achievement_percentage))

        # Get filtered data
        analytics_data = analytics_model.search(domain)
        
        if not analytics_data:
            raise UserError(_("No data found matching the selected criteria."))

        # Generate report based on type and format
        if self.output_format == 'excel':
            report_file, filename = self._generate_excel_report(analytics_data)
        elif self.output_format == 'json':
            report_file, filename = self._generate_json_report(analytics_data)
        else:  # PDF
            report_file, filename = self._generate_pdf_report(analytics_data)

        # Save the generated report
        self.write({
            'report_file': report_file,
            'report_filename': filename
        })

        # Return action to download the report
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content?model=strategic.programme.report.wizard&id={self.id}&field=report_file&download=true&filename={filename}',
            'target': 'self',
        }

    def _generate_excel_report(self, analytics_data):
        """Generate Excel report"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        
        # Define formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#4472C4',
            'font_color': 'white',
            'border': 1
        })
        
        data_format = workbook.add_format({'border': 1})
        percent_format = workbook.add_format({'num_format': '0.00%', 'border': 1})
        
        # Create worksheets based on report type
        if self.report_type == 'comprehensive':
            self._create_comprehensive_excel_sheets(workbook, analytics_data, header_format, data_format, percent_format)
        elif self.report_type == 'thematic_summary':
            self._create_thematic_summary_sheet(workbook, analytics_data, header_format, data_format, percent_format)
        elif self.report_type == 'linkage_effectiveness':
            self._create_linkage_effectiveness_sheet(workbook, analytics_data, header_format, data_format, percent_format)
        elif self.report_type == 'performance_gaps':
            self._create_performance_gaps_sheet(workbook, analytics_data, header_format, data_format, percent_format)
        elif self.report_type == 'contribution_analysis':
            self._create_contribution_analysis_sheet(workbook, analytics_data, header_format, data_format, percent_format)

        workbook.close()
        output.seek(0)
        
        filename = f"strategic_programme_report_{self.report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        return base64.b64encode(output.read()), filename

    def _create_comprehensive_excel_sheets(self, workbook, analytics_data, header_format, data_format, percent_format):
        """Create comprehensive Excel report with multiple sheets"""
        
        # Summary Sheet
        summary_sheet = workbook.add_worksheet('Executive Summary')
        summary_sheet.write(0, 0, 'Strategic-Programme Linkage Analysis', header_format)
        summary_sheet.write(1, 0, f'Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', data_format)
        
        # Overall Statistics
        summary_sheet.write(3, 0, 'Overall Statistics', header_format)
        summary_sheet.write(4, 0, 'Total Strategic KPIs', data_format)
        summary_sheet.write(4, 1, len(set(analytics_data.mapped('strategic_kpi_id.id'))), data_format)
        summary_sheet.write(5, 0, 'Total Programme Indicators', data_format)
        summary_sheet.write(5, 1, len(set(analytics_data.mapped('programme_indicator_id.id'))), data_format)
        summary_sheet.write(6, 0, 'Average Strategic Achievement', data_format)
        summary_sheet.write(6, 1, sum(analytics_data.mapped('strategic_achievement')) / len(analytics_data) / 100, percent_format)
        summary_sheet.write(7, 0, 'Average Programme Achievement', data_format)
        summary_sheet.write(7, 1, sum(analytics_data.mapped('programme_achievement')) / len(analytics_data) / 100, percent_format)

        # Detailed Data Sheet
        detail_sheet = workbook.add_worksheet('Detailed Analysis')
        headers = [
            'Thematic Area', 'Strategic KPI', 'Strategic Achievement %', 'Programme Indicator',
            'Programme Name', 'Programme Achievement %', 'Contribution Weight %', 'Impact Relationship',
            'Performance Gap', 'Responsible Directorate', 'Last Update'
        ]
        
        for col, header in enumerate(headers):
            detail_sheet.write(0, col, header, header_format)
        
        for row, record in enumerate(analytics_data, 1):
            detail_sheet.write(row, 0, record.thematic_area or '', data_format)
            detail_sheet.write(row, 1, record.strategic_kpi_name or '', data_format)
            detail_sheet.write(row, 2, record.strategic_achievement / 100, percent_format)
            detail_sheet.write(row, 3, record.programme_indicator_name or '', data_format)
            detail_sheet.write(row, 4, record.programme_name or '', data_format)
            detail_sheet.write(row, 5, record.programme_achievement / 100, percent_format)
            detail_sheet.write(row, 6, record.contribution_weight / 100, percent_format)
            detail_sheet.write(row, 7, record.impact_relationship or '', data_format)
            detail_sheet.write(row, 8, record.performance_gap or 0, data_format)
            detail_sheet.write(row, 9, record.responsible_directorate or '', data_format)
            detail_sheet.write(row, 10, record.last_update_date.strftime('%Y-%m-%d') if record.last_update_date else '', data_format)

    def _create_thematic_summary_sheet(self, workbook, analytics_data, header_format, data_format, percent_format):
        """Create thematic area summary sheet"""
        sheet = workbook.add_worksheet('Thematic Summary')
        
        # Get thematic summary data
        analytics_model = self.env['strategic.programme.analytics']
        thematic_summary = analytics_model.get_thematic_performance_summary()
        
        headers = [
            'Thematic Area', 'Strategic KPIs Count', 'Programme Indicators Count',
            'Avg Strategic Achievement', 'Avg Programme Achievement', 'Strategic On Track %', 'Programme On Track %'
        ]
        
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)
        
        for row, data in enumerate(thematic_summary, 1):
            sheet.write(row, 0, data['thematic_area'].replace('_', ' ').title(), data_format)
            sheet.write(row, 1, data['strategic_kpis_count'], data_format)
            sheet.write(row, 2, data['programme_indicators_count'], data_format)
            sheet.write(row, 3, data['avg_strategic_achievement'] / 100, percent_format)
            sheet.write(row, 4, data['avg_programme_achievement'] / 100, percent_format)
            sheet.write(row, 5, data['strategic_on_track_pct'] / 100, percent_format)
            sheet.write(row, 6, data['programme_on_track_pct'] / 100, percent_format)

    def _create_linkage_effectiveness_sheet(self, workbook, analytics_data, header_format, data_format, percent_format):
        """Create linkage effectiveness analysis sheet"""
        sheet = workbook.add_worksheet('Linkage Effectiveness')
        
        # Get linkage effectiveness data
        analytics_model = self.env['strategic.programme.analytics']
        effectiveness_data = analytics_model.get_linkage_effectiveness_analysis()
        
        headers = [
            'Strategic KPI', 'Thematic Area', 'Strategic Achievement %', 'Linked Indicators Count',
            'Avg Programme Achievement %', 'Total Contribution Impact', 'Alignment Status'
        ]
        
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)
        
        for row, data in enumerate(effectiveness_data, 1):
            sheet.write(row, 0, data['strategic_kpi_name'], data_format)
            sheet.write(row, 1, data['thematic_area'].replace('_', ' ').title() if data['thematic_area'] else '', data_format)
            sheet.write(row, 2, data['strategic_achievement'] / 100, percent_format)
            sheet.write(row, 3, data['linked_indicators_count'], data_format)
            sheet.write(row, 4, data['avg_programme_achievement'] / 100, percent_format)
            sheet.write(row, 5, data['total_contribution_impact'] or 0, data_format)
            sheet.write(row, 6, data['alignment_status'], data_format)

    def _generate_json_report(self, analytics_data):
        """Generate JSON data export"""
        analytics_model = self.env['strategic.programme.analytics']
        
        report_data = {
            'metadata': {
                'generated_at': datetime.now().isoformat(),
                'report_type': self.report_type,
                'total_records': len(analytics_data),
                'filters_applied': {
                    'thematic_area': self.thematic_areas,
                    'strategic_kpis': self.strategic_kpi_ids.mapped('name'),
                    'programmes': self.programme_ids.mapped('name'),
                    'directorates': self.directorate_ids.mapped('name'),
                    'min_achievement': self.min_achievement_percentage,
                    'max_achievement': self.max_achievement_percentage
                }
            },
            'summary_statistics': analytics_model.generate_strategic_programme_report(),
            'detailed_data': []
        }
        
        # Add detailed records
        for record in analytics_data:
            report_data['detailed_data'].append({
                'strategic_kpi': {
                    'id': record.strategic_kpi_id.id,
                    'name': record.strategic_kpi_name,
                    'kra': record.kra_name,
                    'thematic_area': record.thematic_area,
                    'target': record.strategic_target,
                    'current': record.strategic_current,
                    'achievement_pct': record.strategic_achievement
                },
                'programme_indicator': {
                    'id': record.programme_indicator_id.id,
                    'name': record.programme_indicator_name,
                    'programme': record.programme_name,
                    'target': record.programme_target,
                    'current': record.programme_current,
                    'achievement_pct': record.programme_achievement
                },
                'linkage': {
                    'contribution_weight': record.contribution_weight,
                    'impact_relationship': record.impact_relationship,
                    'performance_gap': record.performance_gap,
                    'contribution_impact': record.contribution_impact
                },
                'management': {
                    'responsible_directorate': record.responsible_directorate,
                    'last_update': record.last_update_date.isoformat() if record.last_update_date else None,
                    'days_since_update': record.days_since_update
                }
            })
        
        json_data = json.dumps(report_data, indent=2, ensure_ascii=False)
        filename = f"strategic_programme_data_{self.report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        return base64.b64encode(json_data.encode('utf-8')), filename

    def _generate_pdf_report(self, analytics_data):
        """Generate PDF report (placeholder - would use reporting engine)"""
        # This would typically use Odoo's QWeb reporting engine
        # For now, return a simple text-based report
        
        report_content = f"""
STRATEGIC-PROGRAMME LINKAGE ANALYSIS REPORT
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Report Type: {self.report_type.replace('_', ' ').title()}

EXECUTIVE SUMMARY
================
Total Strategic KPIs: {len(set(analytics_data.mapped('strategic_kpi_id.id')))}
Total Programme Indicators: {len(set(analytics_data.mapped('programme_indicator_id.id')))}
Average Strategic Achievement: {sum(analytics_data.mapped('strategic_achievement')) / len(analytics_data):.1f}%
Average Programme Achievement: {sum(analytics_data.mapped('programme_achievement')) / len(analytics_data):.1f}%

DETAILED ANALYSIS
================
"""
        
        for record in analytics_data[:10]:  # Limit for demo
            report_content += f"""
Strategic KPI: {record.strategic_kpi_name}
Programme Indicator: {record.programme_indicator_name}
Strategic Achievement: {record.strategic_achievement:.1f}%
Programme Achievement: {record.programme_achievement:.1f}%
Contribution Weight: {record.contribution_weight:.1f}%
Impact Relationship: {record.impact_relationship}
---
"""
        
        filename = f"strategic_programme_report_{self.report_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        return base64.b64encode(report_content.encode('utf-8')), filename
