-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(attempt_id as varchar(100)) as attempt_id,
    cast(registration_id as varchar(100)) as registration_id,
    cast(customer_id as varchar(100)) as customer_key,
    cast(candidate_id as varchar(100)) as candidate_key,
    cast(program_id as varchar(100)) as program_key,
    cast(assessment_id as varchar(100)) as assessment_key,
    cast(test_center_code as varchar(100)) as test_center_key,
    convert(int, convert(char(8), cast(attempt_date as date), 112)) as attempt_date_key,
    cast(attempt_number as int) as attempt_number,
    cast(score as int) as score,
    cast(passing_score as int) as passing_score,
    cast(score - passing_score as int) as score_margin,
    cast(passed as bit) as passed,
    cast(attempt_status as varchar(50)) as attempt_status,
    cast(duration_minutes as int) as duration_minutes,
    cast(1 as int) as attempt_count
from {{ source('silver', 'attempt') }}
