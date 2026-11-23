{{ config(materialized='view', schema='business', alias='Calendar', tags=['business']) }}

-- Grain: one row per calendar date.
-- Standalone business view over Gold source {{ source('gold', 'dim_date') }}; no aggregation is applied.
select
    date_key         AS DateKey,
    calendar_date    AS CalendarDate,
    calendar_year    AS CalendarYear,
    calendar_quarter AS CalendarQuarter,
    month_number     AS MonthNumber,
    month_name       AS MonthName,
    year_month       AS YearMonth,
    week_number      AS WeekNumber,
    day_of_month     AS DayOfMonth,
    day_name         AS DayName,
    is_weekend       AS IsWeekend
from {{ source('gold', 'dim_date') }}
