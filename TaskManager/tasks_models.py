import re


class Task:
    """Класс-модель для работы с задачами.
    Используется для валидации и представления задачи.
    """

    def __init__(self, task_id, title, description,
                 category, deadline, priority, status):
        self.task_id = task_id
        self.title = title
        self.description = description
        self.category = category
        self.deadline = deadline
        self.priority = priority
        self.status = status
        self.priority_options = ['низкий', 'средний', 'высокий']
        self.errors = []

    def validate_priority(self):
        """Валидирует поле priority."""
        if self.priority not in self.priority_options:
            self.errors.append(
                f'Варианты для приоритета только: {self.priority_options}')

    def validate_deadline(self):
        """Валидирует поле deadline."""
        if not re.fullmatch(r'^\d{2}-\d{2}-\d{4}$', self.deadline):
            self.errors.append('Введите дату по типу: 01-01-1945')

    def validate_not_empty(self):
        """Проверяет, что поля не пустые."""
        if not self.title.strip():
            self.errors.append('Поле "title" не может быть пустым.')
        if not self.description.strip():
            self.errors.append('Поле "description" не может быть пустым.')
        if not self.category.strip():
            self.errors.append('Поле "category" не может быть пустым.')
        if not self.deadline.strip():
            self.errors.append('Поле "deadline" не может быть пустым.')
        if not self.priority.strip():
            self.errors.append('Поле "priority" не может быть пустым.')
        if not self.status.strip():
            self.errors.append('Поле "status" не может быть пустым.')

    def is_valid(self):
        """Используется для запуска валидаторов."""
        self.validate_priority()
        self.validate_deadline()
        self.validate_not_empty()
        return not self.errors

    def get_row(self):
        """Представляет задачу для передачи в DataFrame."""
        data_frame = {
            'task_id': [self.task_id],
            'title': [self.title],
            'description': [self.description],
            'category': [self.category],
            'deadline': [self.deadline],
            'priority': [self.priority],
            'status': [self.status],
        }
        return data_frame
