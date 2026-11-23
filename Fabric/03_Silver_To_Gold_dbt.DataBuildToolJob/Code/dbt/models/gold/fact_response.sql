-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(response_id as varchar(100)) as response_id,
    cast(attempt_id as varchar(100)) as attempt_id,
    cast(customer_id as varchar(100)) as customer_key,
    cast(candidate_id as varchar(100)) as candidate_key,
    cast(assessment_id as varchar(100)) as assessment_key,
    cast(topic_id as varchar(100)) as topic_key,
    cast(item_id as varchar(100)) as item_key,
    convert(int, convert(char(8), cast(attempt_date as date), 112)) as attempt_date_key,
    cast(question_sequence as int) as question_sequence,
    cast(is_correct as bit) as is_correct,
    cast(points_available as int) as points_available,
    cast(points_earned as int) as points_earned,
    cast(response_seconds as int) as response_seconds,
    cast(1 as int) as response_count
from {{ source('silver', 'response') }}
