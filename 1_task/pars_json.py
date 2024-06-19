import json
import os
import logging
import time
from functools import wraps

import pandas as pd

from pydantic_model import Operation, ClassForLoad

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s - %(message)s',
                    )
logger = logging.getLogger(__name__)


def time_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Функция '{func.__name__}' отработала за "
                    f"{execution_time:.6f} seconds")
        return result

    return wrapper


@time_decorator
def main_logic():
    """
    Основная логика парсинга json файла
    """
    path_to_json = os.path.join(os.getcwd(), 'begin_and_result_file',
                                'data_json.json')
    path_save_result = os.path.join(os.getcwd(), 'begin_and_result_file',
                                    'result_of_json.csv')

    with open(path_to_json, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    data_for_dataframe = [Operation(**data) for data in json_data]

    data_for_load = list()
    for value in data_for_dataframe:
        for i, _ in enumerate(value.services):
            data_for_load.append(
                create_obj_cls_for_load(value,
                                        name=value.services[i].name,
                                        price=value.services[i].price,
                                        total_price=value.services,
                                        )
            )

        if len(value.services) == 0:
            create_obj_cls_for_load(value)

    df = pd.DataFrame(data_for_load)
    df.to_csv(path_save_result, index=False, sep=';',
              encoding='Windows-1251')


def create_obj_cls_for_load(value: Operation, name=None, price=None,
                            total_price=None) -> dict:
    """
    Функция создания объекта класса ClassForLoad
    :param value: объект класса Operation, откуда берем основные параметры
    :param name: параметр для поля name
    :param price: параметр для поля price
    :param total_price: параметр для поля total_price

    """
    result = ClassForLoad(
        operation_id=value.operation_id,
        operation_date=value.operation_date,
        posting_number=value.posting.posting_number,
        sku=value.items,
        # article=value.,
        type_operation=value.operation_type,
        delivery_schema=value.posting.delivery_schema,
        name=name,
        price=price,
        count_item=len(value.items),
        total_price=total_price,
        quantity=value.items,
    ).dict(by_alias=True)
    return result


if __name__ == '__main__':
    main_logic()
