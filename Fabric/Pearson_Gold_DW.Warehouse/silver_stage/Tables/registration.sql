CREATE TABLE [silver_stage].[registration] (
    [registration_id]     VARCHAR (8000) NULL,
    [customer_id]         VARCHAR (8000) NULL,
    [candidate_id]        VARCHAR (8000) NULL,
    [program_id]          VARCHAR (8000) NULL,
    [assessment_id]       VARCHAR (8000) NULL,
    [test_center_code]    VARCHAR (8000) NULL,
    [registration_date]   DATE           NULL,
    [original_exam_date]  DATE           NULL,
    [registration_status] VARCHAR (8000) NULL,
    [delivery_mode]       VARCHAR (8000) NULL
);


GO