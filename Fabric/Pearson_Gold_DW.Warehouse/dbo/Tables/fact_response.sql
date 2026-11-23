CREATE TABLE [dbo].[fact_response] (
    [response_id]       VARCHAR (100) NULL,
    [attempt_id]        VARCHAR (100) NULL,
    [customer_key]      VARCHAR (100) NULL,
    [candidate_key]     VARCHAR (100) NULL,
    [assessment_key]    VARCHAR (100) NULL,
    [topic_key]         VARCHAR (100) NULL,
    [item_key]          VARCHAR (100) NULL,
    [attempt_date_key]  INT           NULL,
    [question_sequence] INT           NULL,
    [is_correct]        BIT           NULL,
    [points_available]  INT           NULL,
    [points_earned]     INT           NULL,
    [response_seconds]  INT           NULL,
    [response_count]    INT           NULL
);


GO