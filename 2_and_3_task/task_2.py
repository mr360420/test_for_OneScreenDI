import os

from dotenv import load_dotenv

from sql_processor import execute_query_for_task

load_dotenv()


def main_logic():
    list_db = [
        'MSSQL',
        'POSTGRESQL']

    for name_db in list_db:
        if name_db == 'POSTGRESQL':
            schema = os.getenv('POSTGRESQL_DB_SCHEMA')
        else:
            schema = os.getenv('MSSQL_DB_SCHEMA')

            sql_query = f"""
            DELETE FROM {schema}.accrual_report
            WHERE id_o IN (SELECT id_o
                         FROM {schema}.accrual_report
                         GROUP BY id_o
                         HAVING COUNT(*) > 1);

            """
        execute_query_for_task(name_db, sql_query)


if __name__ == "__main__":
    main_logic()
