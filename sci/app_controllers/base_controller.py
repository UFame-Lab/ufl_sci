import asyncio
import traceback
import json
import time
import inspect

from typing import Awaitable, Callable
from pprint import pprint

from sci.sci_settings import DEBUG
from sci.app_action_handlers.action_handlers import BasicActionHandlers
from sci.sci_exceptions import SendResponseError, SCI_AppError
from sci.sci_typing import ecsaddo
from sci.lib.patterns import create_ecsaddo, isecsaddo
from sci.lib.logging import save_log
from sci.lib.common_utils import json_safe
from sci.network.utils import create_response_payload, SCI_ResposnePayload, sendResponse


AUTH_SERVICE_ACTIONS = [
    "node-authentication", 
    "hand-shake"
]


class SCI_BaseAppController(BasicActionHandlers):
    
    BasicActions = {
        "ping-pong": {
            "handler_name": "ping_pong",
            "background": False,
            "max_execution_time": 2,
        }
    }
    
    extra_validators: list[str] = [] 

    def __init__(
        self,
        app_name: str, 
        sci_cli,
        context: dict = {},
        *args,
        **kwargs
    ):
        """
        Meta
        ---
        Patterns:
            pass
        """
        self.app_name: str = app_name
        self.sci_cli = sci_cli
        self.context: dict = context
        self.background_tasks = set() # codespace


    def get_register_data(self):
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Description
        ---
        Метод `get_register_data()` проводит инициализацию приложения и
        возвращает `ecsaddo` где `ecsaddo -> "data" -> "awaitableAppController"`
        `awaitable` ядро приложения.
        
        При инициализации приложения:
        - Запускается валидация `self.BasicActions`, `self.ACTIONS`
        - Запускается пользовательская валидация `start_validation`
        - Создается `asyncio.Queue` для текущего `AppController`
        - Конфигурируется сопрограмма (ядро приложения) на основе 
        `self.app_controller(queue)`

        Return
        ---
        ecsaddo "ok" / "error" / "ex"
        
        F.E
        ```python
        {
            "status": "ok",
            "action": "",
            "data": {
                "description": "",
                "awaitableAppController": <awaitable_self.app_controller(queue)>
            }
        }
        ```
        """
        try:
            ACTIONS = getattr(self, "ACTIONS", False)
            if not ACTIONS:
                raise SCI_AppError(
                    "Пользовательский AppController обязательно должен иметь "
                    "атрибут 'ACTIONS' в котором зарегистрирован как минимум "
                    "1 `actionHandler`"
                )
            ecsaddo_action_settings_validate: ecsaddo = (
                self.action_settings_validate()
            )
            if ecsaddo_action_settings_validate["status"] != "ok":
                return ecsaddo_action_settings_validate
            ecsaddo_start_validation: ecsaddo = self.start_validation()
            if ecsaddo_start_validation["status"] != "ok":
                return ecsaddo_start_validation
            queue = asyncio.Queue()
            awaitableAppController: Awaitable = self.app_controller(queue)
            return create_ecsaddo(
                "ok",
                queue=queue,
                awaitableAppController=awaitableAppController
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "get_register_data (ex)",
                "exception occurred in get_register_data",
                location=True,
                traceback=trc
            )
    
    
    def action_settings_validate(self) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 2]
            ecsaddo
            
        Description
        ---
        Метод `action_settings_validate()` запускает валидацию 
        `action_settings_check()` для:
        
        - `self.BasicActions` - Стандартные `SCI` `actionHandler` обработчики.
        - `self.ACTIONS` - пользовательские `actionHandler` обработчики.

        Валидация заканчивается сразу, как только один `actionHandler` из 
        `self.BasicActions` или `self.ACTIONS` не проходит проверку.

        Return
        ---
        ecsaddo "ok" / "error" / "ex"
        
        """
        try:
            basic_check: ecsaddo = self.action_settings_check(self.BasicActions)
            if basic_check["status"] != "ok":
                return basic_check
            userspace_check: ecsaddo = self.action_settings_check(self.ACTIONS)
            if userspace_check["status"] != "ok":
                return userspace_check
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "action_settings_validate (ex)",
                "exception occurred in action_settings_validate",
                location=False,
                traceback=trc
            )
    
    
    def action_settings_check(
        self, 
        actions_settings: dict
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo

        Description
        ----
        `SCI_BaseAppController.action_settings_check()` является валидатором 
        который проверяет `self.BasicActions` и `self.ACTIONS` на соответствие 
        шаблону:

        ```python
        {
            "action_name": {
                "handler_name": "actionHandler",
                "background": False / True,
                "max_execution_time: 2,
            },
            "action_name": {
                "handler_name": "actionHandler",
                "background": False / True,
                "max_execution_time": 2,
            },
        }
        ```
        
        Важно что-бы заявленный `"actionHandler"` какого либо `"handler_name"` 
        действительно был в интерфейсе текущего `AppController` и при этом 
        являлся функцией - сопрограммы (`async def`).
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        try:
            for action in actions_settings:
                actionHandlerSettings: dict = actions_settings.get(action)
                if not isinstance(actionHandlerSettings, dict):
                    raise ValueError(
                        "Конфигурация ACTIONS не соответствует шаблону"
                    )
                handler_name: str = actionHandlerSettings.get("handler_name")
                if not isinstance(handler_name, str):
                    raise ValueError(
                        "Конфигурация ACTIONS не соответствует шаблону"
                    )
                actionHandler = getattr(self, handler_name, False)
                if not actionHandler or not inspect.iscoroutinefunction(actionHandler):
                    raise ValueError(
                        f"Конфигурация ACTIONS не соответствует шаблону. \n"
                        f"Указанный actionHandler: {handler_name} не найден в "
                        f"{self.__class__.__name__}, или не является "
                        "асинхронной функцией (async def)\n"
                    )
                background = actionHandlerSettings.get("background")
                if not isinstance(background, bool):
                    raise ValueError(
                        "Конфигурация ACTIONS не соответствует шаблону"
                    )
                max_execution_time: (int | float) = (
                    actionHandlerSettings.get("max_execution_time")
                )
                if (
                    not isinstance(max_execution_time, (int, float)) or 
                    isinstance(max_execution_time, bool)
                ):
                    raise ValueError(
                        "Конфигурация ACTIONS не соответствует шаблону"
                    )
                return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "action_settings_check (ex)",
                "exception occurred in action_settings_check",
                location=True,
                traceback=trc
            )
            

    async def app_controller(
        self, 
        queue: asyncio.Queue
    ) -> None:
        """
        Meta
        ---
        Patterns:
            infinity-loop
            log-save
            ecsaddo
            
        Arguments
        ---
        - `queue: asyncio.Queue` - Очередь которую должен прослущивать текущий
        `app_controller`, после запуска (и завершения) `self.startApp()`.
            
        Description
        ---
        Аснихронный метод `app_controller` является ядром приложения.
        Перед тем как `app_controller` перейдет к прослушиванию и обработки
        запросов, запускается асинхронный метод `self.startApp()`, который
        является `userspace` интерфейсом и может инкапсулировать в себя основную
        полезную нагрузку приложения.
        Если нужно что-бы `app_controller` не принимал запросы до завершения
        работы `self.startApp()`, то `self.startApp()` должен быть обычной
        асинхронной функцией.
        Если нужно что-бы `self.startApp()` постоянно работал, то
        `self.startApp()` должен самостоятельно запускать свою полезную нагрузку
        в `asyncio` `background`.
        """
        try:
            ecsaddo_startApp = await self.startApp()
            if ecsaddo_startApp["status"] != "ok":
                raise ValueError(ecsaddo_startApp)
            while True:
                try:
                    EventMessage = await queue.get()
                    # for logging 
                    EventMessage_safe: dict = json.loads(
                        json.dumps(EventMessage, default=json_safe)
                    )
                    # self.actionDispatcher может ожидать полного выполнения
                    # actionHandler, или отправить actionHandler в background.
                    # логика зависит от установленных настроек в self.ACTIONS
                    # NOTE: self.actionDispatcher не возвращает результат работы
                    # actionHandler, actionHandler самостоятельно обрабатывает
                    # свой результат.
                    # self.actionDispatcher возвращает ecsaddo отражающий
                    # успешность передачи EventMessage в целевой actionHandler.
                    ecsaddo_actionDispatcher: ecsaddo = (
                        await self.actionDispatcher(EventMessage)
                    )
                    if ecsaddo_actionDispatcher["status"] != "ok":
                        ecsaddo_actionDispatcher["data"].setdefault(
                            "EventMessage", EventMessage_safe
                        )
                        if DEBUG:
                            pprint(
                                "--------------------\n"
                                f"{self.__class__.__name__}: не удалось "
                                f"обработать 'action': {EventMessage['action']} \n"
                                f"{ecsaddo_actionDispatcher}\n"
                                "--------------------\n"
                            )
                        save_log(
                            self.sci_cli.sci_ref.logfilePath, 
                            ecsaddo_actionDispatcher
                        )
                        continue
                except Exception as ex:
                    trc = traceback.format_exception(ex)
                    data = create_ecsaddo(
                        "ex",
                        "app_controller (ex)",
                        "exciption occurred in app_controller",
                        location=True,
                        traceback=trc,
                        EventMessage=EventMessage_safe
                    )
                    if DEBUG:
                        pprint(
                            "--------------------\n"
                            f"{self.__class__.__name__}: произошло исключение "
                            "в app_controller \n"
                            f"{data}\n"
                            "--------------------\n"
                        )
                    save_log(self.sci_cli.sci_ref.logfilePath, data)
                    continue
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "app_controller (ex)",
                "exception occurred in app_controller",
                location=True,
                traceback=trc
            )
            if DEBUG: 
                pprint(
                    "--------------------\n"
                    f"{self.__class__.__name__}: произошло исключение "
                    "при запуске app_controller \n"
                    f"{data} \n"
                    "--------------------\n"
                )
            save_log(self.sci_cli.sci_ref.logfilePath, data)


    async def actionDispatcher(
        self, 
        EventMessage: dict
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 1]
            ecsaddo
           
        Arguments
        ---
        - `EventMessage` Текущий запрос.
            
        Description
        ---
        `app_controller` совершает `await` `actionDispatcher` для обработки 
        каждого `EventMessage`.
        Главная задача `actionDispatcher` - найти `actionHandler` обработчик
        запроса, запустить его в нужном режиме и вернуть `ecsaddo` "ok".
        NOTE IMPORTANT: если `actionHandler` запускается не в `background`, 
        то он заставляет ождать своего полного выполнения `actionDispatcher` и 
        `app_controller`, в это время все остальные `EventMessage` находятся
        в очереди на выполнение.
        
        Если у `EventMessage` истек `expire_time`, то такой запрос не
        обрабатывается, ответ на запрос не отправляется, `actionDispatcher` 
        возвращает `ecsaddo` "error"
        
        Если `EventMessage` передал не валидный `action`, то в случае 
        если запрос ожидает ответ, `actionDispatcher` должен отправить ответ
        указывая что `action` не найден. 
        `actionDispatcher` возвращает `ecsaddo` "error".
        
        `actionDispatcher` обращает внимание на ключи:
        - `EventMessage["message_payload"]["meta"]["background"]`
        - `EventMessage["message_payload"]["meta"]["max_execution_time"]`
        Наличие которых переопределяет стандартные настройки.
        
        `actionDispatcher` находит `actionHandler` согласно переданному `action`,
        и запускает его через `messageHandler__gw` (который будет обрабатывать
        результат работы `actionHandler`) устанавливая `timeout` таймер согласно
        `max_execution_time`.
        
        Если `EventMessage`, или базовая настройка указывает запуск 
        `actionHandler` в `background`, то `actionDispatcher` оборачивает 
        `actionHandler` в `messageHandler__gw` и запускает задачу в 
        `asyncio background` с установкой `timeout` согласно `max_execution_time`,
        `actionDispatcher` сразу возвращает `ecsaddo` "ok".
        
        Если `EventMessage` или базовая настройка не указывает запуск
        `actionHandler` в `background`, то `actionDispatcher` совершает обычный
        `await`  `messageHandler__gw(EventMessage, actionHandler)` установив
        `timeout` согласно `max_execution_time`.
        После того как `messageHandler__gw(EventMessage, actionHandler)` завершит
        свою работу (не важно с каким результатом), `actionDispatcher` возвращает
        `ecsaddo` "ok".
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        try:
            isAwaitingResponse: str = (
                EventMessage["meta"].get("session_id", None)
            )
            expire_time: (int | float) = (
                EventMessage["message_payload"]["meta"]["expire_time"]
            )
            if time.time() > expire_time:
                # EventMessage "method": "response" не отправляется, так как 
                # скорее всего сессия уже завершилась по timeout
                return create_ecsaddo(
                    "error",
                    "expire time error",
                    "expire time error"
                )
            messageAction: str = EventMessage.get("action")
            actionHandlerSettings: dict = (
                self.ACTIONS.get(messageAction) or 
                self.BasicActions.get(messageAction)
            )
            if not actionHandlerSettings:
                data = create_ecsaddo(
                    "error",
                    "action not found",
                    "Requested action is not supported",   
                )
                if isAwaitingResponse:
                    message_payload: dict = (
                        create_response_payload({}, 404).response_payload
                    )
                    ecsaddo_sendResponse: dict = (
                        await sendResponse(
                            EventMessage, 
                            message_payload, 
                            self.app_name, 
                            self.sci_cli
                        )
                    )
                    if ecsaddo_sendResponse["status"] != "ok":
                        raise SendResponseError(ecsaddo_sendResponse)
                return data
            
            actionHandlerName: str = actionHandlerSettings["handler_name"]
            # Доверяем валидации action_settings_validate
            actionHandler: Callable[[dict], Awaitable] = (
                getattr(self, actionHandlerName, False)
            )
            to_background: bool = (
                EventMessage["message_payload"]["meta"].get("background") 
                if "background" in EventMessage["message_payload"]["meta"] 
                else actionHandlerSettings["background"]
            )
            max_execution_time: (int | float) = (
                EventMessage["message_payload"]["meta"].get("max_execution_time") 
                if "max_execution_time" in EventMessage["message_payload"]["meta"] 
                else actionHandlerSettings["max_execution_time"]
            )
            if to_background:
                # actionHandler обрабатывается в asyncio background
                task = asyncio.create_task(
                    self.messageHandler__gw(EventMessage, actionHandler)
                )
                self.background_tasks.add(task)
                task.add_done_callback(self.background_tasks.discard)
                loop = asyncio.get_event_loop()
                loop.call_later(
                    max_execution_time, 
                    self.background_task_resolver, 
                    task
                )
            else:
                # Ждем завершения actionHandler.
                # NOTE: actionHandler ничего не возвращает, он сам логирует
                # свой результат (при необходимости).
                # если сработает timeout, то возбудится asyncio.TimeoutError
                # EventMessage "method": "response" отправлять не нужно
                # так как сессия скорее всего уже закрылась.
                await asyncio.wait_for(
                    asyncio.create_task(
                        self.messageHandler__gw(EventMessage, actionHandler)
                    ),
                    max_execution_time
                )
            return create_ecsaddo("ok")
        except asyncio.TimeoutError as ex:
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "actionDispatcher (ex)",
                "exception occurred in actionDispatcher",
                location=True,
                traceback=trc
            )
            
            
    @staticmethod
    def background_task_resolver(task: asyncio.Task) -> None:
        """
        `background_task_resolver` завершает задачу `task` отменой 
        """
        try:
            task.cancel() 
        except Exception as ex:
            pass


    async def messageHandler__gw(
        self, 
        EventMessage: dict,
        actionHandler: Callable[..., Awaitable],
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
        - `EventMessage: dict` Данные запроса.
        - `actionHandler: Callable[..., Awaitable]` - асинхронная функция
        обработки запроса, которую нашел `actionDispatcher`.
            
        Description
        ----
        `SCI_BaseAppController.messageHandler__gw` запускает (`await`) обрабочик 
        `SCI_BaseAppController.messageHandler__pl` с передачей `actionHandler`
        и логирует его результат работы в случае если он отрицательный `ecsaddo`
        
        Return
        ---
        None
        """
        try:
            # for logging
            EventMessage_safe: dict = json.loads(
                json.dumps(EventMessage, default=json_safe)
            )
            ecsaddo_messageHandler__pl: ecsaddo = (
                await self.messageHandler__pl(EventMessage, actionHandler)
            )
            if ecsaddo_messageHandler__pl["status"] != "ok":
                ecsaddo_messageHandler__pl.setdefault(
                    "EventMessage",
                    EventMessage_safe
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        f"{self.__class__.__name__}: произошла ошибка "
                        "в messageHandler__pl или actionHandler вернул "
                        "отрицательный ответ \n"
                        f"{ecsaddo_messageHandler__pl}\n"
                        "--------------------\n"
                    )
                save_log(
                    self.sci_cli.sci_ref.logfilePath, 
                    ecsaddo_messageHandler__pl
                )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "messageHandler__gw (ex)",
                "exception occurred in messageHandler__gw",
                location=True,
                traceback=trc,
                EventMessage=EventMessage_safe
            )
            if DEBUG:
                pprint(
                    "--------------------\n"
                    f"{self.__class__.__name__}: произошла ошибка "
                    "в messageHandler__gw \n"
                    f"{data}\n"
                    "--------------------\n"
                )
            save_log(self.sci_cli.sci_ref.logfilePath, data)


    async def messageHandler__pl(
        self,
        EventMessage: dict,
        actionHandler: Callable[..., Awaitable],
    ) -> dict:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 2]
            ecsaddo
        
        Arguments
        ---
        - `EventMessage: dict` Данные запроса.
        - `actionHandler: Callable[..., Awaitable]` - асинхронная функция
        обработки запроса, которую нашел `actionDispatcher`.
         
        Description
        ---
        Асинхронный метод `messageHandler__pl` совершает `await` `actionHandler` 
        предварительно обернув в обертку 
        `actionHandler_safe(EventMessage, actionHandler)`.
        
        В зависимости от того что возвращает `actionHandler`, 
        `messageHandler__pl` должен отправить соответствующий ответ (`EventMessage`)
        пользователю (если ответ ожидается). 
        
        `actionHandler` должен вернуть положительный `ecsaddo`:
        ```python
        {
            "status": "ok",
            "action": "",
            "data": {
                "description": "",
                "response_payload": SCI_ResposnePayload
            }
        }
        ```
        
        В случае если `actionHandler` вернул положительный `ecsaddo` и
        `ecsaddo -> "data" -> "response_payload"`является экземпляром
        `SCI_ResposnePayload`.
        Если пользователь ожидает ответ, то `messageHandler__pl`
        отправит ответный `EventMessage`, указав в качестве  
        `EventMessage -> "message_payload"` - `response_payload` от `ecsaddo`
        `actionHandler`.
        `messageHandler__pl` вернет `ecsaddo` "ok".
        Если пользователь не ожидает ответ, то `messageHandler__pl` сразу
        возвращает `ecsaddo` "ok"
        
        ---
        
        Если `actionHandler` возвращает ответ отличный от `ecsaddo`.
        В таком случае, если пользователь ожидает ответ, то `messageHandler__pl`
        отправит ответный `EventMessage`, указав в качестве  
        `EventMessage -> "message_payload"`
        ```python
        {
            "data": {},
            "meta": {"status_code": 500}
        }
        ```
        `messageHandler__pl` вернет `ecsaddo` "error".
        Если пользователь не ожидает ответ, то `messageHandler__pl` сразу
        возвращает `ecsaddo` "error"
        
        ---
        
        Если `actionHandler` возвращает ответ `ecsaddo` "error" / "ex".
        В таком случае, если пользователь ожидает ответ, то `messageHandler__pl`
        отправит ответный `EventMessage`, указав в качестве  
        `EventMessage -> "message_payload"`
        ```python
        {
            "data": {},
            "meta": {"status_code": 500}
        }
        ```
        `messageHandler__pl` вернет `ecsaddo` "error".
        Если пользователь не ожидает ответ, то `messageHandler__pl` сразу
        возвращает `ecsaddo` "error"
        
        ---
        
        Если `actionHandler` возвращает ответ `ecsaddo` "ok".
        Но `ecsaddo -> "data" -> "response_payload"` не является экземпляром
        `SCI_ResposnePayload`.
        В таком случае, если пользователь ожидает ответ, то `messageHandler__pl`
        отправит ответный `EventMessage`, указав в качестве  
        `EventMessage -> "message_payload"`
        ```python
        {
            "data": {},
            "meta": {"status_code": 500}
        }
        ```
        `messageHandler__pl` вернет `ecsaddo` "error".
        Если пользователь не ожидает ответ, то `messageHandler__pl` сразу
        возвращает `ecsaddo` "error"
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        try:
            isAwaitingResponse = EventMessage["meta"].get("session_id", False)
            ecsaddo_actionHandler: ecsaddo = (
                await self.actionHandler_safe(EventMessage, actionHandler)
            )
            ecsaddo_check: bool = isecsaddo(ecsaddo_actionHandler)
            if not ecsaddo_check:
                # actionHandler вернул не корректный ответ (не ecsaddo).
                if isAwaitingResponse:
                    # предполагается отправка EventMessage "method": "response"
                    # status_code 500 Internal Server Error
                    response_payload: dict = (
                        create_response_payload({}, 500).response_payload
                    )
                    ecsaddo_sendResponse: dict = (
                        await sendResponse(
                            EventMessage, 
                            response_payload, 
                            self.app_name, 
                            self.sci_cli
                        )
                    )
                    if ecsaddo_sendResponse["status"] != "ok":
                        raise SendResponseError(ecsaddo_sendResponse)
                # EventMessage "method": "response" 
                # уже отправлен или ответ не требуется.
                return create_ecsaddo(
                    "error",
                    "wrong return",
                    "actionHandler return wrong value",
                    wrong_value=ecsaddo_actionHandler
                )
            if ecsaddo_actionHandler["status"] != "ok":
                # actionHandler возвращает корректный ответ в виде ecsaddo
                # но статус ecsaddo "error" / "ex"
                if isAwaitingResponse:
                    # 500 # Internal Server Error
                    response_payload: dict = (
                        create_response_payload({}, 500).response_payload
                    )
                    ecsaddo_sendResponse: dict = (
                        await sendResponse(
                            EventMessage, 
                            response_payload, 
                            self.app_name, 
                            self.sci_cli
                        )
                    )
                    if ecsaddo_sendResponse["status"] != "ok":
                        raise SendResponseError(ecsaddo_sendResponse)
                # EventMessage "method": "response" 
                # уже отправлен или ответ не требуется
                return ecsaddo_actionHandler
            elif ecsaddo_actionHandler["status"] == "ok":
                # NOTE для отправки ответа, actionHandler должен вернуть
                # положительный `ecsaddo`, с "data" -> "response_payload"
                # который является экземпляром SCI_ResposnePayload
                if isAwaitingResponse:
                    response_payload: SCI_ResposnePayload = (
                        ecsaddo_actionHandler["data"].get("response_payload")
                    )
                    if not isinstance(response_payload, SCI_ResposnePayload): 
                        response_payload: dict = (
                            create_response_payload({}, 500).response_payload
                        )
                        ecsaddo_sendResponse: dict = (
                            await sendResponse(
                                EventMessage, 
                                response_payload, 
                                self.app_name, 
                                self.sci_cli
                            )
                        )
                        if ecsaddo_sendResponse["status"] != "ok":
                            raise SendResponseError(ecsaddo_sendResponse)
                        return create_ecsaddo(
                            "error",
                            "response_payload error",
                            "To send `EventMessage` `'method': 'response'`, "
                            "`ActionHandler` should return `ecsaddo`, in "
                            "`'data' -> 'response_payload'` there should be an "
                            "instance  `SCI_ResposnePayload`",
                            wrong_value=ecsaddo_actionHandler
                        )
                    # переводим пользовательский SCI_ResposnePayload в dict
                    response_payload: dict = response_payload.response_payload
                    # Отправка EventMessage
                    ecsaddo_sendResponse: dict = (
                        await sendResponse(
                            EventMessage, 
                            response_payload, 
                            self.app_name, 
                            self.sci_cli
                        )
                    )
                    if ecsaddo_sendResponse["status"] != "ok":
                        raise SendResponseError(ecsaddo_sendResponse)
                    # EventMessage "method": "response" отправлен.
                    return create_ecsaddo("ok")
                else:
                    # EventMessage "method": "response" не требуется.
                    return create_ecsaddo("ok")
            # bypass
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "messageHandler__pl (ex)",
                "exception occurred in messageHandler__pl",
                location=True,
                traceback=trc
            )
    
    
    async def actionHandler_safe(
        self, 
        EventMessage: dict,
        actionHandler: Callable[..., Awaitable]
    ):
        """
        Meta
        ---
        Patterns:
            ecsaddo
            safety-wrapper
        
        Arguments
        ---
        - `EventMessage: dict` Данные запроса.
        - `actionHandler: Callable[..., Awaitable]` - асинхронная функция
        обработки запроса, которую нашел `actionDispatcher`.
            
        Description
        ---
        `safety` обертка гарантирует перехват и обработку любого исключения, 
        которое может возникнуть в `actionHandler`
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            return await actionHandler(EventMessage)
        except Exception as ex:
            trc = str(traceback.format_exception(ex))    
            return create_ecsaddo(
                "ex",
                "exception in actionHandler",
                "exception occurred in actionHandler",
                location=True,
                traceback=trc
            )
                 

    async def startApp(self):
        """
        Desciption
        ---
        Асинхронный метод `self.startApp()` является `userspace` интерфейсом и 
        может инкапсулировать в себя основную полезную нагрузку приложения.
        Если нужно что-бы `app_controller` не принимал запросы до завершения
        работы `self.startApp()`, то `self.startApp()` должен быть обычной
        асинхронной функцией.
        Если нужно что-бы `self.startApp()` постоянно работал, то
        `self.startApp()` должен самостоятельно запускать свою полезную нагрузку
        в `asyncio` `background`.
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        return create_ecsaddo("ok")
    
    
    def start_validation(self):
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Description
        ---
        Метод `start_validation` отвечает за запуск дополнительных валидаторов
        из атрибута `self.extra_validators`.
        Атрибут `self.extra_validators` должен иметь тип `list`, в качестве
        значений списка `self.extra_validators` указываются `str` имена 
        методов валидаторов.

        Пользовательский метод валидатор должен быть `sync` методом.
        Пользовательский метод валидатор должен возвращать ответ в виде `ecsaddo`.
        Как только пользовательский метод валидатор возвращает отрицательный
        `ecsaddo`, или ответ отличный от `ecsaddo`, то `start_validation`
        завершает свою работу.
        
        Return
        ---
        `ecsaddo` "ok" / "error" / "ex".
        F.E
        {
            "status": "ex",
            "action": "validation error",
            "data": {
                "description": "validation error",
                "location": "...",
                "traceback": ["..."],
            }
        }
        """
        try:
            if not isinstance(self.extra_validators, list):
                raise ValueError(
                    "Атрибут `extra_validators` должен иметь тип list, "
                    "Значения списка `extra_validators` - (`str`) имена методов"
                    "валидаторов."
                )
            for validator_name in self.extra_validators:
                if not isinstance(validator_name, str):
                    raise ValueError(
                        "Атрибут `extra_validators` должен иметь тип list, "
                        "Значения списка `extra_validators` - (`str`) имена методов"
                        "валидаторов."
                    )
                validator = getattr(self, validator_name, None)
                if validator is None or not inspect.ismethod(validator):
                    raise ValueError(
                        "Атрибут `extra_validators` должен иметь тип list, "
                        "Значения списка `extra_validators` - (`str`) имена методов"
                        "валидаторов."
                    )
                ecsaddo_validator: ecsaddo = validator()
                if not isecsaddo(ecsaddo_validator):
                    raise ValueError(
                        "Методы валидации должны возвращать ответы в "
                        "виде `ecsaddo`"
                    )
                if ecsaddo_validator["status"] != "ok":
                    return ecsaddo_validator
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "validation error",
                "validation error",
                location=True,
                traceback=trc
            )
    

