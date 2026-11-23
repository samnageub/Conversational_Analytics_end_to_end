{{ config(materialized='view', schema='business', alias='TopicPerformance', tags=['business']) }}

-- Grain: one row per item response.
-- Standalone business view over Gold source {{ source('gold', 'fact_response') }}; no aggregation is applied.
select
    attempt_id        AS AttemptId,
    customer_key      AS CustomerKey,
    candidate_key     AS CandidateKey,
    assessment_key    AS AssessmentKey,
    topic_key         AS TopicKey,
    item_key          AS ItemKey,
    attempt_date_key  AS AttemptDateKey,
    question_sequence AS QuestionSequence,
    is_correct        AS IsCorrect,
    points_available  AS PointsAvailable,
    points_earned     AS PointsEarned,
    response_seconds  AS ResponseSeconds,
    response_count    AS ResponseCount
from {{ source('gold', 'fact_response') }}
