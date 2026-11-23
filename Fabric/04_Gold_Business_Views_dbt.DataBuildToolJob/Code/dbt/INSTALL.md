# Install standalone Job 04 project

This is a complete, standalone dbt project for Fabric dbt Job `04_Gold_Business_Views_dbt`. Do not merge it into Job 03. Job 03 remains unchanged and continues to build/test the 14 physical tables in `Pearson_Gold_DW.dbo`.

## Fabric dbt Job configuration

Open `04_Gold_Business_Views_dbt` and set **dbt configurations** to:

- Adapter: `DataWarehouse`
- Connection: `Pearson_Gold_DW`
- Target schema: `dbo`

The connection identity needs read access to `dbo` and permission to create/replace views in schema `business`. dbt creates the schema when the configured identity has the required Warehouse/workspace permissions.

## Put these files in the Job 04 project

Copy the package contents with this exact structure:

```text
dbt_project.yml
macros/
  generate_schema_name.sql
models/
  sources.yml
  business/
    Customer.sql
    Candidate.sql
    Program.sql
    Assessment.sql
    Topic.sql
    Item.sql
    TestCenter.sql
    Calendar.sql
    Registrations.sql
    AssessmentPerformance.sql
    TopicPerformance.sql
    FinancialPerformance.sql
    ExamOperations.sql
    CapacityAndStaffing.sql
    schema.yml
```

`validation/validate_business_views.sql` is an operator validation script; it can remain outside the dbt Job and be run in the `Pearson_Gold_DW` SQL editor after the build.

## Source and schema behavior

- `models/sources.yml` defines source `gold` with `schema: dbo` and no database qualifier. Because Job 04 is connected to `Pearson_Gold_DW`, dbt resolves these sources in the current Warehouse.
- Every model calls `source('gold', '<physical_table>')`; Job 04 has no dependency on Job 03's dbt manifest or local model files.
- The Job target schema remains `dbo`, but each model is configured with custom schema `business`.
- dbt normally combines those names as `dbo_business`. `macros/generate_schema_name.sql` changes only the custom schema named `business` to resolve exactly as `business`. Source resolution is unaffected because source `gold` explicitly declares `schema: dbo`.
- Explicit aliases preserve the exact requested case and relation names.

## Run command

After Job 03 succeeds, run Job 04 with:

```bash
dbt build
```

Equivalent selector command:

```bash
dbt build --select tag:business
```

`dbt build` creates/replaces all 14 business views and runs their tests in the same Job 04 execution.

## Required Airflow order

```text
Bronze notebook
  -> Silver notebook
  -> staging Copy Job override
  -> 03_Silver_To_Gold_dbt
  -> 04_Gold_Business_Views_dbt
  -> semantic model refresh
```

Configure Airflow so Job 04 runs only after Job 03 succeeds, and the semantic-model refresh runs only after Job 04 succeeds.

## Validation

Run `validation/validate_business_views.sql` in `Pearson_Gold_DW`. It lists the expected 14 views in schema `business` and returns five sample rows from each.
