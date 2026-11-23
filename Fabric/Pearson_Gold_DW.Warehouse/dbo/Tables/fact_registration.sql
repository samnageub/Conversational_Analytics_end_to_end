CREATE TABLE [dbo].[fact_registration] (
    [registration_id]        VARCHAR (100) NULL,
    [customer_key]           VARCHAR (100) NULL,
    [candidate_key]          VARCHAR (100) NULL,
    [program_key]            VARCHAR (100) NULL,
    [assessment_key]         VARCHAR (100) NULL,
    [test_center_key]        VARCHAR (100) NULL,
    [registration_date_key]  INT           NULL,
    [original_exam_date_key] INT           NULL,
    [final_exam_date_key]    INT           NULL,
    [registration_status]    VARCHAR (50)  NULL,
    [delivery_mode]          VARCHAR (50)  NULL,
    [was_rescheduled]        BIT           NULL,
    [reschedule_count]       INT           NULL,
    [days_shifted]           INT           NULL,
    [registration_count]     INT           NULL
);


GO