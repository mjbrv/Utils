import pyodbc
import pandas as pd
import numpy as np
import os

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
    'clusters_idleness'
]

def create_tables():
    conn_local =  pyodbc.connect(
        f'DRIVER={driver};SERVER=tcp:{server};PORT=1433;DATABASE={database};'
        f'UID={username};PWD={password};TrustServerCertificate=YES;')
    cursor_local = conn_local.cursor()

    conn_remote = pyodbc.connect(
        f'DRIVER={driver_remote};SERVER=tcp:{server_remote};PORT=1433;DATABASE={database_remote};'
        f'UID={username_remote};PWD={password_remote};TrustServerCertificate=YES;')
    cursor_remote = conn_remote.cursor()

    for remote_table in tables_to_import:
        cursor_remote.execute(f"SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{remote_table}'")
        columns = cursor_remote.fetchall()

        # Create a table in the target database
        create_table_query = f"CREATE TABLE {remote_table} ("
        for column in columns:
            if column[7]=='varchar':
                if column[8]==-1:
                    column[8]='MAX'
                create_table_query += f"{column[3]} {column[7]}({column[8]}), "  # column[8] is length of varchar
            elif column[7]=='datetime2':
                create_table_query += f"{column[3]} {column[7]}({column[13]}), "
            else:
                create_table_query += f"{column[3]} {column[7]}, "  # column[3] is COLUMN_NAME, column[7] is DATA_TYPE
        create_table_query = create_table_query.rstrip(", ") + ")"
        cursor_local.execute(create_table_query)

    cursor_local.commit()
    cursor_remote.close()
    cursor_local.close()

create_tables()
