import pytest
from ..tasks_models import Task


# Тест валидации приоритета (правильный)
def test_validate_priority_valid():
    task = Task(1, 'Test Task', 'Description', 'Category', '01-01-2025', 'высокий', 'новая')
    task.validate_priority()
    assert len(task.errors) == 0  # Ошибок не должно быть


# Тест валидации приоритета (неправильный)
def test_validate_priority_invalid():
    task = Task(1, 'Test Task', 'Description', 'Category', '01-01-2025', 'неизвестный', 'новая')
    task.validate_priority()
    assert 'Варианты для приоритета только: [\'низкий\', \'средний\', \'высокий\']' in task.errors


# Тест валидации даты (правильный формат)
def test_validate_deadline_valid():
    task = Task(1, 'Test Task', 'Description', 'Category', '01-01-2025', 'средний', 'новая')
    task.validate_deadline()
    assert len(task.errors) == 0  # Ошибок не должно быть


# Тест валидации даты (неправильный формат)
def test_validate_deadline_invalid():
    task = Task(1, 'Test Task', 'Description', 'Category', '2025-01-01', 'средний', 'новая')
    task.validate_deadline()
    assert 'Введите дату по типу: 01-01-1945' in task.errors


# Тест проверки пустых полей (все поля заполнены)
def test_validate_not_empty_all_fields():
    task = Task(1, 'Test Task', 'Description', 'Category', '01-01-2025', 'средний', 'новая')
    task.validate_not_empty()
    assert len(task.errors) == 0  # Ошибок не должно быть


# Тест проверки пустого поля "title"
def test_validate_not_empty_empty_title():
    task = Task(1, '', 'Description', 'Category', '01-01-2025', 'средний', 'новая')
    task.validate_not_empty()
    assert 'Поле "title" не может быть пустым.' in task.errors


# Тест метода is_valid (валидная задача)
def test_is_valid_valid_task():
    task = Task(1, 'Test Task', 'Description', 'Category', '01-01-2025', 'средний', 'новая')
    assert task.is_valid() is True  # Задача валидна


# Тест метода is_valid (невалидная задача)
def test_is_valid_invalid_task():
    task = Task(1, '', 'Description', 'Category', '01-01-2025', 'средний', 'новая')
    assert task.is_valid() is False  # Задача не валидна, так как title пустое


# Тест метода get_row
def test_get_row():
    task = Task(1, 'Test Task', 'Description', 'Category', '01-01-2025', 'средний', 'новая')
    row = task.get_row()
    expected = {
        'task_id': [1],
        'title': ['Test Task'],
        'description': ['Description'],
        'category': ['Category'],
        'deadline': ['01-01-2025'],
        'priority': ['средний'],
        'status': ['новая'],
    }
    assert row == expected
