CREATE TABLE [silver_stage].[registration_enriched] (
    [registration_id]     VARCHAR (8000) NULL,
    [customer_id]         VARCHAR (8000) NULL,
    [candidate_id]        VARCHAR (8000) NULL,
    [program_id]          VARCHAR (8000) NULL,
    [assessment_id]       VARCHAR (8000) NULL,
    [test_center_code]    VARCHAR (8000) NULL,
    [registration_date]   DATE           NULL,
    [original_exam_date]  DATE           NULL,
    [final_exam_date]     DATE           NULL,
    [registration_status] VARCHAR (8000) NULL,
    [delivery_mode]       VARCHAR (8000) NULL,
    [was_rescheduled]     BIT            NULL,
    [reschedule_count]    BIGINT         NULL,
    [days_shifted]        INT            NULL
);


GO