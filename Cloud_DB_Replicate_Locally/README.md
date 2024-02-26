## Data Flow and Steps

### Creating a local database using Docker containers
### To replicate tables from a cloud database

1. use the `docker-compose.yml` file to create your docker container with an empty db.
   Note: `docker compose up -d` will create your container with a mssql db inside and run it detached
2. use the `export.py` script to export data from testing/remote env into parquet files
   WARNING: this script will populate your current working directory with `.parquet` files. Run it inside a separate directory to keep your workspace tidy
3. use create_tables.py to create the tables in your local db based on the read schema from remote db.
   Note: this script needs to be run only for the first time to create tables.
4. use the `import.py` file to import the data into your local db.
   Note: This file has to be in the same folder as the `.parquet` files you exported on step 2 (*unless you want to edit the script yourself and make it pull data from wherever you want*)
5. use the `data_pull.ipynb` notebook to see how data can be pulled from your local db into a Pandas Data Frame
