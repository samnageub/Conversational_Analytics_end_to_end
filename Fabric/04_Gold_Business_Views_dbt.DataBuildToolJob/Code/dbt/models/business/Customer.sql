{{ config(materialized='view', schema='business', alias='Customer', tags=['business']) }}

-- Grain: one row per customer.
-- Standalone business view over Gold source {{ source('gold', 'dim_customer') }}; no aggregation is applied.
select
    customer_key     AS CustomerKey,
    customer_name    AS CustomerName,
    customer_segment AS CustomerSegment,
    country          AS Country,
    customer_status  AS CustomerStatus
from {{ source('gold', 'dim_customer') }}
