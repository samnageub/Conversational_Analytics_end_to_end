create view [business].[Topic] as 

-- Grain: one row per topic.
-- Standalone business view over Gold source [Pearson_Gold_DW].[dbo].[dim_topic]; no aggregation is applied.
select
    topic_key         AS TopicKey,
    topic_name        AS TopicName,
    topic_description AS TopicDescription,
    topic_status      AS TopicStatus
from [Pearson_Gold_DW].[dbo].[dim_topic];

GO