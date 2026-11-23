create view [business].[Customer] as 

-- Grain: one row per customer.
-- Standalone business view over Gold source [Pearson_Gold_DW].[dbo].[dim_customer]; no aggregation is applied.
select
    customer_key     AS CustomerKey,
    customer_name    AS CustomerName,
    customer_segment AS CustomerSegment,
    country          AS Country,
    customer_status  AS CustomerStatus
from [Pearson_Gold_DW].[dbo].[dim_customer];

GO