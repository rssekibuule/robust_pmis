# -*- coding: utf-8 -*-


# Safety cleanup to avoid duplicate Strategic Goals seeded by demo scripts
def cleanup_duplicate_goals(env):
    """Remove duplicate strategic goals by name, keeping the XML-defined one when available."""
    SG = env['strategic.goal']

    def dedupe(name, xmlid=None):
        keep = False
        if xmlid:
            try:
                keep = env.ref(xmlid)
            except Exception:
                keep = False
        if not keep:
            keep = SG.search([('name', '=', name)], limit=1)
        if not keep:
            return 0
        dups = SG.search([('name', '=', name), ('id', '!=', keep.id)])
        count = len(dups)
        if count:
            print(f"[post_init] Removing {count} duplicate Strategic Goal(s) for '{name}' (keeping ID {keep.id})")
            dups.unlink()
        return count

    removed = 0
    removed += dedupe('Improve Urban Infrastructure', 'robust_pmis.strategic_goal_improve_urban_infrastructure')
    # Also ensure demo-only goals don't duplicate if the script was run repeatedly
    removed += dedupe('Enhance Service Delivery')
    removed += dedupe('Strengthen Revenue Collection')
    print(f"[post_init] Duplicate cleanup complete. Removed {removed} duplicate goal(s).")
    return True

# Safety cleanup for duplicate Strategic Objectives
# 1) Dedupes within a specific Strategic Goal
# 2) Additionally, dedupes globally by name keeping the canonical XML-defined record
#    and migrating KRAs and programme links to it.
# This makes repeated DB reloads idempotent and prevents duplicate entries in dropdowns.
def cleanup_duplicate_objectives(env):
    SO = env['strategic.objective']

    def dedupe_within_goal(goal_xmlid, keep_xmlid, name):
        try:
            goal = env.ref(goal_xmlid)
        except Exception:
            return 0
        try:
            keep = env.ref(keep_xmlid)
        except Exception:
            keep = SO.search([
                ('strategic_goal_id', '=', goal.id), ('name', '=', name)
            ], limit=1)
            if not keep:
                return 0
        dups = SO.search([
            ('strategic_goal_id', '=', goal.id), ('name', '=', name), ('id', '!=', keep.id)
        ])
        moved = 0
        deleted = 0
        for dup in dups:
            # Reassign KRAs to the canonical objective to preserve data
            if dup.kra_ids:
                dup.kra_ids.write({'strategic_objective_id': keep.id})
                moved += len(dup.kra_ids)
            # Merge programme links (M2M)
            if dup.programme_ids:
                keep.write({'programme_ids': [(4, pid) for pid in dup.programme_ids.ids]})
            dup.unlink()
            deleted += 1
        if deleted:
            print(f"[post_init] Objectives deduped for goal '{goal.name}': kept {keep.id}, moved {moved} KRAs, deleted {deleted} dup(s)")
        return deleted

    def dedupe_globally(keep_xmlid, name):
        deleted = 0
        moved = 0
        try:
            keep = env.ref(keep_xmlid)
        except Exception:
            keep = SO.search([('name', '=', name)], limit=1)
            if not keep:
                return 0
        dups = SO.search([('name', '=', name), ('id', '!=', keep.id)])
        for dup in dups:
            # move KRAs
            if dup.kra_ids:
                dup.kra_ids.write({'strategic_objective_id': keep.id})
                moved += len(dup.kra_ids)
            # merge programme links
            if dup.programme_ids:
                keep.write({'programme_ids': [(4, pid) for pid in dup.programme_ids.ids]})
            dup.unlink()
            deleted += 1
        if deleted:
            print(f"[post_init] Global objectives deduped for '{name}': kept {keep.id}, moved {moved} KRAs, deleted {deleted} dup(s)")
        return deleted

    removed = 0
    removed += dedupe_within_goal(
        'robust_pmis.strategic_goal_improve_urban_infrastructure',
        'robust_pmis.strategic_objective_infrastructure_development_main',
        'Infrastructure Development'
    )
    # Also remove any other 'Infrastructure Development' objectives seeded by older demo files
    removed += dedupe_globally('robust_pmis.strategic_objective_infrastructure_development_main', 'Infrastructure Development')

    print(f"[post_init] Duplicate objective cleanup complete. Removed {removed} duplicate objective(s).")
    return True


def post_init_hook(env):
    """Post-installation hook: cleanup duplicates and normalize legacy views"""
    # Always perform duplicate cleanup first to keep data consistent
    try:
        cleanup_duplicate_goals(env)
        cleanup_duplicate_objectives(env)
    except Exception as e:
        print(f"[post_init] Duplicate cleanup failed: {e}")

    # Normalize legacy 'tree' view types to 'list' on actions and view rels
    try:
        result = env['ir.actions.act_window'].fix_legacy_tree_view_modes()
        print(f"[post_init] Legacy view types normalized: {result}")
    except Exception as e:
        print(f"[post_init] Legacy view normalization failed: {e}")

    # Check if transport programme already exists
    existing_programme = env['kcca.programme'].search([('code', '=', 'ITIS')], limit=1)
    if existing_programme:
        print(f"Transport Infrastructure Programme already exists: {existing_programme.name}")
        return

    print("Creating Transport Infrastructure Programme...")

    # Create the transport infrastructure programme
    programme = env['kcca.programme'].create({
        'name': 'Integrated Transport Infrastructure and Services',
        'code': 'ITIS',
        'description': '''<p><strong>Programme Goal:</strong> To have a safe, integrated and sustainable multi-modal transport system</p>
        <p>Programme focused on developing integrated transport infrastructure and services for Kampala.</p>
        <p><strong>Implementation Structure:</strong></p>
        <ul>
            <li>5 Implementing Directorates</li>
            <li>5 Implementing Divisions (All KCCA Territorial Divisions)</li>
            <li>Strategic Objective: Economic Growth (Master Table Row 1)</li>
        </ul>
        <p><strong>Total Budget:</strong> 1,487.50 UGX Billion across FY2022/23 to FY2026/27</p>''',
        'sequence': 1,
    })

    # Create programme objective
    objective = env['programme.objective'].create({
        'name': 'To develop an inter-modal and seamless transport infrastructure and services',
        'programme_id': programme.id,
        'sequence': 1,
        'description': 'Single programme objective under which all intermediate outcomes are organized',
    })

    # Create intermediate outcomes
    outcome1 = env['intermediate.outcome'].create({
        'name': 'Reduced travel time',
        'objective_id': objective.id,
        'sequence': 1,
        'description': 'Achieve reduced travel time through strategic transport infrastructure development',
    })

    outcome2 = env['intermediate.outcome'].create({
        'name': 'Increased stock of transport infrastructure',
        'objective_id': objective.id,
        'sequence': 2,
        'description': 'Increase the stock of transport infrastructure through capacity enhancement',
    })

    outcome3 = env['intermediate.outcome'].create({
        'name': 'Reduced fatalities',
        'objective_id': objective.id,
        'sequence': 3,
        'description': 'Reduce road fatalities through enhanced transport safety measures',
    })

    # Create performance indicators for outcomes
    env['performance.indicator'].create({
        'name': 'Average Travel time (Min/Km) on KCCA Road',
        'outcome_id': outcome1.id,
        'measurement_unit': 'Minutes per Km',
        'baseline_value': 4.2,
        'target_value': 3.0,
        'indicator_type': 'decreasing',
        'sequence': 1,
    })

    env['performance.indicator'].create({
        'name': 'Proportion of Commuters using mass public transport (Rail & BRT)',
        'outcome_id': outcome1.id,
        'measurement_unit': 'Percentage',
        'baseline_value': 2.0,
        'target_value': 30.0,
        'indicator_type': 'increasing',
        'sequence': 2,
    })

    env['performance.indicator'].create({
        'name': 'Proportion of city road network paved',
        'outcome_id': outcome2.id,
        'measurement_unit': 'Percentage',
        'baseline_value': 37.0,
        'target_value': 52.0,
        'indicator_type': 'increasing',
        'sequence': 1,
    })

    env['performance.indicator'].create({
        'name': 'Km of City Roads Paved',
        'outcome_id': outcome2.id,
        'measurement_unit': 'Kilometers',
        'baseline_value': 770.50,
        'target_value': 1094.00,
        'indicator_type': 'increasing',
        'sequence': 2,
    })

    env['performance.indicator'].create({
        'name': 'Fatalities per 100,000 persons (Roads)',
        'outcome_id': outcome3.id,
        'measurement_unit': 'Number per 100,000',
        'baseline_value': 11.0,
        'target_value': 5.0,
        'indicator_type': 'decreasing',
        'sequence': 1,
    })

    env['performance.indicator'].create({
        'name': 'Proportion of paved road network with street lights',
        'outcome_id': outcome3.id,
        'measurement_unit': 'Percentage',
        'baseline_value': 15.0,
        'target_value': 100.0,
        'indicator_type': 'increasing',
        'sequence': 2,
    })

    # Create interventions
    intervention1 = env['intervention'].create({
        'name': 'Construct and upgrade strategic transport infrastructure',
        'outcome_id': outcome1.id,
        'sequence': 1,
    })

    intervention2 = env['intervention'].create({
        'name': 'Increase capacity of existing transport infrastructure and services',
        'outcome_id': outcome2.id,
        'sequence': 1,
    })

    intervention3 = env['intervention'].create({
        'name': 'Enhance transport safety',
        'outcome_id': outcome3.id,
        'sequence': 1,
    })

    # Create outputs
    output1 = env['output'].create({
        'name': 'Strategic transport infrastructure constructed and upgraded',
        'intervention_id': intervention1.id,
        'sequence': 1,
    })

    output2 = env['output'].create({
        'name': 'Capacity of existing road transport infrastructure and services increased',
        'intervention_id': intervention2.id,
        'sequence': 1,
    })

    output3_1 = env['output'].create({
        'name': 'Road Transport Safety Enhanced',
        'intervention_id': intervention3.id,
        'sequence': 1,
    })

    output3_2 = env['output'].create({
        'name': 'Transport safety capacity strengthened',
        'intervention_id': intervention3.id,
        'sequence': 2,
    })

    # Create sample PIAP actions with budget data
    piap_actions_data = [
        {
            'name': 'Complete detailed design & Construct BRT Pilot Corridor (Bombo Road-Semuliki-Jinja Road-Kireka, Kampala-Zana via Kibuli) including upgrading 14 intersections',
            'output_id': output1.id,
            'budget_fy2022_23': 6.00,
            'budget_fy2023_24': 0.00,
            'budget_fy2024_25': 0.00,
            'budget_fy2025_26': 228.00,
            'budget_fy2026_27': 259.00,
        },
        {
            'name': 'Implement the Kampala City Road Rehabilitation Project financed by the AFDB (83Km & 7 Junctions)',
            'output_id': output2.id,
            'budget_fy2022_23': 131.98,
            'budget_fy2023_24': 85.52,
            'budget_fy2024_25': 0.00,
            'budget_fy2025_26': 0.00,
            'budget_fy2026_27': 0.00,
        },
        {
            'name': 'Operationalize the KCCA Road Safety Unit',
            'output_id': output3_1.id,
            'budget_fy2022_23': 0.00,
            'budget_fy2023_24': 0.10,
            'budget_fy2024_25': 0.00,
            'budget_fy2025_26': 0.00,
            'budget_fy2026_27': 0.00,
        },
        {
            'name': 'Train staff on road safety',
            'output_id': output3_2.id,
            'budget_fy2022_23': 0.05,
            'budget_fy2023_24': 0.05,
            'budget_fy2024_25': 0.05,
            'budget_fy2025_26': 0.05,
            'budget_fy2026_27': 0.05,
            'target_value': 10,
            'measurement_unit': 'Number of staff',
        },
    ]

    for i, action_data in enumerate(piap_actions_data, 1):
        env['piap.action'].create({
            'name': action_data['name'],
            'output_id': action_data['output_id'],
            'sequence': i,
            'budget_fy2022_23': action_data.get('budget_fy2022_23', 0.0),
            'budget_fy2023_24': action_data.get('budget_fy2023_24', 0.0),
            'budget_fy2024_25': action_data.get('budget_fy2024_25', 0.0),
            'budget_fy2025_26': action_data.get('budget_fy2025_26', 0.0),
            'budget_fy2026_27': action_data.get('budget_fy2026_27', 0.0),
            'target_value': action_data.get('target_value', 0.0),
            'measurement_unit': action_data.get('measurement_unit', ''),
            'status': 'in_progress',
        })

    print(f"✅ Transport Infrastructure Programme created successfully!")
    print(f"   Programme: {programme.name}")
    print(f"   Objectives: 1")
    print(f"   Intermediate Outcomes: 3")
    print(f"   Interventions: 3")
    print(f"   Outputs: 4")
    print(f"   PIAP Actions: {len(piap_actions_data)}")
    print(f"   Performance Indicators: 6")

def update_kpi_classifications(env):
    """
    Update KPI classification fields based on existing relationships.
    This function can be called manually to update KPI classifications.
    """
    print("Updating KPI classification fields...")

    # Get all KPIs
    kpis = env['key.performance.indicator'].search([])
    print(f"Found {len(kpis)} KPIs to update classifications for")

    # Update classification fields
    count = 0
    for kpi in kpis:
        kpi._compute_classification_fields()
        count += 1
        if count % 100 == 0:
            print(f"Processed {count}/{len(kpis)} KPIs")

    # Log results
    env.cr.execute("""
        SELECT classification_level, parent_type, COUNT(*)
        FROM key_performance_indicator
        GROUP BY classification_level, parent_type
    """)
    results = env.cr.fetchall()
    for level, parent_type, count in results:
        print(f"Updated {count} KPIs with level: {level}, parent_type: {parent_type}")

    print(f"✅ Successfully updated classifications for {len(kpis)} KPIs")

    return True
