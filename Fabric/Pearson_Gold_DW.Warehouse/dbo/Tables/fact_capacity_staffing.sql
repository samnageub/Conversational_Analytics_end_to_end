CREATE TABLE [dbo].[fact_capacity_staffing] (
    [capacity_staffing_key]       VARCHAR (109)  NOT NULL,
    [test_center_key]             VARCHAR (100)  NULL,
    [planning_date_key]           INT            NULL,
    [physical_capacity]           INT            NULL,
    [planned_demand]              INT            NULL,
    [capacity_gap]                INT            NULL,
    [planning_status]             VARCHAR (50)   NULL,
    [proctors_scheduled]          INT            NULL,
    [proctors_absent]             INT            NULL,
    [proctors_available]          INT            NULL,
    [proctors_required]           INT            NULL,
    [staffing_gap]                INT            NULL,
    [is_understaffed]             BIT            NULL,
    [staffing_coverage_rate]      DECIMAL (9, 4) NULL,
    [capacity_staffing_day_count] INT            NULL
);


GO