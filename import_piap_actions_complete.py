#!/usr/bin/env python3
"""
Complete PIAP Actions Import Script
Imports all PIAP Actions data from the Transport Programme analysis table
"""

def import_complete_piap_actions(env):
    """Import complete PIAP Actions dataset with all interventions, outputs and actions"""
    
    print("🚀 Starting Complete PIAP Actions Import...")
    
    # Get the transport programme and its components
    programme = env['kcca.programme'].search([('name', '=', 'Integrated Transport Infrastructure and Services')])
    if not programme:
        print("❌ Transport Programme not found! Please run the transport indicators script first.")
        return False
    
    objective = env['programme.objective'].search([('programme_id', '=', programme.id)])
    outcomes = env['intermediate.outcome'].search([('objective_id', '=', objective.id)])
    
    # Create outcome mapping
    outcome_map = {}
    for outcome in outcomes:
        if 'travel time' in outcome.name.lower():
            outcome_map['reduced_travel_time'] = outcome
        elif 'transport infrastructure' in outcome.name.lower():
            outcome_map['increased_infrastructure'] = outcome
        elif 'transport safety' in outcome.name.lower():
            outcome_map['enhanced_safety'] = outcome
    
    print(f"✅ Found programme with {len(outcomes)} outcomes")
    
    # Define the complete PIAP Actions dataset structure
    piap_data = {
        # Intervention 1.1.1: Construct and upgrade strategic transport infrastructure
        'intervention_1_1_1': {
            'name': 'Construct and upgrade strategic transport infrastructure',
            'outcome': 'reduced_travel_time',
            'outputs': {
                'output_1_1_1_1': {
                    'name': 'Strategic transport infrastructure constructed and upgraded',
                    'actions': [
                        {
                            'name': 'Km of BRT Network constructed',
                            'baseline_value': 0.0,
                            'target_value': 14.7,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 0.0,
                            'budget_fy2028_29': 4.2,
                            'budget_fy2029_30': 5.1,
                            'total_budget': 14.7
                        },
                        {
                            'name': 'No of Traffic Diversion Flyovers constructed',
                            'baseline_value': 2.0,
                            'target_value': 4.0,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 1.0,
                            'budget_fy2027_28': 2.0,
                            'budget_fy2028_29': 0.0,
                            'budget_fy2029_30': 1.0,
                            'total_budget': 4.0
                        },
                        {
                            'name': 'Km of meter gauge commuter rail revamped',
                            'baseline_value': 26.0,
                            'target_value': 26.0,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 5.0,
                            'budget_fy2028_29': 5.0,
                            'budget_fy2029_30': 10.0,
                            'total_budget': 20.0
                        },
                        {
                            'name': 'Km of Cable Car System constructed',
                            'baseline_value': 0.0,
                            'target_value': 7.0,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 2.0,
                            'budget_fy2028_29': 2.5,
                            'budget_fy2029_30': 2.5,
                            'total_budget': 7.0
                        },
                        {
                            'name': '% completion of Feasibility study & detailed design for LRT',
                            'baseline_value': 0.75,
                            'target_value': 100.0,
                            'measurement_unit': 'Percentage',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 100.0,
                            'budget_fy2027_28': 50.0,
                            'budget_fy2028_29': 100.0,
                            'budget_fy2029_30': 4.0,
                            'total_budget': 100.0
                        }
                    ]
                }
            }
        },
        
        # Intervention 1.2.1: Increase capacity of existing transport infrastructure and services
        'intervention_1_2_1': {
            'name': 'Increase capacity of existing transport infrastructure and services',
            'outcome': 'increased_infrastructure',
            'outputs': {
                'output_1_2_1_1': {
                    'name': 'Capacity of existing road transport infrastructure and services increased',
                    'actions': [
                        {
                            'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KIIDP',
                            'baseline_value': 44.00,
                            'target_value': 44.00,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 24.00,
                            'budget_fy2026_27': 20.00,
                            'budget_fy2027_28': 0.00,
                            'budget_fy2028_29': 0.00,
                            'budget_fy2029_30': 0.00,
                            'total_budget': 44.00
                        },
                        {
                            'name': 'Km of KCCA roads & junctions upgraded/reconstructed under KIIDP II',
                            'baseline_value': 0.00,
                            'target_value': 0.00,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 0.00,
                            'budget_fy2026_27': 0.00,
                            'budget_fy2027_28': 0.00,
                            'budget_fy2028_29': 0.00,
                            'budget_fy2029_30': 0.00,
                            'total_budget': 0.00
                        },
                        {
                            'name': 'Km of KCCA roads & junctions upgraded/reconstructed under OPMU/UCP',
                            'baseline_value': 0.00,
                            'target_value': 105.75,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 14.80,
                            'budget_fy2026_27': 22.70,
                            'budget_fy2027_28': 25.00,
                            'budget_fy2028_29': 25.00,
                            'budget_fy2029_30': 18.25,
                            'total_budget': 105.75
                        }
                    ]
                }
            }
        },
        
        # Intervention 1.3.1: Enhance transport safety
        'intervention_1_3_1': {
            'name': 'Enhance transport safety',
            'outcome': 'enhanced_safety',
            'outputs': {
                'output_1_3_1_1': {
                    'name': 'Road Transport Safety Enhanced',
                    'actions': [
                        {
                            'name': 'Number of Fatalities in City Road',
                            'baseline_value': 411,
                            'target_value': 275,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 380,
                            'budget_fy2026_27': 356,
                            'budget_fy2027_28': 331,
                            'budget_fy2028_29': 305,
                            'budget_fy2029_30': 275,
                            'total_budget': 275
                        },
                        {
                            'name': 'Number of road safety Audits Inspections conducted',
                            'baseline_value': 0.00,
                            'target_value': 30,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 6,
                            'budget_fy2026_27': 3,
                            'budget_fy2027_28': 6,
                            'budget_fy2028_29': 7,
                            'budget_fy2029_30': 8,
                            'total_budget': 30
                        },
                        {
                            'name': 'Number of Street Lights Installed (Under AFD Funding)',
                            'baseline_value': 7000,
                            'target_value': 15000,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.00,
                            'budget_fy2026_27': 5000,
                            'budget_fy2027_28': 5000,
                            'budget_fy2028_29': 2500,
                            'budget_fy2029_30': 2500,
                            'total_budget': 15000
                        },
                        {
                            'name': 'Number of Street Lights Installed (Under PPP Arrangement)',
                            'baseline_value': 0.00,
                            'target_value': 10000,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.00,
                            'budget_fy2026_27': 2500,
                            'budget_fy2027_28': 2500,
                            'budget_fy2028_29': 2500,
                            'budget_fy2029_30': 2500,
                            'total_budget': 10000
                        }
                    ]
                },
                'output_1_3_1_1_additional': {
                    'name': 'KCCA Road Safety Unit Operationalized',
                    'actions': [
                        {
                            'name': 'Operationalise the KCCA Road Safety Unit',
                            'baseline_value': 0.00,
                            'target_value': 1.00,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.10,
                            'budget_fy2026_27': 0.10,
                            'budget_fy2027_28': 0.00,
                            'budget_fy2028_29': 0.00,
                            'budget_fy2029_30': 0.20,
                            'total_budget': 0.20
                        },
                        {
                            'name': 'Undertake Road Safety Audits',
                            'baseline_value': 0.00,
                            'target_value': 1.00,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 1.25,
                            'budget_fy2026_27': 0.30,
                            'budget_fy2027_28': 0.35,
                            'budget_fy2028_29': 0.00,
                            'budget_fy2029_30': 1.10,
                            'total_budget': 1.10
                        },
                        {
                            'name': 'Construct road safety infrastructure across the city (humps, signage, zebra crossings, road markings etc)',
                            'baseline_value': 0.00,
                            'target_value': 1.00,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 4.90,
                            'budget_fy2026_27': 4.10,
                            'budget_fy2027_28': 4.10,
                            'budget_fy2028_29': 4.10,
                            'budget_fy2029_30': 16.80,
                            'total_budget': 16.80
                        },
                        {
                            'name': 'Conduct road safety campaigns (Radios/TV commercials, Billboards, Newspaper articles, messaging etc)',
                            'baseline_value': 0.00,
                            'target_value': 1.00,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.50,
                            'budget_fy2026_27': 0.50,
                            'budget_fy2027_28': 0.50,
                            'budget_fy2028_29': 0.50,
                            'budget_fy2029_30': 2.50,
                            'total_budget': 2.50
                        },
                        {
                            'name': 'Streamline Boda Operations (Elections, Registration, Boda Soda App, semi-station, Licensing, Boda stages)',
                            'baseline_value': 0.00,
                            'target_value': 1.00,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.50,
                            'budget_fy2026_27': 1.00,
                            'budget_fy2027_28': 0.50,
                            'budget_fy2028_29': 0.00,
                            'budget_fy2029_30': 2.00,
                            'total_budget': 2.00
                        },
                        {
                            'name': 'Develop and maintain a road safety dashboard for the city',
                            'baseline_value': 0.00,
                            'target_value': 1.00,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.00,
                            'budget_fy2026_27': 0.00,
                            'budget_fy2027_28': 0.05,
                            'budget_fy2028_29': 0.00,
                            'budget_fy2029_30': 0.25,
                            'total_budget': 0.25
                        },
                        {
                            'name': 'Review and update the Kampala Road Safety Strategy and Action Plan',
                            'baseline_value': 0.00,
                            'target_value': 1.00,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.10,
                            'budget_fy2026_27': 0.00,
                            'budget_fy2027_28': 0.00,
                            'budget_fy2028_29': 0.10,
                            'budget_fy2029_30': 0.20,
                            'total_budget': 0.20
                        },
                        {
                            'name': 'Publish Annual Road Safety Reports',
                            'baseline_value': 0.00,
                            'target_value': 1.00,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.05,
                            'budget_fy2026_27': 0.05,
                            'budget_fy2027_28': 0.05,
                            'budget_fy2028_29': 0.05,
                            'budget_fy2029_30': 0.25,
                            'total_budget': 0.25
                        },
                        {
                            'name': 'Install Street Lights including crime hotspots under the AFD project (15,000)',
                            'baseline_value': 0.00,
                            'target_value': 15000,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 55.00,
                            'budget_fy2026_27': 65.00,
                            'budget_fy2027_28': 32.50,
                            'budget_fy2028_29': 32.50,
                            'budget_fy2029_30': 185.00,
                            'total_budget': 185.00
                        },
                        {
                            'name': 'Install Street Lights under PPP Arrangement (10,000)',
                            'baseline_value': 0.00,
                            'target_value': 10000,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 0.00,
                            'budget_fy2026_27': 0.00,
                            'budget_fy2027_28': 0.00,
                            'budget_fy2028_29': 0.00,
                            'budget_fy2029_30': 0.00,
                            'total_budget': 0.00
                        }
                    ]
                },
                'output_1_3_1_2': {
                    'name': 'Transport safety capacity strengthened',
                    'actions': [
                        {
                            'name': 'Number of staff trained on Transport safety',
                            'baseline_value': 10,
                            'target_value': 25,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 10,
                            'budget_fy2026_27': 10,
                            'budget_fy2027_28': 10,
                            'budget_fy2028_29': 10,
                            'budget_fy2029_30': 25,
                            'total_budget': 25
                        },
                        {
                            'name': 'Number of stakeholders trained on Transport safety',
                            'baseline_value': 25,
                            'target_value': 25,
                            'measurement_unit': 'Number',
                            'budget_fy2025_26': 25,
                            'budget_fy2026_27': 25,
                            'budget_fy2027_28': 25,
                            'budget_fy2028_29': 25,
                            'budget_fy2029_30': 25,
                            'total_budget': 25
                        }
                    ]
                }
            }
        },

        # Additional PIAP Actions from the table - Major Infrastructure Projects
        'piap_actions_major_infrastructure': {
            'name': 'Major Infrastructure Development Projects',
            'outcome': 'reduced_travel_time',
            'outputs': {
                'output_major_projects': {
                    'name': 'Major Transport Infrastructure Projects Implemented',
                    'actions': [
                        {
                            'name': 'Complete detailed design & Construct BRT Pilot Corridor (Busega-Jinja Road, Busega-Jinja Road, Kampala-Jinja Road, Kampala-Entebbe Road)',
                            'baseline_value': 0.0,
                            'target_value': 1.0,
                            'measurement_unit': 'Project',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 0.0,
                            'budget_fy2028_29': 168.75,
                            'budget_fy2029_30': 168.75,
                            'total_budget': 337.50
                        },
                        {
                            'name': 'Complete detailed & implement the Kampala Flyover Phase 2 comprising of Mukwano, Kyanja Roads, Mukono, Pece Road and Soroti City Junctions',
                            'baseline_value': 0.0,
                            'target_value': 1.0,
                            'measurement_unit': 'Project',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 0.0,
                            'budget_fy2028_29': 168.75,
                            'budget_fy2029_30': 168.75,
                            'total_budget': 337.50
                        },
                        {
                            'name': 'Support the improvement of passenger railway services to Uganda Railways Corporation to improve the Kampala-Mukono-Jinja route and Kampala-Kyengera-Mityana route',
                            'baseline_value': 0.0,
                            'target_value': 1.0,
                            'measurement_unit': 'Project',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 3.00,
                            'budget_fy2027_28': 11.25,
                            'budget_fy2028_29': 14.06,
                            'budget_fy2029_30': 14.06,
                            'total_budget': 42.38
                        },
                        {
                            'name': 'Undertake feasibility studies and detailed designs for the Kampala light rail system',
                            'baseline_value': 0.0,
                            'target_value': 1.0,
                            'measurement_unit': 'Study',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 1.88,
                            'budget_fy2028_29': 3.75,
                            'budget_fy2029_30': 3.75,
                            'total_budget': 9.38
                        },
                        {
                            'name': 'Undertake additional engineering and optimise parking in the City under KCPP/OPMU/UCP phase 2 (30Km)',
                            'baseline_value': 0.0,
                            'target_value': 30.0,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 0.0,
                            'budget_fy2028_29': 78.00,
                            'budget_fy2029_30': 78.00,
                            'total_budget': 156.00
                        }
                    ]
                }
            }
        },

        # Road Infrastructure Projects
        'piap_actions_road_projects': {
            'name': 'Road Infrastructure Implementation Projects',
            'outcome': 'increased_infrastructure',
            'outputs': {
                'output_road_projects': {
                    'name': 'Road Infrastructure Projects Completed',
                    'actions': [
                        {
                            'name': 'Implement the Kampala City Road Rehabilitation Project financed by the AfDB (about 8.77 km/USD)',
                            'baseline_value': 0.0,
                            'target_value': 8.77,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 217.16,
                            'budget_fy2026_27': 65.0,
                            'budget_fy2027_28': 0.0,
                            'budget_fy2028_29': 0.0,
                            'budget_fy2029_30': 0.0,
                            'total_budget': 217.16
                        },
                        {
                            'name': 'Implement road improvement projects under the OPMU-UCP financed by the World Bank (about 8.3 Junctions)',
                            'baseline_value': 0.0,
                            'target_value': 8.3,
                            'measurement_unit': 'Junctions',
                            'budget_fy2025_26': 113.96,
                            'budget_fy2026_27': 96.41,
                            'budget_fy2027_28': 17.56,
                            'budget_fy2028_29': 0.0,
                            'budget_fy2029_30': 0.0,
                            'total_budget': 228.02
                        },
                        {
                            'name': 'Implement road improvement projects financed by Government of Uganda (GoU) - GoTT Services Project',
                            'baseline_value': 0.0,
                            'target_value': 1.0,
                            'measurement_unit': 'Project',
                            'budget_fy2025_26': 75.00,
                            'budget_fy2026_27': 118.00,
                            'budget_fy2027_28': 130.00,
                            'budget_fy2028_29': 130.00,
                            'budget_fy2029_30': 96.10,
                            'total_budget': 550.00
                        },
                        {
                            'name': 'Implement Road improvement under the Kampala City Roads and Bridges Upgrading Project financed by JICA (12Km & 1 Pedestrian Bridge - Jali, Kawempe Projects & Queensway Close Project)',
                            'baseline_value': 0.0,
                            'target_value': 12.0,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 517.85,
                            'budget_fy2027_28': 197.54,
                            'budget_fy2028_29': 197.54,
                            'budget_fy2029_30': 149.15,
                            'total_budget': 1061.91
                        },
                        {
                            'name': 'Upgrade 8 Arterial roads in the City under KCPP/OPMU/UCP phase 2 (30Km)',
                            'baseline_value': 0.0,
                            'target_value': 30.0,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 0.0,
                            'budget_fy2028_29': 78.00,
                            'budget_fy2029_30': 78.00,
                            'total_budget': 156.00
                        },
                        {
                            'name': 'Design, complete & upgrade key junctions under KCPP-Mukwano, Kyanja, Pece and Soroti City Junctions',
                            'baseline_value': 0.0,
                            'target_value': 4.0,
                            'measurement_unit': 'Junctions',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 55.00,
                            'budget_fy2028_29': 40.00,
                            'budget_fy2029_30': 30.00,
                            'total_budget': 78.00
                        },
                        {
                            'name': 'Modernise and optimise parking in the City under KCPP/OPMU/UCP phase 2 (30Km)',
                            'baseline_value': 0.0,
                            'target_value': 1.0,
                            'measurement_unit': 'System',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 0.0,
                            'budget_fy2027_28': 0.10,
                            'budget_fy2028_29': 0.10,
                            'budget_fy2029_30': 0.00,
                            'total_budget': 0.20
                        },
                        {
                            'name': 'Implement the Statutory Instrument for Restriction of Heavy Goods Vehicles as assessed, reviewed and updated',
                            'baseline_value': 0.0,
                            'target_value': 1.0,
                            'measurement_unit': 'Policy',
                            'budget_fy2025_26': 0.0,
                            'budget_fy2026_27': 2.15,
                            'budget_fy2027_28': 0.10,
                            'budget_fy2028_29': 0.00,
                            'budget_fy2029_30': 0.00,
                            'total_budget': 2.20
                        }
                    ]
                }
            }
        },

        # Performance Indicators from the table
        'performance_indicators': {
            'name': 'Transport Performance Monitoring',
            'outcome': 'reduced_travel_time',
            'outputs': {
                'output_performance_monitoring': {
                    'name': 'Transport Performance Indicators Tracked',
                    'actions': [
                        {
                            'name': 'Average Travel time (MMHH) on KCCA Road Links',
                            'baseline_value': 4.2,
                            'target_value': 3.0,
                            'measurement_unit': 'Minutes',
                            'budget_fy2025_26': 4.2,
                            'budget_fy2026_27': 4.0,
                            'budget_fy2027_28': 3.8,
                            'budget_fy2028_29': 3.5,
                            'budget_fy2029_30': 3.0,
                            'total_budget': 3.0
                        },
                        {
                            'name': 'Proportion of commuting trips using public transport in the City',
                            'baseline_value': 25.0,
                            'target_value': 50.0,
                            'measurement_unit': 'Percentage',
                            'budget_fy2025_26': 25.0,
                            'budget_fy2026_27': 30.0,
                            'budget_fy2027_28': 35.0,
                            'budget_fy2028_29': 40.0,
                            'budget_fy2029_30': 50.0,
                            'total_budget': 50.0
                        },
                        {
                            'name': 'Proportion of city road network with street lights',
                            'baseline_value': 15.0,
                            'target_value': 100.0,
                            'measurement_unit': 'Percentage',
                            'budget_fy2025_26': 15.0,
                            'budget_fy2026_27': 30.0,
                            'budget_fy2027_28': 50.0,
                            'budget_fy2028_29': 75.0,
                            'budget_fy2029_30': 100.0,
                            'total_budget': 100.0
                        },
                        {
                            'name': 'Proportion of city road network paved',
                            'baseline_value': 37.0,
                            'target_value': 51.0,
                            'measurement_unit': 'Percentage',
                            'budget_fy2025_26': 39.0,
                            'budget_fy2026_27': 64.0,
                            'budget_fy2027_28': 48.0,
                            'budget_fy2028_29': 51.0,
                            'budget_fy2029_30': 51.0,
                            'total_budget': 51.0
                        },
                        {
                            'name': 'Km of City Roads Paved',
                            'baseline_value': 776.50,
                            'target_value': 1094.08,
                            'measurement_unit': 'Km',
                            'budget_fy2025_26': 68.82,
                            'budget_fy2026_27': 142.24,
                            'budget_fy2027_28': 82.40,
                            'budget_fy2028_29': 64.69,
                            'budget_fy2029_30': 51.48,
                            'total_budget': 1094.08
                        },
                        {
                            'name': 'Fatalities per 100,000 persons (Roads)',
                            'baseline_value': 11.00,
                            'target_value': 5.00,
                            'measurement_unit': 'Rate',
                            'budget_fy2025_26': 10.00,
                            'budget_fy2026_27': 9.00,
                            'budget_fy2027_28': 8.00,
                            'budget_fy2028_29': 6.00,
                            'budget_fy2029_30': 5.00,
                            'total_budget': 5.00
                        }
                    ]
                }
            }
        }
    }
    
    # Import the data
    total_actions_created = 0
    
    for intervention_key, intervention_data in piap_data.items():
        print(f"\n📋 Processing {intervention_data['name']}...")
        
        # Get the outcome
        outcome = outcome_map.get(intervention_data['outcome'])
        if not outcome:
            print(f"❌ Outcome not found for {intervention_data['outcome']}")
            continue
        
        # Create intervention
        intervention = env['intervention'].create({
            'name': intervention_data['name'],
            'outcome_id': outcome.id,
            'programme_id': programme.id,
            'objective_id': objective.id
        })
        
        print(f"✅ Created intervention: {intervention.name}")
        
        # Process outputs
        for output_key, output_data in intervention_data['outputs'].items():
            # Create output
            output = env['output'].create({
                'name': output_data['name'],
                'intervention_id': intervention.id,
                'outcome_id': outcome.id,
                'programme_id': programme.id,
                'objective_id': objective.id
            })
            
            print(f"  ✅ Created output: {output.name}")
            
            # Process PIAP Actions
            for action_data in output_data['actions']:
                piap_action = env['piap.action'].create({
                    'name': action_data['name'],
                    'output_id': output.id,
                    'intervention_id': intervention.id,
                    'outcome_id': outcome.id,
                    'objective_id': objective.id,
                    'programme_id': programme.id,
                    'baseline_value': action_data['baseline_value'],
                    'target_value': action_data['target_value'],
                    'measurement_unit': action_data['measurement_unit'],
                    'budget_fy2022_23': action_data.get('budget_fy2022_23', 0.0),
                    'budget_fy2023_24': action_data.get('budget_fy2023_24', 0.0),
                    'budget_fy2024_25': action_data.get('budget_fy2024_25', 0.0),
                    'budget_fy2025_26': action_data.get('budget_fy2025_26', 0.0),
                    'budget_fy2026_27': action_data.get('budget_fy2026_27', 0.0),
                    'budget_fy2027_28': action_data.get('budget_fy2027_28', 0.0),
                    'budget_fy2028_29': action_data.get('budget_fy2028_29', 0.0),
                    'budget_fy2029_30': action_data.get('budget_fy2029_30', 0.0),
                    'total_budget': action_data['total_budget'],
                    'status': 'planned',
                    'progress': 0.0,
                    'responsible_user_id': 1  # Admin user
                })
                
                total_actions_created += 1
                print(f"    ✅ Created PIAP Action: {piap_action.name}")
    
    print(f"\n🎉 IMPORT COMPLETED SUCCESSFULLY!")
    print(f"📊 Total PIAP Actions created: {total_actions_created}")
    print(f"📋 Total Interventions created: {len(piap_data)}")
    
    return True

if __name__ == "__main__":
    print("This script should be run from within Odoo shell")
    print("Usage: exec(open('import_piap_actions_complete.py').read())")
    print("Then: result = import_complete_piap_actions(env)")
