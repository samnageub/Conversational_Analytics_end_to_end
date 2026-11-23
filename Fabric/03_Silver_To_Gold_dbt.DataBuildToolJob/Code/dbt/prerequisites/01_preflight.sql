-- Run this in Pearson_Gold_DW before the dbt build.
-- Same-workspace Lakehouse SQL endpoints are queried with three-part names.

select top (1) *
from [Pearson_Silver_LH].[dbo].[customer];

select
    count_big(*) as silver_customer_rows
from [Pearson_Silver_LH].[dbo].[customer];
