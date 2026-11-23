CREATE TABLE [dbo].[dim_date] (
    [date_key]         INT          NULL,
    [calendar_date]    DATE         NULL,
    [calendar_year]    INT          NULL,
    [calendar_quarter] VARCHAR (2)  NULL,
    [month_number]     INT          NULL,
    [month_name]       VARCHAR (20) NULL,
    [year_month]       VARCHAR (20) NULL,
    [week_number]      INT          NULL,
    [day_of_month]     INT          NULL,
    [day_name]         VARCHAR (20) NULL,
    [is_weekend]       BIT          NULL
);


GO