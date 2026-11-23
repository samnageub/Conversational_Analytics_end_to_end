-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(customer_id as varchar(100)) as customer_key,
    cast(customer_name as varchar(250)) as customer_name,
    cast(segment as varchar(100)) as customer_segment,
    cast(country as varchar(100)) as country,
    cast(status as varchar(50)) as customer_status
from {{ source('silver', 'customer') }}
