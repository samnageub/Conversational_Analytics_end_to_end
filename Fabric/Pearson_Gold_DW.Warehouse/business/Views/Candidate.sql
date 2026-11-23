create view [business].[Candidate] as 

-- Grain: one row per candidate.
-- Standalone business view over Gold source [Pearson_Gold_DW].[dbo].[dim_candidate]; no aggregation is applied.
select
    candidate_key          AS CandidateKey,
    customer_key           AS CustomerKey,
    candidate_display_name AS CandidateDisplayName,
    region_code            AS RegionCode,
    region_name            AS RegionName,
    candidate_status       AS CandidateStatus
from [Pearson_Gold_DW].[dbo].[dim_candidate];

GO