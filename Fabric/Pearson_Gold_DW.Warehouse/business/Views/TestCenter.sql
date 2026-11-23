create view [business].[TestCenter] as 

-- Grain: one row per test center.
-- Standalone business view over Gold source [Pearson_Gold_DW].[dbo].[dim_test_center]; no aggregation is applied.
select
    test_center_key     AS TestCenterKey,
    test_center_name    AS TestCenterName,
    city                AS City,
    state               AS State,
    region              AS Region,
    base_daily_capacity AS BaseDailyCapacity,
    test_center_status  AS TestCenterStatus
from [Pearson_Gold_DW].[dbo].[dim_test_center];

GO