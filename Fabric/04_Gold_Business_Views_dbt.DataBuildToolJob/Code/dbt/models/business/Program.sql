{{ config(materialized='view', schema='business', alias='Program', tags=['business']) }}

-- Grain: one row per program.
-- Standalone business view over Gold source {{ source('gold', 'dim_program') }}; no aggregation is applied.
select
    program_key      AS ProgramKey,
    customer_key     AS CustomerKey,
    program_code     AS ProgramCode,
    program_name     AS ProgramName,
    program_category AS ProgramCategory,
    program_status   AS ProgramStatus
from {{ source('gold', 'dim_program') }}
