CREATE TABLE [silver_stage].[exam_journey] (
    [registration_id]    VARCHAR (8000) NULL,
    [original_exam_date] DATE           NULL,
    [final_exam_date]    DATE           NULL,
    [reschedule_count]   BIGINT         NULL,
    [was_delivered]      INT            NULL,
    [was_cancelled]      INT            NULL,
    [was_no_show]        INT            NULL,
    [was_rescheduled]    BIT            NULL,
    [days_shifted]       INT            NULL
);


GO