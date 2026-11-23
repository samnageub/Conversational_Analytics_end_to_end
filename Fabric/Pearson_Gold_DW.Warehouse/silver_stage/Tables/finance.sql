CREATE TABLE [silver_stage].[finance] (
    [transaction_id]   VARCHAR (8000) NULL,
    [customer_id]      VARCHAR (8000) NULL,
    [candidate_id]     VARCHAR (8000) NULL,
    [registration_id]  VARCHAR (8000) NULL,
    [assessment_id]    VARCHAR (8000) NULL,
    [transaction_date] DATE           NULL,
    [transaction_type] VARCHAR (8000) NULL,
    [amount]           FLOAT (53)     NULL,
    [currency]         VARCHAR (8000) NULL,
    [payment_status]   VARCHAR (8000) NULL
);


GO