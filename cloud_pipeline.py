import os
import random
import pandas as pd
from decimal import Decimal
from google.cloud import bigquery
from google.api_core.exceptions import Conflict
from datetime import datetime, timedelta


def run_cloud_infrastructure_pipeline():
    # 1. Establish Secure Pathways
    base_dir = os.path.dirname(os.path.abspath(__file__))
    credential_path = os.path.join(base_dir, 'config', 'cloud_credentials.json')
    sql_script_path = os.path.join(base_dir, 'sql_queries', 'schema_blueprint.sql')

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    client = bigquery.Client()
    print(f"🔄 Authenticated with GCP Project: {client.project}")

    # 2. Verify/Construct the Dataset Container
    dataset_id = f"{client.project}.SaaS_Enterprise_Scaling"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = "US"

    try:
        client.create_dataset(dataset, timeout=30)
        print(f"✅ Cloud Dataset pool created successfully!")
    except Conflict:
        print(f"ℹ️ Cloud Dataset pool already exists. Proceeding to table verification...")

    # 3. Read and Execute the DDL Schema Script
    if not os.path.exists(sql_script_path):
        print("❌ Error: Missing schema_blueprint.sql file!")
        return

    with open(sql_script_path, 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()

    try:
        query_job = client.query(sql_script)
        query_job.result()
        print("🎉 Relational database architecture verified live on the cloud.")
    except Exception as e:
        print(f"❌ Structural Deployment Failure: {e}")
        return

    # 4. Use Free Batch Load Jobs for Metadata
    print("📡 Ingesting reference metadata into 'dim_currency_schema' via Batch Job...")
    currency_table_id = f"{dataset_id}.dim_currency_schema"

    # Convert numerical values to high-precision Decimal to prevent byte length mismatches
    currency_rows = [
        {"Currency_Code": "USD", "Exchange_Rate_To_USD": Decimal('1.0'), "Regional_Tax_Rate": Decimal('0.00')},
        {"Currency_Code": "EUR", "Exchange_Rate_To_USD": Decimal('1.08'), "Regional_Tax_Rate": Decimal('0.19')},
        {"Currency_Code": "KES", "Exchange_Rate_To_USD": Decimal('0.0078'), "Regional_Tax_Rate": Decimal('0.16')}
    ]

    table = client.get_table(currency_table_id)
    if table.num_rows == 0:
        df_currency = pd.DataFrame(currency_rows)
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        load_job = client.load_table_from_dataframe(df_currency, currency_table_id, job_config=job_config)
        load_job.result()
        print("✅ Currency configuration dimensions loaded securely into the cloud!")
    else:
        print("ℹ️ Currency configuration metadata already present in the cloud. Skipping duplicate loading.")

    # 5. GENERATE AND STREAM TRANSACTION DATA (Fact Table Ingestion)
    print("🚀 Algorithmically simulating 500 enterprise transactional data records...")
    transaction_table_id = f"{dataset_id}.fact_transactions"

    currencies = ['USD', 'EUR', 'KES']
    rates = {'USD': 1.0, 'EUR': 1.08, 'KES': 0.0078}
    plans = ['Basic_Monthly', 'Pro_Monthly', 'Enterprise_Annual']

    transaction_rows = []
    start_date = datetime(2026, 1, 1)

    for i in range(2001, 2501):
        tx_id = f"TXN-{i}"
        date_val = start_date + timedelta(days=random.randint(0, 280), hours=random.randint(0, 23))
        cust_id = f"CUST-{random.randint(5000, 9999)}"
        plan = random.choice(plans)
        currency = random.choice(currencies)

        if 'Basic' in plan:
            amount = 29.0
        elif 'Pro' in plan:
            amount = 99.0
        else:
            amount = 1200.0

        rate = rates[currency]
        normalized_usd = amount * rate

        # FIX: Cast numerical fields explicitly to high-precision Decimal objects
        transaction_rows.append({
            "Transaction_ID": tx_id,
            "Timestamp": pd.to_datetime(date_val.strftime('%Y-%m-%d %H:%M:%S')),
            "Customer_ID": cust_id,
            "Plan_Type": plan,
            "Original_Amount": Decimal(str(amount)),
            "Original_Currency": currency,
            "Normalized_Amount_USD": Decimal(str(round(normalized_usd, 4))),
            "Pipeline_Audit_Status": "Processed: Verified Cloud Batch Load"
        })

    print(f"⚡ Executing free Batch Load job directly into Cloud Fact Table...")
    df_transactions = pd.DataFrame(transaction_rows)

    # Configure job to append new transactions seamlessly
    tx_job_config = bigquery.LoadJobConfig(write_disposition="WRITE_APPEND")

    try:
        tx_load_job = client.load_table_from_dataframe(df_transactions, transaction_table_id, job_config=tx_job_config)
        tx_load_job.result()
        print(f"🎉 Success! 500 transactional matrix rows loaded safely into BigQuery.")
        print(f"👉 Your data is fully scaled and optimized inside 'fact_transactions'!")
    except Exception as ex:
        print(f"❌ Transaction Batch Loading Failure: {ex}")


def run_cloud_analytical_queries():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(base_dir, 'config', 'cloud_credentials.json')
    client = bigquery.Client()

    sql_path = os.path.join(base_dir, 'sql_queries', 'business_insights.sql')
    print(f"\n📊 Reading high-performance enterprise analysis code from: {sql_path}")

    with open(sql_path, 'r', encoding='utf-8') as file:
        queries = file.read().split(';')  # Separate the two distinct query statements

    for idx, query in enumerate(queries):
        if query.strip() == "":
            continue
        print(f"\n⚡ Compiling Cloud Query {idx + 1} inside BigQuery engine...")
        try:
            query_job = client.query(query)
            results = query_job.to_dataframe()  # Retrieve data natively as a pandas table
            print(results.to_string(index=False))
        except Exception as e:
            print(f"❌ Query execution failed: {e}")


if __name__ == '__main__':
    run_cloud_infrastructure_pipeline()
    run_cloud_analytical_queries()
