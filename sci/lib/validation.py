import copy
import traceback

from typing import Callable, Any, Optional

from sci.lib.patterns import create_ecsaddo


class ValidationError(ValueError):
    def __init__(
        self,
        location: list[str | int] = [], 
        action: str = "", 
        description: str = "",
        /, *args
    ):
        """
        Arguments
        ---
        - `location: list[str | int] = []` - Список содержащий путь к месту
            ошибки. `["one_key", 0, "some_key"]`
        
        - `action: str = ""` - Краткий `action` тег ошибки.
        
        - `description: str = ""` - Подробное описание ошибки.
        
        - args: tuple - Дополнительные (не ожидаемые) аргументы
        
        Example
        ---
        raise ValidationError(["some_key", 0, "some_key"], "action", "description")
        
        Description
        ---
        ex.args
        (location, action, description)
        """
        if not isinstance(location, list):
            action = str(location)
            location = []
        return super().__init__(location, action, description, *args)


class BaseValidate:
    """
    Meta
    ---
    Patterns:
        ecsaddo
        
    Description
    ---
    Валидация проходит в 3 этапа.
    
    1) - Вызывается метод `self.safe_wrapper(self.pre_validation)` - 
    который допускается переопределять и в нем осуществлять какую либо 
    предварительную проверку над `self.validation_data`.
    
    2) - Вызывается метод `self.safe_wrap(self.build_validation_plan())`
    который должен вернуть список с настройками каждого валидатора в виде кортежа.
    Если `self.build_validation_plan()` вернул ожидаемый ответ, то
    вызывается каждый валидатор из ответа `build_validation_plan()` 
    
    3) - Вызывается метод `self.safe_wrapper(self.full_validation)` 
    который допускается переопределять.
    В методе `self.full_validation` можно провести общую валидацию по всей, 
    уже проверенной структуре `self.validation_data`.
    
    NOTE: Полробное описание и примеры смотри в документации.
    """

    def start_validation(self) -> dict:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Description:
            Метод `start_validation` является точкой запуска валидации.

        Return
        ---
        Результат `start_validation()` при успешной валидации.
            {
                "status": "ok",
                "action": "successfully validation",
                "data": {
                    "description": "successfully validation",
                }
            }
            
        Результат `start_validation()` если валидация не пройдена.
            {
                "status": "error",
                "action": "failed validation",
                "data": {
                    "description": "failed validation",
                    "error_list": [
                        (
                            ["key_one", 0, "some_key"], 
                            "type error",
                            "some description"
                        ),
                        (
                            ["key_one", 1, "some_key"],
                            "structure error",
                            "some description" 
                        ),
                    ],
                }
            }
            
        Результат `start_validation()` если во время возникли исключения.
            {
                "status": "ex",
                "action": "failed validation",
                "data": {
                    "description": "failed validation",
                    "location": "...",
                    "error_list": [
                        (
                            ["key_one", 0, "some_key"], 
                            "type error",
                            "some description"
                        ),
                        (
                            ["key_one", 1, "some_key"],
                            "structure error",
                            "some description" 
                        ),
                    ],
                    "traceback_list": [
                        [...], [...], [...]
                    ]
                }
            }
        """
        try:
            self.traceback_list: list[list[str]] = list()
            self.error_list: list[tuple[list[str|int], str]] = list()
            # Первый этап валидации
            self.safe_wrapper(self.pre_validation)
            if self.error_list or self.traceback_list:
                return self.complete_validation()
            self.validation_plan: list[tuple[str, dict]] = self.safe_wrapper(
                self.build_validation_plan
            )
            if not isinstance(self.validation_plan, list):
                raise ValueError(
                    "method `build_validation_plan` must be return type list"
                )
            if self.error_list or self.traceback_list:
                return self.complete_validation()
            for num, validator_data in enumerate(self.validation_plan):
                try:
                    if not isinstance(validator_data, tuple):
                        raise ValueError("validator data must be type tuple")
                    validator_name: str = validator_data[0]
                    validator_kwargs: dict = (
                        validator_data[1] if len(validator_data) > 1 else {}
                    )
                    if "required" not in validator_kwargs:
                        validator_kwargs.setdefault("required", True) 
                    validator: Callable = getattr(self, validator_name)
                    self.safe_wrapper(validator, num=num, **validator_kwargs)
                except Exception as ex:
                    trc = str(traceback.format_exception(ex))
                    self.traceback_list.append(trc)
            if self.error_list or self. traceback_list:
                return self.complete_validation()
            # Третий этап валидации
            self.safe_wrapper(self.full_validation)
            return self.complete_validation()
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            self.traceback_list.append(trc)
            return create_ecsaddo(
                "ex",
                "failed validation",
                "failed validation",
                location=True,
                error_list=self.error_list,
                traceback_list=self.traceback_list,
            )    
        
        
    def safe_wrapper(self, func, *args, **kwargs) -> Optional[Any]:
        """
        Arguments
        ---
        - `func` - Оборачиваемая функция
        
        - `args` - Кортеж с позиционными аргументами
        
        - `kwargs` - словарь с именованными аргументами
        
        Description
        ---
        Метод `safe_wrapper` является защитной оберткой вызова функции `func`.
        Если в `func` всплывает исключение `ValidationError`, тогда `safe_wrapper`
        Добавляет информацию об ошибке в self.error_list.append(ex.args)
        P.S: `ex.args` - `(["key1", 0, "key2"], "type error", "some description")`
        Если в `func` всплывает любое другое исключение, то `safe_wrapper`
        отлавливает его и добавляет в `self.traceback_list.append(trc)`
        
        Return
        ---
        Any
        """
        try:
            return func(*args, **kwargs)
        except ValidationError as ex:
            self.error_list.append(ex.args)
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            self.traceback_list.append(trc)
            
        
    def complete_validation(self) -> dict:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Description
        ---
        Метод `complete_validation` является завершающим методом валидации.
        `complete_validation` проверяет атрибуты `self.error_list` и 
        `traceback_list`.
        
        Если атрибут `self.traceback` не пустой, тогда `complete_validation`
        вернет.
            {
                "status": "ex",
                "action": "failed validation",
                "data": {
                    "description": "failed validation",
                    "location": "...",
                    "error_list": [
                        (
                            ["key_one", 0, "some_key"], 
                            "type error",
                            "some description"
                        ),
                        (
                            ["key_one", 1, "some_key"],
                            "structure error",
                            "some description" 
                        ),
                    ],
                    "traceback_list": [
                        [...], [...], [...]
                    ]
                }
            }
            
        Иначе если атрибут `self.error_list` не пустой, тогда 
        `complete_validation` вернет.
            {
                "status": "error",
                "action": "failed validation",
                "data": {
                    "description": "failed validation",
                    "error_list": [
                        (
                            ["key_one", 0, "some_key"], 
                            "type error",
                            "some description"
                        ),
                        (
                            ["key_one", 1, "some_key"],
                            "structure error",
                            "some description" 
                        ),
                    ],
                }
            }
            
        Если `self.error_list` и `self.traceback_list` пустой тогда 
        `complete_validation` вернет:
            {
                "status": "ok",
                "action": "successfully validation",
                "data": {
                    "description": "successfully validation",
                    "clear_data": {...},
                }
            }
        """
        if self.traceback_list:
            return create_ecsaddo(
                "ex",
                "failed validation",
                "failed validation",
                location=True,
                error_list=self.error_list,
                traceback_list=self.traceback_list,
            )
        elif self.error_list:
            return create_ecsaddo(
                "error",
                "failed validation",
                "failed validation",
                error_list=self.error_list,
            )
        return create_ecsaddo(
            "ok",
            "successfully validation",
            "successfully validation",
        )
    
        
    def build_validation_plan(self) -> list:
        """
        Description
        ---
        Метод `build_validation_plan` является переопределяемым методом и всегда
        вызывается через обертку `self.safe_wrapper()`
        Метод должен вернуть список с настройками валидации для второго этапа
        валидации.
        (смотри пример)
        
        Return
        ---
        [
            ("node_rq_check", {"required": True}),
            ("wsBridgeBroker_check", {"required": True}),
            ("broker_connection_settings_check", {"required": True})
        ]
        """
        return []
            
            
    def pre_validation(self):
        """
        Description
        ---
        Метод `pre_validation` является переопределяемым методом и всегда
        вызывается через обертку `self.safe_wrapper()`.
        
        В `self.pre_validation` можно осуществить какую либо предварительную 
        проверку над `self.validation_data`.
        
        Метод `self.pre_validation` не должен ничего возвращать.
        Если пользовательская проверка в `self.pre_validation` не проходит, то 
        должно быть вызвано исключение 
        `ValidationError(["location",], "action", "description")`. 
        Защитная обертка `self.safe_wrapper()` самостоятельно отловит исключение 
        `ValidationError`, и добавит его данные (`ex.args`) в `self.error_list`.

        Если в `self.pre_validation` возникает исключение, то защитная обертка 
        `self.safe_wrapper()` поймает это исключение, и `traceback` в виде 
        `list[str]` этого исключения добавит в `self.traceback_list`
        
        Пример реализации метода `self.pre_validation()`
        ```python
        def pre_validation(self):
            if not isinstance(self.validate_data, dict):
                raise ValidationError(
                    [], "structure error", "validate data error"
                )
        ```
        """
        pass
    
    
    def full_validation(self):
        """
        Метод `full_validation` является переопределяемым методом и всегда
        вызывается через обертку `self.safe_wrapper()`
        
        В методе `self.full_validation` можно провести общую валидацию по всей, 
        уже проверенной структуре `self.validation_data`.

        Метод `self.full_validation` не должен ничего возвращать.
        
        Если пользовательская проверка в `self.full_validation` не проходит, то 
        должно быть вызвано исключение 
        `ValidationError(["location",], "action", "description")`. 
        Защитная обертка `self.safe_wrapper()` самостоятельно отловит исключение 
        `ValidationError`, и добавит его данные (`ex.args`) в `self.error_list`.

        Если в `self.full_validation` возникает исключение, то защитная обертка 
        `self.safe_wrapper()` поймает это исключение, и `traceback` в виде 
        `list[str]` этого исключения добавит в `self.traceback_list`
        """
        pass
    
            
    def join(
        self, 
        error_list: list[tuple[list[str | int], str]], 
        *args: tuple
    ) -> list[tuple[list[str | int], str]]:
        """
        Arguments
        ---
        - `error_list: list[tuple[list[str | int], str]]` - Список с кортежами 
        каждый кортеж отражает информацию об ошибке. 
        Первый элемент кортежа - список хранящий (по элементам) адрес где 
        возникла ошибка. 
        Второй элемент кортежа - `action` сообщение об ошибке.
        Третий элемент кортежа - `description` описание ошибки
        ```python
            [
                (
                    ["key1", "key2", 0, "key3"], 
                    "type error", 
                    "some description"
                ),
                (
                    ["key1", "key2", 0, "key4"], 
                    "structure error", 
                    "some description"
                ),
            ]
        ```
            
        - `*args: tuple` - Кортеж с переданными позиционными аргументами.
        Каждый элемент кортежа, это дополнительный префиксный ключ который
        будет добавлен к адресу каждой ошибки из `error_list` 
            `("some_key", "some_key", 3, "some_key")`
            
        Example
        ---
        ```python
        error_list = [
            (
                ["key1", "key2", 0, "key3"], 
                "type error", 
                "some description"
            ),
            (
                ["key1", "key2", 0, "key4"], 
                "structure error", 
                "some description"
            ),
        ]
        error_list = self.join(error_list, "start_key", "first_key")
        => error_list 
        [
            (
                ["start_key", "first_key", "key1", "key2", 0, "key3"], 
                "type error",
                "some description"
            ),
            (
                ["start_key", "first_key", "key1", "key2", 0, "key4"], 
                "structure error",
                "some description",
            ),
        ]
        ```
            
        Description
        ---
        Метод `join` конкатенирует кортеж `args` с списком `path_chain` каждой
        ошибки из `error_list`, и возвращает новый, измененный `error_list`
        
        Return
        ---
        Новый список - измененный `error_list`
        """
        error_list = copy.deepcopy(error_list)
        for error_tuple in error_list:    
            path_chain, *_ = error_tuple
            path_chain.reverse()
            prefix_paths = list(args)
            prefix_paths.reverse()
            path_chain += prefix_paths
            path_chain.reverse()
        return error_list
    
    
    def extract_alert(self, docstring: str, key: str, tag: str = "id:") -> str:
        """
        Arguments
        ---
        - `docstring: str` - Docstring какого либо метода
        - `key: str` - Уникальный идентификатор относительно `tag + key` 
        которого будет осуществляться поиск начала целевого блока.
        - `tag: str` - Метка начала блоков с `alert` текстом.
        
        Description
        ---
        Метод `extract_alert` позволяет из `docstring` какого либо метода
        извлечь необходимый `alert` относительно `tag + key`.
        
        Example
        ---
        ```python
        '''
        id:VZpORlzSL
        `auth_nodes_settings -> "local_nodes" -> "node_name"`
        Имя ключа `"node_name"` должно быть `str`, длинной `>=` 50 символов.
        '''
        
        alert = self.extract_alert(docstring, key="VZpORlzSL", tag="id:")
        alert
        > '`auth_nodes_settings -> "local_nodes" -> "node_name"` Имя ключа `"node_name"` должно быть `str`, длинной `>=` 50 символов.'
        ```
        
        Return
        ---
        Извлеченный `alert` без `\n`, сплошной строкой.
        """
        try:
            tagkey: str = tag + key
            necessary_tagkey_start_index = docstring.find(tagkey)
            if necessary_tagkey_start_index == -1:
                # return ""
                raise ValueError()
            necessary_block_start_index: int = (
                necessary_tagkey_start_index + len(tagkey)
            )
            necessary_block_from_beginning: str = (
                docstring[necessary_block_start_index : ]
            )
            necessary_block_from_beginning: str = (
                necessary_block_from_beginning.lstrip()
            )
            necessary_block_from_beginning_by_chars: list = (
                necessary_block_from_beginning.split(" ")
            )
            # Удаляем пустые строки
            necessary_block_from_beginning_by_chars = [
                char 
                for char in necessary_block_from_beginning_by_chars 
                if char
            ]
            try:
                necessary_block_end_index: int = (
                    necessary_block_from_beginning_by_chars.index("\n")
                )
            except Exception as ex:
                necessary_block_end_index = None
            necessary_block_by_chars: list = (
                necessary_block_from_beginning_by_chars[ : necessary_block_end_index]
            )
        
            necessary_block_by_chars: list = (
                list(map(lambda char: char.strip(), necessary_block_by_chars))
            )
            necessary_block = " ".join(necessary_block_by_chars)
            return necessary_block
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            # print(trc)
            return ""