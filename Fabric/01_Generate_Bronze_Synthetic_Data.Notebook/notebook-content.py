# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "9a14dc1e-95e5-4453-be3e-86fbdc26ac9a",
# META       "default_lakehouse_name": "Pearson_Bronze_LH",
# META       "default_lakehouse_workspace_id": "fa8de806-3675-4a4b-84e4-50290ac5ea80",
# META       "known_lakehouses": [
# META         {
# META           "id": "9a14dc1e-95e5-4453-be3e-86fbdc26ac9a"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # 🥉 Bronze Layer | Raw Data Landing
# 
# ### Pearson Conversational Analytics PoC
# 
# The **Bronze layer** represents how operational and analytical data arrives in Microsoft Fabric from multiple enterprise source patterns.
# 
# ---
# 
# ### 📥 Source Patterns
# 
# | Source Pattern | Demo Representation | Example Data |
# |---|---|---|
# | 🔄 **Data Factory / ETL** | `etl_*` | Registrations, attempts, responses, finance, exam events, staffing |
# | 🔗 **OneLake Shortcuts** | `shortcutted_*` | Customers, candidates, programs, assessments, topics, test centers |
# | 🧱 **Databricks / Unity Catalog** | `mirrored_*` | Exam capacity |
# 
# > **PoC note:** Source-system patterns are simulated through table naming in this demo. The focus is demonstrating how Fabric can bring multiple data domains together in OneLake.
# 
# ---
# 
# ### What happens in Bronze?
# 
# **Source Systems → Raw Landing → Preserve Source Structure**
# 
# - Data remains close to its source representation  
# - Source lineage and ingestion pattern are retained  
# - Minimal business transformation is applied  
# - Raw operational history is preserved  
# - Data is prepared for downstream refinement  
# 
# ---
# 
# ### Data Domains
# 
# **Assessment & Learning**
# - Candidates  
# - Programs  
# - Assessments  
# - Topics  
# - Items  
# - Attempts & responses  
# 
# **Exam Operations**
# - Registrations  
# - Exam scheduling  
# - Rescheduled exams  
# - Test centers  
# - Capacity planning  
# - Proctor staffing  
# 
# **Financial**
# - Payments  
# - Refunds  
# 
# ---
# 
# ### ➡️ Next Layer
# 
# **Bronze → Silver**
# 
# The Silver layer will standardize, validate, deduplicate, and enrich these datasets into consistent business entities.


# CELL ********************

# ============================================================
# Pearson Conversational Analytics PoC
# Notebook: 01_Generate_Bronze_Synthetic_Data
#
# Default Lakehouse:
# Pearson_Bronze_LH
#
# Bronze source-pattern conventions:
#   etl_*          = simulated Fabric Data Factory ingestion
#   shortcutted_*  = simulated OneLake shortcut source
#   mirrored_*     = simulated Databricks Unity Catalog mirror
#
# All organizations, candidates, exams, transactions,
# staffing records, and financial records are synthetic.
# ============================================================

from pyspark.sql import Row
from pyspark.sql import functions as F
from datetime import date, timedelta
import random
import uuid

# ============================================================
# 0. CONFIGURATION
# ============================================================

SEED = 42
random.seed(SEED)

START_DATE = date(2025, 1, 1)
END_DATE = date(2026, 10, 31)

NUM_CANDIDATES_PER_CUSTOMER = 500
REGISTRATIONS_PER_CUSTOMER = 1600
QUESTIONS_PER_ATTEMPT = 30
ITEMS_PER_TOPIC = 10

# ============================================================
# 1. GENERAL UTILITIES
# ============================================================

def uid():
    return str(uuid.uuid4())


def random_date(start_date, end_date):
    number_of_days = (end_date - start_date).days

    return start_date + timedelta(
        days=random.randint(0, number_of_days)
    )


def clamp(value, low, high):
    return max(low, min(high, value))


def write_table(df, table_name):

    (
        df.write
        .format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )

    row_count = df.count()

    print(
        f"Created {table_name:<35} "
        f"{row_count:>12,} rows"
    )


# ============================================================
# 2. REFERENCE DATA
# ============================================================

CUSTOMERS = [
    {
        "customer_id": "C001",
        "customer_name": "Northstar Learning",
        "segment": "Enterprise",
        "country": "United States"
    },
    {
        "customer_id": "C002",
        "customer_name": "Apex Certification",
        "segment": "Enterprise",
        "country": "United States"
    },
    {
        "customer_id": "C003",
        "customer_name": "Contoso Professional Testing",
        "segment": "Enterprise",
        "country": "United States"
    }
]

PROGRAMS = [
    {
        "program_code": "P01",
        "program_name": "Cloud Architecture Certification",
        "category": "Technology"
    },
    {
        "program_code": "P02",
        "program_name": "Data Engineering Professional",
        "category": "Data"
    },
    {
        "program_code": "P03",
        "program_name": "Security Operations Professional",
        "category": "Security"
    }
]

ASSESSMENT_LEVELS = [
    {
        "assessment_code": "A01",
        "level": "Associate",
        "passing_score": 70,
        "duration_minutes": 60,
        "price": 150.00
    },
    {
        "assessment_code": "A02",
        "level": "Professional",
        "passing_score": 72,
        "duration_minutes": 75,
        "price": 200.00
    },
    {
        "assessment_code": "A03",
        "level": "Expert",
        "passing_score": 75,
        "duration_minutes": 90,
        "price": 250.00
    }
]

TOPICS = [
    {
        "topic_id": "T01",
        "topic_name": "Architecture",
        "description": "Architecture and solution design"
    },
    {
        "topic_id": "T02",
        "topic_name": "Security",
        "description": "Security controls and identity"
    },
    {
        "topic_id": "T03",
        "topic_name": "Data Engineering",
        "description": "Pipelines and data processing"
    },
    {
        "topic_id": "T04",
        "topic_name": "Analytics",
        "description": "Reporting and analytical concepts"
    },
    {
        "topic_id": "T05",
        "topic_name": "Governance",
        "description": "Governance and compliance"
    },
    {
        "topic_id": "T06",
        "topic_name": "Operations",
        "description": "Monitoring and operations"
    }
]

TEST_CENTERS = [
    {
        "test_center_code": "TC-SEATTLE-01",
        "test_center_name": "Seattle Test Center",
        "city": "Seattle",
        "state": "Washington",
        "region": "West",
        "base_capacity": 120
    },
    {
        "test_center_code": "TC-CHICAGO-01",
        "test_center_name": "Chicago Test Center",
        "city": "Chicago",
        "state": "Illinois",
        "region": "Central",
        "base_capacity": 150
    },
    {
        "test_center_code": "TC-NEWYORK-01",
        "test_center_name": "New York Test Center",
        "city": "New York",
        "state": "New York",
        "region": "East",
        "base_capacity": 180
    },
    {
        "test_center_code": "TC-DALLAS-01",
        "test_center_name": "Dallas Test Center",
        "city": "Dallas",
        "state": "Texas",
        "region": "Central",
        "base_capacity": 140
    }
]

# ============================================================
# 3. SIMULATED SHORTCUT TABLE: CUSTOMER
# ============================================================

customer_rows = []

for customer in CUSTOMERS:

    customer_rows.append(
        Row(
            customer_id=customer["customer_id"],
            customer_name=customer["customer_name"],
            customer_segment=customer["segment"],
            country=customer["country"],
            customer_status="Active",
            source_system="Customer Master",
            source_pattern="Simulated OneLake Shortcut"
        )
    )

df_customer = spark.createDataFrame(customer_rows)

write_table(
    df_customer,
    "shortcutted_customer"
)

# ============================================================
# 4. SIMULATED SHORTCUT TABLE: PROGRAM
# ============================================================

program_rows = []

for customer in CUSTOMERS:

    for program in PROGRAMS:

        program_rows.append(
            Row(
                program_id=(
                    f'{customer["customer_id"]}-'
                    f'{program["program_code"]}'
                ),
                customer_id=customer["customer_id"],
                program_code=program["program_code"],
                program_name=program["program_name"],
                program_category=program["category"],
                program_status="Active",
                source_system="Program Master",
                source_pattern="Simulated OneLake Shortcut"
            )
        )

df_program = spark.createDataFrame(program_rows)

write_table(
    df_program,
    "shortcutted_program"
)

# ============================================================
# 5. SIMULATED SHORTCUT TABLE: ASSESSMENT
# ============================================================

assessment_rows = []

for customer in CUSTOMERS:

    for program in PROGRAMS:

        program_id = (
            f'{customer["customer_id"]}-'
            f'{program["program_code"]}'
        )

        for assessment in ASSESSMENT_LEVELS:

            assessment_rows.append(
                Row(
                    assessment_id=(
                        f'{program_id}-'
                        f'{assessment["assessment_code"]}'
                    ),
                    customer_id=customer["customer_id"],
                    program_id=program_id,
                    assessment_code=assessment["assessment_code"],
                    assessment_name=(
                        f'{program["program_name"]} - '
                        f'{assessment["level"]}'
                    ),
                    assessment_level=assessment["level"],
                    passing_score=assessment["passing_score"],
                    standard_duration_minutes=assessment[
                        "duration_minutes"
                    ],
                    standard_price=float(
                        assessment["price"]
                    ),
                    assessment_status="Active",
                    source_system="Assessment Master",
                    source_pattern="Simulated OneLake Shortcut"
                )
            )

df_assessment = spark.createDataFrame(assessment_rows)

write_table(
    df_assessment,
    "shortcutted_assessment"
)

# ============================================================
# 6. SIMULATED SHORTCUT TABLE: TOPIC
# ============================================================

topic_rows = []

for topic in TOPICS:

    topic_rows.append(
        Row(
            topic_id=topic["topic_id"],
            topic_name=topic["topic_name"],
            topic_description=topic["description"],
            topic_status="Active",
            source_system="Item Bank",
            source_pattern="Simulated OneLake Shortcut"
        )
    )

df_topic = spark.createDataFrame(topic_rows)

write_table(
    df_topic,
    "shortcutted_topic"
)

# ============================================================
# 7. SIMULATED SHORTCUT TABLE: ITEM
# ============================================================

item_rows = []

for topic in TOPICS:

    for item_number in range(
        1,
        ITEMS_PER_TOPIC + 1
    ):

        item_rows.append(
            Row(
                item_id=(
                    f'{topic["topic_id"]}-'
                    f'Q{item_number:03}'
                ),
                topic_id=topic["topic_id"],
                item_name=(
                    f'{topic["topic_name"]} '
                    f'Question {item_number}'
                ),
                difficulty=random.choice(
                    [
                        "Easy",
                        "Medium",
                        "Medium",
                        "Medium",
                        "Hard"
                    ]
                ),
                maximum_points=1,
                item_status="Active",
                source_system="Item Bank",
                source_pattern="Simulated OneLake Shortcut"
            )
        )

df_item = spark.createDataFrame(item_rows)

write_table(
    df_item,
    "shortcutted_item"
)

# ============================================================
# 8. SIMULATED SHORTCUT TABLE: CANDIDATE
# ============================================================

candidate_rows = []

regions = [
    ("NA", "North America"),
    ("EMEA", "Europe / Middle East / Africa"),
    ("APAC", "Asia Pacific")
]

for customer in CUSTOMERS:

    for candidate_number in range(
        1,
        NUM_CANDIDATES_PER_CUSTOMER + 1
    ):

        region_code, region_name = random.choice(
            regions
        )

        candidate_rows.append(
            Row(
                candidate_id=(
                    f'{customer["customer_id"]}-'
                    f'CAN-{candidate_number:05}'
                ),
                customer_id=customer["customer_id"],
                candidate_display_name=(
                    f'Demo Candidate '
                    f'{candidate_number:05}'
                ),
                region_code=region_code,
                region_name=region_name,
                candidate_status="Active",
                source_system="Candidate Master",
                source_pattern="Simulated OneLake Shortcut"
            )
        )

df_candidate = spark.createDataFrame(
    candidate_rows
)

write_table(
    df_candidate,
    "shortcutted_candidate"
)

# ============================================================
# 9. SIMULATED SHORTCUT TABLE: TEST CENTER
# ============================================================

test_center_rows = []

for center in TEST_CENTERS:

    test_center_rows.append(
        Row(
            test_center_code=center[
                "test_center_code"
            ],
            test_center_name=center[
                "test_center_name"
            ],
            city=center["city"],
            state=center["state"],
            region=center["region"],
            base_daily_capacity=center[
                "base_capacity"
            ],
            test_center_status="Active",
            source_system="Test Center Master",
            source_pattern="Simulated OneLake Shortcut"
        )
    )

df_test_center = spark.createDataFrame(
    test_center_rows
)

write_table(
    df_test_center,
    "shortcutted_test_center"
)

# ============================================================
# 10. SIMULATED SHORTCUT TABLE: DATE
# ============================================================

date_rows = []

current_date = START_DATE

while current_date <= END_DATE:

    date_rows.append(
        Row(
            date_key=int(
                current_date.strftime("%Y%m%d")
            ),
            calendar_date=current_date,
            year=current_date.year,
            quarter=(
                f'Q'
                f'{((current_date.month - 1) // 3) + 1}'
            ),
            month_number=current_date.month,
            month_name=current_date.strftime("%B"),
            year_month=current_date.strftime("%Y-%m"),
            week_number=int(
                current_date.strftime("%W")
            ),
            day_of_month=current_date.day,
            day_name=current_date.strftime("%A"),
            is_weekend=(
                current_date.weekday() >= 5
            ),
            source_system="Enterprise Calendar",
            source_pattern="Simulated OneLake Shortcut"
        )
    )

    current_date += timedelta(days=1)

df_date = spark.createDataFrame(date_rows)

write_table(
    df_date,
    "shortcutted_date"
)

# ============================================================
# 11. SIMULATED SHORTCUT TABLE: SECURITY ENTITLEMENT
# ============================================================

security_rows = [
    Row(
        user_principal_name=(
            "northstar.demo@pearsonpoc.local"
        ),
        customer_id="C001",
        access_role="Customer Analyst",
        active=True,
        source_system="Identity Entitlement",
        source_pattern="Simulated OneLake Shortcut"
    ),
    Row(
        user_principal_name=(
            "apex.demo@pearsonpoc.local"
        ),
        customer_id="C002",
        access_role="Customer Analyst",
        active=True,
        source_system="Identity Entitlement",
        source_pattern="Simulated OneLake Shortcut"
    ),
    Row(
        user_principal_name=(
            "contoso.demo@pearsonpoc.local"
        ),
        customer_id="C003",
        access_role="Customer Analyst",
        active=True,
        source_system="Identity Entitlement",
        source_pattern="Simulated OneLake Shortcut"
    ),
    Row(
        user_principal_name=(
            "executive.demo@pearsonpoc.local"
        ),
        customer_id="ALL",
        access_role="Executive",
        active=True,
        source_system="Identity Entitlement",
        source_pattern="Simulated OneLake Shortcut"
    )
]

df_security = spark.createDataFrame(
    security_rows
)

write_table(
    df_security,
    "shortcutted_security_entitlement"
)

# ============================================================
# 12. SIMULATED MIRRORED TABLE: EXAM CAPACITY
#
# Represents operational capacity data mastered in
# Azure Databricks Unity Catalog.
# Physically created locally for this PoC.
# ============================================================

capacity_rows = []
capacity_number = 1

capacity_start_date = date(2025, 1, 1)
capacity_end_date = END_DATE

current_date = capacity_start_date

while current_date <= capacity_end_date:

    for center in TEST_CENTERS:

        exam_level = random.choice(
            ASSESSMENT_LEVELS
        )

        available_seats = max(
            60,
            center["base_capacity"]
            + random.choice(
                [-20, -10, 0, 0, 0, 10, 20]
            )
        )

        demand_factor = random.uniform(
            0.58,
            1.02
        )

        # Higher demand Tuesday through Thursday.
        if current_date.weekday() in [1, 2, 3]:

            demand_factor += random.uniform(
                0.02,
                0.08
            )

        reserved_seats = min(
            available_seats,
            int(
                available_seats
                * demand_factor
            )
        )

        delivery_rate = random.uniform(
            0.90,
            0.98
        )

        delivered_exams = int(
            reserved_seats * delivery_rate
        )

        cancelled_exams = max(
            0,
            reserved_seats - delivered_exams
        )

        utilization_target = (
            0.80
            if exam_level["level"] == "Associate"
            else 0.85
        )

        capacity_rows.append(
            Row(
                capacity_id=(
                    f"CAP{capacity_number:07}"
                ),
                test_center_code=center[
                    "test_center_code"
                ],
                test_center_name=center[
                    "test_center_name"
                ],
                capacity_date=current_date,
                exam_type=exam_level["level"],
                available_seats=available_seats,
                reserved_seats=reserved_seats,
                delivered_exams=delivered_exams,
                cancelled_exams=cancelled_exams,
                utilization_target=float(
                    utilization_target
                ),
                source_system=(
                    "Azure Databricks Unity Catalog"
                ),
                source_pattern=(
                    "Simulated Databricks Mirror"
                )
            )
        )

        capacity_number += 1

    current_date += timedelta(days=1)

df_capacity = spark.createDataFrame(
    capacity_rows
)

write_table(
    df_capacity,
    "mirrored_exam_capacity"
)

# ============================================================
# 13. ETL TABLE: REGISTRATION
# ============================================================

registration_rows = []

registrations_by_customer = {}

for customer in CUSTOMERS:

    customer_registrations = []

    for registration_number in range(
        1,
        REGISTRATIONS_PER_CUSTOMER + 1
    ):

        candidate_number = random.randint(
            1,
            NUM_CANDIDATES_PER_CUSTOMER
        )

        candidate_id = (
            f'{customer["customer_id"]}-'
            f'CAN-{candidate_number:05}'
        )

        program = random.choice(PROGRAMS)
        assessment = random.choice(
            ASSESSMENT_LEVELS
        )
        center = random.choice(TEST_CENTERS)

        program_id = (
            f'{customer["customer_id"]}-'
            f'{program["program_code"]}'
        )

        assessment_id = (
            f'{program_id}-'
            f'{assessment["assessment_code"]}'
        )

        registration_date = random_date(
            START_DATE,
            END_DATE - timedelta(days=45)
        )

        scheduled_date = (
            registration_date
            + timedelta(
                days=random.randint(3, 35)
            )
        )

        if scheduled_date > END_DATE:
            scheduled_date = END_DATE

        registration_status = random.choices(
            [
                "Scheduled",
                "Completed",
                "Cancelled",
                "No Show"
            ],
            weights=[
                8,
                83,
                5,
                4
            ],
            k=1
        )[0]

        registration = Row(
            registration_id=uid(),
            customer_id=customer["customer_id"],
            candidate_id=candidate_id,
            program_id=program_id,
            assessment_id=assessment_id,
            test_center_code=center[
                "test_center_code"
            ],
            registration_date=registration_date,
            scheduled_exam_date=scheduled_date,
            registration_status=registration_status,
            delivery_mode=random.choice(
                [
                    "Test Center",
                    "Online Proctored"
                ]
            ),
            source_system="Assessment Scheduling",
            source_pattern=(
                "Simulated Fabric Data Factory"
            ),
            ingestion_timestamp=(
                registration_date
                + timedelta(days=1)
            )
        )

        registration_rows.append(
            registration
        )

        customer_registrations.append(
            registration
        )

    registrations_by_customer[
        customer["customer_id"]
    ] = customer_registrations

df_registration = spark.createDataFrame(
    registration_rows
)

write_table(
    df_registration,
    "etl_registration"
)

# ============================================================
# 14. ETL TABLE: EXAM EVENTS
#
# Creates lifecycle history:
# Scheduled, Rescheduled, Delivered, Cancelled, No Show
# ============================================================

exam_event_rows = []

final_exam_dates = {}

for registration in registration_rows:

    original_date = (
        registration.scheduled_exam_date
    )

    final_date = original_date

    # Initial scheduling event.
    exam_event_rows.append(
        Row(
            exam_event_id=uid(),
            registration_id=(
                registration.registration_id
            ),
            customer_id=registration.customer_id,
            candidate_id=registration.candidate_id,
            assessment_id=(
                registration.assessment_id
            ),
            test_center_code=(
                registration.test_center_code
            ),
            event_date=original_date,
            event_type="Scheduled",
            original_exam_date=original_date,
            new_exam_date=original_date,
            reschedule_reason=None,
            source_system="Exam Operations",
            source_pattern=(
                "Simulated Fabric Data Factory"
            )
        )
    )

    # Approximately 12% are rescheduled.
    if random.random() < 0.12:

        new_date = original_date + timedelta(
            days=random.randint(1, 14)
        )

        if new_date > END_DATE:
            new_date = END_DATE

        reason = random.choice(
            [
                "Candidate request",
                "Test center capacity",
                "Proctor unavailable",
                "Operational disruption",
                "Severe weather"
            ]
        )

        exam_event_rows.append(
            Row(
                exam_event_id=uid(),
                registration_id=(
                    registration.registration_id
                ),
                customer_id=(
                    registration.customer_id
                ),
                candidate_id=(
                    registration.candidate_id
                ),
                assessment_id=(
                    registration.assessment_id
                ),
                test_center_code=(
                    registration.test_center_code
                ),
                event_date=original_date,
                event_type="Rescheduled",
                original_exam_date=original_date,
                new_exam_date=new_date,
                reschedule_reason=reason,
                source_system="Exam Operations",
                source_pattern=(
                    "Simulated Fabric Data Factory"
                )
            )
        )

        final_date = new_date

    final_exam_dates[
        registration.registration_id
    ] = final_date

    terminal_event_type = {
        "Completed": "Delivered",
        "Cancelled": "Cancelled",
        "No Show": "No Show",
        "Scheduled": "Scheduled"
    }[registration.registration_status]

    if terminal_event_type != "Scheduled":

        exam_event_rows.append(
            Row(
                exam_event_id=uid(),
                registration_id=(
                    registration.registration_id
                ),
                customer_id=(
                    registration.customer_id
                ),
                candidate_id=(
                    registration.candidate_id
                ),
                assessment_id=(
                    registration.assessment_id
                ),
                test_center_code=(
                    registration.test_center_code
                ),
                event_date=final_date,
                event_type=terminal_event_type,
                original_exam_date=original_date,
                new_exam_date=final_date,
                reschedule_reason=None,
                source_system="Exam Operations",
                source_pattern=(
                    "Simulated Fabric Data Factory"
                )
            )
        )

df_exam_event = spark.createDataFrame(
    exam_event_rows
)

write_table(
    df_exam_event,
    "etl_exam_event"
)

# ============================================================
# 15. ETL TABLE: ATTEMPT
# ============================================================

customer_score_baseline = {
    "C001": 78,
    "C002": 74,
    "C003": 71
}

difficulty_penalty = {
    "A01": 0,
    "A02": 3,
    "A03": 7
}

attempt_rows = []

for registration in registration_rows:

    if registration.registration_status != "Completed":
        continue

    assessment_code = (
        registration.assessment_id[-3:]
    )

    assessment_definition = next(
        item
        for item in ASSESSMENT_LEVELS
        if item["assessment_code"]
        == assessment_code
    )

    baseline = (
        customer_score_baseline[
            registration.customer_id
        ]
        - difficulty_penalty[
            assessment_code
        ]
    )

    score = int(
        clamp(
            round(
                random.gauss(
                    baseline,
                    11
                )
            ),
            20,
            100
        )
    )

    passing_score = assessment_definition[
        "passing_score"
    ]

    attempt_date = final_exam_dates[
        registration.registration_id
    ]

    attempt_rows.append(
        Row(
            attempt_id=uid(),
            registration_id=(
                registration.registration_id
            ),
            customer_id=registration.customer_id,
            candidate_id=(
                registration.candidate_id
            ),
            program_id=registration.program_id,
            assessment_id=(
                registration.assessment_id
            ),
            test_center_code=(
                registration.test_center_code
            ),
            attempt_date=attempt_date,
            attempt_number=1,
            score=score,
            passing_score=passing_score,
            passed=score >= passing_score,
            attempt_status="Completed",
            duration_minutes=random.randint(
                35,
                assessment_definition[
                    "duration_minutes"
                ]
            ),
            source_system="Assessment Delivery",
            source_pattern=(
                "Simulated Fabric Data Factory"
            )
        )
    )

df_attempt = spark.createDataFrame(
    attempt_rows
)

write_table(
    df_attempt,
    "etl_attempt"
)

# ============================================================
# 16. ETL TABLE: RESPONSE
# ============================================================

topic_adjustments = {
    "C001": {
        "T01": 0.12,
        "T02": -0.12,
        "T03": 0.02,
        "T04": 0.04,
        "T05": -0.02,
        "T06": 0.00
    },
    "C002": {
        "T01": 0.00,
        "T02": 0.12,
        "T03": 0.02,
        "T04": 0.00,
        "T05": -0.14,
        "T06": -0.02
    },
    "C003": {
        "T01": -0.03,
        "T02": 0.00,
        "T03": 0.12,
        "T04": 0.03,
        "T05": 0.00,
        "T06": -0.14
    }
}

items_by_topic = {}

for topic in TOPICS:

    items_by_topic[
        topic["topic_id"]
    ] = [
        (
            f'{topic["topic_id"]}-'
            f'Q{item_number:03}'
        )
        for item_number in range(
            1,
            ITEMS_PER_TOPIC + 1
        )
    ]

response_rows = []

topic_ids = [
    topic["topic_id"]
    for topic in TOPICS
]

for attempt in attempt_rows:

    base_probability = (
        attempt.score / 100.0
    )

    selected_topics = random.choices(
        topic_ids,
        k=QUESTIONS_PER_ATTEMPT
    )

    for sequence, topic_id in enumerate(
        selected_topics,
        start=1
    ):

        item_id = random.choice(
            items_by_topic[topic_id]
        )

        probability_correct = clamp(
            base_probability
            + topic_adjustments[
                attempt.customer_id
            ][topic_id],
            0.15,
            0.97
        )

        is_correct = (
            random.random()
            <= probability_correct
        )

        response_rows.append(
            Row(
                response_id=uid(),
                attempt_id=attempt.attempt_id,
                customer_id=attempt.customer_id,
                candidate_id=attempt.candidate_id,
                assessment_id=(
                    attempt.assessment_id
                ),
                topic_id=topic_id,
                item_id=item_id,
                attempt_date=attempt.attempt_date,
                question_sequence=sequence,
                is_correct=is_correct,
                points_available=1,
                points_earned=(
                    1 if is_correct else 0
                ),
                response_seconds=random.randint(
                    20,
                    180
                ),
                source_system=(
                    "Assessment Delivery"
                ),
                source_pattern=(
                    "Simulated Fabric Data Factory"
                )
            )
        )

df_response = spark.createDataFrame(
    response_rows
)

write_table(
    df_response,
    "etl_response"
)

# ============================================================
# 17. ETL TABLE: FINANCE
# ============================================================

assessment_price = {
    "A01": 150.00,
    "A02": 200.00,
    "A03": 250.00
}

finance_rows = []

for registration in registration_rows:

    assessment_code = (
        registration.assessment_id[-3:]
    )

    price = assessment_price[
        assessment_code
    ]

    finance_rows.append(
        Row(
            transaction_id=uid(),
            customer_id=registration.customer_id,
            candidate_id=(
                registration.candidate_id
            ),
            registration_id=(
                registration.registration_id
            ),
            assessment_id=(
                registration.assessment_id
            ),
            transaction_date=(
                registration.registration_date
            ),
            transaction_type="Payment",
            amount=float(price),
            currency="USD",
            payment_status="Settled",
            source_system="Finance",
            source_pattern=(
                "Simulated Fabric Data Factory"
            )
        )
    )

    refund_probability = 0.04

    # Intentional Apex refund anomaly.
    if (
        registration.customer_id == "C002"
        and registration.registration_date.year
        == 2026
        and registration.registration_date.month
        in [4, 5]
    ):
        refund_probability = 0.14

    if random.random() <= refund_probability:

        refund_date = min(
            registration.registration_date
            + timedelta(
                days=random.randint(1, 30)
            ),
            END_DATE
        )

        finance_rows.append(
            Row(
                transaction_id=uid(),
                customer_id=(
                    registration.customer_id
                ),
                candidate_id=(
                    registration.candidate_id
                ),
                registration_id=(
                    registration.registration_id
                ),
                assessment_id=(
                    registration.assessment_id
                ),
                transaction_date=refund_date,
                transaction_type="Refund",
                amount=float(-price),
                currency="USD",
                payment_status="Settled",
                source_system="Finance",
                source_pattern=(
                    "Simulated Fabric Data Factory"
                )
            )
        )

df_finance = spark.createDataFrame(
    finance_rows
)

write_table(
    df_finance,
    "etl_finance"
)

# ============================================================
# 18. ETL TABLE: PROCTOR SHIFT
# ============================================================

proctor_rows = []

current_date = START_DATE

while current_date <= END_DATE:

    for center in TEST_CENTERS:

        proctors_scheduled = random.randint(
            5,
            13
        )

        proctors_absent = random.choices(
            [0, 1, 2, 3],
            weights=[64, 22, 10, 4],
            k=1
        )[0]

        proctors_available = max(
            0,
            proctors_scheduled - proctors_absent
        )

        proctors_required = random.randint(
            5,
            11
        )

        proctor_rows.append(
            Row(
                staffing_id=uid(),
                test_center_code=center[
                    "test_center_code"
                ],
                staffing_date=current_date,
                shift_name=random.choice(
                    [
                        "Morning",
                        "Afternoon"
                    ]
                ),
                proctors_scheduled=(
                    proctors_scheduled
                ),
                proctors_absent=proctors_absent,
                proctors_available=(
                    proctors_available
                ),
                proctors_required=(
                    proctors_required
                ),
                staffing_gap=max(
                    0,
                    proctors_required
                    - proctors_available
                ),
                source_system=(
                    "Workforce Scheduling"
                ),
                source_pattern=(
                    "Simulated Fabric Data Factory"
                )
            )
        )

    current_date += timedelta(days=1)

df_proctor = spark.createDataFrame(
    proctor_rows
)

write_table(
    df_proctor,
    "etl_proctor_shift"
)

# ============================================================
# 19. ETL TABLE: TEST CENTER CAPACITY PLAN
# ============================================================

capacity_plan_rows = []

current_date = START_DATE

while current_date <= END_DATE:

    for center in TEST_CENTERS:

        physical_capacity = max(
            60,
            center["base_capacity"]
            + random.choice(
                [-20, -10, 0, 0, 10, 20]
            )
        )

        planned_demand = int(
            physical_capacity
            * random.uniform(
                0.60,
                1.12
            )
        )

        capacity_plan_rows.append(
            Row(
                planning_id=uid(),
                test_center_code=center[
                    "test_center_code"
                ],
                planning_date=current_date,
                physical_capacity=(
                    physical_capacity
                ),
                planned_demand=planned_demand,
                planned_utilization=round(
                    planned_demand
                    / physical_capacity,
                    4
                ),
                capacity_gap=max(
                    0,
                    planned_demand
                    - physical_capacity
                ),
                planning_status=(
                    "Over Capacity"
                    if planned_demand
                    > physical_capacity
                    else "Within Capacity"
                ),
                source_system=(
                    "Capacity Planning"
                ),
                source_pattern=(
                    "Simulated Fabric Data Factory"
                )
            )
        )

    current_date += timedelta(days=1)

df_capacity_plan = spark.createDataFrame(
    capacity_plan_rows
)

write_table(
    df_capacity_plan,
    "etl_test_center_capacity"
)

# ============================================================
# 20. BRONZE TABLE VALIDATION
# ============================================================

expected_tables = [
    "shortcutted_customer",
    "shortcutted_program",
    "shortcutted_assessment",
    "shortcutted_topic",
    "shortcutted_item",
    "shortcutted_candidate",
    "shortcutted_test_center",
    "shortcutted_date",
    "shortcutted_security_entitlement",
    "mirrored_exam_capacity",
    "etl_registration",
    "etl_exam_event",
    "etl_attempt",
    "etl_response",
    "etl_finance",
    "etl_proctor_shift",
    "etl_test_center_capacity"
]

print("")
print("=" * 80)
print("PEARSON BRONZE DATA GENERATION COMPLETE")
print("=" * 80)

print("")
print("TABLE COUNTS")
print("-" * 80)

for table_name in expected_tables:

    count = spark.table(
        table_name
    ).count()

    print(
        f"{table_name:<40} "
        f"{count:>15,}"
    )

# ============================================================
# 21. VALIDATE ATTEMPT PERFORMANCE
# ============================================================

print("")
print("CUSTOMER ASSESSMENT PERFORMANCE")
print("-" * 80)

(
    df_attempt
    .groupBy("customer_id")
    .agg(
        F.count("*").alias(
            "completed_tests"
        ),
        F.round(
            F.avg("score"),
            2
        ).alias(
            "average_score"
        ),
        F.round(
            F.avg(
                F.col("passed").cast("double")
            ) * 100,
            2
        ).alias(
            "pass_rate_pct"
        )
    )
    .orderBy("customer_id")
    .show(truncate=False)
)

# ============================================================
# 22. VALIDATE EXAM EVENTS
# ============================================================

print("")
print("EXAM EVENT SUMMARY")
print("-" * 80)

(
    df_exam_event
    .groupBy("event_type")
    .count()
    .orderBy(F.desc("count"))
    .show(truncate=False)
)

# ============================================================
# 23. VALIDATE RESCHEDULING REASONS
# ============================================================

print("")
print("RESCHEDULE REASONS")
print("-" * 80)

(
    df_exam_event
    .filter(
        F.col("event_type")
        == "Rescheduled"
    )
    .groupBy(
        "reschedule_reason"
    )
    .count()
    .orderBy(
        F.desc("count")
    )
    .show(truncate=False)
)

# ============================================================
# 24. VALIDATE CAPACITY AND STAFFING
# ============================================================

print("")
print("CAPACITY AND STAFFING BY TEST CENTER")
print("-" * 80)

capacity_summary = (
    df_capacity
    .groupBy("test_center_code")
    .agg(
        F.sum(
            "available_seats"
        ).alias(
            "available_seats"
        ),
        F.sum(
            "delivered_exams"
        ).alias(
            "delivered_exams"
        ),
        F.round(
            F.sum("delivered_exams")
            / F.sum("available_seats"),
            4
        ).alias(
            "delivered_utilization"
        )
    )
)

staffing_summary = (
    df_proctor
    .groupBy("test_center_code")
    .agg(
        F.sum(
            "staffing_gap"
        ).alias(
            "total_staffing_gap"
        ),
        F.sum(
            F.when(
                F.col("staffing_gap") > 0,
                1
            ).otherwise(0)
        ).alias(
            "staffing_gap_days"
        )
    )
)

(
    capacity_summary
    .join(
        staffing_summary,
        on="test_center_code",
        how="left"
    )
    .orderBy(
        F.desc(
            "delivered_utilization"
        )
    )
    .show(truncate=False)
)

# ============================================================
# 25. COMPLETION MESSAGE
# ============================================================

print("")
print("=" * 80)
print("SUCCESS")
print("=" * 80)

print(
    """
Bronze synthetic data is ready in Pearson_Bronze_LH.

Source-pattern groups:

Simulated shortcuts
-------------------
shortcutted_customer
shortcutted_program
shortcutted_assessment
shortcutted_topic
shortcutted_item
shortcutted_candidate
shortcutted_test_center
shortcutted_date
shortcutted_security_entitlement

Simulated Databricks mirroring
------------------------------
mirrored_exam_capacity

Simulated Fabric Data Factory ingestion
----------------------------------------
etl_registration
etl_exam_event
etl_attempt
etl_response
etl_finance
etl_proctor_shift
etl_test_center_capacity
"""
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
