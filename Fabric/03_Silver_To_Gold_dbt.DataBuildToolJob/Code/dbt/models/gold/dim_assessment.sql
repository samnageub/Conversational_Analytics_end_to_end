-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(assessment_id as varchar(100)) as assessment_key,
    cast(customer_id as varchar(100)) as customer_key,
    cast(program_id as varchar(100)) as program_key,
    cast(assessment_code as varchar(100)) as assessment_code,
    cast(assessment_name as varchar(250)) as assessment_name,
    cast(assessment_level as varchar(100)) as assessment_level,
    cast(passing_score as int) as passing_score,
    cast(standard_duration_minutes as int) as standard_duration_minutes,
    cast(standard_price as decimal(18, 2)) as standard_price,
    cast(status as varchar(50)) as assessment_status
from {{ source('silver', 'assessment') }}
