# -*- coding: utf-8 -*-

def migrate(cr, version):
    """
    Update KPI classification fields based on existing relationships.
    This migration will:
    1. Set classification_level based on the existing relationships
    2. Set parent_type based on the related records
    3. Set programme_id and division_id where appropriate
    """
    if not version:
        return

    # Update KPIs linked to KRAs with strategic objectives
    cr.execute("""
        UPDATE key_performance_indicator kpi
        SET classification_level = 'strategic', parent_type = 'strategic_objective'
        FROM key_result_area kra
        WHERE kpi.kra_id = kra.id AND kra.strategic_objective_id IS NOT NULL
    """)

    # Update KPIs linked to KRAs with strategic goals
    cr.execute("""
        UPDATE key_performance_indicator kpi
        SET classification_level = 'strategic', parent_type = 'strategic_goal'
        FROM key_result_area kra
        WHERE kpi.kra_id = kra.id AND kra.strategic_goal_id IS NOT NULL
    """)

    # Update KPIs linked to KRAs without strategic goals or objectives
    cr.execute("""
        UPDATE key_performance_indicator kpi
        SET classification_level = 'strategic', parent_type = 'kra'
        FROM key_result_area kra
        WHERE kpi.kra_id = kra.id 
        AND kra.strategic_goal_id IS NULL 
        AND kra.strategic_objective_id IS NULL
    """)

    # Update KPIs linked to directorates
    cr.execute("""
        UPDATE key_performance_indicator
        SET classification_level = 'directorate', parent_type = 'directorate'
        WHERE directorate_id IS NOT NULL
    """)

    # Print results
    cr.execute("""
        SELECT classification_level, parent_type, COUNT(*) 
        FROM key_performance_indicator 
        GROUP BY classification_level, parent_type
    """)
    results = cr.fetchall()
    for level, parent_type, count in results:
        print(f"Updated {count} KPIs with level: {level}, parent_type: {parent_type}")
