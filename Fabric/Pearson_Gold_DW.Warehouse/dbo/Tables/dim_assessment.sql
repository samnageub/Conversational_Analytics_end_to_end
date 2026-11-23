CREATE TABLE [dbo].[dim_assessment] (
    [assessment_key]            VARCHAR (100)   NULL,
    [customer_key]              VARCHAR (100)   NULL,
    [program_key]               VARCHAR (100)   NULL,
    [assessment_code]           VARCHAR (100)   NULL,
    [assessment_name]           VARCHAR (250)   NULL,
    [assessment_level]          VARCHAR (100)   NULL,
    [passing_score]             INT             NULL,
    [standard_duration_minutes] INT             NULL,
    [standard_price]            DECIMAL (18, 2) NULL,
    [assessment_status]         VARCHAR (50)    NULL
);


GO