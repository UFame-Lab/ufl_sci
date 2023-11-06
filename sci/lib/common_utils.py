import random
import string
import inspect


def generate_variable_name(
    length: int,
    prefix: str = ""
) -> str:
    """
    Arguments
    ---
    - `length: int` - Необходимая длина строки.
    
    - `prefix: str` - Прификс строки. (длина префикса входит в общую длину). 
    
    Description
    ---
    `generate_variable_name` генерирует рандомную строку длиной `length`
    включая `prefix` (если аргумент был передан) используя 
    `ascii_letters` + `digits`.
    
    Если len(prefix) >= length, тогда возвращается только префикс.
    
    Return
    ---
    `prefix + length`
    """
    if prefix:
        if len(prefix) >= length:
            length = 0
        else:
            length -= len(prefix)
    # все буквы и цифры
    letters = string.ascii_letters + string.digits
    variable_name = prefix + ''.join(
        random.choices(letters, k=length)
    )
    return variable_name


def json_safe(obj):
    """
    Arguments
    ---
    - `obj` python объект который нужно сериализовать для `JSON`
    
    Description
    ---
    `json_safe` помогает сериализовать python объекты в `JSON `которые 
    самостоятельно не поддерживают сериализацию в `JSON`
    
    Return
    ---
    `str` - valid for JSON
    
    Raises
    ---
    Переданный `obj` не возможно сериализовать в `JSON`
    ```python
    TypeError(f"Object of type '{type(obj).__name__} is not JSON serializable")
    ```
    """
    if isinstance(obj, (tuple, set)):
        return list(obj)
    elif isinstance(obj, object):
        return str(obj)
    else:
        raise TypeError(
            f"Object of type '{type(obj).__name__}' "
            f"is not JSON serializable"
        )
    
    
def separate_recipient_address(
    recipient_name: str
) -> tuple[str]:
    """
    Arguments
    ---
    - `recipient_name: str` - Полный адрес получателя `"node_name:app_name"`
    
    Description
    ---
    Функция `separate_recipient_name_by_components` 
    принимает `recipient_name` в виде `"node_name:app_name"` 
    и возвращает кортеж ("node_name", "app_name")
    
    Return
    ---
    Кортеж `("node_name", "app_name")`
    
    Raises
    ---
    `recipient_name` должен иметь структуру `"node_name:app_name"`
    ```python
    raise ValueError(
        f"Адрес получателя EventMessage должен иметь структуру "
        f"'node_name:app_name'. "
        f"Текущий recipient: {recipient_name}"
    )
    ```
    """
    index = recipient_name.find(":")
    if index == -1:
        raise ValueError(
            f"Адрес получателя EventMessage должен иметь структуру "
            f"'node_name:app_name'. "
            f"Текущий recipient: {recipient_name}"
        )
    node_name = recipient_name[ : index]
    app_name = recipient_name[index + 1 : ]
    return (node_name, app_name)


def get_current_location():
    """
    Return
    ---
    (path_to_module, qual_name)
    """
    try:
        # Получаем frame вызывающего кода
        frame = inspect.currentframe().f_back
        path_to_module = frame.f_code.co_filename
        qual_name = frame.f_code.co_qualname
        return (path_to_module, qual_name)
    except Exception as ex:
        return ('empty', 'empty')


def get_next_delay(
    last_delay: int, 
    multiply: int, 
    max_limit: int
) -> int:
    """
    Arguments
    ---
    - `last_delay: int` - Сколько в секундах состоял прошлый `delay`.
    0 если это первое значение.
    
    - `multiplay: int` - На какое число нужно умножить `last_delay`.
    Если `last_delay` == 0, тогда возвращается число равное `multiply`
    
    - `max_limit: int` - Максимально допустмое число.
    
    Description
    ---
    Умножает `last_delay` на `multiply`.
    Если `last_delay` равняется 0, тогда возвращает `multiply`.
    Если `last_delay` * `multiply` >= `max_limit`, тогда возвращается 
    `max_limit`
    
    Return
    ---
    int
    """
    if last_delay == 0:
        return multiply
    delay = last_delay * multiply
    if delay >= max_limit:
        return max_limit
    else:
        return delay
    
    
def smart_print(*args, **kwargs):
    def get_location_data():
        try:
            # Получаем frame вызывающего кода
            frame = inspect.currentframe().f_back.f_back
            path_to_module = frame.f_code.co_filename
            qual_name = frame.f_code.co_qualname
            return (path_to_module, qual_name)
        except Exception as ex:
            return ('empty', 'empty')
    path_to_module, qual_name = get_location_data()
    print("------------------------")
    print(path_to_module + "\n" + qual_name)
    print(*args, **kwargs)
    print("------------------------\n")