# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pmis_allowed_implementing_programme_codes = fields.Char(
        string='Allowed Implementing Programme Codes',
        config_parameter='robust_pmis.allowed_programme_codes',
        help='Comma-separated list of allowed programme codes for Implementing relations (e.g., AGRO,PSD,ITIS,SUH,DT,HCD,LOR,RRP,WME,PHE,DRC,UPD,AOJ,GS,PST,SED)'
    )

    @api.model
    def get_allowed_programme_codes(self):
        """Return the configured list of allowed programme codes with sane defaults."""
        Param = self.env['ir.config_parameter'].sudo()
        raw = Param.get_param('robust_pmis.allowed_programme_codes')
        if raw:
            # normalize and deduplicate while preserving order
            seen = set()
            result = []
            for code in [c.strip().upper() for c in raw.split(',') if c.strip()]:
                if code not in seen:
                    seen.add(code)
                    result.append(code)
            return result
        # default canonical 16
        return ['AGRO','PSD','ITIS','SUH','DT','HCD','LOR','RRP','WME','PHE','DRC','UPD','AOJ','GS','PST','SED']
