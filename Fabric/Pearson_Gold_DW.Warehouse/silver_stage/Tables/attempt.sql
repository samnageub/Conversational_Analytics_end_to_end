CREATE TABLE [silver_stage].[attempt] (
    [attempt_id]       VARCHAR (8000) NULL,
    [registration_id]  VARCHAR (8000) NULL,
    [customer_id]      VARCHAR (8000) NULL,
    [candidate_id]     VARCHAR (8000) NULL,
    [program_id]       VARCHAR (8000) NULL,
    [assessment_id]    VARCHAR (8000) NULL,
    [test_center_code] VARCHAR (8000) NULL,
    [attempt_date]     DATE           NULL,
    [attempt_number]   INT            NULL,
    [score]            INT            NULL,
    [passing_score]    INT            NULL,
    [passed]           BIT            NULL,
    [attempt_status]   VARCHAR (8000) NULL,
    [duration_minutes] INT            NULL
);


GO