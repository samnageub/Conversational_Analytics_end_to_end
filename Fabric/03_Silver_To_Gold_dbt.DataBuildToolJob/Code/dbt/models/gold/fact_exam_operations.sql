-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    concat(
        cast(test_center_code as varchar(100)),
        '|',
        convert(char(8), cast(operation_date as date), 112)
    ) as exam_operations_key,
    cast(test_center_code as varchar(100)) as test_center_key,
    convert(int, convert(char(8), cast(operation_date as date), 112)) as operation_date_key,
    cast(coalesce(available_seats, 0) as int) as available_seats,
    cast(coalesce(reserved_seats, 0) as int) as reserved_seats,
    cast(coalesce(delivered_exams, 0) as int) as delivered_exams,
    cast(coalesce(cancelled_exams, 0) as int) as cancelled_exams,
    cast(coalesce(actual_utilization_rate, 0) as decimal(9, 4)) as actual_utilization_rate,
    cast(operational_pressure as varchar(20)) as operational_pressure,
    cast(1 as int) as operation_day_count
from {{ source('silver', 'daily_test_center_operations') }}
