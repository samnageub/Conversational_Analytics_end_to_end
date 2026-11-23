-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

with capacity_by_day as (
    select
        test_center_code,
        planning_date,
        max(physical_capacity) as physical_capacity,
        max(planned_demand) as planned_demand,
        max(capacity_gap) as capacity_gap,
        max(planning_status) as planning_status
    from {{ source('silver', 'capacity_plan') }}
    group by test_center_code, planning_date
),
staffing_by_day as (
    select
        test_center_code,
        staffing_date,
        sum(proctors_scheduled) as proctors_scheduled,
        sum(proctors_absent) as proctors_absent,
        sum(proctors_available) as proctors_available,
        sum(proctors_required) as proctors_required,
        sum(staffing_gap) as staffing_gap
    from {{ source('silver', 'proctor_staffing') }}
    group by test_center_code, staffing_date
)
select
    concat(
        cast(coalesce(c.test_center_code, s.test_center_code) as varchar(100)),
        '|',
        convert(char(8), cast(coalesce(c.planning_date, s.staffing_date) as date), 112)
    ) as capacity_staffing_key,
    cast(coalesce(c.test_center_code, s.test_center_code) as varchar(100)) as test_center_key,
    convert(int, convert(char(8), cast(coalesce(c.planning_date, s.staffing_date) as date), 112)) as planning_date_key,
    cast(coalesce(c.physical_capacity, 0) as int) as physical_capacity,
    cast(coalesce(c.planned_demand, 0) as int) as planned_demand,
    cast(coalesce(c.capacity_gap, 0) as int) as capacity_gap,
    cast(c.planning_status as varchar(50)) as planning_status,
    cast(coalesce(s.proctors_scheduled, 0) as int) as proctors_scheduled,
    cast(coalesce(s.proctors_absent, 0) as int) as proctors_absent,
    cast(coalesce(s.proctors_available, 0) as int) as proctors_available,
    cast(coalesce(s.proctors_required, 0) as int) as proctors_required,
    cast(coalesce(s.staffing_gap, 0) as int) as staffing_gap,
    cast(case when coalesce(s.staffing_gap, 0) > 0 then 1 else 0 end as bit) as is_understaffed,
    cast(
        case
            when coalesce(s.proctors_required, 0) > 0
                then cast(s.proctors_available as decimal(18, 4)) / cast(s.proctors_required as decimal(18, 4))
            else null
        end
        as decimal(9, 4)
    ) as staffing_coverage_rate,
    cast(1 as int) as capacity_staffing_day_count
from capacity_by_day as c
full outer join staffing_by_day as s
    on c.test_center_code = s.test_center_code
   and c.planning_date = s.staffing_date
