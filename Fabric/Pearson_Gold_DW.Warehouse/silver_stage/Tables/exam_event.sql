CREATE TABLE [silver_stage].[exam_event] (
    [exam_event_id]      VARCHAR (8000) NULL,
    [registration_id]    VARCHAR (8000) NULL,
    [customer_id]        VARCHAR (8000) NULL,
    [candidate_id]       VARCHAR (8000) NULL,
    [assessment_id]      VARCHAR (8000) NULL,
    [test_center_code]   VARCHAR (8000) NULL,
    [event_date]         DATE           NULL,
    [event_type]         VARCHAR (8000) NULL,
    [original_exam_date] DATE           NULL,
    [new_exam_date]      DATE           NULL,
    [reschedule_reason]  VARCHAR (8000) NULL
);


GO