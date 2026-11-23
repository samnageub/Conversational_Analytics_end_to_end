{{ config(materialized='view', schema='business', alias='AssessmentPerformance', tags=['business']) }}

-- Grain: one row per assessment attempt.
-- Standalone business view over Gold source {{ source('gold', 'fact_attempt') }}; no aggregation is applied.
select
    attempt_id       AS AttemptId,
    registration_id  AS RegistrationId,
    customer_key     AS CustomerKey,
    candidate_key    AS CandidateKey,
    program_key      AS ProgramKey,
    assessment_key   AS AssessmentKey,
    test_center_key  AS TestCenterKey,
    attempt_date_key AS AttemptDateKey,
    attempt_number   AS AttemptNumber,
    score            AS Score,
    passing_score    AS PassingScore,
    score_margin     AS ScoreMargin,
    passed           AS Passed,
    attempt_status   AS AttemptStatus,
    duration_minutes AS DurationMinutes,
    attempt_count    AS AttemptCount
from {{ source('gold', 'fact_attempt') }}
