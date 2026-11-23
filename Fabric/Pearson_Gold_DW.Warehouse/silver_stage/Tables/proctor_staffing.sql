CREATE TABLE [silver_stage].[proctor_staffing] (
    [staffing_id]            VARCHAR (8000) NULL,
    [test_center_code]       VARCHAR (8000) NULL,
    [staffing_date]          DATE           NULL,
    [shift_name]             VARCHAR (8000) NULL,
    [proctors_scheduled]     INT            NULL,
    [proctors_absent]        INT            NULL,
    [proctors_available]     INT            NULL,
    [proctors_required]      INT            NULL,
    [staffing_gap]           INT            NULL,
    [is_understaffed]        BIT            NULL,
    [staffing_coverage_rate] FLOAT (53)     NULL
);


GO