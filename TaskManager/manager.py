import os
import pandas as pd

from tasks_models import Task
from helpers import make_message, start_menu
from constants import (HELLOW_MSG,
                       NOT_FOUND_MSG,
                       COMMAND_NOT_EXISTS,
                       SUCCESS_MSG,
                       NOT_INT_MSG)


class BaseTaskManager:
    ''' Базовый класс для трекера.

    При необходимости, от него можно наследоваться,
    чтобы получить доступ к базовым методам.
    '''
    def __init__(self, csv_path) -> None:
        self.last_index = 0  # Устанавливаем id задачи
        self.__task_fields = [
            'task_id',
            'title',
            'description',
            'category',
            'deadline',
            'priority',
            'status'
        ]
        self.csv_path = csv_path
        self.__create_csv()  # Создаем csv, если не создан
        self.get_last_index()  # Если csv есть, получаем последний id задачи

    @property
    def task_fields(self):
        ''' Свойство для имен полей задачи.

        Поля должны быть неизменны.
        '''

        return self.__task_fields

    def __create_csv(self):
        ''' Создает csv, если он не существует.

        Делает первую пустую задачу для отсчета id.
        '''

        if not os.path.isfile(self.csv_path):
            first_task = {field: ['Тестовое'] for field in self.task_fields}
            first_task['task_id'] = 0
            df = pd.DataFrame(first_task)
            self.save_csv(df)

    def get_last_index(self):
        ''' Получает последний id задачи из csv. '''

        df = pd.read_csv(self.csv_path)
        self.last_index = df.tail(1)['task_id'].iloc[0]

    def read_csv(self):
        ''' Создает DataFrame из csv. '''

        df = pd.read_csv(self.csv_path)
        return df

    def save_csv(self, df):
        ''' Сохраняет DataFrame в csv. '''

        df.to_csv(self.csv_path, index=False)


class TaskManager(BaseTaskManager):
    ''' Основной класс менеджера.

    Служит интерфейсом для взаимодействия с трекером.
    Наследуется от базового класса.
    '''

    def write_to_csv(self, new_task):
        ''' Записывает задачу в конец csv через конкатенацию DataFrame. '''

        df = self.read_csv()
        new_row = new_task.get_row()
        new_row['task_id'] = [self.last_index + 1]
        new_row = pd.DataFrame(new_row)
        df = pd.concat([df, new_row], ignore_index=True)
        self.save_csv(df)
        self.last_index += 1

    @make_message(divider='=')
    def create_task(self):
        ''' Создает задачу. '''

        new_task_fields = [self.last_index]

        for field in self.task_fields[1:]:
            rec = input(f'Введите {field}: ')
            new_task_fields.append(rec)

        new_task = Task(*new_task_fields)

        if new_task.is_valid():
            self.write_to_csv(new_task)
            return SUCCESS_MSG
        else:
            return '\n'.join(new_task.errors)

    @make_message(divider='=')
    def list_tasks(self):
        ''' Выводит полный список задач. '''

        df = self.read_csv()
        return df.to_string(index=False)

    @make_message(divider='=')
    def list_through_categories(self):
        ''' Выводит задачи по категориям. '''

        category = input('Введите категорию: ')

        df = self.read_csv()
        df = df[df['category'] == category]

        if df.empty:
            return NOT_FOUND_MSG
        return df.to_string(index=False)

    @make_message(divider='=')
    def update_task(self):
        ''' Обновляет задачу. '''
        try:
            task_id = int(input('Введите task_id: '))
        except Exception:
            return NOT_INT_MSG

        df = self.read_csv()

        if not df['task_id'].isin([task_id]).any():
            return NOT_FOUND_MSG

        updated_fields = [task_id]
        for field in self.task_fields[1:]:
            rec = input(f'Введите {field}: ')
            updated_fields.append(rec)

        updated_task = Task(*updated_fields)
        if updated_task.is_valid():
            for field_name, field_value in updated_task.get_row().items():
                df.loc[df['task_id'] == task_id, field_name] = field_value[0]
            self.save_csv(df)
            return SUCCESS_MSG
        return updated_task.errors

    @make_message(divider='%')
    def search_task(self):
        ''' Ищет задачи по совпадению введенной строки. '''
        find = input('Что ищем? ')
        df = self.read_csv()

        # Создаем новый DataFrame, применяя функцию lambda ко всем столбцам
        filtered_df = df[df.apply(
            lambda row: row.astype(str).str.contains(find).any(), axis=1)]
        return filtered_df.to_string(index=False)

    @make_message(divider='-')
    def delete_task(self):
        ''' Удаляет задачу. '''
        df = self.read_csv()

        try:
            task_id = int(input('Введите task_id: '))
        except Exception:
            return NOT_INT_MSG

        if not df['task_id'].isin([task_id]).any():
            return NOT_FOUND_MSG

        # Создаем новый DataFrame, исключая строку с нужным task_id
        df = df[df['task_id'] != task_id]

        self.save_csv(df)
        return SUCCESS_MSG

    @make_message(divider='=')
    def start(self):
        ''' Точка входа в работу менеджера. '''

        commands = {
            '0': self.create_task,
            '1': self.list_tasks,
            '2': self.list_through_categories,
            '3': self.update_task,
            '4': self.delete_task,
            '5': self.search_task
        }

        print(start_menu())
        command = commands.get(input())

        if command:
            print(command())
        else:
            print(COMMAND_NOT_EXISTS)


if __name__ == '__main__':
    csv_path = 'tasks.csv'
    manager = TaskManager(csv_path)

    print(HELLOW_MSG)
    while True:
        manager.start()
