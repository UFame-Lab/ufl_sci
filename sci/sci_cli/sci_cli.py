import traceback
import asyncio
import json
import time

from typing import Awaitable, Callable
from pprint import pprint

import redis.asyncio as redis

from sci import sci_settings
from sci.network.utils import search_wsBridgeBroker
from sci.lib.common_utils import (
    generate_variable_name, 
    separate_recipient_address,
    json_safe
)
from sci.sci_typing import ecsaddo
from sci.sci_exceptions import SCIRuntimeError, DestinationError
from sci.lib.patterns import create_ecsaddo
from sci.lib.logging import save_log
from sci.app_controllers.base_controller import AUTH_SERVICE_ACTIONS
from sci.sci_cli.validators import EventMessage_Validate



class SCI_cli:
    def __init__(
        self, 
        SCI_SETTINGS: dict, 
        sci_mode: str, 
        sci_ref,
    ):
        """
        Arguments
        ---
        - `SCI_SETTINGS: dict` - Настройки текущего `sci node`
        
        - `sci_mode: str` - В каком режиме запускается текущий `sci node`.
        "standart", "only_local", "shadow".
        
        - `sci_ref` - ссылка на экземпляр `SCI`
        """
        self.SCI_SETTINGS: dict = SCI_SETTINGS
        self.sci_mode: str = sci_mode
        self.sci_ref = sci_ref


    async def send_message(
        self, 
        EventMessage : dict,
        ping_pong: bool = False,
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__gw lvl 1]
            save-log

        Arguments
        ---
        `EventMessage: dict` - `EventMessage` который нужно провалидировать и
        передать в `sci_core` на отправку в целевой `sci node`
        
        `ping-pong: bool = False` - Использовать ли `ping-pong` для проверки
        активности целевого узла / приложения.

        Description
        ----
        Асинхронный метод `send_message()` является `__gw` методом передачи
        сообщения в `sci_core`.
        
        Return
        ---
        `ecsaddo` "ok" / "error" / "ex" отражающий успешность передачи 
        `EventMessage` в `sci_core`.
        """
        try:
            EventMessage_safe: dict = json.loads(
                json.dumps(EventMessage, default=json_safe)
            )
            ecsaddo_send_message__pl: ecsaddo = (
                await self.send_message__pl(EventMessage, ping_pong)
            )
            if ecsaddo_send_message__pl["status"] != "ok":
                ecsaddo_for_logging: dict = json.loads(
                    json.dumps(ecsaddo_send_message__pl, default=json_safe)
                )
                ecsaddo_for_logging["data"].setdefault(
                    "EventMessage", EventMessage_safe
                )
                ecsaddo_for_logging["data"].setdefault(
                    "SCI_SETTINGS", self.SCI_SETTINGS
                )
                if sci_settings.DEBUG:
                    pprint(
                        "--------------------\n"
                        "sci_cli: Передача EventMessage в sci_core "
                        "завершилась ошибкой \n"
                        f"{ecsaddo_for_logging}\n"
                        "--------------------\n"
                    )
                save_log(
                    self.sci_ref.logfilePath, 
                    ecsaddo_for_logging
                )
            return ecsaddo_send_message__pl
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "send_message (ex)",
                "exception occurred in send_message",
                location=True,
                traceback=trc,
                EventMessage=EventMessage_safe,
                SCI_SETTINGS=self.SCI_SETTINGS,
            )
            if sci_settings.DEBUG:
                pprint(
                    "--------------------\n"
                    "sci_cli: Передача EventMessage в sci_core "
                    "завершилась исключением \n"
                    f"{data}\n"
                    "--------------------\n"
                )
            save_log(self.sci_ref.logfilePath, data)
            # "status": "ex"
            return data
            


    async def send_message__pl(
        self, 
        EventMessage: dict,
        ping_pong: bool,
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 1]
            ecsaddp

        Arguments
        ---
        `EventMessage: dict` - `EventMessage` который нужно провалидировать и
        передать в `sci_core` на отправку.
        
        `ping-pong: bool = False` - Использовать ли `ping-pong`.
        
        Description
        ---
        Асинхронный метод `send_message__pl()` является основным `payload`
        методом валидации и передачи `EventMessage` в `sci_core`
        целевого `sci node`
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        F.E
        ```python
        {
            "status": "ok",
            "action": "",
            "data": {
                "description": "",
                "awaitable_response": <lambda function -> awaitable_resposne>
            }
        }
        ```
        """
        try:
            max_startup_time = int(time.time() + 3) 
            while True:
                if int(time.time()) > max_startup_time:
                    raise SCIRuntimeError("sci core is not running")
                is_ready = self.sci_ref.core_is_ready()
                if not is_ready:
                    await asyncio.sleep(0.3)
                    continue
                break
            # Отправляем SCI_Message на валидацию
            ecsaddo_validate: ecsaddo = EventMessage_Validate(
                validation_data=EventMessage, 
                sci_mode=self.sci_mode,
                SCI_SETTINGS=self.SCI_SETTINGS
            ).start_validation()
            if ecsaddo_validate["status"] != "ok":
                return ecsaddo_validate
            EventMessage["meta"].setdefault("sci_mode", self.sci_mode)
            if EventMessage["meta"]["mType"] == "request":
                if self.sci_mode != "shadow":
                    ecsaddo_destination_check: dict = (
                        self.destination_check(EventMessage)
                    )
                    if ecsaddo_destination_check["status"] != "ok":
                        # "error",
                        # "recipient not found",
                        # "recipient not found"
                        return ecsaddo_destination_check
                if ping_pong:
                    await_timeout = sci_settings.await_pp_timeout
                    expire_time = sci_settings.pp_expire_time + time.time()  
                    ping_pong_Message = {
                        "sender": EventMessage["sender"],
                        "action": "ping-pong",
                        "address_section": EventMessage["address_section"],
                        "meta": {
                            "mType": "request",
                            "sci_mode": self.sci_mode,
                        },
                        "message_payload": {
                            "data": {},
                            "meta": {
                                "expire_time": expire_time  
                            },
                        },
                        "response_settings": {
                            "isAwaiting": True,
                            "await_timeout": await_timeout
                        }
                    }
                    ecsaddo_sender__pl: dict = await self.sender__pl(
                        ping_pong_Message
                    )
                    if ecsaddo_sender__pl["status"] != "ok":
                        return ecsaddo_sender__pl
                    awaitable_response: Callable[..., Awaitable] = (
                        ecsaddo_sender__pl["data"]["awaitable_response"]
                    )
                    try:
                        ping_pong_result = await asyncio.wait_for(
                            asyncio.create_task(awaitable_response()),
                            await_timeout + 0.5
                        )
                    except asyncio.TimeoutError as ex:
                        ping_pong_result = create_ecsaddo(
                            "error",
                            "ping-pong not answer",
                            "ping-pong not answer",
                        )
                    if not isinstance(ping_pong_result, SCI_Response):
                        # Основной запрос не отправляется.
                        return ping_pong_result # "status": "error" - "ping-pong error"
                    
                    if ping_pong_result.status_code == 524: # "timeout"
                        return create_ecsaddo(
                            "error",
                            "ping-pong timeout",
                            "ping-pong timeout"
                        )
                    elif ping_pong_result.status_code == 404: # Not found
                        return create_ecsaddo(
                            "error",
                            "recipient not found",
                            "recipient not found",
                        )
                    elif ping_pong_result.status_code == 401: # Unauthorized
                        # Не используется
                        return create_ecsaddo(
                            "error",
                            "SCI node unauthorized",
                            "SCI node unauthorized",
                        )
                    elif (
                        ping_pong_result.status_code == 406 or 
                        ping_pong_result.status_code != 200
                    ): # Acceptable
                        return create_ecsaddo(
                            "error",
                            "ping-pong error",
                            "ping-pong error"
                        )
            ecsaddo_sender__pl = await self.sender__pl(EventMessage)
            return ecsaddo_sender__pl
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "send_message__pl (ex)",
                "exception occurred in send_message__pl",
                location=True,
                traceback=trc
            )
          

    async def sender__pl(
        self, 
        EventMessage: dict
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 2]
            ecsaddo
           
        Arguments
        ---
        - `EventMessage: dict` Сообщение которое нужно передать в `sci_core`
        целевого `sci node`. 
            
        Description:
        Асинхронный метод `sender__pl()` передает `EventMessage` в `sci_core`
        целевого `sci node`.
        В зависимости от режима работы `sci node` 
        ("standart", "only_local", "shadow"), если `EventMessage` указывает
        на ожидание ответа, то `sender__pl` конфигурирует `awaitable_response` -
        `lambda` функцию возвращающую `awaitable` объект ожидания ответа, 
        и добавляет ее конфигурацию в текущий `EventMessage` для того чтобы
        `sci_core` текущего `sci node` смог отправить ответ.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        ```python
        {
            "status": "ok",
            "action": "",
            "data": {
                "description": "",
                "awaitable_response": <lambda function -> awaitable_resposne>
            }
        }
        ```
        """
        try:
            promise = False
            if (
                EventMessage["meta"]["mType"] == "request" and
                EventMessage["response_settings"]["isAwaiting"]
            ):
                ecsaddo_get_awaitable_response_promise: ecsaddo = (
                    self.get_awaitable_response_promise()
                )
                if ecsaddo_get_awaitable_response_promise["status"] != "ok":
                    return ecsaddo_get_awaitable_response_promise
                promise: Callable[..., Awaitable] = (
                    ecsaddo_get_awaitable_response_promise["data"]["promise"]
                )
                promise: Callable[..., Awaitable] = (
                    self.convert_to_sci_response(promise)
                )
                EventMessage["response_settings"].setdefault(
                    "awaiting_response_queue_settings", 
                    ecsaddo_get_awaitable_response_promise["data"].get(
                        "awaiting_response_queue_settings"
                    )
                )
            # Отправляем сообщение в sci_core целевого `sci node`
            ecsaddo_send_to_sci_core: dict = (
                await self.send_to_sci_core(EventMessage)
            )
            if ecsaddo_send_to_sci_core["status"] == "ok" and promise:
                ecsaddo_send_to_sci_core['data'].setdefault(
                    "awaitable_response", 
                    promise
                )
            return ecsaddo_send_to_sci_core
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "sender__pl (ex)",
                "excrption occurred in sender__pl",
                location=True,
                traceback=trc
            )
    

    async def send_to_sci_core(
        self, 
        EventMessage: dict
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Arguments
        ---
        - `EventMessage: dict` Отправляемое сообщение.
            
        Description
        ---
        Асинхронная функция `send_to_sci_core()` передает `EventMessage` в 
        `sci_core` целевого `sci node`.
        Если текуший `sci node` запущен в режиме "standart" или "only_local",
        тогда `EventMessage` передается в `sci_core` текущего `sci node`.
        Если текущий `sci node` запущен в режиме "shadow", тогда `EventMessage`
        передается в `sci_core` целевого (связанного) `sci node`
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        try:
            if self.sci_mode == "shadow":
                related_node_name: str = self.SCI_SETTINGS.get(
                    "related_node_rq"
                )
                redis_conn: redis.Redis = self.SCI_SETTINGS.get(
                    "local_broker_connection_settings"
                ).get("redis").get("redis_conn")
                await redis_conn.rpush(
                    related_node_name,
                    json.dumps(EventMessage)
                )
            else:
                # "only_local", "standart"
                queue: asyncio.Queue = self.SCI_SETTINGS.get("node_aq")
                await queue.put(EventMessage)
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "send_to_sci_core (ex)",
                ("exception occurred during "
                "send message to sci_core in send_to_sci_core"),
                location=True,
                traceback=trc
            )
            

    def destination_check(
        self, 
        EventMesage: dict
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Arguments
        ---
        - `EventMessage: dict` Отправляемое сообщение.
            
        Description
        ---
        Метод `destination_check()` проверяет действительно ли `EventMessage`
        может быть отправлен относительно текущего `sci_core`.
        
        NOTE:
        `EventMessage` `"mType": "response"` не проходит `destination_check`,
        так как считается что "response" должен быть отправлен по тому же пути,
        по которому пришел "request". 
        
        `EventMessage` отправляемый от `sci node` "shadow" не проходит 
        `destination_check` в `sci_cli`, так как у текущего `sci node` "shadow"
        не хватает данных для осуществления проверок. Такой `EventMessage` будет
        проходить `destination_check` в `sci_core` целевого, связанного `sci node`
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        try:
            address_section: dict = EventMesage["address_section"]
            action: str = EventMesage["action"]
            recipient_node_name, recipient_app_name = (
                separate_recipient_address(
                    address_section["recipient"]
                )
            )
            current_node_name: str = self.SCI_SETTINGS["node_name"]
            if address_section["interface"] == "local-aq":
                if recipient_node_name != current_node_name:
                    raise DestinationError("wrong recipient value")
                if recipient_app_name in self.SCI_SETTINGS["app_controllers"]:
                    return create_ecsaddo("ok")
            elif address_section["interface"] == "local-rq":
                if recipient_node_name == current_node_name:
                    raise DestinationError("wrong recipient value")
                if (
                    action in AUTH_SERVICE_ACTIONS or
                    recipient_node_name in 
                    self.SCI_SETTINGS["nodes"]["local_nodes"]
                ):
                    return create_ecsaddo("ok")
            elif address_section["interface"] == "remote-rq":
                if recipient_node_name == current_node_name:
                    raise DestinationError("wrong recipient value")
                if (
                    action in AUTH_SERVICE_ACTIONS or
                    recipient_node_name in 
                    self.SCI_SETTINGS["nodes"]["remote_nodes"]
                ):
                    return create_ecsaddo("ok")
            elif address_section["interface"] == "ws":
                if (
                    recipient_node_name in
                    self.SCI_SETTINGS["nodes"]["local_nodes"] or
                    recipient_node_name in
                    self.SCI_SETTINGS["nodes"]["remote_nodes"]
                ):
                    raise DestinationError("wrong recipient value")
                wsBridge_name = address_section["wsbridge"]
                wsBridgeBroker_settings: tuple[str, dict] = (
                    search_wsBridgeBroker(self.SCI_SETTINGS, wsBridge_name)
                )
                if wsBridgeBroker_settings:
                    return create_ecsaddo("ok")
            raise DestinationError("recipient not found")
        except DestinationError as ex:
            return create_ecsaddo(
                "error",
                "recipient not found",
                "recipient not found",
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "recipient not found",
                "exception occurred in destination_check (sci_cli)",
                location=True,
                traceback=trc
            )


    def get_awaitable_response_promise(self) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 2]
            ecsaddo

        Description
        ----
        Метод `get_awaitable_response_promise()` возвращает `lambda` 
        функцию которая хранит контекст для формирования сопрограммы, и при 
        вызове возвращает готовую `awaitable` сопрограмму ожидания ответа 
        (относительно текущего режима `SCI` node).

        Если текущий режим `SCI` node - "shadow", тогда сопрограмма будет 
        ожидать результат из redis переменной.

        Если Текущий режим `SCI` node - "standart", "only_local", тогда 
        сопрограмма будет ожидать результат из `asyncio.Queue`

        Для того чтобы `sci_core` понял куда отправлять ответ, метод 
        `SCI_cli.get_awaitable_response_promise()` возвращает `ecsaddo` в 
        "data" которого есть ключ
    
        ```python
            "awaiting_response_queue_settings": {
                "q_type": "redis_variable_name" / "aq",
                "queue": "redis var name" / <asyncio.Queue>
            }
        ```
        - "q_type": "redis_variable_name" 
            указывает на то, что ответ нужно записать в redis переменную
        - "q_type": "aq" 
            asyncio queue - указывает на то, что ответ нужно будет записать в 
            `asyncio.Queue` 
        """
        try:
            if self.sci_mode == "shadow":
                q_type =  "redis_variable_name"
                queue: str = generate_variable_name(
                    length=30, 
                    prefix="sci_response:"
                )
                promise: Callable[..., Awaitable[dict]] = (
                    lambda: self.await_rq_response(queue)
                )
            else:
                # "only_local", "standart"
                queue = asyncio.Queue()
                q_type =  "aq"
                promise: Callable[..., Awaitable[dict]] = (
                    lambda: self.await_aq_response(queue)
                )
            return create_ecsaddo(
                "ok",
                promise=promise,
                awaiting_response_queue_settings= {
                    "q_type": q_type,
                    "queue": queue
                }
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "create awaitable response error",
                ("exception occurred during create "
                "awaitable response in get_promise"),
                location=True,
                traceback=trc
            )
        
        
    async def await_aq_response(
        self, 
        aq_name: asyncio.Queue
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            save-log
           
        Arguments
        ---
        - `aq_name: asyncio.Queue` `asyncio.Queue` очередь ожидания ответа.
            
        Description
        ---
        `await_aq_response()` асинхронная функция которая совершает `await` 
        переданной `asyncio.Queue`

        Ответ в заявленную очередь `asyncio.Queue` отправляет `sci_core` когда:
        - `ResponseSession` создал и завершил текущую сессию по `timeout`
        
        - `ResponseSession`создал сессию, получил ответ и успешно завершает 
        текущую сессию
        
        - `post_manager__pl()` `EventMessage` не прошел `destination_check` в
        `sci_core`, `ResponseSession` сессию не создавал, `sci_core` отправляет
        ответ в заявленные конфигурации ожидания ответа `EventMessage`.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            response = await aq_name.get()
            return response
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "await aq error",
                "exception occurred during await response in await_aq_response",
                location=True,
                traceback=trc
            )
            save_log(self.sci_ref.logfilePath, data)
            return data
        

    async def await_rq_response(
        self, 
        rq_name: str
        ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            save-log
           
        Arguments
        ---
        - `rq_name: str` - имя `redis` переменной ожидания ответа.
            
        Description
        ---
        `await_aq_response()` асинхронная функция которая совершает `await` 
        переданной `asyncio.Queue`

        Ответ в заявленную очередь `asyncio.Queue` отправляет `sci_core` когда:
        - `ResponseSession` создал и завершил текущую сессию по `timeout`
        
        - `ResponseSession`создал сессию, получил ответ и успешно завершает 
        текущую сессию
        
        - `post_manager__pl()` `EventMessage` не прошел `destination_check` в
        `sci_core`, `ResponseSession` сессию не создавал, `sci_core` отправляет
        ответ в заявленные конфигурации ожидания ответа `EventMessage`.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            redis_conn: redis.Redis = self.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            ).get("redis").get("redis_conn")
            response_b: tuple[bytes] = await redis_conn.blpop(rq_name)
            response_str: str = response_b[-1].decode()
            ecsaddo_final_response : dict = json.loads(response_str)
            return ecsaddo_final_response
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "await rq error",
                "exception occurred during await response in await_rq_response",
                location=True,
                traceback=trc
            )
            save_log(self.sci_ref.logfilePath, data)
            return data
            
            
    def convert_to_sci_response(
        self, 
        await_response: Callable[..., Awaitable]
    ):
        """
        Arguments
        ---
        - `await_response: Callable[..., Awaitable]` awaitable ожидания ответа.
        
        Description
        ---
        Вспомогательный декоратор `convert_to_sci_response` позволяет
        сериализовать `EventMessage` `"mType": "response"` в экземпляр
        `SCI_Response`.
        """
        async def wrapper(*args, **kwargs):
            session_result = await await_response(*args, **kwargs)
            response = SCI_Response(session_result)
            return response
        return wrapper
                
                
class SCI_Response:
    """
    Экземпляр класса `SCI_Response` позволяет легко получить доступ к 
    основным ключам `EventMessage` `"mType": "response"`.
    
    - `response.status_code` - Статус ответа. 
    `EventMessage -> "message_payload" -> "meta" -> "status_code"`
    
    - `response_data` - `EventMessage -> "message_payload" -> "data"`
    
    - `response.session_result` - `ecsaddo` всей сессии.
    """
    def __init__(
        self, 
        session_result: dict
    ):
        self.session_result = session_result
        self.read_resposne()
        
        
    def __str__(self):
        return f"<{self.__class__.__name__}: {self.status_code}>"
    
    
    def read_resposne(self):
        try:
            if self.session_result["status"] != "ok":
                # 408 - Request Timeout
                # 406 -  Not Acceptable
                # "sci_core not answer" 
                if self.session_result["action"] == "session timeout error":
                    # SCI_core.ResponseSession завершил сессию по `timeout`
                    self.status_code = 524 #  A Timeout Occurred
                elif self.session_result["action"] == "recipient not found":
                    self.status_code = 404 # Not Found
                elif self.session_result["action"] == "authorized error":
                    self.status_code = 401 # Unauthorized
                else:
                    # EventMessage не прошел проверки или фатальная ошибка
                    self.status_code = 406 # Not Acceptable
                self.response_data = {}
            else:
                status_code: int = (
                    self.session_result["data"]["response"].get(
                        "message_payload"
                    )["meta"]["status_code"]
                )
                response_data: dict = (
                    self.session_result["data"]["response"].get(
                        "message_payload"
                    )["data"]
                )
                self.status_code = status_code
                self.response_data = response_data
        except Exception as ex:
            # trc = str(traceback.format_exception(ex))
            # print(trc)
            self.status_code = 666
            self.response_data = {}