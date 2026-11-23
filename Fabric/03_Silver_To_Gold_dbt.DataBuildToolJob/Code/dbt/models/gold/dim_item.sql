-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(item_id as varchar(100)) as item_key,
    cast(topic_id as varchar(100)) as topic_key,
    cast(item_name as varchar(500)) as item_name,
    cast(difficulty as varchar(50)) as difficulty,
    cast(maximum_points as int) as maximum_points,
    cast(status as varchar(50)) as item_status
from {{ source('silver', 'item') }}
