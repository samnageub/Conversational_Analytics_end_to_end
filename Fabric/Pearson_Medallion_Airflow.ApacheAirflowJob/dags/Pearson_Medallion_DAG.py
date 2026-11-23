from airflow import DAG
from airflow.providers.microsoft.fabric.operators.run_item import MSFabricRunJobOperator
from airflow_powerbi_plugin.operators.powerbi import PowerBIDatasetRefreshOperator

with DAG(
    dag_id="Pearson_Medallion_DAG",
    catchup=False,
) as dag:

    generate_bronze = MSFabricRunJobOperator(
        task_id="Pearson_Generate_Bronze_Data",
        fabric_conn_id="fabric_pearson",
        workspace_id="fa8de806-3675-4a4b-84e4-50290ac5ea80",
        item_id="3eba442a-b8d9-4df5-b008-bed3291c52ae",
        job_type="RunNotebook",
        timeout=600,
        wait_for_termination=True,
        deferrable=False,
    )

    bronze_to_silver = MSFabricRunJobOperator(
        task_id="Pearson_Bronze_To_Silver",
        fabric_conn_id="fabric_pearson",
        workspace_id="fa8de806-3675-4a4b-84e4-50290ac5ea80",
        item_id="26e24541-594e-431d-a63f-ae80f81c3c02",
        job_type="RunNotebook",
        timeout=600,
        wait_for_termination=True,
        deferrable=False,
    )

    clear_gold_stage = MSFabricRunJobOperator(
        task_id="Pearson_Clear_Gold_Stage",
        fabric_conn_id="fabric_pearson",
        workspace_id="fa8de806-3675-4a4b-84e4-50290ac5ea80",
        item_id="66f26ce4-77e1-4394-8e93-cc9f168c17d3",
        job_type="RunNotebook",
        timeout=600,
        wait_for_termination=True,
        deferrable=False,
    )

    silver_to_gold_stage = MSFabricRunJobOperator(
        task_id="Pearson_Silver_To_Gold_Stage",
        fabric_conn_id="fabric_pearson",
        workspace_id="fa8de806-3675-4a4b-84e4-50290ac5ea80",
        item_id="77c09aac-cb20-4b45-a245-360d9032015e",
        job_type="RunCopyJob",
        timeout=1200,
        wait_for_termination=True,
        deferrable=False,
    )

    build_gold_model = MSFabricRunJobOperator(
        task_id="Pearson_Build_Gold_Model",
        fabric_conn_id="fabric_pearson",
        workspace_id="fa8de806-3675-4a4b-84e4-50290ac5ea80",
        item_id="4de8d4b4-9382-40fc-9ea6-4967b716d6b4",
        job_type="DBTItems",
        timeout=1800,
        wait_for_termination=True,
        deferrable=False,
    )

    build_business_views = MSFabricRunJobOperator(
        task_id="Pearson_Build_Business_Views",
        fabric_conn_id="fabric_pearson",
        workspace_id="fa8de806-3675-4a4b-84e4-50290ac5ea80",
        item_id="a0f54ca4-0dae-4a07-b9c6-d68263a0f49a",
        job_type="DBTItems",
        timeout=1800,
        wait_for_termination=True,
        deferrable=False,
    )

    refresh_assessment_semantic_model = PowerBIDatasetRefreshOperator(
        powerbi_conn_id="generic_powerbi_default",
        task_id="Pearson_Refresh_Assessment_Analytics_SM",
        dataset_id="100f5a47-da2c-4474-9cf2-01f2296f8c90",
        group_id="fa8de806-3675-4a4b-84e4-50290ac5ea80",
    )

    generate_bronze >> bronze_to_silver >> clear_gold_stage >> silver_to_gold_stage >> build_gold_model >> build_business_views >> refresh_assessment_semantic_model
