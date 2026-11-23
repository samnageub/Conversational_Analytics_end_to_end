{{ config(materialized='view', schema='business', alias='ExamOperations', tags=['business']) }}

-- Grain: one row per test-center/date operational record.
-- Standalone business view over Gold source {{ source('gold', 'fact_exam_operations') }}; no aggregation is applied.
select
    test_center_key         AS TestCenterKey,
    operation_date_key      AS OperationDateKey,
    available_seats         AS AvailableSeats,
    reserved_seats          AS ReservedSeats,
    delivered_exams         AS DeliveredExams,
    cancelled_exams         AS CancelledExams,
    actual_utilization_rate AS ActualUtilizationRate,
    operational_pressure    AS OperationalPressure,
    operation_day_count     AS OperationDayCount
from {{ source('gold', 'fact_exam_operations') }}
