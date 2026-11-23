-- Run in Pearson_Gold_DW after the dbt build.
-- Expected first result: exactly 14 rows in schema business.
select
    s.name as SchemaName,
    v.name as ViewName
from sys.views as v
inner join sys.schemas as s
    on v.schema_id = s.schema_id
where s.name = N'business'
  and v.name in
  (
      N'Customer', N'Candidate', N'Program', N'Assessment',
      N'Topic', N'Item', N'TestCenter', N'Calendar',
      N'Registrations', N'AssessmentPerformance', N'TopicPerformance',
      N'FinancialPerformance', N'ExamOperations', N'CapacityAndStaffing'
  )
order by v.name;

select top (5) * from [business].[Customer];
select top (5) * from [business].[Candidate];
select top (5) * from [business].[Program];
select top (5) * from [business].[Assessment];
select top (5) * from [business].[Topic];
select top (5) * from [business].[Item];
select top (5) * from [business].[TestCenter];
select top (5) * from [business].[Calendar];
select top (5) * from [business].[Registrations];
select top (5) * from [business].[AssessmentPerformance];
select top (5) * from [business].[TopicPerformance];
select top (5) * from [business].[FinancialPerformance];
select top (5) * from [business].[ExamOperations];
select top (5) * from [business].[CapacityAndStaffing];
