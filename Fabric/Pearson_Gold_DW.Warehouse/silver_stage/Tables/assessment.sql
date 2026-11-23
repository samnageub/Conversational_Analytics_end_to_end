CREATE TABLE [silver_stage].[assessment] (
    [assessment_id]             VARCHAR (8000) NULL,
    [customer_id]               VARCHAR (8000) NULL,
    [program_id]                VARCHAR (8000) NULL,
    [assessment_code]           VARCHAR (8000) NULL,
    [assessment_name]           VARCHAR (8000) NULL,
    [assessment_level]          VARCHAR (8000) NULL,
    [passing_score]             INT            NULL,
    [standard_duration_minutes] INT            NULL,
    [standard_price]            FLOAT (53)     NULL,
    [status]                    VARCHAR (8000) NULL
);


GO