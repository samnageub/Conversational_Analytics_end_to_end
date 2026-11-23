CREATE TABLE [dbo].[fact_exam_operations] (
    [exam_operations_key]     VARCHAR (109)  NOT NULL,
    [test_center_key]         VARCHAR (100)  NULL,
    [operation_date_key]      INT            NULL,
    [available_seats]         INT            NULL,
    [reserved_seats]          INT            NULL,
    [delivered_exams]         INT            NULL,
    [cancelled_exams]         INT            NULL,
    [actual_utilization_rate] DECIMAL (9, 4) NULL,
    [operational_pressure]    VARCHAR (20)   NULL,
    [operation_day_count]     INT            NULL
);


GO