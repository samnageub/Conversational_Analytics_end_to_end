# Fallback staging (use only if the direct preflight fails)

The default project uses the supported same-workspace path:
`Pearson_Gold_DW` dbt execution -> `Pearson_Silver_LH` SQL analytics endpoint -> Delta tables.
Do not stage data when `prerequisites/01_preflight.sql` succeeds.

If the Warehouse identity cannot query the Lakehouse endpoint after access is corrected, use a Fabric **Copy job** (or Data Pipeline Copy activity) as the least-complex physical staging fallback:

1. In `Pearson_Gold_DW`, create schema `silver_stage` once:
   `CREATE SCHEMA [silver_stage];`
2. Create one Copy job in `pearson_conversational_analytics_poc`.
3. Source: the SQL analytics endpoint for `Pearson_Silver_LH`, schema `dbo`.
4. Destination: `Pearson_Gold_DW`, schema `silver_stage`.
5. Copy these 15 tables with overwrite/recreate semantics before every dbt build:
   `customer`, `program`, `assessment`, `topic`, `item`, `candidate`,
   `test_center`, `calendar`, `registration_enriched`, `attempt`, `response`,
   `finance`, `proctor_staffing`, `capacity_plan`, `daily_test_center_operations`.
6. Replace `models/sources.yml` with `fallback/sources_staged.yml` (renamed to `sources.yml`).
7. Orchestrate: Silver notebook -> Copy job -> dbt build.

This fallback preserves Bronze Lakehouse -> Silver Lakehouse -> dbt -> Gold Warehouse. The staging schema is transport-only; dbt still owns all 14 Gold tables in `dbo`.
