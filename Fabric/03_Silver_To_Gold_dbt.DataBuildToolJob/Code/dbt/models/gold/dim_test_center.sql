-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(test_center_code as varchar(100)) as test_center_key,
    cast(test_center_name as varchar(250)) as test_center_name,
    cast(city as varchar(100)) as city,
    cast(state as varchar(100)) as state,
    cast(region as varchar(100)) as region,
    cast(base_daily_capacity as int) as base_daily_capacity,
    cast(status as varchar(50)) as test_center_status
from {{ source('silver', 'test_center') }}
