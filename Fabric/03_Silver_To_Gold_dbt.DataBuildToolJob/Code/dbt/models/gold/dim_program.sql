-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(program_id as varchar(100)) as program_key,
    cast(customer_id as varchar(100)) as customer_key,
    cast(program_code as varchar(100)) as program_code,
    cast(program_name as varchar(250)) as program_name,
    cast(category as varchar(100)) as program_category,
    cast(status as varchar(50)) as program_status
from {{ source('silver', 'program') }}
