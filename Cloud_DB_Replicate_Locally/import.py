import pyodbc
import pandas as pd
import numpy as np
import os

# local folder name to save tables
base_folder = "./tables"

# local db info
server = '123.0.0.1'
database = 'your_db_name'
username = 'your_username'
password = 'your_pass'
driver = '{ODBC Driver 18 for SQL Server}'

# name of the tables you need to replicate locally
tables_to_import = [
    'all_purpose_cluster_configuration_timeline',
    'all_purpose_cost',
    'cluster_events',
    'cluster_timeline_segments',
    'clusters_idleness',
    'clusters_idleness_cost',
    'consumption_scheduler_metadata',
    'consumption_scheduler_metadata_format',
    'cost_alerts_config',
    'cost_per_subscription_month',
    'cost_per_workspace_job_month',
    'cost_per_workspace_month',
    'databricks_account_users',
    'databricks_service_configuration',
    'databricks_tokens',
    'databricks_workspaces',
    'databricks_workspaces_username_mapping',
    'dbu_rates',
    'email_service_account',
    'fiscal_year_config',
    'job_run_analysis',
    'job_run_cluster_analysis',
    'job_run_task_cost',
    'notebook_analysis',
    'pipeline_analysis',
    'pipeline_cost',
    'pool_cost',
    'sql_warehouse_analysis',
    'sql_warehouse_cost',
    'sql_warehouse_dbu_rates',
    'standard_dbu_prices',
    'standard_vm_prices',
    'workspace_cost',
]

batch_size = 100

batch_size = 100  # Set your batch size here


# Function to clean the data
def clean_data(val):
    if str(val) in ["nan", "NaT"]:
        return None
    return val


def run2():
    with pyodbc.connect(
            f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};'
            f'UID={username};PWD={password};TrustServerCertificate=YES;') as conn:

        for table in tables_to_import:
            print(f"--- PROCESSING --- {table}")
            df = pd.read_parquet(os.path.join(base_folder, f"{table}.parquet"))

            all_cols_names = [col for col in df.columns if "Unnamed" not in col]
            all_cols = ",".join(all_cols_names)
            all_vparams = ",".join(["?" for _ in all_cols_names])


            insert_stmt = f"INSERT INTO {table} ({all_cols}) VALUES ({all_vparams})"

            with conn.cursor() as cursor:
                try:
                    cursor.execute(f"truncate table {table}")
                except Exception as e:
                    print(e)
            conn.commit()

            for start_row in range(0, df.shape[0], batch_size):
                end_row = min(start_row + batch_size, df.shape[0])
                chunk = df.iloc[start_row:end_row]
                data_to_insert = [tuple(clean_data(row[col_name]) for col_name in all_cols_names) for index, row in
                                  chunk.iterrows()]

                with conn.cursor() as cursor:
                    try:
                        cursor.executemany(insert_stmt, data_to_insert)
                    except Exception as e:
                        print(e)
                conn.commit()


run2()
