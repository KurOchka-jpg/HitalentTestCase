from constants import START_MENU


def find_length(result):
    """Находит длину первой строки для красивого отображения."""
    length = len(str(result).splitlines()[0])
    return length


def make_message(divider):
    """Декоратор для вывода сообщений.
    На вход получает символ-разделитель.
    Используется для красоты.
    """
    def make_message_dec(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            divider_length = find_length(result)
            message = (
                f'{divider * divider_length} \n'
                f'{result} \n'
                f'{divider * divider_length}\n'
            )
            return message
        return wrapper
    return make_message_dec


@make_message(divider='+')
def start_menu():
    return START_MENU
