from inquirer import prompt
import inquirer


class DatabaseManager:
    def __init__(self):
        pass

    def step_1(self):
        questions_ms_1 = [
            inquirer.List('choice',
                          message="Выберите пункт меню:",
                          choices=['Загрузить данные',
                                   'Удалить данные', 'Выход'])
        ]
        choice_ms_1 = prompt(questions_ms_1)['choice']
        if choice_ms_1 == 'Загрузить данные':
            print("Данные загружены")
        elif choice_ms_1 == 'Удалить данные':
            print("Удалил данные")

    def main_logic(self):
        while True:
            questions = [
                inquirer.List('choice',
                              message="Выберите пункт меню:",
                              choices=['MS',
                                       'PG', 'Выход'])
            ]

            choice = prompt(questions)['choice']

            if choice == 'MS':
                self.step_1()

            elif choice == 'PG':
                self.step_1()

            elif choice == 'Выход':
                break



if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.main_logic()
