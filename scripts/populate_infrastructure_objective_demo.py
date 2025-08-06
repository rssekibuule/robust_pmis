# Odoo shell script: populate demo KRAs and KPIs for Infrastructure Development objective
print('--- Populating demo KRAs and KPIs for Infrastructure Development objective ---')

# Find the objective
objective = env['strategic.objective'].search([('name', 'ilike', 'Infrastructure Development')], limit=1)
if not objective:
    print('❌ ERROR: Strategic Objective "Infrastructure Development" not found.')
else:
    print(f'✅ Found objective: {objective.name} (ID: {objective.id})')
    # Create 5 demo KRAs
    kra_names = [
        'Road Network Expansion',
        'Public Transport Enhancement',
        'Urban Drainage Improvement',
        'Non-Motorized Transport Promotion',
        'Smart Infrastructure Deployment'
    ]
    kpi_templates = [
        ('Kilometers of new roads constructed', 'km', 50, 20),
        ('Number of new buses deployed', 'buses', 100, 40),
        ('Drainage channels upgraded', 'channels', 30, 10),
        ('Kilometers of cycling lanes added', 'km', 25, 8),
        ('Smart traffic lights installed', 'lights', 15, 5)
    ]
    kra_ids = []
    for i, kra_name in enumerate(kra_names):
        kra = env['key.result.area'].create({
            'name': kra_name,
            'strategic_objective_id': objective.id,
            'description': f'Demo KRA {i+1} for Infrastructure Development',
            'sequence': (i+1)*10,
            'target_value': 100.0,
            'current_value': 50.0,
            'active': True,
        })
        kra_ids.append(kra.id)
        print(f'  - Created KRA: {kra.name}')
        # Create 5 KPIs for each KRA
        for j in range(5):
            kpi_name, unit, target, current = kpi_templates[j]
            kpi = env['key.performance.indicator'].create({
                'name': f'{kpi_name} (Demo {j+1})',
                'kra_id': kra.id,
                'description': f'Demo KPI {j+1} for {kra.name}',
                'target_value': target + j*5,
                'current_value': current + j*2,
                'unit_of_measure': unit,
                'frequency': 'annual',
                'active': True,
                'weight': 1.0,
            })
            print(f'    - Created KPI: {kpi.name}')
    env.cr.commit()
    print('✅ Demo KRAs and KPIs created and committed.')
