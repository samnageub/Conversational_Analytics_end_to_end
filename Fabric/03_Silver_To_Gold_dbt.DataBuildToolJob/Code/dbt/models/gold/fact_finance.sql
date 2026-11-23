-- Physical Gold table; schema is inherited from the Fabric job target (dbo).

select
    cast(transaction_id as varchar(100)) as transaction_id,
    cast(registration_id as varchar(100)) as registration_id,
    cast(customer_id as varchar(100)) as customer_key,
    cast(candidate_id as varchar(100)) as candidate_key,
    cast(assessment_id as varchar(100)) as assessment_key,
    convert(int, convert(char(8), cast(transaction_date as date), 112)) as transaction_date_key,
    cast(transaction_type as varchar(50)) as transaction_type,
    cast(amount as decimal(18, 2)) as amount,
    cast(currency as char(3)) as currency,
    cast(payment_status as varchar(50)) as payment_status,
    cast(1 as int) as transaction_count
from {{ source('silver', 'finance') }}
