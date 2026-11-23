# Pearson conversational analytics PoC — Gold dbt project

This package builds **14 physical Gold tables** in `Pearson_Gold_DW.dbo` from cleaned Delta tables in `Pearson_Silver_LH.dbo`.

## Architecture and supported source path

`Pearson_Bronze_LH` -> `Pearson_Silver_LH` -> `03_Silver_To_Gold_dbt` -> `Pearson_Gold_DW.dbo`

The default source definition is intentional: a dbt job running against a Fabric Warehouse can read a Lakehouse SQL analytics endpoint in the **same workspace** with three-part naming. dbt compiles `source('silver', 'customer')` to the equivalent of `[Pearson_Silver_LH].[dbo].[customer]`. Only Lakehouse Delta tables registered under the **Tables** area are exposed through that read-only endpoint.

Run `prerequisites/01_preflight.sql` in `Pearson_Gold_DW` first. If it succeeds, use the project unchanged. If it fails after permissions and same-workspace placement are verified, follow `fallback/README.md`; do not add unsupported ad-hoc linked-server or four-part-name syntax.

## Put the files in the Fabric dbt Job

Open `03_Silver_To_Gold_dbt` in workspace `pearson_conversational_analytics_poc`.

1. At the project root, replace/create `dbt_project.yml` with this package's file.
2. Under `models/`, add `sources.yml` and `schema.yml`.
3. Under `models/gold/`, add all 14 `.sql` files.
4. The `prerequisites/`, `fallback/`, and `validation/` folders are operator documentation/scripts; they do not need to be added to the dbt Job.
5. In **dbt configurations**, set:
   - Adapter: `DataWarehouse`
   - Connection: `Pearson_Gold_DW`
   - Schema: `dbo`
6. The connection identity needs read access to `Pearson_Silver_LH` and read/write access to `Pearson_Gold_DW`.

Do **not** add `+schema: dbo` to the project. The target profile already supplies `dbo`; inheriting it avoids accidental custom schema names such as `dbo_dbo`.

## Build

Recommended command:

```bash
dbt build --select tag:gold
```

In the Fabric UI, choose **Build** and run all project resources (or use advanced selector `tag:gold`). Build creates/replaces the 14 physical tables and then runs the schema tests. No ephemeral models are used; each model is a direct select or a flat CTE query compatible with the `dbt-fabric` Warehouse adapter.

## Gold tables and grain

| Table | Grain | Primary key |
|---|---|---|
| `dim_customer` | one customer | `customer_key` |
| `dim_candidate` | one candidate | `candidate_key` |
| `dim_program` | one program | `program_key` |
| `dim_assessment` | one assessment | `assessment_key` |
| `dim_topic` | one topic | `topic_key` |
| `dim_item` | one item | `item_key` |
| `dim_test_center` | one test center | `test_center_key` |
| `dim_date` | one calendar date | `date_key` |
| `fact_registration` | one registration | `registration_id` |
| `fact_attempt` | one assessment attempt | `attempt_id` |
| `fact_response` | one item response | `response_id` |
| `fact_finance` | one financial transaction | `transaction_id` |
| `fact_exam_operations` | one test center/day | `exam_operations_key` |
| `fact_capacity_staffing` | one test center/day | `capacity_staffing_key` |

Dimension keys are deterministic natural keys cast to consistent Warehouse types. They remain stable across full-refresh builds and avoid unstable `row_number()` surrogate keys. Composite daily fact keys use test center plus `YYYYMMDD`.

## Compact validation checklist

- [ ] `dbt build --select tag:gold` succeeds with no model or test failures.
- [ ] Exactly 14 `dim_*`/`fact_*` tables appear in `Pearson_Gold_DW.dbo`.
- [ ] Every table returns rows for the supplied PoC data.
- [ ] All 14 primary-key uniqueness/not-null tests pass.
- [ ] Dimension parent relationships pass (`candidate/program/assessment -> customer`, `assessment -> program`, `item -> topic`).
- [ ] Fact relationships pass to customer, candidate, program, assessment, topic, item, test center, and date where applicable.
- [ ] `fact_attempt.registration_id` resolves to `fact_registration`; `fact_response.attempt_id` resolves to `fact_attempt`; `fact_finance.registration_id` resolves to `fact_registration`.
- [ ] `validation/validate_gold.sql` returns 14 row-count rows and zero duplicate groups.
- [ ] The physical names retain `dim_` and `fact_`; friendly views are intentionally out of scope.
- [ ] Fabric lineage shows the Silver source endpoint feeding the dbt job and the dbt job writing the Gold Warehouse.

## Documentation references

- Microsoft Learn — Common dbt job patterns in Fabric: https://learn.microsoft.com/en-us/fabric/data-factory/common-dbt-job-patterns
- Microsoft Learn — Configure a dbt job: https://learn.microsoft.com/en-us/fabric/data-factory/dbt-job-configure
- dbt Developer Hub — Fabric configurations: https://docs.getdbt.com/reference/resource-configs/fabric-configs
