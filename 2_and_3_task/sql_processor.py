import os
from typing import Literal

import pandas as pd
import sqlalchemy as sa
from dotenv import load_dotenv

load_dotenv()


def execute_query_for_task(name_db: Literal['MSSQL', 'POSTGRESQL'],
                           sql_query: str = None, df: pd.DataFrame = None):
    """
    Функция выполнения запроса к БД
    :param name_db: имя базы данных
    :param sql_query: если обновление строк, то вставляем sql запрос
    :param df: если добавляем строки, то вставляем df
    :return:

    """
    if name_db == 'POSTGRESQL':
        settings_url = (
            f'postgresql+psycopg2://'
            f'{os.getenv('POSTGRESQL_LOGIN')}:{os.getenv('POSTGRESQL_PASSWORD')}'
            f'@{os.getenv('POSTGRESQL_HOST')}:{os.getenv('POSTGRESQL_PORT')}'
            f'/{os.getenv('POSTGRESQL_DB_NAME')}'
        )
        schema = os.getenv('POSTGRESQL_DB_SCHEMA')
    elif name_db == 'MSSQL':
        settings_url = (
            f'mssql://'
            f'{os.getenv('MSSQL_LOGIN')}:{os.getenv('MSSQL_PASSWORD')}'
            f'@{os.getenv('MSSQL_DB_NAME')}'
        )
        schema = os.getenv('MSSQL_DB_SCHEMA')
    else:
        raise Exception('Неизвестная база данных')

    sql_engine = sa.create_engine(settings_url)

    connection = sql_engine.connect()

    if isinstance(df, pd.DataFrame):
        df.to_sql('temp_table', con=connection,
                  if_exists='replace', index=False,
                  schema=schema)
    else:
        connection.execute(sa.text(sql_query))

    connection.commit()
    connection.detach()
    connection.close()
