create view [business].[Item] as 

-- Grain: one row per item.
-- Standalone business view over Gold source [Pearson_Gold_DW].[dbo].[dim_item]; no aggregation is applied.
select
    item_key       AS ItemKey,
    topic_key      AS TopicKey,
    item_name      AS ItemName,
    difficulty     AS Difficulty,
    maximum_points AS MaximumPoints,
    item_status    AS ItemStatus
from [Pearson_Gold_DW].[dbo].[dim_item];

GO