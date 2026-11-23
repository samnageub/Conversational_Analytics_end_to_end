CREATE TABLE [silver_stage].[exam_capacity] (
    [capacity_id]          VARCHAR (8000) NULL,
    [test_center_code]     VARCHAR (8000) NULL,
    [capacity_date]        DATE           NULL,
    [exam_type]            VARCHAR (8000) NULL,
    [available_seats]      INT            NULL,
    [reserved_seats]       INT            NULL,
    [delivered_exams]      INT            NULL,
    [cancelled_exams]      INT            NULL,
    [utilization_target]   FLOAT (53)     NULL,
    [reservation_rate]     FLOAT (53)     NULL,
    [delivery_utilization] FLOAT (53)     NULL,
    [unused_seats]         INT            NULL
);


GO