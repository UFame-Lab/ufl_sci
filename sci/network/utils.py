import traceback
from sci.lib.patterns import create_ecsaddo
from sci.sci_typing import ecsaddo


class SCI_ResposnePayload:
    """
    Description
    ---
    Класс `SCI_ResposnePayload` предоставляет интерфейс для создания структуры
    данных, которая соответствует шаблоннаму `EventMessage -> "message_payload"`
    
    ```python
    {
        "data": {"key": "value"},
        "meta": {
            "status_code": 200
        }
    }
    ```
    
    Example
    ---
    ```python
    message_payload: SCI_ResposnePayload = SCI_ResposnePayload({"key": "value"}, 200)
    message_payload: dict = message_payload.response_payload
    ```
    """
    def __init__(
        self, 
        response_data: dict, 
        status_code: int,
        *args, **kwargs
    ):
        """
        Arguments
        ---
        - `response_data: dict` - Словарь который будет помещен в качестве
        значения ключа `data`
        
        - `status_code: int` - Числовой идентификатор который будет помещен
        в качестве значения `meta -> "status_code"`
        
        - `*args`
        
        - `**kwargs`
        
        Raises
        ---
        Если `response_data` не `dict`
        ```python
        raise ValueError("response_payload -> data должна иметь тип dict")
        ```
        
        Если `status_code` не `int`
        ```python
        raise ValueError("response_payload: status_code error")
        ```
        """
        if not isinstance(response_data, dict):
            raise ValueError(
                "response_payload -> data должна иметь тип dict"
            )
        self.response_data = response_data
        if not isinstance(status_code, int): # + bool
            raise ValueError(
                "response_payload: status_code error"
            )
        self.status_code = int(status_code)
    
    
    @property
    def response_payload(self):
        """
        Description
        ---
        Свойство возвращающая валидный `message_payload` на основе
        атрибутов `self.response_data`, `self.status_code`.
        
        ```python
        {
            "data": {"key": "value"},
            "meta": {
                "status_code": 200
            }
        }
        ```
        """
        return {
            "data": self.response_data,
            "meta": {
                "status_code": self.status_code
            }
        }


def create_response_payload(
    response_data: dict, 
    status_code: int = 200
):
    """
    Arguments
    ---
    - `response_data: dict` - Словарь который будет помещен в качестве
        значения ключа `data`
    
    - `status_code: int = 200` - Числовой идентификатор который будет помещен
        в качестве значения `meta -> "status_code"`. Значение по умолчанию 200.
    
    Description
    ---
    Вспомогательная функция `create_response_payload` позволяет лего создать
    валидный `EventMessage -> "message_payload"` на основе `SCI_ResposnePayload`
    
    Return
    ---
    Экземпляр `SCI_ResposnePayload`
    """
    return SCI_ResposnePayload(response_data, status_code)


async def sendResponse(
    EventMessage: dict,
    response_payload: dict,
    app_name: str,
    sci_cli,
) -> ecsaddo:
    """
    Meta
    ---
    Doc:
        pass
    Patterns
        ecsaddo
        
    Arguments
    ----
    - `EventMessage: dict` - `EventMessage` `"mType": "request"` относительно 
    которого нужно сконфигурировать и отправить 
    `"EventMessage"` `"mType": "response"` 
    
    - `response_payload: dict` Словарь соответствующий структуре:
    
    ```python
    {
        "data": {"key": "value"},
        "meta": {
            "status_code": 200
        }
    }
    ```
    
    - `app_name: str` - Имя текущего приложения которое будет указано в
    качестве значения `EventMessage -> "sender"`
    
    - `sci_cli` - Экземпляр `SCI_cli` от `sci node`, относительно которого
    нужно отправить сообщение.
    
    Description
    ---
    Асинхронная функция `sendResponse` позволяет сконфигурировать и отправить
    ответный `EventMessage` `"mType": "response"` относительно 
    `EventMessage` `"mType": "request"`
    
    Return
    ---
    `ecsaddo` "ok", "error", "ex"
    """
    try:
        EventResponse = {
            "sender": app_name,
            "action": EventMessage["action"],
            "address_section": {
                "recipient": EventMessage["sender"],
                "interface": (
                    EventMessage["address_section"]["interface"]
                )
            },
            "meta": {
                "mType": "response",
                "session_id": EventMessage["meta"]["session_id"],
            },
            "message_payload": response_payload,
        }
        if EventMessage["address_section"]["interface"] == "ws":
            EventResponse["address_section"].setdefault(
                "wsbridge", 
                EventMessage["address_section"]["wsbridge"]
            )
        ecsaddo = await sci_cli.send_message(EventResponse)
        return ecsaddo
    except Exception as ex:
        trc = str(traceback.format_exception(ex))
        return create_ecsaddo(
            "ex",
            "sendResponse (ex)",
            "exception occurred in sendResponse",
            location=True,
            traceback=trc
        )
        
    
def search_wsBridgeBroker(
    SCI_SETTINGS: dict, 
    wsBridge_name: str
) -> tuple[str, dict]:
    """ 
    Arguments
    ---
    - `SCI_SETTINGS: dict` - Настройки текущего `sci node`
    - `wsBridge_name: str` Имя `wsBridge` для которого совершается поиск
    `wsBridgeBroker`.
    
    Description
    ---
    Функция `search_wsBridgeBroker` совершает поиск `wsBridgeBroker` для
    `wsBridge_name`
    
    Сперва совершается поиск в `SCI_SETTINGS["websocket_connections"]`, затем
    в `SCI_SETTINGS["nodes"]["local_nodes"]`, затем в
    `SCI_SETTINGS["nodes"]["remote_nodes"]`
    
    Return
    ---
    ("node", dict) - Текущий `SCI` узел явялется `wsBridgeBroker`, dict -
    это настройки `wsBridgerBroker` из 
    `SCI_SETTINGS -> "websocket_connections" -> "wsBridge_name"`
    
    ("local_node", dict) -> Текущий `SCI` node не явялетс `wsBridgeBroker`.
    `wsBridgeBroker` является `SCI`node из 
    `SCI_SETTINGS -> "nodes" -> "local_nodes"`, dict - это настройки
    соответствующего `SCI` node из `SCI_SETTINGS -> "nodes" -> "local_nodes"`
    
    ("remote_node", dict) -> Текущий `SCI` node не явялетс `wsBridgeBroker`.
    `wsBridgeBroker` является `SCI`node из 
    `SCI_SETTINGS -> "nodes" -> "remote_nodes"`, dict - это настройки
    соответствующего `SCI` node из `SCI_SETTINGS -> "nodes" -> "remote_nodes"`
    
    None - wsBridgeBroker не найден
    """
    if wsBridge_name in SCI_SETTINGS["websocket_connections"]:
        wsBridgeBroker_settings: tuple[str, dict] = (
            "node",
            SCI_SETTINGS["websocket_connections"].get(wsBridge_name)
        )
        return wsBridgeBroker_settings
    else:
        local_nodes: dict = SCI_SETTINGS["nodes"]["local_nodes"]
        for local_node in local_nodes:
            wsBridgeBroker: tuple[str] = (
                local_nodes[local_node].get("wsBridgeBroker", tuple())
            )
            if wsBridge_name in wsBridgeBroker:
                wsBridgeBroker_settings: tuple[str, dict] = (
                    "local_node",
                    local_nodes[local_node]
                )
                return wsBridgeBroker_settings
        remote_nodes: dict = SCI_SETTINGS["nodes"]["remote_nodes"]
        for remote_node in remote_nodes:
            wsBridgeBroker: tuple[str] = (
                remote_nodes[remote_node].get("wsBridgeBroker", tuple())
            )
            if wsBridge_name in wsBridgeBroker:
                wsBridgeBroker_settings: tuple[str, dict] = (
                    "remote_node",
                    remote_nodes[remote_node]
                )
                return wsBridgeBroker_settings
    return None