"""
One-time maintenance script:
- Keep only the specified 16 programmes in the 'implementing' category for all directorates
- Remove division relationships for all other programmes (for all divisions)
- Ensure DEMO programmes appear only under 'Direct Programmes' (no implementing directorates, relations marked is_direct)

Usage (from repo root or odoo root):
  odoo-bin shell -d robust_pmis -c ~/.odoorc -q -c "exec(open('addons/robust_pmis/cleanup_programmes_implementing.py').read(), {'env': env})"

The script is idempotent; it only updates/cleans as needed.
"""

from odoo import api


# Adjust if your authoritative list differs.
# Using programme codes for precision.
ALLOWED_PROGRAMME_CODES = [
    'AGRO',  # Agro-Industrialization
    'PSD',   # Private Sector Development
    'ITIS',  # Integrated Transport Infrastructure and Services
    'SUH',   # Sustainable Urbanization and Housing
    'DT',    # Digital Transformation
    'HCD',   # Human Capital Development
    'LOR',   # Legislation, Oversight and Representation
    'RRP',   # Road Rehabilitation Programme
    'WME',   # Waste Management Enhancement
    'PHE',   # Primary Healthcare Expansion
    'DRC',   # Digital Revenue Collection
    'UPD',   # Urban Planning & Development
    'AOJ',   # Administration of Justice
    'GS',    # Governance and Security
    'PST',   # Public Sector Transformation
    'SED',   # Sustainable Energy Development
]


def run(env):
    Programme = env['kcca.programme']
    DivisionRel = env['division.programme.rel']

    # Discover programmes by code
    allowed_progs = Programme.search([('code', 'in', ALLOWED_PROGRAMME_CODES)])
    allowed_codes_found = set(allowed_progs.mapped('code'))

    print(f"Keeping {len(allowed_progs)} implementing programmes by code: {sorted(list(allowed_codes_found))}")

    # 1) Clean 'implementing' category for all directorates: only allowed remain
    #    Clear implementing_directorate_ids for non-allowed programmes
    non_allowed_impl = Programme.search([
        ('id', 'not in', allowed_progs.ids),
        ('implementing_directorate_ids', '!=', False),
    ])
    if non_allowed_impl:
        print(f"Clearing implementing_directorate_ids for {len(non_allowed_impl)} non-allowed programmes ...")
        non_allowed_impl.write({'implementing_directorate_ids': [(5, 0, 0)]})
    else:
        print("No non-allowed programmes found with implementing directorates.")

    # 2) Remove Division relationships for programmes not in allowed list (for all divisions)
    rels_to_remove = DivisionRel.search([('programme_id', 'not in', allowed_progs.ids)])
    if rels_to_remove:
        print(f"Removing {len(rels_to_remove)} division-programme relations for non-allowed programmes ...")
        rels_to_remove.unlink()
    else:
        print("No division relations to remove for non-allowed programmes.")

    # 3) Ensure DEMO programmes only appear under 'Direct Programmes'
    demo_prog_domain = [('name', 'ilike', 'DEMO')]  # matches 'DEMO – ...'
    demo_programmes = Programme.search(demo_prog_domain)
    if demo_programmes:
        print(f"Normalizing {len(demo_programmes)} DEMO programmes ...")
        # Ensure they are not marked as implementing under directorates
        demo_programmes.write({'implementing_directorate_ids': [(5, 0, 0)]})

        # Ensure any existing division relations are flagged as direct
        demo_rels = DivisionRel.search([('programme_id', 'in', demo_programmes.ids)])
        if demo_rels:
            print(f"Marking {len(demo_rels)} DEMO relations as direct (is_direct=True) ...")
            demo_rels.write({'is_direct': True})
    else:
        print("No DEMO programmes found to normalize.")

    # 4) Ensure allowed programmes still have implementing tag if previously set via ProgrammeDirectorateRel
    #    (We don't synthesize new ones here; only preserve/leave intact.)
    print("Cleanup complete.")


# Execute when run from Odoo shell with env injected
run(env)
