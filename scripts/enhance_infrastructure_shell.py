#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("=== ENHANCING INFRASTRUCTURE DEVELOPMENT OBJECTIVE ===")

# Find the Infrastructure Development strategic objective
objective = env['strategic.objective'].search([
    ('name', 'ilike', 'Infrastructure Development')
], limit=1)

if not objective:
    print("❌ Infrastructure Development objective not found!")
    raise SystemExit(1)

print(f"📋 Found objective: {objective.name}")
print(f"   Current KRAs: {len(objective.kra_ids)}")
print(f"   Linked Programmes: {len(objective.programme_ids)}")

# Create comprehensive KRAs for Infrastructure Development
kra_data = [
    {
        'name': 'Transport Infrastructure Development',
        'description': 'Develop and maintain efficient transport infrastructure including roads, bridges, and public transit systems',
        'sequence': 10,
        'target_value': 100.0,
        'current_value': 75.0,
    },
    {
        'name': 'Urban Housing and Settlement Development',
        'description': 'Promote sustainable housing development and improve informal settlements',
        'sequence': 20, 
        'target_value': 100.0,
        'current_value': 60.0,
    },
    {
        'name': 'Public Infrastructure Maintenance',
        'description': 'Maintain and upgrade existing public infrastructure to ensure service delivery',
        'sequence': 30,
        'target_value': 100.0,
        'current_value': 85.0,
    },
    {
        'name': 'Smart City Infrastructure',
        'description': 'Develop ICT and digital infrastructure for smart city initiatives',
        'sequence': 40,
        'target_value': 100.0,
        'current_value': 45.0,
    }
]

created_kras = []
for kra_info in kra_data:
    # Check if KRA already exists
    existing_kra = env['key.result.area'].search([
        ('name', '=', kra_info['name']),
        ('strategic_objective_id', '=', objective.id)
    ])
    
    if not existing_kra:
        kra = env['key.result.area'].create({
            'name': kra_info['name'],
            'description': kra_info['description'],
            'sequence': kra_info['sequence'],
            'strategic_objective_id': objective.id,
            'target_value': kra_info['target_value'],
            'current_value': kra_info['current_value'],
            'active': True,
        })
        created_kras.append(kra)
        print(f"✅ Created KRA: {kra.name}")
    else:
        created_kras.append(existing_kra)
        print(f"📌 Using existing KRA: {existing_kra.name}")

# Create comprehensive KPIs for each KRA
kpi_data = [
    # Transport Infrastructure KPIs
    {
        'kra_name': 'Transport Infrastructure Development',
        'kpis': [
            {
                'name': 'Kilometers of Roads Rehabilitated',
                'description': 'Total kilometers of roads rehabilitated and upgraded annually',
                'target_value': 150.0,
                'current_value': 112.0,
                'unit_of_measure': 'Kilometers',
                'frequency': 'annual',
            },
            {
                'name': 'Bridge Construction and Rehabilitation',
                'description': 'Number of bridges constructed and rehabilitated',
                'target_value': 5.0,
                'current_value': 3.0,
                'unit_of_measure': 'Number',
                'frequency': 'annual',
            },
            {
                'name': 'Public Transport Coverage',
                'description': 'Percentage of city areas covered by public transport',
                'target_value': 80.0,
                'current_value': 65.0,
                'unit_of_measure': 'Percentage',
                'frequency': 'quarterly',
            },
        ]
    },
    # Housing and Settlement KPIs
    {
        'kra_name': 'Urban Housing and Settlement Development',
        'kpis': [
            {
                'name': 'Affordable Housing Units Delivered',
                'description': 'Number of affordable housing units constructed annually',
                'target_value': 2000.0,
                'current_value': 1200.0,
                'unit_of_measure': 'Units',
                'frequency': 'annual',
            },
            {
                'name': 'Informal Settlement Upgrades',
                'description': 'Number of informal settlements upgraded with basic services',
                'target_value': 10.0,
                'current_value': 6.0,
                'unit_of_measure': 'Number',
                'frequency': 'annual',
            },
            {
                'name': 'Building Permits Issued',
                'description': 'Number of building permits processed and issued',
                'target_value': 500.0,
                'current_value': 320.0,
                'unit_of_measure': 'Number',
                'frequency': 'quarterly',
            },
        ]
    },
    # Public Infrastructure Maintenance KPIs
    {
        'kra_name': 'Public Infrastructure Maintenance',
        'kpis': [
            {
                'name': 'Infrastructure Maintenance Response Time',
                'description': 'Average time to respond to infrastructure maintenance requests',
                'target_value': 48.0,
                'current_value': 72.0,
                'unit_of_measure': 'Hours',
                'frequency': 'monthly',
            },
            {
                'name': 'Water Infrastructure Uptime',
                'description': 'Percentage of time water infrastructure is operational',
                'target_value': 95.0,
                'current_value': 88.0,
                'unit_of_measure': 'Percentage',
                'frequency': 'monthly',
            },
            {
                'name': 'Electricity Infrastructure Coverage',
                'description': 'Percentage of city areas with reliable electricity supply',
                'target_value': 90.0,
                'current_value': 82.0,
                'unit_of_measure': 'Percentage',
                'frequency': 'quarterly',
            },
        ]
    },
    # Smart City Infrastructure KPIs
    {
        'kra_name': 'Smart City Infrastructure',
        'kpis': [
            {
                'name': 'Digital Service Points Established',
                'description': 'Number of digital service points established across the city',
                'target_value': 50.0,
                'current_value': 22.0,
                'unit_of_measure': 'Number',
                'frequency': 'annual',
            },
            {
                'name': 'Internet Connectivity Coverage',
                'description': 'Percentage of city areas with high-speed internet access',
                'target_value': 75.0,
                'current_value': 35.0,
                'unit_of_measure': 'Percentage',
                'frequency': 'quarterly',
            },
            {
                'name': 'Smart Traffic Management Systems',
                'description': 'Number of intersections with smart traffic management',
                'target_value': 100.0,
                'current_value': 25.0,
                'unit_of_measure': 'Number',
                'frequency': 'annual',
            },
        ]
    }
]

total_kpis_created = 0
for kra_group in kpi_data:
    # Find the KRA
    kra = env['key.result.area'].search([
        ('name', '=', kra_group['kra_name']),
        ('strategic_objective_id', '=', objective.id)
    ], limit=1)
    
    if kra:
        print(f"\n📊 Creating KPIs for KRA: {kra.name}")
        for kpi_info in kra_group['kpis']:
            # Check if KPI already exists
            existing_kpi = env['key.performance.indicator'].search([
                ('name', '=', kpi_info['name']),
                ('kra_id', '=', kra.id)
            ])
            
            if not existing_kpi:
                kpi = env['key.performance.indicator'].create({
                    'name': kpi_info['name'],
                    'description': kpi_info['description'],
                    'target_value': kpi_info['target_value'],
                    'current_value': kpi_info['current_value'],
                    'unit_of_measure': kpi_info['unit_of_measure'],
                    'frequency': kpi_info['frequency'],
                    'kra_id': kra.id,
                    'active': True,
                    'weight': 1.0,
                })
                total_kpis_created += 1
                achievement = (kpi_info['current_value'] / kpi_info['target_value']) * 100 if kpi_info['target_value'] > 0 else 0
                print(f"   ✅ Created KPI: {kpi.name} ({achievement:.1f}% achievement)")
            else:
                print(f"   📌 KPI already exists: {existing_kpi.name}")

# Link additional programmes to the Infrastructure Development objective
print(f"\n🔗 LINKING PROGRAMMES TO INFRASTRUCTURE DEVELOPMENT")

# Find infrastructure-related programmes
infrastructure_programmes = env['kcca.programme'].search([
    '|', '|', '|',
    ('name', 'ilike', 'transport'),
    ('name', 'ilike', 'infrastructure'),
    ('name', 'ilike', 'road'),
    ('name', 'ilike', 'housing'),
])

for programme in infrastructure_programmes:
    if programme not in objective.programme_ids:
        objective.write({
            'programme_ids': [(4, programme.id)]
        })
        print(f"   ✅ Linked programme: {programme.name}")
    else:
        print(f"   📌 Programme already linked: {programme.name}")

# Commit the changes
env.cr.commit()

# Final summary
print(f"\n=== SUMMARY ===")
print(f"📋 Strategic Objective: {objective.name}")
print(f"   KRAs Created/Updated: {len(created_kras)}")
print(f"   New KPIs Created: {total_kpis_created}")
print(f"   Total Programmes Linked: {len(objective.programme_ids)}")

# Reload and show current counts
objective.invalidate_cache()
print(f"\n📊 UPDATED COUNTS:")
print(f"   KRAs: {len(objective.kra_ids)}")
print(f"   KPIs: {len(objective.kra_ids.mapped('kpi_ids'))}")
print(f"   Programmes: {len(objective.programme_ids)}")

print(f"\n✅ Infrastructure Development objective enhanced successfully!")
