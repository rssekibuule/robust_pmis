# KPI Hierarchy Classification System

## Overview

The KPI Hierarchy Classification System provides a comprehensive framework for organizing and grouping Key Performance Indicators (KPIs) according to the organizational structure. This system enables better reporting, visualization, and analysis of performance data across different organizational levels.

## Classification Structure

KPIs are classified using two primary dimensions:

### 1. Classification Level

This defines the hierarchical level the KPI belongs to within the organization:

- **Strategic Level**: High-level KPIs tied to strategic goals and objectives
- **Operational Level**: Mid-level KPIs related to operational execution
- **Tactical Level**: Short-term KPIs for tactical initiatives
- **Programme Level**: KPIs specific to programme performance
- **Division Level**: KPIs measuring division-specific performance
- **Directorate Level**: KPIs for directorate-level performance

### 2. Parent Type

This defines the specific entity type the KPI directly relates to:

- **Strategic Goal**: KPIs directly measuring strategic goal achievement
- **Strategic Objective**: KPIs measuring strategic objective performance
- **KRA**: KPIs under specific Key Result Areas
- **Programme**: KPIs for specific programmes
- **Division**: KPIs for specific divisions
- **Directorate**: KPIs for specific directorates

## System Features

### Automatic Classification

The system automatically classifies KPIs based on their relationships:

- KPIs linked to KRAs with strategic objectives or goals are classified as "strategic" level
- KPIs linked to programmes are classified as "programme" level
- KPIs linked to divisions are classified as "division" level
- KPIs linked to directorates are classified as "directorate" level

### Hierarchical Path

Each KPI maintains a hierarchical path that shows its position in the organization structure. For example:

- Strategic Goal > Strategic Objective > KRA > KPI
- Directorate > Division > Programme > KPI

### Search and Filtering

The system enables advanced search and filtering capabilities:

- Filter KPIs by classification level
- Filter KPIs by parent type
- Group KPIs by any organizational dimension

## User Interface

### Form View Enhancements

The KPI form now includes an "Organizational Classification" section displaying:

- Classification Level
- Parent Type
- Programme (if applicable)
- Division (if applicable)

### List View Enhancements

The KPI list view now displays classification information for better visibility:

- Classification Level column
- Parent Type column

### Search View Filters

New filters allow users to search and organize KPIs:

- Filter by Classification Level (Strategic, Operational, etc.)
- Filter by Parent Type (Strategic Goal, Programme, etc.)
- Group by any hierarchical dimension

## Reporting Benefits

The classification system enables advanced reporting capabilities:

1. **Hierarchical Reports**: Generate reports that show KPI performance by organizational hierarchy
2. **Cross-Cutting Analysis**: Analyze KPIs across different organizational dimensions
3. **Accountability Tracking**: Clearly identify which organizational units are responsible for which KPIs

## Implementation Notes

The classification system was implemented with minimal disruption to existing functionality:

- Existing KPIs are automatically classified based on their current relationships
- Migration scripts ensure all KPIs have appropriate classification values
- The system is fully backward-compatible with existing reports and views

## Future Enhancements

Planned enhancements to the classification system include:

1. **Custom Classification Rules**: Allow administrators to define custom classification rules
2. **Weighting by Level**: Apply different weights to KPIs based on their classification level
3. **Cascading Targets**: Enable target values to cascade down the organizational hierarchy
4. **Dashboard Hierarchy View**: Visual representation of the KPI hierarchy in dashboards
