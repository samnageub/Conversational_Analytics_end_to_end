create view [business].[FinancialPerformance] as 

-- Grain: one row per financial transaction.
-- Standalone business view over Gold source [Pearson_Gold_DW].[dbo].[fact_finance]; no aggregation is applied.
select
    registration_id      AS RegistrationId,
    customer_key         AS CustomerKey,
    candidate_key        AS CandidateKey,
    assessment_key       AS AssessmentKey,
    transaction_date_key AS TransactionDateKey,
    transaction_type     AS TransactionType,
    amount               AS Amount,
    currency             AS Currency,
    payment_status       AS PaymentStatus,
    transaction_count    AS TransactionCount
from [Pearson_Gold_DW].[dbo].[fact_finance];

GO