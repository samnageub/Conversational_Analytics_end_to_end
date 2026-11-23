create view [business].[Program] as 

-- Grain: one row per program.
-- Standalone business view over Gold source [Pearson_Gold_DW].[dbo].[dim_program]; no aggregation is applied.
select
    program_key      AS ProgramKey,
    customer_key     AS CustomerKey,
    program_code     AS ProgramCode,
    program_name     AS ProgramName,
    program_category AS ProgramCategory,
    program_status   AS ProgramStatus
from [Pearson_Gold_DW].[dbo].[dim_program];

GO