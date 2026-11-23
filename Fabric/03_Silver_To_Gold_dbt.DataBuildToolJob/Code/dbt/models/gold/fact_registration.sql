-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(registration_id as varchar(100)) as registration_id,
    cast(customer_id as varchar(100)) as customer_key,
    cast(candidate_id as varchar(100)) as candidate_key,
    cast(program_id as varchar(100)) as program_key,
    cast(assessment_id as varchar(100)) as assessment_key,
    cast(test_center_code as varchar(100)) as test_center_key,
    convert(int, convert(char(8), cast(registration_date as date), 112)) as registration_date_key,
    convert(int, convert(char(8), cast(original_exam_date as date), 112)) as original_exam_date_key,
    convert(int, convert(char(8), cast(coalesce(final_exam_date, original_exam_date) as date), 112)) as final_exam_date_key,
    cast(registration_status as varchar(50)) as registration_status,
    cast(delivery_mode as varchar(50)) as delivery_mode,
    cast(was_rescheduled as bit) as was_rescheduled,
    cast(reschedule_count as int) as reschedule_count,
    cast(days_shifted as int) as days_shifted,
    cast(1 as int) as registration_count
from {{ source('silver', 'registration_enriched') }}
