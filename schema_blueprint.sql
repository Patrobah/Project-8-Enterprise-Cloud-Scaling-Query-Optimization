-- ====================================================================
-- PROJECT 8: ENTERPRISE CLOUD SCALING BLUEPRINT SCHEMA
-- TARGET WAREHOUSE: GOOGLE BIGQUERY (SQL SERVER DIALECT COMPATIBLE)
-- ====================================================================

-- NOTE: BigQuery manages schemas using standard relational DDL.
-- Run this script to spin up your cloud tables.

-- 1. Create the Core Project Dataset Storage Pool
-- (Execute this manually via your upload engine pipeline)

-- 2. Build the Core Relational Subscription Fact Table
CREATE TABLE IF NOT EXISTS `SaaS_Enterprise_Scaling.fact_transactions` (
    Transaction_ID STRING NOT NULL OPTIONS(description="Primary business operational key for transactions"),
    Timestamp TIMESTAMP NOT NULL OPTIONS(description="Standardized date-time processing marker"),
    Customer_ID STRING NOT NULL OPTIONS(description="Foreign key identifier linking profiles"),
    Plan_Type STRING NOT NULL OPTIONS(description="The subscription structure tier tier"),
    Original_Amount NUMERIC OPTIONS(description="The unformatted invoice amount value"),
    Original_Currency STRING OPTIONS(description="The source currency tracking token (USD, EUR, KES)"),
    Normalized_Amount_USD NUMERIC OPTIONS(description="Unified base financial index normalized via pipeline FX lookups"),
    Pipeline_Audit_Status STRING OPTIONS(description="Data engineering validation trail logs")
)
OPTIONS(
    description="Main enterprise transactional ledger table optimized for analytical cloud tracking metrics"
);

-- 3. Build the Dimensional Reference Metadata Configuration Table
CREATE TABLE IF NOT EXISTS `SaaS_Enterprise_Scaling.dim_currency_schema` (
    Currency_Code STRING NOT NULL OPTIONS(description="Unique system tracking primary key"),
    Exchange_Rate_To_USD NUMERIC NOT NULL OPTIONS(description="Fixed conversion multiplier constant"),
    Regional_Tax_Rate NUMERIC OPTIONS(description="Dynamic spatial tax bracket indices")
);


