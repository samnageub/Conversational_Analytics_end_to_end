CREATE TABLE [dbo].[fact_attempt] (
    [attempt_id]       VARCHAR (100) NULL,
    [registration_id]  VARCHAR (100) NULL,
    [customer_key]     VARCHAR (100) NULL,
    [candidate_key]    VARCHAR (100) NULL,
    [program_key]      VARCHAR (100) NULL,
    [assessment_key]   VARCHAR (100) NULL,
    [test_center_key]  VARCHAR (100) NULL,
    [attempt_date_key] INT           NULL,
    [attempt_number]   INT           NULL,
    [score]            INT           NULL,
    [passing_score]    INT           NULL,
    [score_margin]     INT           NULL,
    [passed]           BIT           NULL,
    [attempt_status]   VARCHAR (50)  NULL,
    [duration_minutes] INT           NULL,
    [attempt_count]    INT           NULL
);


GO