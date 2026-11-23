CREATE TABLE [silver_stage].[daily_test_center_operations] (
    [test_center_code]        VARCHAR (8000) NULL,
    [operation_date]          DATE           NULL,
    [available_seats]         BIGINT         NULL,
    [reserved_seats]          BIGINT         NULL,
    [delivered_exams]         BIGINT         NULL,
    [cancelled_exams]         BIGINT         NULL,
    [proctors_scheduled]      BIGINT         NULL,
    [proctors_available]      BIGINT         NULL,
    [proctors_required]       BIGINT         NULL,
    [staffing_gap]            BIGINT         NULL,
    [physical_capacity]       INT            NULL,
    [planned_demand]          INT            NULL,
    [planned_capacity_gap]    INT            NULL,
    [actual_utilization_rate] FLOAT (53)     NULL,
    [staffing_coverage_rate]  FLOAT (53)     NULL,
    [operational_pressure]    VARCHAR (8000) NULL
);


GO