{{ config(materialized='view', schema='business', alias='CapacityAndStaffing', tags=['business']) }}

-- Grain: one row per test-center/date capacity and staffing record.
-- Standalone business view over Gold source {{ source('gold', 'fact_capacity_staffing') }}; no aggregation is applied.
select
    test_center_key             AS TestCenterKey,
    planning_date_key           AS PlanningDateKey,
    physical_capacity           AS PhysicalCapacity,
    planned_demand              AS PlannedDemand,
    capacity_gap                AS CapacityGap,
    planning_status             AS PlanningStatus,
    proctors_scheduled          AS ProctorsScheduled,
    proctors_absent             AS ProctorsAbsent,
    proctors_available          AS ProctorsAvailable,
    proctors_required           AS ProctorsRequired,
    staffing_gap                AS StaffingGap,
    is_understaffed             AS IsUnderstaffed,
    staffing_coverage_rate      AS StaffingCoverageRate,
    capacity_staffing_day_count AS CapacityStaffingDayCount
from {{ source('gold', 'fact_capacity_staffing') }}
