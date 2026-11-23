-- Fabric notebook source

-- METADATA ********************

-- META {
-- META   "kernel_info": {
-- META     "name": "sqldatawarehouse"
-- META   },
-- META   "dependencies": {
-- META     "warehouse": {
-- META       "default_warehouse": "3ab5ffe5-c5d1-a044-4679-6574250227eb",
-- META       "known_warehouses": [
-- META         {
-- META           "id": "3ab5ffe5-c5d1-a044-4679-6574250227eb",
-- META           "type": "Datawarehouse"
-- META         }
-- META       ]
-- META     }
-- META   }
-- META }

-- CELL ********************

/* ============================================================
   Pearson Conversational Analytics PoC
   Notebook: 02A_Clear_Gold_Stage

   Purpose:
   Reset transient Silver staging tables before the full
   Silver -> Gold Copy Job.

   Airflow sequence:
   Bronze -> Silver -> CLEAR STAGE -> Copy -> dbt -> Views
   ============================================================ */


/* ============================================================
   1. CLEAR SILVER STAGING TABLES
   ============================================================ */

TRUNCATE TABLE silver_stage.customer;
TRUNCATE TABLE silver_stage.candidate;
TRUNCATE TABLE silver_stage.program;
TRUNCATE TABLE silver_stage.assessment;
TRUNCATE TABLE silver_stage.topic;
TRUNCATE TABLE silver_stage.item;
TRUNCATE TABLE silver_stage.test_center;
TRUNCATE TABLE silver_stage.calendar;

TRUNCATE TABLE silver_stage.registration_enriched;
TRUNCATE TABLE silver_stage.attempt;
TRUNCATE TABLE silver_stage.response;
TRUNCATE TABLE silver_stage.finance;

TRUNCATE TABLE silver_stage.daily_test_center_operations;
TRUNCATE TABLE silver_stage.proctor_staffing;
TRUNCATE TABLE silver_stage.capacity_plan;


/* ============================================================
   2. VALIDATE THAT STAGING IS EMPTY

   Every RowCount below should return 0.
   ============================================================ */

SELECT
    'customer' AS TableName,
    COUNT_BIG(*) AS RowCount
FROM silver_stage.customer

UNION ALL

SELECT
    'candidate',
    COUNT_BIG(*)
FROM silver_stage.candidate

UNION ALL

SELECT
    'program',
    COUNT_BIG(*)
FROM silver_stage.program

UNION ALL

SELECT
    'assessment',
    COUNT_BIG(*)
FROM silver_stage.assessment

UNION ALL

SELECT
    'topic',
    COUNT_BIG(*)
FROM silver_stage.topic

UNION ALL

SELECT
    'item',
    COUNT_BIG(*)
FROM silver_stage.item

UNION ALL

SELECT
    'test_center',
    COUNT_BIG(*)
FROM silver_stage.test_center

UNION ALL

SELECT
    'calendar',
    COUNT_BIG(*)
FROM silver_stage.calendar

UNION ALL

SELECT
    'registration_enriched',
    COUNT_BIG(*)
FROM silver_stage.registration_enriched

UNION ALL

SELECT
    'attempt',
    COUNT_BIG(*)
FROM silver

-- METADATA ********************

-- META {
-- META   "language": "sql",
-- META   "language_group": "sqldatawarehouse"
-- META }
