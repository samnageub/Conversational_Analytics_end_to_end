CREATE TABLE [silver_stage].[response] (
    [response_id]       VARCHAR (8000) NULL,
    [attempt_id]        VARCHAR (8000) NULL,
    [customer_id]       VARCHAR (8000) NULL,
    [candidate_id]      VARCHAR (8000) NULL,
    [assessment_id]     VARCHAR (8000) NULL,
    [topic_id]          VARCHAR (8000) NULL,
    [item_id]           VARCHAR (8000) NULL,
    [attempt_date]      DATE           NULL,
    [question_sequence] INT            NULL,
    [is_correct]        BIT            NULL,
    [points_available]  INT            NULL,
    [points_earned]     INT            NULL,
    [response_seconds]  INT            NULL
);


GO