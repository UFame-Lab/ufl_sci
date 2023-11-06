import asyncio
import traceback
import json
import time

from pprint import pprint

from typing import Awaitable, Optional

import websockets
import redis.asyncio as redis

from sci.lib.common_utils import (
    generate_variable_name, separate_recipient_address
)
from sci.sci_settings import DEBUG
from sci.lib.patterns import create_ecsaddo
from sci.lib.logging import save_log
from sci.lib.common_utils import json_safe, get_next_delay
from sci.network.utils import (
    create_response_payload, sendResponse, search_wsBridgeBroker
)
from sci.sci_exceptions import SendResponseError, DestinationError
from sci.app_controllers.base_controller import AUTH_SERVICE_ACTIONS
from sci.lib.common_utils import smart_print
from sci import sci_settings
from sci.sci_typing import ecsaddo



class ResponseSession:
    def __init__(self) -> None:
        self.SCI_ResponseSessions = {}


    async def create_and_start_session__pl(
        self, 
        EventMessage: dict
    ) -> ecsaddo:
        """"
        Meta
        ---
        Patterns:
            [__pl lvl 2]
            ecsaddo

        Arguments
        ---
        - `EventMessage: dict`

        Description
        ---
        Асинхронный метод `create_and_start_session__pl()` 
        отвечает за регистрацию новой сессии в `self.SCI_ResponseSessions` и 
        запуск `background` обработчика сессии 
        `ResponseSession.session_handler__()`.

        `EventMessage` отправляется в 
        `ResponseSessions.create_and_start_session__pl()` только если имеет 
        "mType": "request", запрашивает ожидания "resposne", текущий `sci_core`
        является отправителем `EventMessage`.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            queue = asyncio.Queue()
            unique_session_id: str = generate_variable_name(
                length=35, 
                prefix=sci_settings.SCI_SESSION_PREFIX
            )
            # recipient = EventMessage["address_section"]["recipient"]
            awaiting_response_queue_settings: dict = (
                EventMessage.get("response_settings").get(
                    "awaiting_response_queue_settings"
                )
            )
            await_timeout: int = (
                EventMessage.get("response_settings").get("await_timeout")
            )
            # Формируем данные сессии
            sci_session = {
                "queue": queue,
                "awaiting_response_queue_settings": (
                    awaiting_response_queue_settings
                ),
                "await_timeout": await_timeout,
            }
            self.SCI_ResponseSessions.setdefault(unique_session_id, sci_session)
            # Добавляем идентификатор сессии в 
            # `SCI_Message -> "meta" -> "session_id"`
            EventMessage["meta"].setdefault("session_id", unique_session_id)
            task = asyncio.create_task(
                self.session_handler__gw(sci_session, EventMessage)
            )
            # сохраняем ссылку на asyncio.Task в записи сесси
            # для того чтобы сборщик мусора не удалил ее раньше
            # времени.
            sci_session.setdefault("session_handler", task)
            def remove_session_after_done(
                *args, 
                **kwargs
            ) -> None:
                """
                Description
                ---
                callback удаления завершенной сессии
                из ResponseSession
                """
                try:
                    del self.SCI_ResponseSessions[unique_session_id]
                except Exception as ex:
                    pass
            # Регистрируем callback на удаление сессии из SCI_ResponseSessions
            # После того как задача обработки сессии завершит свою работу
            task.add_done_callback(remove_session_after_done)
            # Сессия добавлена в `self.SCI_ResponseSessions`
            # Идентификатор сессии добавлен в `SCI_Message -> "meta" -> "session_id"`
            # background задача обработки сессии запущена.
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "create_and_start_session__pl (ex)",
                "exception occurred in create_and_start_session__pl",
                location=True,
                traceback=trc
            )
            

    async def session_handler__gw(
        self,
        sci_session: dict,
        EventMessage: dict,
    ) -> None:
        """
        Meta
        ---
        Patterns:
            [__gw lvl 1]
            log-save
            ecsaddo
            
        Arguments
        ---
        - `sci_session: dict`
        - `EventMessage: dict`
        
        Description
        ---
        Асинхронный метод `session_handler__gw()` является 
        основным `__gw` методом обработки текущий сессии.

        Метод `session_handler__gw()` вызывает `session_handler__pl()`, и в 
        случае если `session_handler__pl()` возвращает отрицательный 
        `ecsaddo`, то `session_handler__gw()` логирует этот результат.
        
        Return
        ---
        None
        """
        try:
            EventMessage_safe: dict = json.loads(
                json.dumps(EventMessage, default=json_safe)
            )
            ecsaddo = await self.session_handler__pl(sci_session)
            if ecsaddo["status"] != "ok":
                ecsaddo["data"].setdefault("EventMessage", EventMessage_safe)
                ecsaddo["data"].setdefault("sci_session", sci_session)
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        "ResponseSession: обработка сессии "
                        "завершилась ошибкой \n"
                        f"{ecsaddo}\n"
                        "--------------------\n"
                    )
                save_log(self.sci_ref.logfilePath, ecsaddo)
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "session_handler__gw (ex)",
                "exception occurred in session_handler__gw",
                location=True,
                traceback=trc,
                EventMessage=EventMessage_safe,
                sci_session=sci_session
            )
            if DEBUG:
                pprint(
                    "--------------------\n"
                    "ResponseSession: обработка сессии "
                    "завершилась исключением \n"
                    f"{data}\n"
                    "--------------------\n"
                )
            save_log(self.sci_ref.logfilePath, data)


    async def session_handler__pl(
        self, 
        sci_session: dict
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 1]
            ecsaddo
            
        Arguments
        ---
        - `sci_session: dict`
            
        Description
        ----
        Асинхронный метод `session_handler__pl()` выполняет 
        основную логику работы (`background` `asyncio.Task`) обработки 
        выполнения текущей (своей) response сессии.
        Обработка сессии может завершится в двух случаях.
        - Обработчику удалось получить ответ.
        - Обработчику не удалось получить ответ.
        Обработка сессии завершилась по `timeout`

        После того как обработка сессии завершается, 
        `session_handler__pl()` вызывает `resolve_session()` 
        для отправки результат обработки сессии `summary_response_data` 
        в переменную ожидания ответ которую отслеживает `awaitable resposne`.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            queue: asyncio.Queue = sci_session.get("queue")
            response = None
            await_timeout: int = sci_session.get("await_timeout")
            async def collect_responses() -> (bool):
                while True:
                    EventMessage = await queue.get()
                    nonlocal response # warning
                    response = EventMessage
                    return True
            try:
                # Ожидаем выполнения `asyncio.Task` обработчика текущей сессии
                # Если обработчику сессии удалось получить ответ от
                # заяленного участника сесиии, то 
                # `asyncio.Task` - collect_responses завершится самостоятельно, 
                # и в качестве результата вернет True.
                # Если обработчику сессии не удается получить ответ от
                # заявленного участника сесии на протяжении await_timeout,
                # то возбуждается исключение asyncio.exceptions.TimeoutError
                await asyncio.wait_for(
                    asyncio.create_task(collect_responses()), await_timeout
                )
                # Обработчику сессии удалось получить ответ от заяленного
                # участника сесиии.
                # формируем ecsaddo ответ который будет отправлен в 
                # queue - `awaitable_response` - результат работы сессии
                ecsaddo_result_session: ecsaddo = (
                    create_ecsaddo("ok", response=response)
                )
            except asyncio.exceptions.TimeoutError as ex:
                # обработчику сессии не удается получить ответ от заявленного
                # участника сесии на протяжении await_timeout
                # формируем ecsaddo ответ который будет отправлен в 
                # queue - `awaitable resposne` - результат работы сессии
                ecsaddo_result_session = create_ecsaddo(
                    "error",
                    "session timeout error",
                    "session timeout error",
                    response=response
                )
            ecsaddo_resolve_session: dict = (
                await self.resolve_session(sci_session, ecsaddo_result_session)
            )
            return ecsaddo_resolve_session
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "session_handler__pl (ex)",
                "exception occurred in session_handler__pl",
                location=True,
                traceback=trc
            )
            

    async def resolve_session(
        self, 
        sci_session: dict,
        summary_response_data: dict,
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
           
        Arguments
        ---
        - `sci_session: dict`
        - `summary_response_data: dict`
            
        Description
        ----
        Асинхронный метод `resolve_session()` отправляет `summary_response_data`
        в `sci_session -> "awaiting_response_queue_settings"`
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex".
        """
        try:
            awaiting_response_queue_settings: dict = (
                sci_session.get(
                    "awaiting_response_queue_settings"
                )
            )
            queue: (asyncio.Queue | str) = (
                awaiting_response_queue_settings["queue"]
            )
            if awaiting_response_queue_settings["q_type"] == "aq":
                await queue.put(summary_response_data)
            elif (
                awaiting_response_queue_settings["q_type"] == 
                "redis_variable_name"
            ):
                # self.SCI_SETTINGS - атрибут SCI_core
                redis_conn: redis.Redis = self.SCI_SETTINGS.get(
                    "local_broker_connection_settings"
                ).get("redis").get("redis_conn")
                await redis_conn.rpush(queue, json.dumps(summary_response_data))
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "resolve_session (ex)",
                "exception occurred in resolve_session",
                location=True,
                traceback=trc
            )
        

    async def response_distribution(
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
        - `EventMessage: dict`
            
        Description
        -----
        Асинхронный метод `response_destribution()` 
        принимает `EventMessage` "mType": "response", 
        точкой назначения которого является текущий `sci node`.
        `response_destribution()` должен найти соответствующую 
        активную сессию в `self.SCI_ResponseSessions` по `session_id`, и 
        передать в ее `queue` данное `EventMessage` сообщение.

        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            sci_session: dict = self.SCI_ResponseSessions.get(
                EventMessage["meta"]["session_id"]
            )
            if not sci_session:
                # Если сессия не найдена
                return create_ecsaddo(
                    "error",
                    "session not found",
                    "session not found",
                )
            queue: asyncio.Queue = sci_session.get("queue")
            await queue.put(EventMessage)
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "response_distribution (ex)",
                "exception occurred in response_distribution",
                location=True,
                traceback=trc
            )


class PostManager: 
    def __init__(
        self, 
        EventMessage: dict, 
        sci_core_ref
    ):
        """
        Arguments
        ---
        - `EventMessage: dict`
        - `sci_core_ref` - ссылка на текущий экземпляр `sci_core`.
        """
        self.EventMessage = EventMessage
        self.sci_core_ref = sci_core_ref
        
        
    async def post_manager__gw(self):
        """
        Meta
        ---
        Patterns:
            async background
            [__gw lvl 1]
            log-save
            ecsaddo
            
        Description
        ---
        Асинхронный метод `post_manager__gw` для распределения `EventMessage`
        вызывает `post_manager__pl()`.
        Если `post_manager__pl()` возвращает отрицательный `ecsaddo`, то 
        `post_manager__gw` логирует его.
        """
        try:
            EventMessage_safe: dict = json.loads(
                json.dumps(self.EventMessage, default=json_safe)
            )
            ecsaddo: dict = await self.post_manager__pl()
            if ecsaddo["status"] != "ok":
                ecsaddo["data"].setdefault("EventMessage", EventMessage_safe)    
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        "PostManager: обработка EventMessage "
                        "завершилась ошибкой \n"
                        f"{ecsaddo}\n"
                        "--------------------\n"
                    )
                save_log(self.sci_core_ref.sci_ref.logfilePath, ecsaddo)
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "post_manager__gw (ex)",
                "exception occurred ind post_manager__gw",
                location=True,
                traceback=trc,
                EventMessage=EventMessage_safe
            )
            if DEBUG:
                pprint(
                    "--------------------\n"
                    "PostManager: обработка EventMessage "
                    "завершилась исключением \n"
                    f"{data}\n"
                    "--------------------\n"
                )
            save_log(self.sci_core_ref.sci_ref.logfilePath, data)
            
            
    async def post_manager__pl(self):
        """
        Meta
        ---
        Patterns:
            [__pl lvl 1]
            ecsaddo
            
        Description
        ---
        Асинхронный метод `post_manager__pl` является главным методом
        распределения и обработки `EventMessage`.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex".
        """
        try:
            self.isNodeSender: bool = self.сheckSenderNode(self.EventMessage)
            self.recipient_node_name, self.recipient_app_name = (
                separate_recipient_address(
                    self.EventMessage["address_section"]["recipient"]
                )
            )
            self.current_node_name: str = (
                self.sci_core_ref.SCI_SETTINGS["node_name"]
            )
            self.current_node_is_recipient: bool = (
                True 
                if self.current_node_name == self.recipient_node_name 
                else False
            )
            self.send_interface: str = (
                self.EventMessage["address_section"]["interface"]
            )
            self.mType: str = self.EventMessage["meta"]["mType"]
            self.client_node_mode: str = self.EventMessage["meta"]["sci_mode"]
            self.isAwaitingResponse: bool = (
                self.EventMessage["meta"].get("session_id", False) or 
                self.EventMessage.get(
                    "response_settings", dict()
                ).get("isAwaiting", False)
            )
            if (
                self.isNodeSender and 
                self.current_node_is_recipient and
                self.send_interface in ("local-rq", "remote-rq", "ws")
            ):
                ecsaddo_error = create_ecsaddo(
                    "error",
                    "recipient address error",
                    "The current node cannot be both a recipient and a sender",
                )
                if self.isNodeSender and self.isAwaitingResponse:
                    ecsaddo_resolve_awaitable_response: dict  = (
                        await self.resolve_awaitable_response(ecsaddo_error)
                    )
                    if ecsaddo_resolve_awaitable_response["status"] != "ok":
                        return ecsaddo_resolve_awaitable_response
                return ecsaddo_error
            if (
                self.current_node_is_recipient and 
                self.send_interface in ("local-rq", "remote-rq", "ws")
            ):
                self.sender_node_name, self.sender_app_name = (
                    separate_recipient_address(self.EventMessage["sender"])
                )
            if (
                self.current_node_is_recipient and
                self.mType == "request" and
                self.send_interface in ("local-rq", "remote-rq", "ws")
            ):
                # Если текущий узел является получателем, тогда мы сразу
                # проверяем авторизован ли `SCI` узел отправителя.
                # Исключение: `EventMessage -> "action"` - AUTH_SERVICE_ACTIONS
                # автоматически проходят проверку.
                ecsaddo_node_auth_check: dict = self.node_auth_check()
                if ecsaddo_node_auth_check["status"] != "ok":
                    return ecsaddo_node_auth_check
                
            if self.send_interface == "local-aq" and self.mType == "request":
                ecsaddo_destination_aq_check: dict = (
                    self.destination_aq_check()
                )
                if ecsaddo_destination_aq_check["status"] != "ok":
                    if self.isNodeSender and self.isAwaitingResponse:
                        ecsaddo_resolve_awaitable_response: dict  = (
                            await self.resolve_awaitable_response(
                                ecsaddo_destination_aq_check
                            )
                        )
                        if ecsaddo_resolve_awaitable_response["status"] != "ok":
                            return ecsaddo_resolve_awaitable_response
                    return ecsaddo_destination_aq_check
            elif  (
                self.send_interface in ("local-rq", "remote-rq") and
                self.mType == "request"
            ):
                ecsaddo_destination_rq_check: dict = (
                    self.destination_rq_check()
                )
                if ecsaddo_destination_rq_check["status"] != "ok":
                    if self.isNodeSender and self.isAwaitingResponse:
                        ecsaddo_resolve_awaitable_response: dict  = (
                            await self.resolve_awaitable_response(
                                ecsaddo_destination_rq_check
                            )
                        )
                        if ecsaddo_resolve_awaitable_response["status"] != "ok":
                            return ecsaddo_resolve_awaitable_response
                        return ecsaddo_destination_rq_check
                    elif (
                        self.current_node_is_recipient and 
                        self.isAwaitingResponse
                    ):
                        ecsaddo_send_simple_response: dict = (
                            await self.send_simple_response({}, 404)
                        )
                        if ecsaddo_send_simple_response["status"] != "ok":
                            return ecsaddo_send_simple_response
                    return ecsaddo_destination_rq_check
                    
            elif self.send_interface == "ws" and self.mType == "request":
                ecsaddo_destination_ws_check: dict = (
                    self.destination_ws_check()
                )
                if ecsaddo_destination_ws_check["status"] != "ok":
                    if self.isNodeSender and self.isAwaitingResponse:
                        ecsaddo_resolve_awaitable_response: dict  = (
                            await self.resolve_awaitable_response(
                                ecsaddo_destination_ws_check
                            )
                        )
                        if ecsaddo_resolve_awaitable_response["status"] != "ok":
                            return ecsaddo_resolve_awaitable_response
                        return ecsaddo_destination_ws_check
                    elif (
                        self.current_node_is_recipient and
                        self.isAwaitingResponse
                    ):
                        ecsaddo_send_simple_response: dict = (
                            await self.send_simple_response({}, 404)
                        )
                        if ecsaddo_send_simple_response["status"] != "ok":
                            return ecsaddo_send_simple_response
                        return ecsaddo_destination_ws_check
                    elif (
                        not self.isNodeSender and
                        not self.current_node_is_recipient and
                        self.EventMessage["meta"].get("foreigner")
                    ):
                        pass
                    return ecsaddo_destination_ws_check
            if (
                self.current_node_is_recipient and
                self.send_interface in ("local-rq", "remote-rq", "ws") and
                self.EventMessage["action"] not in AUTH_SERVICE_ACTIONS
            ):
                if self.send_interface == "local-rq":
                    node_type = "local_nodes"
                elif self.send_interface == "remote-rq":
                    node_type = "remote_nodes"
                elif self.send_interface == "ws":
                    node_type = "remote_ws_nodes"
                node_conf: dict = (
                    self.sci_core_ref.SCI_SETTINGS["nodes"][node_type].get(
                        self.sender_node_name
                    )
                )
                node_conf["time_last_activity"] = int(time.time())
            if (
                self.isNodeSender and 
                self.mType == "request" and 
                self.isAwaitingResponse
            ):
                # EventMessage запросил регистрацию в ResponseSession
                # Текуший SCI node является отправной точкой EventMessage
                # Поэтому регистрация ResponseSession происходит именно
                # относительно текушего SCI EventMessage
                ecsaddo_create_session: dict = (
                    await self.sci_core_ref.create_and_start_session__pl(
                        self.EventMessage
                    )
                )
                if ecsaddo_create_session["status"] != "ok":
                    # Не удалось создать и запустить сессию
                    return ecsaddo_create_session 
            if self.isNodeSender:
                # Если текущий `SCI` node явялется отправителем, это указывает
                # на то, что `EventMessage -> "sender"` имеет вид - "app_name"
                # Нужно привести его к виду "node_name:app_name"
                collect_name = [
                    self.sci_core_ref.SCI_SETTINGS["node_name"], 
                    ":", 
                    self.EventMessage["sender"]
                ]
                self.EventMessage["sender"] = ''.join(collect_name)
                
            # Маршрутизация
            if self.send_interface in ("local-aq", "local-rq", "remote-rq"):
                if (
                    self.current_node_is_recipient and
                    self.mType == "response"
                ):
                    # Если EventMessage имеет тип "response", и текущий
                    # SCI узел является получателем, то отправляем 
                    # EventMessage на распределение в SCI_ResponseSessions 
                    ecsaddo_response_distribution: dict = (
                        await self.sci_core_ref.response_distribution(
                            self.EventMessage
                        )
                    )
                    return ecsaddo_response_distribution
                else:
                    # Во всех остальных случаях:
                    # EventMessage - request, или response (но текущий
                    # узел не является получателем).
                    # Передаем EventMessage на непосредственную отправку
                    # указаному получателю.
                    ecsaddo_internalSender__pl = await self.internalSender__pl()
                    return ecsaddo_internalSender__pl
            elif self.send_interface == "ws":
                if (
                    self.current_node_is_recipient and
                    self.mType == "response"
                ):
                    # Если EventMessage имеет тип "response", и текущий
                    # SCI узел является получателем, то отправляем 
                    # EventMessage на распределение в SCI_ResponseSessions 
                    ecsaddo_response_distribution: dict = (
                        await self.sci_core_ref.response_distribution(
                            self.EventMessage
                        )
                    )
                    return ecsaddo_response_distribution
                else:
                    # Во всех остальных случаях:
                    # EventMessage - request, или response (но текущий
                    # узел не является получателем).
                    # Передаем EventMessage на непосредственную отправку
                    # указаному получателю.
                    ecsaddo_externalSender__pl = await self.externalSender__pl()
                    return ecsaddo_externalSender__pl
            raise ValueError("wrong EventMessage")
                        
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "post_manager__pl (ex)",
                "exception occurred in post_manager__pl",
                location=True,
                traceback=trc
            )
        
        
    async def resolve_awaitable_response(
        self,
        ecsaddo: dict
    ) -> ecsaddo:
        """
        Arguments
        ---
        - `ecsaddo` ответ который нужно отправить в переменную ожидания.
        
        Description
        ---
        Асинхронный метод `resolve_awaitable_response` вызывается когда:
        - `EventMessage` `"mType": "request"` не прошел проверки в `sci_core`
        отправителе. (сессия еще не была создана, но пользователь ожидает ответ)
        - `EventMessage` ожидает ответ.
          
        Асинхронный метод `resolve_awaitable_response` отправлет `ecsaddo`
        в переменную ожидания.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            awaiting_response_queue_settings: dict = (
                self.EventMessage["response_settings"].get(
                    "awaiting_response_queue_settings"
                )
            )
            if not awaiting_response_queue_settings:
                raise ValueError(
                    "EventMessage  'request' с ожиданием 'response' "
                    "когда приходит в sci_core узла отправителя, "
                    "должен иметь обязательный ключ: "
                    "`EventMessage -> 'response_settings' -> 'awaiting_response_queue_settings'`"
                )
            ecsaddo_result_session: dict = create_ecsaddo(
                "error",
                ecsaddo["action"],
                ecsaddo["data"]["description"],
                response=None
            )
            fake_sci_session = dict.fromkeys(
                ("awaiting_response_queue_settings",), 
                awaiting_response_queue_settings
            )
            ecsaddo_resolve_fake_session: dict = (
                await self.sci_core_ref.resolve_session(
                    sci_session=fake_sci_session, 
                    summary_response_data=ecsaddo_result_session
                )
            )
            if ecsaddo_resolve_fake_session['status'] != "ok":
                # Не удалось отправить ответ в response promise (log)
                return ecsaddo_resolve_fake_session
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "resolve_awaitable_response (ex)",
                "exception occured in resolve_awaitable_response",
                location=True,
                traceback=trc,
            )
            
            
    async def send_simple_response(
        self, 
        response_data: dict,
        status_code: int
    ) -> ecsaddo:
        """
        Arguments
        ---
        - `response_data: dict` Данные которые будут вставлены в качестве
        значения `EventMessage -> "message_payload" -> data`.
        
        - `status_code: int` Данные которые будут вставлены в качестве
        значения `EventMessage -> "message_payload" -> "meta" -> "status_code"`.
        
        Description
        ---
        Асинхронный метод `send_simple_response` конфигурирует 
        `EventMessage` `"mType": "response"` на основе `response_data`, 
        `status_code` и отправляет относительно текущего `EventMessage`
        `"mType": "request"`.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            if self.EventMessage["action"] not in AUTH_SERVICE_ACTIONS:
                response_payload: dict = (
                    create_response_payload(
                        response_data, status_code
                    ).response_payload
                )
                ecsaddo_sendResponse: dict = (
                    await sendResponse(
                        self.EventMessage,
                        response_payload,
                        "postManager",
                        self.sci_core_ref.sci_ref.sci_cli
                    )
                )
                if ecsaddo_sendResponse["status"] != "ok":
                    raise SendResponseError(ecsaddo_sendResponse)
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "send_simple_response (ex)",
                "exception occurred in send_simple_response",
                location=True,
                traceback=trc
            )
        
            
    def сheckSenderNode(
        self, 
        EventMessage: dict
    ) -> bool:
        """
        Meta
        ---
        Patterns:
            pass
           
        Arguments
        ---
        - `EventMessage: dict`
            
        Description
        ---
        Метод `сheckSenderNode` проверяет, является ли текущий `sci node`
        отправителем `EventMessage`.
        
        Если в `EventMessage -> "sender"` заполнено не полностью, значит 
        текущий `sci node` является отправителем.
        
        Если в `EventMessage -> "sender"` заполнено полностью, значит текущий
        `sci node` является получателем.
        
        Return
        ---
        True - текущий узел отправитель.
        False - текущий узел не отправитель.
        """
        result = EventMessage["sender"].find(":")
        if result == -1:
            return True
        return False
        
            
    def destination_aq_check(self)  -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Description
        ---
        Метод `destination_aq_check` вызывается если `EventMessage` отправляется
        или было получено по интерфейсу `"local-aq"`
    
        Return
        ---
        ecsaddo "ok" / "error" / "ex"
        """
        try:
            if self.client_node_mode in  ("standart", "only_local"):
                # `EventMessage` отправляетс от `SCI` node "standart" / "only_local" и 
                # текущий `SCI` node является отправителем, тогда все необходимые
                # проверки уже были осуществленны в `sci_cli.destination_check()`
                return create_ecsaddo("ok")
            elif self.client_node_mode == "shadow":
                if not self.current_node_is_recipient or not self.isNodeSender:
                    raise DestinationError("wrong recipient value")
                if (
                    self.recipient_app_name in 
                    self.sci_core_ref.SCI_SETTINGS["app_controllers"]
                ):
                    return create_ecsaddo("ok")
            raise DestinationError("recipient not found")
        except DestinationError as ex:
            return create_ecsaddo(
                "error",
                "recipient not found",
                "recipient not found"
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "recipient not found",
                "exception occured in destination_aq_check",
                location=True,
                traceback=trc
            )
    
    
    def destination_rq_check(self) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Description
        ---
        Метод `destination_rq_check` вызывается если `EventMessage` отправляется
        или было получено по интерфейсу `"local-rq"` / `"remote-rq"`
            
        Return
        ---
        ecsaddo "ok" / "error" / "ex"
        """
        try:
            action = self.EventMessage["action"]
            if self.isNodeSender and self.current_node_is_recipient:
                raise DestinationError("wrong recipient value") 
            if self.client_node_mode in ("standart") and self.isNodeSender:
                # `EventMessage` отправляетс от `sci node` "standart" и 
                # текущий `sci node` является отправителем, тогда все необходимые
                # проверки уже были осуществленны в `sci_cli.destination_check()`
                return create_ecsaddo("ok")
            elif self.client_node_mode == "shadow" and self.isNodeSender:
                # `EventMessage` отправляется от `sci node` "shadow" и 
                # текущий `sci node` является отправителем, тогда мы должны
                # осуществить все необходимые `destination` проверки, так как
                # они не были осуществленны в `sci_cli`
                if (
                    self.send_interface == 'local-rq' and
                    action in AUTH_SERVICE_ACTIONS or
                    self.recipient_node_name in 
                    self.sci_core_ref.SCI_SETTINGS["nodes"]["local_nodes"]
                ):
                    return create_ecsaddo("ok")
                elif (
                    self.send_interface == "remote-rq" and
                    action in AUTH_SERVICE_ACTIONS or
                    self.recipient_node_name in
                    self.sci_core_ref.SCI_SETTINGS["nodes"]["remote_nodes"]
                ):
                    return create_ecsaddo("ok")
                
            if self.current_node_is_recipient:
                # Текущий `sci node` является получателем.
                if (
                    self.recipient_app_name in 
                    self.sci_core_ref.SCI_SETTINGS["app_controllers"]
                ):
                    return create_ecsaddo("ok")
            raise DestinationError("recipient not found")
        except DestinationError as ex:
            return create_ecsaddo(
                "error",
                "recipient not found",
                "recipient not found"
            )
        except Exception as ex:
            trc = traceback.format_exception(ex)
            return create_ecsaddo(
                "ex",
                "recipient not found",
                "exception occured in destination_rq_check",
                location=True,
                traceback=trc
            )
        
            
    def destination_ws_check(self) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Description
        ---
        Метод `destination_ws_check` вызывается если `EventMessage` отправляется
        или было получено по интерфейсу "ws"
            
        Return
        ---
        ecsaddo "ok" / "error" / "ex"
        """
        try:
            wsBridge_name: str = (
                self.EventMessage["address_section"].get("wsbridge")
            )
            if self.isNodeSender and self.current_node_is_recipient:
                raise DestinationError("wrong recipient value") 
            if self.client_node_mode in ("standart") and self.isNodeSender:
                # `EventMessage` отправляетс от `sci node` "standart" и 
                # текущий `sci node` является отправителем, тогда все необходимые
                # проверки уже были осуществленны в `sci_cli.destination_check()`
                return create_ecsaddo("ok")
            elif self.client_node_mode == "shadow" and self.isNodeSender:
                # `EventMessage` отправляется от `sci node` "shadow" и 
                # текущий `sci node` является отправителем, тогда мы должны
                # осуществить все необходимые `destination` проверки, так как
                # они не были осуществленны в `sci_cli`
                if (
                    self.recipient_node_name in 
                    self.sci_core_ref.SCI_SETTINGS["nodes"]["local_nodes"] or 
                    self.recipient_node_name in 
                    self.sci_core_ref.SCI_SETTINGS["nodes"]["remote_nodes"]
                ):
                    # Если `EventMessage` отправляется от текущего `sci node`,
                    # то `recipient node` не должен быть в пределах досягаемости
                    # относительно текущего `sci node`, так как иначе теряется
                    # смысл и необходимость использовать ws интерфейс. 
                    raise DestinationError("wrong recipient value")
                # Проверям есть ли относительно текущего `sci node`, узел
                # являющийся брокером заявленного `wsBridge`
                wsBridgeBroker_settings: tuple[str, dict] = (
                    search_wsBridgeBroker(
                        SCI_SETTINGS=self.sci_core_ref.SCI_SETTINGS,
                        wsBridge_name=wsBridge_name
                    )
                )
                if wsBridgeBroker_settings:
                    self.wsBridgeBroker_settings = wsBridgeBroker_settings
                    return create_ecsaddo("ok")
            elif self.current_node_is_recipient:
                # Текущий `sci node` является получателем.
                if (
                    self.recipient_app_name in 
                    self.sci_core_ref.SCI_SETTINGS["app_controllers"]
                ):
                    return create_ecsaddo("ok")
            elif not self.isNodeSender and not self.current_node_is_recipient:
                return create_ecsaddo("ok")
            raise DestinationError("recipient not found")
        except DestinationError as ex:
            return create_ecsaddo(
                "error",
                "recipient not found",
                "recipient not found"
            )
        except Exception as ex:
            trc = traceback.format_exception(ex)
            return create_ecsaddo(
                "ex",
                "recipient not found",
                "exception occured in destination_ws_check",
                location=True,
                traceback=trc
            )


    def node_auth_check(self) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo

        Description
        ---
        Метод node_auth_check вызывается только если текущий sci node` является
        узлом получателем.
        Метод node_auth_check отвечает за проверку:
        Является ли `sci node` отправителя авторизированным в текущем узле.
        Если узел отправителя авторизирован, то он должен находится в:
        `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / "remote_ws_nodes"`
        
        NOTE: Если `EventMessage -> "action"` in AUTH_SERVICE_ACTIONS, то
        проверка автоматически считается пройденной.
        
        Return
        ---
        ecsaddo "ok" / "error" / "ex"
        """
        try:
            action = self.EventMessage["action"]
            # Если текущий SCI node является получателем,
            # И EventMessage имеет интерфейс "local-rq", "remote-rq"
            # То поле "sender" должно быть полностью заполнено "node_name:app_name"
            # Так как текущий SCI node не может быть одновременно
            # получателем и отправителем при интерейсе 
            # "local-rq", "remote-rq", "ws"    
            # Если текущий SCI node является получателем EventMessage
            # То потенциальный ответ будет отправлен относительно
            # EventMessage["sender"] и по зеркальному "interface".
            if (
                self.send_interface == "local-rq" and
                action in AUTH_SERVICE_ACTIONS or
                self.sender_node_name in 
                self.sci_core_ref.SCI_SETTINGS["nodes"]["local_nodes"]
            ):
                return create_ecsaddo("ok")
            elif (
                self.send_interface == "remote-rq" and
                action in AUTH_SERVICE_ACTIONS or
                self.sender_node_name in 
                self.sci_core_ref.SCI_SETTINGS["nodes"]["remote_nodes"]
            ):
                return create_ecsaddo("ok")
            elif (
                self.send_interface == "ws" and
                action in AUTH_SERVICE_ACTIONS or
                self.sender_node_name in 
                self.sci_core_ref.SCI_SETTINGS["nodes"]["remote_ws_nodes"]
            ):
                return create_ecsaddo("ok")
            return create_ecsaddo(
                "error",
                "authorized error"
                "sender SCI node is not authorized"
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "node_auth_check (ex)",
                "exception occured in node_auth_check",
                location=True,
                traceback=trc
            )
            
    
    async def externalSender__pl(self) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 2]
            ecsaddo
            
        Description
        ---
        Асинхронный метод `externalSender__pl` занимается непосредственной
        отправкой сообщений по интерфейсу: "local-aq", "local-rq", "remote-rq".
        
        Return
        ---
        `ecsaddo` "ok" / "error" / "ex"
        """
        try:
            wsBridge_name: Optional[str] = (
                self.EventMessage["address_section"].get("wsbridge")
            )
            SCI_SETTINGS: dict = self.sci_core_ref.SCI_SETTINGS
            if self.isNodeSender:
                ecsaddo_cleaning_before_sending: dict = (
                    self.cleaning_before_sending()
                )
                if ecsaddo_cleaning_before_sending["status"] != "ok":
                    return ecsaddo_cleaning_before_sending
            if self.current_node_is_recipient:
                # Доверяем self.destination_ws_check()
                app_controller: asyncio.Queue = (
                    SCI_SETTINGS["app_controllers"].get(self.recipient_app_name)
                )
                if app_controller:
                    await app_controller.put(self.EventMessage)
                    return create_ecsaddo("ok")
            elif self.isNodeSender:
                # Устанавливается в self.destination_ws_check если 
                # self.client_node_mode "shadow"
                wsBridgeBroker_settings: tuple[str, dict] = (
                    getattr(self, "wsBridgeBroker_settings", False)
                )
                # destination_ws_check проверялся в `sci_cli` поэтому
                # self.wsBridgeBroker_settings нет.
                if not wsBridgeBroker_settings:
                    self.wsBridgeBroker_settings: tuple[str, dict] = (
                        search_wsBridgeBroker(SCI_SETTINGS, wsBridge_name)
                    )
                if self.wsBridgeBroker_settings[0] == "node":
                    # Текущий `SCI` node является `wsBridgeBroker`
                    # Отправка `EventMessage` в `wsBridge` server
                    wsBridgeBroker_aq: asyncio.Queue = (
                        self.wsBridgeBroker_settings[1]["wsBridgeBroker_aq"]
                    )
                    eventData = create_ecsaddo(
                        "ok",
                        "send-EM",
                        EventMessage=self.EventMessage
                    )
                    await wsBridgeBroker_aq.put(eventData)
                    return create_ecsaddo("ok")
                elif self.wsBridgeBroker_settings[0] == "local_node":
                    # Отправка `EventMessage` в `SCI` node который является
                    # `wsBridgeBroker`
                    local_node: dict = self.wsBridgeBroker_settings[1]
                    node_rq_name: str = local_node.get("node_rq")
                    redis_conn: redis.Redis = (
                        SCI_SETTINGS["local_broker_connection_settings"].get(
                            "redis"
                        ).get("redis_conn")
                    )
                    EventMessage_json: str = json.dumps(self.EventMessage)
                    await redis_conn.rpush(
                        node_rq_name,
                        EventMessage_json
                    )
                    return create_ecsaddo("ok")
                elif self.wsBridgeBroker_settings[0] == "remote_node":
                    # Отправка `EventMessage` в `SCI` node который является
                    # `wsBridgeBroker`
                    remote_node: dict = self.wsBridgeBroker_settings[1]
                    node_rq_name: str = remote_node.get("node_rq")
                    redis_conn = redis.Redis(
                        **remote_node["broker_connection_settings"]["redis"]
                    )
                    EventMessage_json: str = json.dumps(self.EventMessage)
                    await redis_conn.rpush(
                        node_rq_name,
                        EventMessage_json
                    )
                    await redis_conn.close()
                    return create_ecsaddo("ok")
            elif not self.isNodeSender and not self.current_node_is_recipient:
                # Текущий `SCI` node, не получатель и не отправитель.
                # Текущий `SCI` node является `wsBridgeBroker`
                self.foreigner =  (
                    self.EventMessage["meta"].get("foreigner", False)
                )
                if self.foreigner:
                    # `EventMessage` пришел от `wsBridge`, текущий `SCI` node
                    # Должен отправить его в `SCI` node назначения.
                    # Так как `EventMessage` прошел проверку 
                    # `self.destination_ws_check`, это означачает что `SCI` node
                    # назначения находится в области видимости текущего `SCI` node
                    if (
                        self.recipient_node_name in 
                        self.sci_core_ref.SCI_SETTINGS["nodes"]["local_nodes"]
                    ):
                        self.ws_recipient_node: tuple[str, dict] = (
                            "local_node",
                            self.sci_core_ref.SCI_SETTINGS["nodes"].get(
                                "local_nodes"
                            ).get(self.recipient_node_name)
                        )
                    elif (
                        self.recipient_node_name in
                        self.sci_core_ref.SCI_SETTINGS["nodes"]["remote_nodes"]
                    ):
                        self.ws_recipient_node: tuple[str, dict] = (
                            "remote_node",
                            self.sci_core_ref.SCI_SETTINGS["nodes"].get(
                                "remote_nodes"
                            ).get(self.recipient_node_name)
                        )
                    if not getattr(self, "ws_recipient_node", False):
                        return create_ecsaddo(
                            "error",
                            "foreigner error",
                            "current foreigner node does not know about the recipient node"
                        )
                    if self.ws_recipient_node[0] == "local_node":
                        local_node: dict = self.ws_recipient_node[1]
                        node_rq_name: str = local_node.get("node_rq")
                        redis_conn: redis.Redis = (
                            SCI_SETTINGS["local_broker_connection_settings"].get(
                                "redis"
                            ).get("redis_conn")
                        )
                        EventMessage_json: str = json.dumps(self.EventMessage)
                        await redis_conn.rpush(
                            node_rq_name,
                            EventMessage_json
                        )
                        return create_ecsaddo("ok")
                    elif self.ws_recipient_node[0] == "remote_node":
                        remote_node: dict = self.ws_recipient_node[1]
                        node_rq_name: str = remote_node.get("node_rq")
                        redis_conn = redis.Redis(
                            **remote_node["broker_connection_settings"]["redis"]
                        )
                        EventMessage_json: str = json.dumps(self.EventMessage)
                        await redis_conn.rpush(
                            node_rq_name,
                            EventMessage_json
                        )
                        await redis_conn.close()
                        return create_ecsaddo("ok")
                else:
                    # Текущий `SCI` node является `wsBridgeBroker` и должен
                    # передать `EventMessage` в `wsBridge`.
                    # пройденая проверка `self.destination_ws_check` означает
                    # что текущий узел действительно явялется `wsBridgeBroker`
                    # заявленного `wsBridge`
                    wsBridgeBroker_settings: dict = (
                        SCI_SETTINGS["websocket_connections"].get(wsBridge_name)
                    )
                    wsBridgeBroker_aq: asyncio.Queue = (
                        wsBridgeBroker_settings["wsBridgeBroker_aq"]
                    )
                    eventData = create_ecsaddo(
                        "ok",
                        "send-EM",
                        EventMessage=self.EventMessage
                    )
                    await wsBridgeBroker_aq.put(eventData)
                    return create_ecsaddo("ok")       
            return create_ecsaddo(
                "error",
                "recipient not found",
                "recipient not found (in externalSender__pl",
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "externalSender__pl (ex)",
                ("exception occurred during send_message "
                "in externalSender__pl"),
                location=True,
                traceback=trc
            )
            
            
    async def internalSender__pl(self):
        """
        Meta
        ---
        Doc:
            pass
        Patterns:
            [__pl lvl 2]
            ecsaddo
            
        Description
        ---
        Асинхронный метод `internalSender__pl` занимается непосредственной
        отправкой сообщений по интерфейсу: "ws".
        
        Return
        ---
        `ecsaddo` "ok" / "error" / "ex"
        ---
        pass
        """
        try:
            SCI_SETTINGS: dict = self.sci_core_ref.SCI_SETTINGS
            action = self.EventMessage["action"]
            if self.isNodeSender:
                ecsaddo_cleaning_before_sending: dict = (
                    self.cleaning_before_sending()
                )
                if ecsaddo_cleaning_before_sending["status"] != "ok":
                    return ecsaddo_cleaning_before_sending
            if self.current_node_is_recipient:
                # "local-aq", "local-rq", "remote-rq"
                app_controller: asyncio.Queue = (
                    SCI_SETTINGS["app_controllers"].get(self.recipient_app_name)
                )
                if app_controller:
                    await app_controller.put(self.EventMessage)
                    return create_ecsaddo("ok")
            elif self.isNodeSender and self.send_interface == "local-rq":
                # Проверка destination осуществлялась еще в `sci_core` и `sci_cli`
                if action in AUTH_SERVICE_ACTIONS and self.mType == "request":
                    local_node: dict = (
                        self.EventMessage["meta"]["to_node_addr"]["node_conf"]
                    )
                else:
                    
                    local_node: dict = SCI_SETTINGS["nodes"]["local_nodes"].get(
                        self.recipient_node_name
                    )
                node_rq_name: str = local_node.get("node_rq")
                redis_conn: redis.Redis = (
                    SCI_SETTINGS["local_broker_connection_settings"].get(
                        "redis"
                    ).get("redis_conn")
                )
                EventMessage_json: str = json.dumps(self.EventMessage)
                await redis_conn.rpush(
                    node_rq_name,
                    EventMessage_json
                )
                return create_ecsaddo("ok")
            elif self.isNodeSender and self.send_interface == "remote-rq":
                if action in AUTH_SERVICE_ACTIONS and self.mType == "request":
                    remote_node: dict = (
                        self.EventMessage["meta"]["to_node_addr"]["node_conf"]
                    )
                else:
                    remote_node: dict = SCI_SETTINGS["nodes"]["remote_nodes"].get(
                        self.recipient_node_name
                    )
                node_rq_name = remote_node.get("node_rq")
                redis_conn = redis.Redis(
                    **remote_node["broker_connection_settings"]["redis"]
                )
                EventMessage_json: str = json.dumps(self.EventMessage)
                await redis_conn.rpush(
                    node_rq_name,
                    EventMessage_json
                )
                await redis_conn.close()
                return create_ecsaddo("ok")
            return create_ecsaddo(
                "error",
                "recipient not found",
                "recipient not found (in internalSender__pl",
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "internalSender__pl (ex)",
                ("exception occurred during send_message "
                "in internalSender__pl"),
                location=True,
                traceback=trc
            )
            
            
    def cleaning_before_sending(self) -> ecsaddo:
        """
        Meta
        ----
        Patterns:
            ecsaddo
            
        Description
        ---
        Метод `cleaning_before_sending()` отвечает за очистку 
        `EventMessage` от лишних полей перед отправкой получателю.
        
        Например если `EventMessage` `"mType": "request"`, и имеет ключ
        `EventMessage -> "meta" -> "session_id"` то из `EventMessage`
        должен быть удален весь `EventMessage -> "resposne_settings"`
        так как он может хранить не сериализуемые `python` объекты, и в `sci_core`
        получателе не нужен.

        Return
        ---
        `ecsaddo` "ok" / "error" / "ex"
        """
        try:
            if self.mType == "response":
                pass
            elif self.mType == "request":
                if self.EventMessage["meta"].get("session_id"):
                    del self.EventMessage["response_settings"]
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "cleaning_before_sending (ex)",
                "exception occurred in cleaning_before_sending",
                location=True,
                traceback=trc
            )
            
            
class SCI_core(ResponseSession):
    def __init__(
        self, 
        SCI_SETTINGS: dict, 
        sci_mode: str, 
        sci_ref,
    ):
        """
        Arguments
        ---
        - `SCI_SETTINGS: dict` Настройки текущего `sci node`
        
        - `sci_mode: str` В каком режиме запущен текущий `sci node`
        ("standart", "only_local", "shadow")
        
        - `sci_ref` - ссылка на экземпляр текущего `sci`
        """
        super().__init__() # self.SCI_ResponseSessions = {}
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = sci_mode
        self.sci_ref = sci_ref
        self.is_working = False


    def __call__(self) -> Awaitable:
        """
        Return
        ---
        `awaitable` `sci_core`
        """
        return self.sci_controller__gw__pl()

    
    async def sci_controller__gw__pl(self) -> None:
        """
        Meta
        ---
        Patterns:
            [__gw__pl lvl 1]
            infinity-loop
            log-save
            ecsaddo
            
        Description
        ---
        `sci_core`
        
        Return
        ---
        None
        """
        # получает awaitable точки которые нужно прослушивать
        main_receiver = asyncio.Queue()
        event_wait_list: list[asyncio.Event] = []
        self.listen_node_aq_readyEvent = asyncio.Event()
        event_wait_list.append(self.listen_node_aq_readyEvent)
        if self.sci_mode == "standart":
            self.listen_node_rq_readyEvent = asyncio.Event()
            event_wait_list.append(self.listen_node_rq_readyEvent)
        node_queue: list[Awaitable] = (
            self.collecting_receiver_message_points(main_receiver)
        )
        # background прослушивания входных точек
        background_tasks_listening_node_queue = [
            asyncio.create_task(task) for task in node_queue
        ]
        # background задачи обработки EventMessage
        message_delivery_background_task = set()
        # регистрация awaitableAppControllers в background
        background_app_controllers = [
            asyncio.create_task(task) 
            for task in 
            self.sci_ref.awaitableAppControllers
        ]
        await asyncio.wait(
            [
                asyncio.create_task(event.wait()) for event in event_wait_list
            ],
            return_when=asyncio.ALL_COMPLETED
        )
        self.is_working = True
        while True:
            try:
                EventMessage = await main_receiver.get()
                # Для обратной совместимости
                main_receiver.task_done()
                # Создаем background задачу обработки сообщения 
                delivery_task = asyncio.create_task(
                    PostManager(
                        EventMessage=EventMessage, 
                        sci_core_ref=self
                    ).post_manager__gw()
                )
                # Добавляем background задачу обработки сообщения в множество
                # message_delivery_background_task Для того что-бы сборщик 
                # мусора не удалил ссылку на нее раньше времени.
                message_delivery_background_task.add(delivery_task)
                # Добавляем в задачу callback на удаление себя из
                # множества message_delivery_background_task, сразу как толкьо 
                # задача завершится
                delivery_task.add_done_callback(
                    message_delivery_background_task.discard
                )
            except Exception as ex:
                trc = str(traceback.format_exception(ex))
                data = create_ecsaddo(
                    "ex",
                    "sci_controller__gw__pl (ex)",
                    "exception occurred in sci_controller__gw__pl",
                    location=True,
                    traceback=trc
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        "SCI_core: произошло исключение при получении "
                        "сообщения из 'main_receiver` или при регистрации "
                        "background задачи обработки сообщения в PostManager\n"
                        f"{data}\n"
                        "--------------------\n"
                    )
                save_log(self.sci_ref.logfilePath, data)
                continue
                
        
    async def wsBridgeBroker(
        self, 
        main_receiver: asyncio.Queue, 
        wsBridgeBroker_settings: dict,
        wsBridgeBroker_name: str,
    ) -> None:
        """
        Meta
        ---
        Patterns:
            infinity-loop
            log-save
            ecsaddo
            asyncio background
            
        Arguments
        ---
        - `main_receiver: asyncio.Queue` - `asyncio.Queue` который прослушивает
        `sci_core` для принятия сообщений.
        
        - `wsBridgeBroker_settings: dict` - настройки текущего `wsBridgeBroker`
        
        - `wsBridgeBroker_name: str` - имя текущего `wsBridgeBroker`
        
        Return
        ---
        None
        """
        delay_try_connection = 0 # 2-4-8-16-32-64-128-(256 max)
        transfer_background_task = []
        url: str = wsBridgeBroker_settings["url"]
        headers: dict = wsBridgeBroker_settings["headers"]
        wsBridgeBroker_aq: asyncio.Queue = (
            wsBridgeBroker_settings["wsBridgeBroker_aq"]
        )
        while True:
            try:
                async with websockets.connect(
                    url, extra_headers=headers
                ) as ws_client:
                    transfer_task = asyncio.create_task(
                        self.transfer_current_node_chain(
                            wsBridgeBroker_settings
                        )
                    )
                    transfer_background_task.append(transfer_task)
                    wsBridgeBroker_settings["status"] = True
                    tasks = {
                        # Получение сообщений от `wsBridge`
                        asyncio.create_task(
                            ws_client.recv(), 
                            name="ws_client_recv"
                        ),
                        # отправка сообщений в `wsBridge`
                        asyncio.create_task(
                            wsBridgeBroker_aq.get(),
                            name="wsBridgeBroker_aq_recv"
                        )
                    }
                    while True:
                        whenFirstComplete = asyncio.wait(
                            tasks, 
                            return_when=asyncio.FIRST_COMPLETED
                        )
                        done, pending = await whenFirstComplete
                        for task in done:
                            tasks.discard(task)
                            result = await task
                            if task.get_name() == "wsBridgeBroker_aq_recv":
                                await ws_client.send(
                                    json.dumps(result)
                                )
                                tasks.add(
                                    asyncio.create_task(
                                        wsBridgeBroker_aq.get(),
                                        name="wsBridgeBroker_aq_recv"
                                    )
                                )
                            elif task.get_name() == "ws_client_recv":
                                await main_receiver.put(
                                    json.loads(result)
                                )
                                tasks.add(
                                    asyncio.create_task(
                                        ws_client.recv(),
                                        name="ws_client_recv"
                                    )
                                )
            except Exception as ex:
                wsBridgeBroker_settings["status"] = False
                trc = str(traceback.format_exception(ex))
                [task.cancel() for task in transfer_background_task] # warning
                transfer_background_task.clear()
                data = create_ecsaddo(
                    "ex",
                    "wsBridgeBroker (ex)",
                    "exception occured in wsBridgeBroker",
                    location=True,
                    traceback=trc
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        f"SCI_core: исключение в wsBridgerBroker: "
                        f"{wsBridgeBroker_name}\n"
                        f"{wsBridgeBroker_settings} \n"
                        f"{data}\n"
                        "--------------------\n"
                    )
                save_log(self.sci_ref.logfilePath, data)
                delay_try_connection = get_next_delay(
                    delay_try_connection, 2, 256
                )
                await asyncio.sleep(delay_try_connection)
                

    async def listen_node_rq(
        self,
        main_receiver: asyncio.Queue
    ) -> None:
        """
        Meta
        ---
        Patterns:
            infinity-loop
            log-save
            ecsaddo
            asyncio background
            
        Arguments
        ---
        - `main_receiver: asyncio.Queue` - `asyncio.Queue` который прослушивает
        `sci_core` для принятия сообщений.
        
        Description
        ---
        Асинхронный метод `listen_node_rq` прослушивает 
        `SCI_SETTINGS -> "node_rq"`.
        Когда получает `EventMessage`, передает его в `main_receiver`
        
        Return
        ---
        None
        """
        redis_conn: redis.Redis = (
            self.SCI_SETTINGS.get("local_broker_connection_settings").get(
                "redis"
            ).get("redis_conn")
        )
        node_rq: str = self.SCI_SETTINGS.get("node_rq")
        startup_flag = True
        while True:
            try:
                if startup_flag:
                    # только 1 раз
                    await redis_conn.delete(node_rq)
                    startup_flag = False
                    self.listen_node_rq_readyEvent.set()
                # (b'l_three', b'lol')
                message_b = await redis_conn.blpop(node_rq)
                message_str = message_b[-1].decode()
                try:
                    message = json.loads(message_str)
                except Exception:
                    # Пропускаем сообщение если его не удается перевести
                    # из JSON like-str в dict
                    continue
                await main_receiver.put(message)
            # except redis.ConnectionError as ex:
            #     break
            except Exception as ex:
                trc = str(traceback.format_exception(ex))
                data = create_ecsaddo(
                    "ex",
                    "apoMdRywWoGaBnM",
                    "exception occurred in listen_node_rq",
                    location=True,
                    traceback=trc
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        "SCI_core: произошло исключение при получении "
                        "сообщения из 'listen_node_rq` и передаче его в "
                        "`main_receiver`\n"
                        f"{data}\n"
                        "--------------------\n"
                    )
                save_log(self.sci_ref.logfilePath, data)
                await asyncio.sleep(3)
    

    async def listen_node_aq(
        self,
        main_receiver: asyncio.Queue
    ):
        """
        Meta
        ---
        Doc:
            obsidian://open?vault=ufl_SCI_0.1&file=Dev%2Fcode_doc%2Fdata%2FSCI_core.get_local_message_point()
        Patterns:
            infinity-loop
            log-save
            ecsaddo
            asyncio background
            
        Arguments
        ---
        - `main_receiver: asyncio.Queue` - `asyncio.Queue` который прослушивает
        `sci_core` для принятия сообщений.
        
        Description
        ---
        Асинхронный метод `listen_node_aq` прослушивает 
        `SCI_SETTINGS -> "node_aq"`.
        Когда получает `EventMessage`, передает его в `main_receiver`
        
        Return
        ---
        None
        """
        try:
            node_aq: asyncio.Queue = self.SCI_SETTINGS.get("node_aq")
            self.listen_node_aq_readyEvent.set()
            while True:
                message = await node_aq.get()
                if not isinstance(message, dict):
                    # не dict сообщения пропускаются
                    continue
                await main_receiver.put(message)
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "gDOPIBYpYvHQqtWzLAzT",
                "exception occurred in listen_node_aq",
                location=True,
                traceback=trc
            )
            if DEBUG:
                pprint(
                    "--------------------\n"
                    "SCI_core: произошло исключение при получении "
                    "сообщения из 'listen_node_aq` и передаче его в "
                    "`main_receiver`\n"
                    f"{data}\n"
                    "--------------------\n"
                )
            save_log(self.sci_ref.logfilePath, data)


    def collecting_receiver_message_points(
        self,
        main_receiver: asyncio.Queue
    )-> list[Awaitable]:
        """
        Arguments
        ---
       - `main_receiver: asyncio.Queue` - `asyncio.Queue` который прослушивает
        `sci_core` для принятия сообщений.
        
        Description
        ---
        Метод `collecting_receiver_message_points` в зависимости от того
        в каком режиме запущен `sci node`, собирает `awaitable` точки принятия
        сообщений.
        
        Если `sci node` запущен как `standart`, то будут использоваться:
        - `self.listen_node_aq(main_receiver)`
        - `self.listen_node_rq(main_receiver)`
        - Плюс все зарегистрированные в `SCI_SETTINGS -> "websocket_connections"` 
        `self.wsBridgeBroker(main_receiver)`
        
        Если `sci node` запущен как `only_local`, то будут использоваться:
        - `self.listen_node_aq(main_receiver)`
        
        Если `sci node` запущен как `shadow`, то `sci_core` не запускается.
        
        Return
        ---
        ```python
        [
            <awaitable_self.listen_node_aq(main_receiver)>,
            <awaitable_self.self.listen_node_rq(main_receiver)>,
            <awaitable_self.self.wsBridgeBroker(main_receiver)>
        ]
        ```
        """
        message_points = []
        if self.sci_mode == "only_local":
            message_points.append(self.listen_node_aq(main_receiver))
        elif self.sci_mode == "standart":
            message_points.append(self.listen_node_aq(main_receiver))
            message_points.append(self.listen_node_rq(main_receiver))
            for wsBridgeBroker_name in (
                self.SCI_SETTINGS["websocket_connections"]
            ):
                message_points.append(
                    self.wsBridgeBroker(
                        main_receiver, 
                        self.SCI_SETTINGS["websocket_connections"].get(
                            wsBridgeBroker_name
                        ),
                        wsBridgeBroker_name
                    )
                )
        return message_points
    
    
    async def transfer_current_node_chain(
        self,
        wsBridge_settings: dict
    ) -> None:
        """
        Meta
        ---
        Patterns:
            infinity-loop
            log-save
            async background task
            ecsaddo
           
        Arguments
        ---
        - `wsBridge_settings: dict` - Настройки текущего `wsBridge`
            
        Description
        ---
        `transfer_current_node_chain` запускается как `background` задача.
        
        В момент запуска `transfer_current_node_chain` сразу отправляет в
        `wsBridge` актуальные данные `SCI_SETTINGS -> "nodes"`.
        
        Затем на протяжении `startup_activity_time_for_transfer_nodeChain` 
        секунд работает `startup` режим, при котором, проверка актуальности
        `SCI_SETTINGS -> "nodes"` осуществляется каждые 
        `await_startup_delay_to_check_update_nodeChain` секунд на протяжении
        `startup_activity_time_for_transfer_nodeChain`.
        Если данные были изменены относительно прошлой проверки, то обновленные
        данные отправляются в `wsBridge`.
        
        После `startup`, `transfer_current_node_chain` переходит в обычный
        режим, при котором проверка актуальности совершается каждые 
        `await_delay_to_check_update_nodeChain` секунд, и 100% отправка
        данных, (даже если не было изменений) каждые 
        `await_delay_to_transfer_nodeChain` секунд.
        
        ---
        
        Отправка актуальных данных в `wsBridge`
        ```python
        {
            "status": "ok",
            "action": "nodeChain-update",
            "data": {
                "description": "",
                "actual_data": {
                    "wsBridgeBroker": "node_name",
                    "nodeChain": ["node_name", "node_name",]
                }
            }
        }
        ```
        """
        try:
            start_flag = True
            latest_data =  {}
            time_next_shipment = (
                int(time.time()) + sci_settings.await_delay_to_transfer_nodeChain
            )
            end_startup_greatest_activity: float = (
                time.time() + 
                sci_settings.startup_activity_time_for_transfer_nodeChain
            )
            wsBridgeBroker_aq: asyncio.Queue = (
                wsBridge_settings["wsBridgeBroker_aq"]
            )
            while True:
                current_time = time.time()
                if current_time <=  end_startup_greatest_activity:
                    await asyncio.sleep(
                        0 
                        if start_flag 
                        else sci_settings.await_startup_delay_to_check_update_nodeChain
                    )
                    if start_flag: start_flag = False
                else:
                    await asyncio.sleep(
                        sci_settings.await_delay_to_check_update_nodeChain
                    )
                actual_data = {
                    "wsBridgeBroker_nodeName": self.SCI_SETTINGS["node_name"],
                    "nodeChain": []
                }
                for local_node in self.SCI_SETTINGS["nodes"]["local_nodes"]:
                    actual_data["nodeChain"].append(local_node)
                for remote_node in self.SCI_SETTINGS["nodes"]["remote_nodes"]:
                    actual_data["nodeChain"].append(remote_node)
                if (
                    self.is_nodeChain_update(latest_data, actual_data) or 
                    int(time.time()) >= time_next_shipment
                ):
                    ecsaddo = create_ecsaddo(
                        "ok", 
                        "nodeChain-update",
                        actual_data=actual_data
                    )
                    # Отправляем "node-chain" сообщение в `wsBridge`
                    await wsBridgeBroker_aq.put(ecsaddo)
                    # Обновляем время следующей отправки.
                    time_next_shipment = int(time.time()) + 120
                    latest_data = actual_data
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "transfer_current_node_chain (ex)",
                "exception occurred in transfer_current_node_chain",
                location=True,
                traceback=trc,
            )
            if DEBUG:
                pprint(
                    "--------------------\n"
                    f"{self.__class__.__name__} исключение в "
                    f"transfer_current_node_chain \n"
                    f"{data} \n"
                    "--------------------\n"
                )
            save_log(self.sci_ref.logfilePath, data)
            
            
    def is_nodeChain_update(
        self, 
        latest_data: dict, 
        actual_data: dict
    ) -> bool:
        """
        Arguments
        ---
        `latest_data: dict` - Прошлые данные.
        В первый раз будет передан пустой словарь `{}`
        ```python
        {
            "wsBridgeBroker_nodeName": self.SCI_SETTINGS["node_name"],
            "nodeChain": ["first_node", "second_node"]
        }
        ```
        
        `actual_data: dict` - Актуальные данные.
        ```python
        {
            "wsBridgeBroker_nodeName": self.SCI_SETTINGS["node_name"],
            "nodeChain": ["first_node", "second_node", "third_node"]
        }
        ```
        
        Description
        ---
        Метод `is_nodeChain_update` проверяет есть ли изменения в `actual_data`
        относительно `latest_data`
        
        Return
        ---
        `True` - Есть изменения в `actual_data` относительно `latest_data`.
        `False` - Изменений в `actual_data` относительно `latest_data` нет.
        """
        if not len(latest_data):
            return True
        for node_name in actual_data["nodeChain"]:
            if node_name not in latest_data["nodeChain"]:
                return True
        for node_name in latest_data["nodeChain"]:
            if node_name not in actual_data["nodeChain"]:
                return True
        return False
            