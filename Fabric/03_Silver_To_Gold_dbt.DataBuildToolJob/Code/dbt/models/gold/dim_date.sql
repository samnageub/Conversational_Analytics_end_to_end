-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(date_key as int) as date_key,
    cast(calendar_date as date) as calendar_date,
    cast(year as int) as calendar_year,
    cast(quarter as varchar(2)) as calendar_quarter,
    cast(month_number as int) as month_number,
    cast(month_name as varchar(20)) as month_name,
    cast(year_month as varchar(20)) as year_month,
    cast(week_number as int) as week_number,
    cast(day_of_month as int) as day_of_month,
    cast(day_name as varchar(20)) as day_name,
    cast(is_weekend as bit) as is_weekend
from {{ source('silver', 'calendar') }}
