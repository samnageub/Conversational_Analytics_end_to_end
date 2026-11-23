CREATE TABLE [silver_stage].[calendar] (
    [date_key]      BIGINT         NULL,
    [calendar_date] DATE           NULL,
    [year]          BIGINT         NULL,
    [quarter]       VARCHAR (8000) NULL,
    [month_number]  BIGINT         NULL,
    [month_name]    VARCHAR (8000) NULL,
    [year_month]    VARCHAR (8000) NULL,
    [week_number]   BIGINT         NULL,
    [day_of_month]  BIGINT         NULL,
    [day_name]      VARCHAR (8000) NULL,
    [is_weekend]    BIT            NULL
);


GO