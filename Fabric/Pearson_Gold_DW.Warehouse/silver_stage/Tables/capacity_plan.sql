CREATE TABLE [silver_stage].[capacity_plan] (
    [planning_id]         VARCHAR (8000) NULL,
    [test_center_code]    VARCHAR (8000) NULL,
    [planning_date]       DATE           NULL,
    [physical_capacity]   INT            NULL,
    [planned_demand]      INT            NULL,
    [planned_utilization] FLOAT (53)     NULL,
    [capacity_gap]        INT            NULL,
    [planning_status]     VARCHAR (8000) NULL,
    [is_over_capacity]    BIT            NULL
);


GO