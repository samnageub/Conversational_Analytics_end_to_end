{{ config(materialized='view', schema='business', alias='Topic', tags=['business']) }}

-- Grain: one row per topic.
-- Standalone business view over Gold source {{ source('gold', 'dim_topic') }}; no aggregation is applied.
select
    topic_key         AS TopicKey,
    topic_name        AS TopicName,
    topic_description AS TopicDescription,
    topic_status      AS TopicStatus
from {{ source('gold', 'dim_topic') }}
