-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(candidate_id as varchar(100)) as candidate_key,
    cast(customer_id as varchar(100)) as customer_key,
    cast(candidate_display_name as varchar(250)) as candidate_display_name,
    cast(region_code as varchar(50)) as region_code,
    cast(region_name as varchar(100)) as region_name,
    cast(status as varchar(50)) as candidate_status
from {{ source('silver', 'candidate') }}
