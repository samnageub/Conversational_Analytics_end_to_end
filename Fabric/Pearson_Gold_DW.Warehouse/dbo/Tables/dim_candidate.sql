CREATE TABLE [dbo].[dim_candidate] (
    [candidate_key]          VARCHAR (100) NULL,
    [customer_key]           VARCHAR (100) NULL,
    [candidate_display_name] VARCHAR (250) NULL,
    [region_code]            VARCHAR (50)  NULL,
    [region_name]            VARCHAR (100) NULL,
    [candidate_status]       VARCHAR (50)  NULL
);


GO