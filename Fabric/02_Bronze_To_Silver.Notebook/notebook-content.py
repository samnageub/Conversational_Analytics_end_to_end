# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "973f350a-735d-4651-a81b-88807d8bc6a9",
# META       "default_lakehouse_name": "Pearson_Silver_LH",
# META       "default_lakehouse_workspace_id": "fa8de806-3675-4a4b-84e4-50290ac5ea80",
# META       "known_lakehouses": [
# META         {
# META           "id": "973f350a-735d-4651-a81b-88807d8bc6a9"
# META         },
# META         {
# META           "id": "9a14dc1e-95e5-4453-be3e-86fbdc26ac9a"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 🥈 Silver Layer | Clean, Standardize & Enrich
# 
# ### Pearson Conversational Analytics PoC
# 
# The **Silver layer** transforms raw multi-source Bronze data into trusted, standardized business entities that can be consistently consumed across analytics and AI experiences.
# 
# ---
# 
# ### 🔄 Transformation Flow
# 
# **🥉 Bronze Raw Data**  
# ↓  
# **Clean + Standardize + Validate + Deduplicate + Enrich**  
# ↓  
# **🥈 Trusted Silver Business Entities**
# 
# ---
# 
# ### 🧹 Data Quality & Standardization
# 
# This notebook:
# 
# - Removes source-specific prefixes such as `etl_`, `shortcutted_`, and `mirrored_`
# - Standardizes data types and status values
# - Normalizes identity and text attributes
# - Removes duplicate business records
# - Validates relationships between assessment entities
# - Removes ingestion-specific metadata that isn't needed downstream
# 
# ---
# 
# ### 🔗 Business Integration & Enrichment
# 
# Raw datasets are combined to create richer operational context.
# 
# #### Exam Journey
# 
# **Registration + Exam Events**
# 
# Creates a consolidated exam journey including:
# 
# - Original exam date
# - Final exam date
# - Rescheduled indicator
# - Number of reschedules
# - Days shifted
# - Delivered / cancelled / no-show status
# 
# #### Test Center Operations
# 
# **Exam Capacity + Capacity Planning + Proctor Staffing**
# 
# Creates a daily operational view covering:
# 
# - Available seats
# - Reserved seats
# - Delivered exams
# - Utilization
# - Planned demand
# - Proctors required
# - Proctors available
# - Staffing gaps
# - Operational pressure
# 
# ---
# 
# ### ✅ Data Quality Validation
# 
# The notebook validates key relationships such as:
# 
# **Customer → Registration → Attempt → Response**
# 
# **Program → Assessment → Attempt**
# 
# **Topic → Item → Response**
# 
# **Test Center → Capacity → Staffing → Exam Operations**
# 
# Records with unexpected relationship gaps are surfaced during notebook validation.
# 
# ---
# 
# ### 🎯 Silver Outcome
# 
# The Silver layer provides **trusted business entities**, including:
# 
# `customer` • `candidate` • `program` • `assessment` • `topic` • `item`  
# 
# `registration` • `attempt` • `response` • `finance`  
# 
# `exam_journey` • `reschedule_event`  
# 
# `exam_capacity` • `proctor_staffing` • `capacity_plan`  
# 
# `daily_test_center_operations`
# 
# ---
# 
# ### ➡️ Next Layer
# 
# **Silver → Gold**
# 
# The Gold Warehouse will organize these trusted entities into analytics-ready business models optimized for:
# 
# 📊 **Power BI**  
# 🤖 **Copilot & Data Agents**  
# 🧠 **Fabric IQ / Ontology**  
# 🔎 **Conversational Analytics**


# CELL ********************

# ============================================================
# Pearson Conversational Analytics PoC
# Notebook: 02_Bronze_To_Silver
#
# READS:
#   Pearson_Bronze_LH
#
# WRITES:
#   Pearson_Silver_LH  <-- default Lakehouse
#
# Purpose:
# Clean, standardize, deduplicate and enrich Bronze data.
# ============================================================

from pyspark.sql import functions as F
from pyspark.sql.window import Window

# ============================================================
# 0. CONFIGURATION
# ============================================================

# ============================================================
# BRONZE SOURCE ACCESS
#
# Read Bronze Delta tables directly through OneLake paths.
# This keeps Pearson_Silver_LH as the default/output Lakehouse.
# ============================================================

# ============================================================
# BRONZE SOURCE ACCESS
#
# Dynamically resolve the correct OneLake path instead of
# hardcoding workspace or Lakehouse identifiers.
# ============================================================

BRONZE_LAKEHOUSE = "Pearson_Bronze_LH"

bronze_info = notebookutils.lakehouse.getWithProperties(
    name=BRONZE_LAKEHOUSE
)

bronze_base_path = (
    bronze_info["properties"]["abfsPath"]
)

print(
    "Bronze Lakehouse path:",
    bronze_base_path
)


def bronze(table_name):
    """Read from Bronze lakehouse Tables path.

    The Bronze lakehouse is schema-enabled, so Delta tables live under
    `Tables/dbo/<table_name>`. The previous path without `dbo/` caused
    PATH_NOT_FOUND errors.
    """
    table_path = f"{bronze_base_path}/Tables/dbo/{table_name}"

    return (
        spark.read
        .format("delta")
        .load(table_path)
    )


def write_silver(df, table_name):
    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )

    print(
        f"Created Silver table: "
        f"{table_name:<30} "
        f"{df.count():>12,} rows"
    )

# ============================================================
# 1. CUSTOMER
# ============================================================

customer = (
    bronze("shortcutted_customer")
    .select(
        "customer_id",
        "customer_name",
        F.col("customer_segment").alias("segment"),
        "country",
        F.col("customer_status").alias("status")
    )
    .dropDuplicates(["customer_id"])
)

write_silver(customer, "customer")

# ============================================================
# 2. PROGRAM
# ============================================================

program = (
    bronze("shortcutted_program")
    .select(
        "program_id",
        "customer_id",
        "program_code",
        "program_name",
        F.col("program_category").alias("category"),
        F.col("program_status").alias("status")
    )
    .dropDuplicates(["program_id"])
)

write_silver(program, "program")

# ============================================================
# 3. ASSESSMENT
# ============================================================

assessment = (
    bronze("shortcutted_assessment")
    .select(
        "assessment_id",
        "customer_id",
        "program_id",
        "assessment_code",
        "assessment_name",
        "assessment_level",
        F.col("passing_score").cast("int"),
        F.col("standard_duration_minutes").cast("int"),
        F.col("standard_price").cast("double"),
        F.col("assessment_status").alias("status")
    )
    .dropDuplicates(["assessment_id"])
)

write_silver(assessment, "assessment")

# ============================================================
# 4. TOPIC
# ============================================================

topic = (
    bronze("shortcutted_topic")
    .select(
        "topic_id",
        "topic_name",
        "topic_description",
        F.col("topic_status").alias("status")
    )
    .dropDuplicates(["topic_id"])
)

write_silver(topic, "topic")

# ============================================================
# 5. ITEM
# ============================================================

item = (
    bronze("shortcutted_item")
    .select(
        "item_id",
        "topic_id",
        "item_name",
        "difficulty",
        F.col("maximum_points").cast("int"),
        F.col("item_status").alias("status")
    )
    .dropDuplicates(["item_id"])
)

write_silver(item, "item")

# ============================================================
# 6. CANDIDATE
# ============================================================

candidate = (
    bronze("shortcutted_candidate")
    .select(
        "candidate_id",
        "customer_id",
        "candidate_display_name",
        "region_code",
        "region_name",
        F.col("candidate_status").alias("status")
    )
    .dropDuplicates(["candidate_id"])
)

write_silver(candidate, "candidate")

# ============================================================
# 7. TEST CENTER
# ============================================================

test_center = (
    bronze("shortcutted_test_center")
    .select(
        "test_center_code",
        "test_center_name",
        "city",
        "state",
        "region",
        F.col("base_daily_capacity").cast("int"),
        F.col("test_center_status").alias("status")
    )
    .dropDuplicates(["test_center_code"])
)

write_silver(test_center, "test_center")

# ============================================================
# 8. DATE
# ============================================================

calendar = (
    bronze("shortcutted_date")
    .select(
        "date_key",
        "calendar_date",
        "year",
        "quarter",
        "month_number",
        "month_name",
        "year_month",
        "week_number",
        "day_of_month",
        "day_name",
        "is_weekend"
    )
    .dropDuplicates(["calendar_date"])
)

write_silver(calendar, "calendar")

# ============================================================
# 9. SECURITY ENTITLEMENT
# ============================================================

security_entitlement = (
    bronze("shortcutted_security_entitlement")
    .select(
        F.lower(
            F.trim("user_principal_name")
        ).alias("user_principal_name"),
        "customer_id",
        "access_role",
        "active"
    )
    .dropDuplicates(
        ["user_principal_name", "customer_id"]
    )
)

write_silver(
    security_entitlement,
    "security_entitlement"
)

# ============================================================
# 10. EXAM CAPACITY
#
# Simulated mirrored Databricks source becomes a regular
# Silver business entity.
# ============================================================

exam_capacity = (
    bronze("mirrored_exam_capacity")
    .select(
        "capacity_id",
        "test_center_code",
        "capacity_date",
        "exam_type",
        F.col("available_seats").cast("int"),
        F.col("reserved_seats").cast("int"),
        F.col("delivered_exams").cast("int"),
        F.col("cancelled_exams").cast("int"),
        F.col("utilization_target").cast("double")
    )
    .withColumn(
        "reservation_rate",
        F.when(
            F.col("available_seats") > 0,
            F.round(
                F.col("reserved_seats")
                / F.col("available_seats"),
                4
            )
        )
    )
    .withColumn(
        "delivery_utilization",
        F.when(
            F.col("available_seats") > 0,
            F.round(
                F.col("delivered_exams")
                / F.col("available_seats"),
                4
            )
        )
    )
    .withColumn(
        "unused_seats",
        F.col("available_seats")
        - F.col("delivered_exams")
    )
    .dropDuplicates(["capacity_id"])
)

write_silver(exam_capacity, "exam_capacity")

# ============================================================
# 11. REGISTRATION
# ============================================================

registration = (
    bronze("etl_registration")
    .select(
        "registration_id",
        "customer_id",
        "candidate_id",
        "program_id",
        "assessment_id",
        "test_center_code",
        "registration_date",
        F.col("scheduled_exam_date")
            .alias("original_exam_date"),
        F.initcap(
            F.trim("registration_status")
        ).alias("registration_status"),
        "delivery_mode"
    )
    .dropDuplicates(["registration_id"])
)

write_silver(registration, "registration")

# ============================================================
# 12. EXAM EVENT
# ============================================================

exam_event = (
    bronze("etl_exam_event")
    .select(
        "exam_event_id",
        "registration_id",
        "customer_id",
        "candidate_id",
        "assessment_id",
        "test_center_code",
        "event_date",
        F.initcap(
            F.trim("event_type")
        ).alias("event_type"),
        "original_exam_date",
        "new_exam_date",
        "reschedule_reason"
    )
    .dropDuplicates(["exam_event_id"])
)

write_silver(exam_event, "exam_event")

# ============================================================
# 13. CREATE EXAM JOURNEY
#
# One row per registration with final exam date and
# rescheduling attributes.
# ============================================================

exam_journey = (
    exam_event
    .groupBy("registration_id")
    .agg(
        F.min("original_exam_date")
            .alias("original_exam_date"),

        F.max("new_exam_date")
            .alias("final_exam_date"),

        F.sum(
            F.when(
                F.col("event_type") == "Rescheduled",
                1
            ).otherwise(0)
        ).alias("reschedule_count"),

        F.max(
            F.when(
                F.col("event_type") == "Delivered",
                1
            ).otherwise(0)
        ).alias("was_delivered"),

        F.max(
            F.when(
                F.col("event_type") == "Cancelled",
                1
            ).otherwise(0)
        ).alias("was_cancelled"),

        F.max(
            F.when(
                F.col("event_type") == "No Show",
                1
            ).otherwise(0)
        ).alias("was_no_show")
    )
    .withColumn(
        "was_rescheduled",
        F.col("reschedule_count") > 0
    )
    .withColumn(
        "days_shifted",
        F.datediff(
            F.col("final_exam_date"),
            F.col("original_exam_date")
        )
    )
)

write_silver(exam_journey, "exam_journey")

# ============================================================
# 14. ENRICH REGISTRATION WITH EXAM JOURNEY
# ============================================================

registration_enriched = (
    registration.alias("r")
    .join(
        exam_journey.alias("j"),
        on="registration_id",
        how="left"
    )
    .select(
        "registration_id",
        "r.customer_id",
        "r.candidate_id",
        "r.program_id",
        "r.assessment_id",
        "r.test_center_code",
        "r.registration_date",
        "r.original_exam_date",
        "j.final_exam_date",
        "r.registration_status",
        "r.delivery_mode",
        F.coalesce(
            F.col("j.was_rescheduled"),
            F.lit(False)
        ).alias("was_rescheduled"),
        F.coalesce(
            F.col("j.reschedule_count"),
            F.lit(0)
        ).alias("reschedule_count"),
        F.coalesce(
            F.col("j.days_shifted"),
            F.lit(0)
        ).alias("days_shifted")
    )
)

write_silver(
    registration_enriched,
    "registration_enriched"
)

# ============================================================
# 15. ATTEMPT
# ============================================================

attempt = (
    bronze("etl_attempt")
    .select(
        "attempt_id",
        "registration_id",
        "customer_id",
        "candidate_id",
        "program_id",
        "assessment_id",
        "test_center_code",
        "attempt_date",
        F.col("attempt_number").cast("int"),
        F.col("score").cast("int"),
        F.col("passing_score").cast("int"),
        F.col("passed").cast("boolean"),
        "attempt_status",
        F.col("duration_minutes").cast("int")
    )
    .dropDuplicates(["attempt_id"])
)

write_silver(attempt, "attempt")

# ============================================================
# 16. RESPONSE
# ============================================================

response = (
    bronze("etl_response")
    .select(
        "response_id",
        "attempt_id",
        "customer_id",
        "candidate_id",
        "assessment_id",
        "topic_id",
        "item_id",
        "attempt_date",
        F.col("question_sequence").cast("int"),
        F.col("is_correct").cast("boolean"),
        F.col("points_available").cast("int"),
        F.col("points_earned").cast("int"),
        F.col("response_seconds").cast("int")
    )
    .dropDuplicates(["response_id"])
)

write_silver(response, "response")

# ============================================================
# 17. FINANCE
# ============================================================

finance = (
    bronze("etl_finance")
    .select(
        "transaction_id",
        "customer_id",
        "candidate_id",
        "registration_id",
        "assessment_id",
        "transaction_date",
        F.initcap(
            F.trim("transaction_type")
        ).alias("transaction_type"),
        F.col("amount").cast("double"),
        F.upper("currency").alias("currency"),
        "payment_status"
    )
    .dropDuplicates(["transaction_id"])
)

write_silver(finance, "finance")

# ============================================================
# 18. PROCTOR STAFFING
# ============================================================

proctor_staffing = (
    bronze("etl_proctor_shift")
    .select(
        "staffing_id",
        "test_center_code",
        F.col("staffing_date").alias("staffing_date"),
        "shift_name",
        F.col("proctors_scheduled").cast("int"),
        F.col("proctors_absent").cast("int"),
        F.col("proctors_available").cast("int"),
        F.col("proctors_required").cast("int"),
        F.col("staffing_gap").cast("int")
    )
    .withColumn(
        "is_understaffed",
        F.col("staffing_gap") > 0
    )
    .withColumn(
        "staffing_coverage_rate",
        F.when(
            F.col("proctors_required") > 0,
            F.round(
                F.col("proctors_available")
                / F.col("proctors_required"),
                4
            )
        )
    )
    .dropDuplicates(["staffing_id"])
)

write_silver(
    proctor_staffing,
    "proctor_staffing"
)

# ============================================================
# 19. CAPACITY PLAN
# ============================================================

capacity_plan = (
    bronze("etl_test_center_capacity")
    .select(
        "planning_id",
        "test_center_code",
        "planning_date",
        F.col("physical_capacity").cast("int"),
        F.col("planned_demand").cast("int"),
        F.col("planned_utilization").cast("double"),
        F.col("capacity_gap").cast("int"),
        "planning_status"
    )
    .withColumn(
        "is_over_capacity",
        F.col("planned_demand")
        > F.col("physical_capacity")
    )
    .dropDuplicates(["planning_id"])
)

write_silver(
    capacity_plan,
    "capacity_plan"
)

# ============================================================
# 20. DAILY TEST CENTER OPERATIONS
#
# Integrates:
# - capacity
# - staffing
# - delivered exams
# - demand
#
# This will become a powerful Gold analytics fact.
# ============================================================




# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

# Read the three existing Silver tables
exam_capacity = spark.table("exam_capacity")
proctor_staffing = spark.table("proctor_staffing")
capacity_plan = spark.table("capacity_plan")


# ============================================================
# Daily capacity
# ============================================================

daily_capacity = (
    exam_capacity
    .groupBy(
        "test_center_code",
        F.col("capacity_date").alias("operation_date")
    )
    .agg(
        F.sum("available_seats").alias("available_seats"),
        F.sum("reserved_seats").alias("reserved_seats"),
        F.sum("delivered_exams").alias("delivered_exams"),
        F.sum("cancelled_exams").alias("cancelled_exams")
    )
)


# ============================================================
# Daily staffing
# ============================================================

daily_staffing = (
    proctor_staffing
    .groupBy(
        "test_center_code",
        F.col("staffing_date").alias("operation_date")
    )
    .agg(
        F.sum("proctors_scheduled").alias("proctors_scheduled"),
        F.sum("proctors_available").alias("proctors_available"),
        F.sum("proctors_required").alias("proctors_required"),
        F.sum("staffing_gap").alias("staffing_gap")
    )
)


# ============================================================
# Daily capacity plan
# ============================================================

daily_plan = (
    capacity_plan
    .groupBy(
        "test_center_code",
        F.col("planning_date").alias("operation_date")
    )
    .agg(
        F.max("physical_capacity").alias("physical_capacity"),
        F.max("planned_demand").alias("planned_demand"),
        F.max("capacity_gap").alias("planned_capacity_gap")
    )
)


# ============================================================
# Integrated daily operations
# ============================================================

daily_test_center_operations = (
    daily_capacity
    .join(
        daily_staffing,
        ["test_center_code", "operation_date"],
        "left"
    )
    .join(
        daily_plan,
        ["test_center_code", "operation_date"],
        "left"
    )
    .withColumn(
        "actual_utilization_rate",
        F.when(
            F.col("available_seats") > 0,
            F.round(
                F.col("delivered_exams")
                / F.col("available_seats"),
                4
            )
        )
    )
    .withColumn(
        "staffing_coverage_rate",
        F.when(
            F.col("proctors_required") > 0,
            F.round(
                F.col("proctors_available")
                / F.col("proctors_required"),
                4
            )
        )
    )
    .withColumn(
        "operational_pressure",
        F.when(
            (F.col("actual_utilization_rate") >= 0.90)
            & (F.col("staffing_gap") > 0),
            "High"
        )
        .when(
            (F.col("actual_utilization_rate") >= 0.80)
            | (F.col("staffing_gap") > 0),
            "Medium"
        )
        .otherwise("Normal")
    )
)


# ============================================================
# Persist into Pearson_Silver_LH
# ============================================================

(
    daily_test_center_operations.write
    .format("delta")
    .mode("overwrite")
    .option("overwriteSchema", "true")
    .saveAsTable("daily_test_center_operations")
)


# ============================================================
# Validate
# ============================================================

print(
    "daily_test_center_operations rows:",
    spark.table("daily_test_center_operations").count()
)

spark.table("daily_test_center_operations") \
    .show(20, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
