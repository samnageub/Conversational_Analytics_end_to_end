{{ config(materialized='view', schema='business', alias='Registrations', tags=['business']) }}

-- Grain: one row per registration.
-- Standalone business view over Gold source {{ source('gold', 'fact_registration') }}; no aggregation is applied.
select
    registration_id        AS RegistrationId,
    customer_key           AS CustomerKey,
    candidate_key          AS CandidateKey,
    program_key            AS ProgramKey,
    assessment_key         AS AssessmentKey,
    test_center_key        AS TestCenterKey,
    registration_date_key  AS RegistrationDateKey,
    original_exam_date_key AS OriginalExamDateKey,
    final_exam_date_key    AS FinalExamDateKey,
    registration_status    AS RegistrationStatus,
    delivery_mode          AS DeliveryMode,
    was_rescheduled        AS WasRescheduled,
    reschedule_count       AS RescheduleCount,
    days_shifted           AS DaysShifted,
    registration_count     AS RegistrationCount
from {{ source('gold', 'fact_registration') }}
