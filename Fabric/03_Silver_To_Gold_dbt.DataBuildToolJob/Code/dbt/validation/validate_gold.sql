-- Run in Pearson_Gold_DW after dbt build.
-- Result 1: exactly 14 rows, each with row_count > 0 for the supplied synthetic PoC data.
select 'dim_customer' as table_name, count_big(*) as row_count from dbo.dim_customer
union all select 'dim_candidate', count_big(*) from dbo.dim_candidate
union all select 'dim_program', count_big(*) from dbo.dim_program
union all select 'dim_assessment', count_big(*) from dbo.dim_assessment
union all select 'dim_topic', count_big(*) from dbo.dim_topic
union all select 'dim_item', count_big(*) from dbo.dim_item
union all select 'dim_test_center', count_big(*) from dbo.dim_test_center
union all select 'dim_date', count_big(*) from dbo.dim_date
union all select 'fact_registration', count_big(*) from dbo.fact_registration
union all select 'fact_attempt', count_big(*) from dbo.fact_attempt
union all select 'fact_response', count_big(*) from dbo.fact_response
union all select 'fact_finance', count_big(*) from dbo.fact_finance
union all select 'fact_exam_operations', count_big(*) from dbo.fact_exam_operations
union all select 'fact_capacity_staffing', count_big(*) from dbo.fact_capacity_staffing;

-- Result 2: all duplicate counts should be 0.
select 'dim_customer.customer_key' as check_name, count_big(*) as duplicate_groups
from (select customer_key from dbo.dim_customer group by customer_key having count_big(*) > 1) d
union all select 'dim_candidate.candidate_key', count_big(*) from (select candidate_key from dbo.dim_candidate group by candidate_key having count_big(*) > 1) d
union all select 'dim_program.program_key', count_big(*) from (select program_key from dbo.dim_program group by program_key having count_big(*) > 1) d
union all select 'dim_assessment.assessment_key', count_big(*) from (select assessment_key from dbo.dim_assessment group by assessment_key having count_big(*) > 1) d
union all select 'dim_topic.topic_key', count_big(*) from (select topic_key from dbo.dim_topic group by topic_key having count_big(*) > 1) d
union all select 'dim_item.item_key', count_big(*) from (select item_key from dbo.dim_item group by item_key having count_big(*) > 1) d
union all select 'dim_test_center.test_center_key', count_big(*) from (select test_center_key from dbo.dim_test_center group by test_center_key having count_big(*) > 1) d
union all select 'dim_date.date_key', count_big(*) from (select date_key from dbo.dim_date group by date_key having count_big(*) > 1) d
union all select 'fact_registration.registration_id', count_big(*) from (select registration_id from dbo.fact_registration group by registration_id having count_big(*) > 1) d
union all select 'fact_attempt.attempt_id', count_big(*) from (select attempt_id from dbo.fact_attempt group by attempt_id having count_big(*) > 1) d
union all select 'fact_response.response_id', count_big(*) from (select response_id from dbo.fact_response group by response_id having count_big(*) > 1) d
union all select 'fact_finance.transaction_id', count_big(*) from (select transaction_id from dbo.fact_finance group by transaction_id having count_big(*) > 1) d
union all select 'fact_exam_operations.exam_operations_key', count_big(*) from (select exam_operations_key from dbo.fact_exam_operations group by exam_operations_key having count_big(*) > 1) d
union all select 'fact_capacity_staffing.capacity_staffing_key', count_big(*) from (select capacity_staffing_key from dbo.fact_capacity_staffing group by capacity_staffing_key having count_big(*) > 1) d;
