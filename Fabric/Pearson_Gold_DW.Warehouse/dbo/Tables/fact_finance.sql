CREATE TABLE [dbo].[fact_finance] (
    [transaction_id]       VARCHAR (100)   NULL,
    [registration_id]      VARCHAR (100)   NULL,
    [customer_key]         VARCHAR (100)   NULL,
    [candidate_key]        VARCHAR (100)   NULL,
    [assessment_key]       VARCHAR (100)   NULL,
    [transaction_date_key] INT             NULL,
    [transaction_type]     VARCHAR (50)    NULL,
    [amount]               DECIMAL (18, 2) NULL,
    [currency]             CHAR (3)        NULL,
    [payment_status]       VARCHAR (50)    NULL,
    [transaction_count]    INT             NULL
);


GO