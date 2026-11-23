create view [business].[Assessment] as 

-- Grain: one row per assessment.
-- Standalone business view over Gold source [Pearson_Gold_DW].[dbo].[dim_assessment]; no aggregation is applied.
select
    assessment_key            AS AssessmentKey,
    customer_key              AS CustomerKey,
    program_key               AS ProgramKey,
    assessment_code           AS AssessmentCode,
    assessment_name           AS AssessmentName,
    assessment_level          AS AssessmentLevel,
    passing_score             AS PassingScore,
    standard_duration_minutes AS StandardDurationMinutes,
    standard_price            AS StandardPrice,
    assessment_status         AS AssessmentStatus
from [Pearson_Gold_DW].[dbo].[dim_assessment];

GO