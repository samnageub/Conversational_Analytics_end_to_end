-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(topic_id as varchar(100)) as topic_key,
    cast(topic_name as varchar(250)) as topic_name,
    cast(topic_description as varchar(1000)) as topic_description,
    cast(status as varchar(50)) as topic_status
from {{ source('silver', 'topic') }}
