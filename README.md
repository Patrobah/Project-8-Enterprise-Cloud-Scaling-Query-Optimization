# ☁️ Project 8: Enterprise Scaling & Data Query Optimization
## Cloud Data Warehouse Implementation & Analytical Pipeline

An end-to-end cloud data engineering and analytical optimization pipeline that ports local transactional data streams into an enterprise-grade cloud architecture. This project sets up an authenticated bridge between a local **Python ETL engine** and a serverless **Cloud Data Warehouse (Google BigQuery)**, deploying optimized relational tables and compiling high-efficiency cloud SQL statements.

---

## 🏗️ Cloud System Architecture
The application layout bypasses local memory limitations by hosting processing loads inside Google Cloud Platform (GCP) using a decoupled dimensional blueprint schema:
* **`SaaS_Enterprise_Scaling` Dataset:** The isolated project storage pool managed inside the US multi-region data center.
* **`fact_transactions` Table:** High-precision data warehouse fact table optimized via 128-bit `NUMERIC` data columns and structured `TIMESTAMP` entries.
* **`dim_currency_schema` Table:** Dimensional reference metadata table mapping currency conversion coefficients directly inside the cloud environment.

---

## 🛠️ Data Engineering & Ingestion Walkthrough

### 1. Relational Schema Setup (`schema_blueprint.sql`)
The cloud warehouse infrastructure is built utilizing a structural Data Definition Language (DDL) file. It implements relational column parameters, database documentation overrides (`OPTIONS`), and strict data type constraints to safeguard database structure:

```sql
CREATE TABLE IF NOT EXISTS `SaaS_Enterprise_Scaling.fact_transactions` (
    Transaction_ID STRING NOT NULL,
    Timestamp TIMESTAMP NOT NULL,
    Customer_ID STRING NOT NULL,
    Plan_Type STRING NOT NULL,
    Original_Amount NUMERIC,
    Original_Currency STRING,
    Normalized_Amount_USD NUMERIC,
    Pipeline_Audit_Status STRING
);
```

### 2. Sandbox-Safe Batch ETL Pipeline (`cloud_pipeline.py`)
To handle cloud data integration without incurring operational overhead or triggering sandbox firewall rules, the pipeline implements several programmatic strategies:
- **Service Account Authentication:** Leverages secure JSON private connection key mapping to negotiate server access parameters safely.
- **Bypassing Ingestion Redirection:** Switches execution logic from streaming queries (`insert_rows_json`) over to free **Batch Load Jobs** using `load_table_from_dataframe` to upload data frame records without requiring a billing profile.
- **Precision Balancing:** Converts standard 64-bit float numbers into high-precision `decimal.Decimal` objects to prevent 128-bit cloud byte mismatch failures (`Got bytestring of length 8, expected 16`).

---

## 📊 Live Cloud Data Warehouse Metrics
The analytical view script (`business_insights.sql`) handles business intelligence calculations directly inside the BigQuery cloud engine, outputting verified financial benchmarks to the console:

### 1. Subscription Segment Distribution Matrix

| Subscription Plan Type | Total Active Contracts | Gross Generated Revenue (USD) | Average Revenue Per Account (ARPU) |
| :--- | :---: | :---: | :---: |
| **Enterprise_Annual** | 635 | \$537,848.16 | \$847.00 |
| **Pro_Monthly** | 693 | \$47,636.56 | \$68.74 |
| **Basic_Monthly** | 672 | \$13,932.22 | \$20.73 |

### 2. High-Stakes Financial Run-Rates
- **Total Monthly Recurring Revenue (MRR):** **`$106,389.46`**
- **Projected Annual Recurring Revenue (ARR):** **`$1,276,673.56`**

*Calculated via dynamic common table expressions (CTEs) that accurately scale long-term enterprise packages down to their monthly equivalent fractions (`Raw_Revenue / 12`).*

---

## 💻 Technical Stack Profile
- **Cloud Infrastructure Platform:** Google Cloud Platform (GCP)
- **Core Cloud Environment:** Google BigQuery (Serverless Data Warehouse)
- **Data Engineering Languages:** Python 3.x, Structured Query Language (SQL / T-SQL Dialect)
- **Primary Libraries:** Pandas, PyArrow, Db-Dtypes, Google Cloud Client Core
