import pyodbc
import pandas as pd
import os

# local folder name to save tables
base_folder = "./tables"

# local db info
server = '123.0.0.1'
database = 'your_db_name'
username = 'your_username'
password = 'your_pass'
driver = '{ODBC Driver 18 for SQL Server}'

# remote db info
server_remote = 'your-remote-db.database.windows.net'
database_remote = 'your-remote-db'
username_remote = 'your-remote-db-username'
password_remote = 'your-remote-db-pass'
driver_remote = '{ODBC Driver 18 for SQL Server}'
port_remote = 1433

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

with pyodbc.connect('DRIVER=' + driver + ';SERVER=tcp:' + server + ';PORT=' + str(
        port) + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password + ";TrustServerCertificate=YES") as conn:
    for table in tables_to_import:
        with conn.cursor() as cursor:
            print(f"--- PROCESSING --- {table}")
            # rows = cursor.execute(f"SELECT TOP 10 * FROM {table}").fetchall()
            df = pd.read_sql(f"SELECT * FROM {table}", conn)

            try:
                df.to_parquet(os.path.join(base_folder, f"{table}.parquet"))
            except Exception as e:
                print(e)
            print("done")
