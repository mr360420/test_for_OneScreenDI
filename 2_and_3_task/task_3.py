import os
import glob

from dotenv import load_dotenv
import pandas as pd

from sql_processor import execute_query_for_task

load_dotenv()


def main_logic():
    list_db = [
        'MSSQL',
        'POSTGRESQL']

    directory_for_file = 'files_for_3_task'
    directory = os.path.join(os.getcwd(), directory_for_file)
    csv_file = glob.glob(os.path.join(directory, '*.csv'))
    df_for_update = pd.read_csv(csv_file[0], sep=';')

    for name_db in list_db:
        if name_db == 'POSTGRESQL':
            schema = os.getenv('POSTGRESQL_DB_SCHEMA')
        else:
            schema = os.getenv('MSSQL_DB_SCHEMA')

        sql_query = f"""
        UPDATE {schema}.rating r
        SET sku = (SELECT sku_new
                   FROM {schema}.temp_table tt 
        WHERE r.sku = tt.sku_old)
        WHERE sku IN (SELECT sku_old 
        FROM {schema}.temp_table);

        DROP TABLE IF EXISTS {schema}.temp_table;
            """
        execute_query_for_task(name_db, df=df_for_update)
        execute_query_for_task(name_db, sql_query)


if __name__ == "__main__":
    main_logic()
