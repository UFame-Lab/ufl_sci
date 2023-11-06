import asyncio
import traceback
import time

from typing import Callable, Awaitable, Optional
from pprint import pprint

import redis.asyncio as redis

from sci import sci_settings
from sci.app_controllers.base_controller import SCI_BaseAppController
from sci.lib.common_utils import generate_variable_name
from sci.lib.patterns import create_ecsaddo
from sci.network.utils import create_response_payload
from sci.lib.logging import save_log
from sci.sci_settings import DEBUG
from sci.apps.nodeLifespanSystemSCIApp.validators import (
    NodeLifespanSystemSCIAppContext_Validate
)
from sci.sci_typing import ecsaddo
# from sci.lib.common_utils import smart_print
            

class NodeLifespanSystemSCIApp(SCI_BaseAppController):
    
    extra_validators: list[str] = ["context_validate"] 
    
    ACTIONS = {
        "node-authentication": {
            "handler_name": "node_authentication",
            "background": True,
            "max_execution_time": 5,
        },
        "hand-shake": {
            "handler_name": "hand_shake",
            "background": True,
            "max_execution_time": 5,
        }
    }
    
    
    ###################
    ## actionHandler ##
    ###################
    async def node_authentication(
        self, 
        EventMessage: dict
    ) -> ecsaddo:
        """
        Arguments
        ---
        - `EventMessage: dict`
        
        Meta
        ---
        Patterns:
            actionHandler
            ecsaddo
        
        Description
        ---
        `actionHandler` - `node_authentication` принимает запрос аутентификации
        от `sub` узла.
        
        Узел принимающий запрос, является `related_main` узлом.
        Узел отправляющий запрос, является `related_sub` узлом. 
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        try:
            # P.S: `action` такие как `"node-authentication"`, `"handshake"`
            # являются специальными сервисными `action`, их особенность
            # заключается в том, что адрес (и настройки) 
            # получателя таких `EventMessage` указывается в
            # `EventMessage -> "meta" -> "to_node_addr"`, так как такие узлы
            # еще не прошли аутентификацию и их нет в 
            # `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / 
            # "remote_ws_nodes"`.
            SCI_SETTINGS: dict = self.sci_cli.SCI_SETTINGS
            # `node_data` sub узла который запросил аутентификацию.
            related_subNode_node_data: dict = (
                EventMessage["message_payload"]["data"]
            )
            related_subNode_node_name: str = (
                related_subNode_node_data.get("node_name")
            )
            related_subNode_interface: str = (
                related_subNode_node_data.get("interface")
            )
            related_subNode_node_conf: dict = (
                related_subNode_node_data.get("node_conf")
            )          
            to_node_addr = related_subNode_node_data
            # Так как `actionHandler` "handshake" `sub` узла не знает адрес
            # текущего `main` SCI node, тогда мы добавляем
            # `EventMessage -> "meta" -> "back_node_addr"` куда мы указываем
            # адреес по которому `sub` узел отправил `EventMessage` `action` -
            # "node_authentication" в текущий `main` узел.
            back_node_addr: dict = EventMessage["meta"]["to_node_addr"]
            handshake_auth_key = generate_variable_name(30, prefix="hsak_") 
            EventMessage_handshake = {
                "sender": self.app_name,
                "action": "hand-shake",
                "address_section": {
                    "recipient": f"{related_subNode_node_name}:{self.app_name}",
                    "interface": related_subNode_interface
                },
                "meta": {
                    "mType": "request",
                    "to_node_addr": to_node_addr,
                    "back_node_addr": back_node_addr
                },
                "message_payload": {
                    "data": {
                        "handshake_auth_key": handshake_auth_key,
                        "handshake_lvl": "start",
                    },
                    "meta": {
                        "background": True
                    },   
                },
                "response_settings": {
                    "isAwaiting": False,
                }
            }
            if related_subNode_interface == "ws":
                EventMessage_handshake["address_section"].setdefault(
                    "wsbridge", EventMessage["address_section"]["wsbridge"]
                )
            ecsaddo_send_message: dict = (
                await self.sci_cli.send_message(
                    EventMessage_handshake, ping_pong=False
                )
            )
            if ecsaddo_send_message["status"] != "ok":
                return ecsaddo_send_message
                   
            redis_conn: redis.Redis = (
                SCI_SETTINGS["local_broker_connection_settings"].get(
                    "redis"
                ).get("redis_conn")
            )
            # Ожидаем 5 секунд, пока `sub` node проходящий аутентификацию не 
            # отправит ответ на `handshake`        
            handshake_result: Optional[tuple[bytes]] = (
                await redis_conn.brpop(handshake_auth_key, timeout=5)
            )
            # `sub` node проходящий авторизацию не ответил на `handshake`
            if not handshake_result:
                return create_ecsaddo(
                    "error",
                    "handshake try error",
                    "handshake try error",
                    node_data=related_subNode_node_name
                )
            # handshake_ok: str = handshake_result[-1].decode()
            # `sub` node успешно ответил на `handshake` запрос.
            # `sub` node успешно прошел авторизацию.
            # Добавляем `node_data` текущего `sub` node в коллекцию 
            # `related_sub_nodes` обернув в задачу-таймер, с delay на 20 секунд.
            # Все `sub` node прошедшие аутентификацию попадают в `related_sub_nodes`
            # на основе которой работает background задача 
            # self.lifespanSubNodeSentinel которая отслеживает активность `sub`
            # узлов.
            # Если какой либо узел слишком долго остается не активным,
            # Настройка `max_related_sub_nodes_latency_activity`
            # Значит `sub` узел будет удален из 
            # `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / 
            # "remote_ws_nodes"`
            self.related_sub_nodes.add(
                asyncio.create_task(
                    self.wrap_to_timer(
                        related_subNode_node_data,
                        sci_settings.polling_related_sub_nodes_time
                    )
                )
            )
            self.reload_timerManager(
                self.waitWhenAnyTimerCheckRelatedSubNodesIsReady
            )
            related_subNode_node_conf["time_last_activity"] = int(time.time())
            related_subNode_node_conf["relation_type"] = "related_sub"
            if related_subNode_interface == "local-rq":
                SCI_SETTINGS["nodes"].get(
                    "local_nodes"
                )[related_subNode_node_name] = related_subNode_node_conf
            elif related_subNode_interface == "remote-rq":
                SCI_SETTINGS["nodes"].get(
                    "remote_nodes"
                )[related_subNode_node_name] = related_subNode_node_conf
            elif related_subNode_interface == "ws":
                SCI_SETTINGS["nodes"].get(
                    "remote_ws_nodes"
                )[related_subNode_node_name] = related_subNode_node_conf
            wsBridgeBroker = list(
                self.sci_cli.SCI_SETTINGS["websocket_connections"].keys()
            )
            if related_subNode_interface in ("local-rq", "remote-rq"):    
                success_auth_data = {
                    "wsBridgeBroker": wsBridgeBroker
                }
            else:
                success_auth_data = {}
            response_payload = (
                create_response_payload(success_auth_data, 200)
            )
            # Если `sub` Node успешно прошел процедуру аутентификации, тогда
            # его `node_data` уже должна быть добавлена в:
            # `SCI_SETTINGS -> "nodes" -> "locl_nodes" / "remote_nodes" / 
            # "remote_ws_nodes"`
            # Клиенту ожидаюшего ответа от node-authentication 
            # совершается попытка отправить "response" с
            # `EventMessage -> "message_payload" -> 
            #   "meta" -> "status_code": 200` 
            return create_ecsaddo(
                "ok",
                response_payload=response_payload
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "node_authentication (ex)",
                "exception occurred in node_authentication",
                location=True,
                traceback=trc
            )
            

    ###################
    ## actionHandler ##
    ###################
    async def hand_shake(
        self, 
        EventMessage: dict
    ) -> ecsaddo:
        """
        Arguments
        ---
         - `EventMessage: dict`
        
        Description
        ---
        Принимает `EventMessgae` "request" без ожидания ответа от `main` узла.
        `EventMessage -> "message_payload" -> "data" -> "handshake_lvl" = "start"`
        `EventMessage -> "message_payload" -> "data" -> "handshake_auth_key"
        Относительно которого текущий `SCI` node (sub) пытается пройти
        аутентификацию.
        
        Отправляет `EventMessage` "request" без ожидания ответа в "main" узел
        относительно кторого текущий `SCI` node (sub) пытается пройти
        аутентификацию.
        `EventMessage` означает подтверждение `handshake`
        `EventMessage -> "message_payload" -> "data" -> "handshake_lvl" = "end"`
        `EventMessage -> "message_payload" -> "data" -> "handshake_auth_key"
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        try:
            handshake_payload_data: dict = (
                EventMessage["message_payload"]["data"]
            )
            handshake_lvl: str = handshake_payload_data["handshake_lvl"]
            handshake_auth_key: str = handshake_payload_data["handshake_auth_key"]
            if handshake_lvl == "start":
                # Принимает `EventMessgae` "request" без ожидания ответа от 
                # `main` узла.
                # Относительно которого текущий `SCI` node (sub) пытается пройти
                # аутентификацию.
                to_node_addr: dict = EventMessage["meta"]["back_node_addr"]
                EventMessage_handshake_end = {
                    "sender": self.app_name,
                    "action": "hand-shake",
                    "address_section": {
                        "recipient": f"{to_node_addr['node_name']}:{self.app_name}",
                        "interface": to_node_addr["interface"]
                    },
                    "meta": {
                        "mType": "request",
                        "to_node_addr": to_node_addr,
                    },
                    "message_payload": {
                        "data": {
                            "handshake_auth_key": handshake_auth_key,
                            "handshake_lvl": "end"
                        },
                        "meta": {
                            "background": True,
                        }
                    },
                    "response_settings": {
                        "isAwaiting": False
                    }
                }
                if to_node_addr["interface"] == "ws":
                    EventMessage_handshake_end["address_section"].setdefault(
                        "wsbridge", EventMessage["address_section"]["wsbridge"]
                    )
                ecsaddo_send_message = (
                    await self.sci_cli.send_message(
                        EventMessage_handshake_end,
                        ping_pong=False,
                    )
                )
                
                if ecsaddo_send_message["status"] != "ok":
                    return ecsaddo_send_message
                return create_ecsaddo("ok")
            elif handshake_lvl == "end":
                # Отправляет `EventMessage` "request" без ожидания ответа в 
                # "main" узел относительно кторого текущий `SCI` node (sub) 
                # пытается пройти аутентификацию.
                redis_conn: redis.Redis = (
                    self.sci_cli.SCI_SETTINGS.get(
                        "local_broker_connection_settings"
                    )["redis"]["redis_conn"]
                )
                await redis_conn.rpush(handshake_auth_key, "ok")
                return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "hand_shake (ex)",
                "exception occurred in hand_shake",
                location=True,
                traceback=trc
            )
            
        
    ################################
    ## API actionHandlers [end]   ##
    ################################
    
    
    async def startApp(self):
        """
        Meta
        ---
        Patterns:
            ecsaddo
            
        Description
        ---
        Точка инициализации основной логики NodeLifespanSystemSCIApp
        
        Return
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            self.recovery_nodes: set = {
                asyncio.create_task(asyncio.sleep(int(time.time())))
            }
            self.related_main_nodes: set = {
                asyncio.create_task(asyncio.sleep(int(time.time())))
            }
            self.related_sub_nodes: set = {
                asyncio.create_task(asyncio.sleep(int(time.time())))
            }
            self.local_handshake_session = {}
            self.reconnectionNodes_readyEvent = asyncio.Event()
            self.lifespanMainNodeSentinel_readyEvent = asyncio.Event()
            self.lifespanSubNodeSentinel_readyEvent = asyncio.Event()
            self.node_lifespan_tasks_is_ready = asyncio.create_task(
                asyncio.wait(
                    [
                        asyncio.create_task(
                            self.reconnectionNodes_readyEvent.wait()
                        ),
                        asyncio.create_task(
                            self.lifespanMainNodeSentinel_readyEvent.wait()
                        ),
                        asyncio.create_task(
                            self.lifespanSubNodeSentinel_readyEvent.wait()
                        )
                    ],
                    return_when=asyncio.ALL_COMPLETED
                )
            )
            auth_nodes_settings: dict = self.context.get("auth_nodes_settings")
            if auth_nodes_settings is not None:
                local_nodes: dict = auth_nodes_settings.get("local_nodes")
                remote_nodes: dict = auth_nodes_settings.get("remote_nodes")
                remote_ws_nodes: dict = auth_nodes_settings.get("remote_ws_nodes")
                if local_nodes:
                    for local_node in local_nodes:
                        self.recovery_nodes.add(
                            asyncio.create_task(
                                    self.wrap_to_timer(
                                    {
                                        "interface": "local-rq",
                                        "node_name": local_node,
                                        "node_conf": local_nodes[local_node],
                                    },
                                    0,
                                ),
                            )
                        )
                if remote_nodes:
                    for remote_node in remote_nodes:
                        self.recovery_nodes.add(
                            asyncio.create_task(
                                    self.wrap_to_timer(
                                    {
                                        "interface": "remote-rq",
                                        "node_name": remote_node,
                                        "node_conf": remote_nodes[remote_node]
                                    },
                                    0,
                                ),
                            )
                        )
                if remote_ws_nodes:
                    for remote_ws_node in remote_ws_nodes:
                        is_dependent: bool = (
                            remote_ws_nodes[remote_ws_node].get(
                                "dependent", False
                            )
                        )
                        delay_time: int = (
                            sci_settings.wait_delay_for_ws_auth_dependent 
                            if is_dependent 
                            else sci_settings.wait_delay_for_ws_auth
                        )
                        self.recovery_nodes.add(
                            asyncio.create_task(
                                    self.wrap_to_timer(
                                    {
                                        "interface": "ws",
                                        "node_name": remote_ws_node,
                                        "node_conf": remote_ws_nodes[remote_ws_node]
                                    },
                                    delay_time,
                                ),
                            )
                        )
            self.to_background(
                self.reconnectionNodes(), self.background_tasks
            )
            self.to_background(
                self.lifespanMainNodeSentinel(), self.background_tasks
            )
            self.to_background(
                self.lifespanSubNodeSentinel(), self.background_tasks
            )
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "startApp (ex)",
                "exception occurred in startApp",
                traceback=trc
            )
        
     
    def to_background(
        self, 
        aw: Awaitable, 
        collector: set
    ):
        """
        Arguments
        ---
        - `aw: Awaitable` - awaitable задача
        - `collector: set` - множество куда нужно будет сохранить ссылку на
        `background` задачу.
        
        Description
        ---
        Всмпомогательный метод `to_background` запускает `awaitable` задачу
        в `background`, и добавляет ссылку на задачу в множество `collector`
        для того чтобы `python` сборщик мусора произвольно не удалил задачу.
        Задаче устанавливается `add_done_callback` удаленя задачу из множества
        `collector` после того как задачу будкет завершена.
                
        Return
        ---
        объект `asyncio.Task`
        """
        task = asyncio.create_task(aw)
        collector.add(task)
        task.add_done_callback(collector.discard)
        return task  
        
    
    async def reconnectionNodes(self) -> None:
        """
        Meta
        ---
        Patterns:
            [__gw__pl lvl 1]
            infinity-loop
            save-log
            timerManager
            asyncio background task
            ecsaddo
        
        Description
        ----
        Метод reconnectionNodes является async background задачей которая в
        бесконечном цикле создает `timerManager` 
        self.waitWhenAnyTimerReconnectionNodeIsReady на основе коллекции
        `self.recovery_nodes` в которую входят отложенные задачи-таймеры
        возвращаюшие кортеж (node_data, delay) данные  какого либо 
        `related_main_node` относительно которого нужно совершить (отправить) 
        попытку авторизации.
        
        `node_data: dict` - Данные авторизируемого узла.
        ```python
            {
                "interface": "remote-rq",
                "node_name": "some_node_name",
                "node_conf": {
                    "node_rq": "sci_rq_name",
                    "wsBridgeBroker": (,),
                }
            }
        ```
            
        `delay: int` - прошлое значение таймера. По умолчанию первоначальное
            значение 0. Если в текущей попытке узел не прйдет аутентификацию, то
            delat с каждой последующей попыткой будет увеличиваться вдвое.
        
        Попытка аутентификации осуществляется в `background` задаче 
        self.send_auth__gw.
        
        Если node_data узел по какой либо причине не проходит аутентификацию, то
        он снова добавляется в self.recovery_nodes в виде задаче-таймера
        с delay больше в 2 раза чем было прошлое.
        `timerManager` `waitWhenAnyTimerReconnectionNodeIsReady` перезапускается
        для того что-бы он смог подхватить изменения self.recovery_nodes
        
        Если node_data узла успешно проходит авторизацию, тогда узел добавляется
        в `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / "remote_ws_nodes"`
        После чего добавляется в коллекцию `self.related_main_nodes` относительно
        которой совершаются `ping-pong` опросы всех `related_main_nodes`
        авторизированных узлов, на предмет работоспособности.
        После чего перезапускается `timerManager` 
        `self.waitWhenAnyTimerPingRelatedMainNodesIsReady` для подхвата 
        изменений в `self.related_main_nodes`.
        """
        start_flag = True
        while True:
            try:
                self.waitWhenAnyTimerReconnectionNodeIsReady = (
                    asyncio.create_task(
                        asyncio.wait(
                            self.recovery_nodes,
                            return_when=asyncio.FIRST_COMPLETED
                        )
                    )
                )
                if start_flag:
                    self.reconnectionNodes_readyEvent.set()
                    await self.node_lifespan_tasks_is_ready
                    start_flag = False
                timerManager_result = await self.waitWhenAnyTimerReconnectionNodeIsReady
                done, pending = timerManager_result
                for task in done:
                    self.recovery_nodes.discard(task)
                    node_data, delay = await task
                    self.to_background(
                        self.send_auth__gw(node_data, delay), 
                        self.background_tasks
                    ) 
            except asyncio.CancelledError as ex:
                cancel_action = ex.args[0] if len(ex.args) else None
                if cancel_action == "reload":
                    continue
                raise ex # warning
            except Exception as ex:
                trc = str(traceback.format_exception(ex))
                data = create_ecsaddo(
                    "ex",
                    "reconnectionNodes (ex)",
                    "exception occurred in reconnectionNodes",
                    location=True,
                    traceback=trc,
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        f"{self.__class__.__name__}: произошло исключение в "
                        "background задаче reconnectionNodes \n"
                        f"{data}"
                        "--------------------\n"
                    )
                save_log(self.sci_cli.sci_ref.logfilePath, data)
                await asyncio.sleep(1)
                continue
     
        
    async def send_auth__gw(
        self, 
        node_data: dict, 
        last_delay: int
    ):
        """
        Meta
        ----
        Patterns:
            [__gw lvl 1]
            log-save
            asyncio background
            ecsaddo
            
        Arguments
        ---
        - `node_data: dict`  Данные узла куда нужно отправить запрос на
        аутентификацию.
        
        ```python
        {
            "interface": "remote-rq",
            "node_name": "some_node_name",
            "node_conf": {
                "node_rq": "sci_rq_name",
                "wsBridgeBroker": (,),
            }
        }
        ```
        
        - `last_delay: int` - прошлое значение таймера. По умолчанию 
        первоначальное значение 0. 
        Если в текущей попытке узел не пройдет аутентификацию, то delat с каждой 
        последующей попыткой будет увеличиваться вдвое.
            
        Description
        ----
        Метод self.send_auth__gw запускается как async background задача и
        отвечает за непосредственную аутентификацию node_data узла.
            
        Если node_data узел по какой либо причине не проходит аутентификацию, то
        он снова добавляется в self.recovery_nodes в виде задаче-таймера
        с delay больше в 2 раза чем было прошлое.
        `timerManager` `waitWhenAnyTimerReconnectionNodeIsReady` перезапускается
        для того что-бы он смог подхватить изменения self.recovery_nodes
        
        Если node_data узла успешно проходит аутентификацию, тогда узел добавляется
        в `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / "remote_ws_nodes"`
        После чего добавляется в коллекцию `self.related_main_nodes` относительно
        которой совершаются `ping-pong` опросы всех `related_main_nodes`
        авторизированных узлов, на предмет работоспособности.
        После чего перезапускается `timerManager` 
        `self.waitWhenAnyTimerPingRelatedMainNodesIsReady` для подхвата 
        изменений в `self.related_main_nodes`.
        """
        try:
            ecsaddo_send_auth__pl: ecsaddo = (
                await self.send_auth__pl(node_data)
            )
            if ecsaddo_send_auth__pl["status"] != "ok":
                self.recovery_nodes.add(
                    asyncio.create_task(
                        self.wrap_to_timer(
                            node_data,
                            self.get_next_delay(last_delay),
                        ),
                    )
                )
                # Перезапускаем задачу waitWhenAnyTimerReconnectionNodeIsReady
                # Для того что-бы подхватить обновления self.recovery_nodes
                self.reload_timerManager(
                    self.waitWhenAnyTimerReconnectionNodeIsReady
                )
                ecsaddo_send_auth__pl["data"].setdefault(
                    "node_data", node_data
                )
                ecsaddo_send_auth__pl["data"].setdefault(
                    "last_delay", last_delay
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        f"{self.__class__.__name__}: Произошла ошибка или "
                        "исключение в background задаче send_auth \n"
                        f"{ecsaddo_send_auth__pl}"
                        "--------------------\n"
                    )
                save_log(
                    self.sci_cli.sci_ref.logfilePath, 
                    ecsaddo_send_auth__pl
                )
            elif ecsaddo_send_auth__pl["status"] == "ok":
                # Если node_data узла успешно проходит авторизацию, тогда узел 
                # добавляется в `SCI_SETTINGS -> "nodes" -> "local_nodes" / 
                # "remote_nodes" / "remote_ws_nodes"`
                # После чего добавляется в коллекцию `self.related_main_nodes` 
                # относительно которой совершаются `ping-pong` опросы всех 
                # `related_main_nodes` авторизированных узлов, на предмет 
                # работоспособности. После чего перезапускается `timerManager` 
                # `self.waitWhenAnyTimerPingRelatedMainNodesIsReady` для подхвата 
                # изменений в `self.related_main_nodes`.
                SCI_SETTINGS: dict = self.sci_cli.SCI_SETTINGS
                self.related_main_nodes.add(
                    asyncio.create_task(
                        self.wrap_to_timer(
                            node_data,
                            sci_settings.pp_polling_related_main_nodes_time
                        )
                    )
                )
                self.reload_timerManager(
                    self.waitWhenAnyTimerPingRelatedMainNodesIsReady
                )
                # Обновляем time_last_activity
                node_data["node_conf"]["time_last_activity"] = int(time.time())
                # Обновляем relation_type
                node_data["node_conf"]["relation_type"] = "related_main"
                if node_data["interface"] == "local-rq":
                    SCI_SETTINGS["nodes"].get(
                        "local_nodes"
                    )[node_data["node_name"]] = node_data["node_conf"]
                elif node_data["interface"] == "remote-rq":
                    SCI_SETTINGS["nodes"].get(
                        "remote_nodes"
                    )[node_data["node_name"]] = node_data["node_conf"]
                elif node_data["interface"] == "ws":
                    SCI_SETTINGS["nodes"].get(
                        "remote_ws_nodes"
                    )[node_data["node_name"]] = node_data["node_conf"]
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "send_auth__gw (ex)",
                "exception occurred in send_auth__gw",
                location=True,
                traceback=trc,
                node_data=node_data,
                last_delay=last_delay,
            )
            if DEBUG:
                pprint(
                    "--------------------\n"
                    f"{self.__class__.__name__}: произошло исключение в "
                    "background задаче send_auth__gw \n"
                    f"{data}"
                    "--------------------\n"
                )
            save_log(self.sci_cli.sci_ref.logfilePath, data)
    
        
    async def send_auth__pl(
        self, 
        node_data: dict, 
    ) -> ecsaddo:
        """
        Meta
        ----
        Patterns:
            [__pl lvl 1]
            ecsaddo
            
        Arguments
        ---
        - `node_data: dict`  Данные узла куда нужно отправить запрос на
        аутентификацию.
        
        ```python
        {
            "interface": "remote-rq",
            "node_name": "some_node_name",
            "node_conf": {
                "node_rq": "sci_rq_name",
                "wsBridgeBroker": (,),
            }
        }
        ```
    
        Desciprion
        ---
        Полное описание процедуры аутентификации смотри в документации.
        
        Return
        ---
        ecsaddo "ok", "error", "ex"
        """
        try:
            # `EventMessage -> "meta" -> "to_node_addr"` - указывается
            # адрес node_data т.е адрес узла из `context` который в данный
            # момент начинает процедуру аутентификации.
            # P.S: `action` такие как `"node-authentication"`, `"handshake"`
            # являются специальными сервисными `action`, их особенность
            # заключается в том, что адрес (и настройки) 
            # получателя таких `EventMessage` указывается в
            # `EventMessage -> "meta" -> "to_node_addr"`, так как такие узлы
            # Еще не прошли аутентификация и их нет в 
            # `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / 
            # "remote_ws_nodes"`.
            # Соответственно для того что-бы `related_main_node` к которому
            # отправляется запрос авторизации знал адрес и настройки текущего
            # SCI узла, они указываются в 
            # `EventMessage -> "message_payload" -> "data"`
            SCI_SETTINGS: dict = self.sci_cli.SCI_SETTINGS
            if node_data["interface"] == "local-rq":
                address_section = {
                    "recipient": f"{node_data['node_name']}:{self.app_name}",
                    "interface": node_data["interface"],
                }
                payload_data = {
                    "interface": node_data["interface"],
                    "node_name": SCI_SETTINGS["node_name"],
                    "node_conf": {
                        "node_rq": SCI_SETTINGS["node_rq"],
                        "wsBridgeBroker": tuple(
                            SCI_SETTINGS["websocket_connections"].keys()
                        )
                    }
                }
            elif node_data["interface"] == "remote-rq":
                local_settings: dict = SCI_SETTINGS.get(
                    "local_broker_connection_settings"
                )
                host: str = local_settings["redis"].get(
                    "host"
                )[node_data["node_conf"]["back_address"]]
                port: int = local_settings["redis"]["port"]
                password: Optional[int] = local_settings["redis"]["password"]
                db: int = local_settings["redis"]["db"]
                address_section = {
                    "recipient": f"{node_data['node_name']}:{self.app_name}",
                    "interface": node_data["interface"],
                }
                payload_data = {
                    "interface": node_data["interface"],
                    "node_name": SCI_SETTINGS["node_name"],
                    "node_conf": {
                        "node_rq": SCI_SETTINGS["node_rq"],
                        "wsBridgeBroker": tuple(
                            SCI_SETTINGS["websocket_connections"].keys()
                        ),
                        "broker_connection_settings":{
                            "redis": {
                                "host": host,
                                "port": port,
                                "password": password,
                                "db": db
                            }
                        }
                    }
                }
            elif node_data["interface"] == "ws":
                address_section = {
                    "recipient": f"{node_data['node_name']}:{self.app_name}",
                    "interface": node_data["interface"],
                    "wsbridge": node_data["node_conf"]["wsbridge"],
                }
                payload_data = {
                    "interface": node_data["interface"],
                    "node_name": SCI_SETTINGS["node_name"],
                    "node_conf": {
                        "wsbridge": node_data["node_conf"]["wsbridge"]
                    }
                }
                
            EventMessage = {
                "sender": self.app_name,
                "action": "node-authentication", # service action
                "address_section": address_section,
                "meta": {
                    "mType": "request",
                    "to_node_addr": node_data,
                },
                "message_payload": {
                    "data": payload_data,
                    "meta": {
                        "background": True,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            ecsaddo_send_message = (
                await self.sci_cli.send_message(
                    EventMessage, ping_pong=False
                )
            )
            if ecsaddo_send_message["status"] != "ok":
                return ecsaddo_send_message
            awaitable_response: Callable[..., Awaitable] = (
                ecsaddo_send_message["data"]["awaitable_response"]
            )
            result = await awaitable_response()
            if result.status_code != 200:
                return create_ecsaddo(
                    "error",
                    "auth try error",
                    "auth try error",
                )
            if node_data["interface"] in ("local-rq", "remote-rq"):
                wsBridgeBroker: list = result.response_data.get("wsBridgeBroker")
                node_data["node_conf"]["wsBridgeBroker"] = wsBridgeBroker
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "send_auth__pl (ex)",
                "exception occurred in send_auth__pl",
                location=True,
                traceback=trc
            )
        
    
    async def wrap_to_timer(
        self, 
        node_data: dict, 
        delay: (int | float)
    ) -> tuple[dict, int]:
        """
        Arguments
        ---
        `node_data: dict` - Данные авторизуемого узла
        ```python
            {
                "interface": "local-rq",
                "node_name": "some_node_name",
                "node_conf": {
                    "node_rq": "sci_rq_name",
                    "wsBridgeBroker": (,),   
                },
            }
        ```
        
        `delay: int` - задержка перед возвращением данных.
        
        Description
        ---
        Метод wrap_to_timer - таймер который возвращает кортеж
        (node_data, delay) по истечению `delay`
        """
        await asyncio.sleep(delay)
        return (node_data, delay) 


    def get_next_delay(self, last_delay: int) -> int:
        """
        Увеличивает `last_delay` в два раза.
        Если `last_delay` равняется `0`, тогда метод возвращает `2`.
        Если `last_delay * 2 >= max_delay_btwn_try_reconnection_node`, 
        тогда возвращается `max_delay_btwn_try_reconnection_node` так это
        максимально допустимая задержка.
        """
        max_available = sci_settings.max_delay_btwn_try_reconnection_node
        if last_delay == 0:
            return 2
        delay = last_delay * 2
        if delay >= max_available:
            return max_available
        else:
            return delay
        
        
    async def lifespanMainNodeSentinel(self):
        """
        Meta
        ---
        Patterns:
            [__gw__pl lvl 1]
            infinity-loop
            save-log
            timerManager
            asyncio background task
            ecsaddo
        
        Description
        ---
        Метод `lifespanMainNodeSentinel` является async background задачей 
        которая в бесконечном цикле создает `timerManager`
        `self.waitWhenAnyTimerPingRelatedMainNodesIsReady` на основе коллекции
        `self.related_main_nodes` в которую взодят отложенные задачи-таймеры
        возвращаюшие кортеж (`node_data`, `delay`) данные какого либо
        `related_main_node` относительно которого нужно совершить `ping-pong`
        опрос.
        
        ```python
        `node_data: dict` - Данные авторизованного `main` узла.
            {
                "interface": "remote-rq",
                "node_name": "some_node_name",
                "node_conf": {
                    "node_rq": "sci_rq_name",
                    "wsBridgeBroker": (,),
                }
            }
        ``` 
            
        `delay: int` - прошлое значение таймера. По умолчанию для 
        lifespanMainNodeSentinel все таймеры `ping-pong` опросов устанавливаются
        на 20 секунд.
        
        Попытка отправки `ping-pong` опроса осуществляется в `background` задаче
        `self.background_related_main_node_check_task`
        
        Задача отправляет `ping-pong` в `node` согласно `node_data`
        Если `node` отвечает, тогда задача зарегистрирует задачу-таймер
        на следующий опрос (`ping-pong`) в `self.related_main_nodes`
        и пеерзапустит `self.waitWhenAnyTimerPingRelatedMainNodesIsReady`
        для подхвата новой задачи.
        Если опрашиваемый `node` не отвечает, тогда задача добавляет
        задачу-таймер на реконект в список `self.recovery_nodes` с
        начальным промежутком в 2 секунды, и перезапускает задачу
        `self.waitWhenAnyTimerReconnectionNodeIsReady`
        что-бы она подхватила новую задачу-таймер.
        """
        start_flag = True
        while True:
            try:
                self.waitWhenAnyTimerPingRelatedMainNodesIsReady = (
                    asyncio.create_task(
                        asyncio.wait(
                            self.related_main_nodes,
                            return_when=asyncio.FIRST_COMPLETED
                        )
                    )
                )
                if start_flag:
                    self.lifespanMainNodeSentinel_readyEvent.set()
                    await self.node_lifespan_tasks_is_ready
                    start_flag = False
                timerManager_result = (
                    await self.waitWhenAnyTimerPingRelatedMainNodesIsReady
                )
                done, pending = timerManager_result
                for task in done:
                    self.related_main_nodes.discard(task)
                    node_data, delay = await task
                    self.to_background(
                        self.related_main_node_is_alive_check__gw(
                            node_data, delay
                        ),
                        self.background_tasks
                    )
            except asyncio.CancelledError as ex:
                cancel_action = ex.args[0] if len(ex.args) else None
                if cancel_action == "reload":
                    continue
                raise ex # warning
            except Exception as ex:
                trc = str(traceback.format_exception(ex))
                data = create_ecsaddo(
                    "ex",
                    "lifespanMainNodeSentinel (ex)",
                    "exception occurred in lifespanMainNodeSentinel",
                    location=True,
                    traceback=trc
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        f"{self.__class__.__name__}: произошло исключение в "
                        "background задаче lifespanMainNodeSentinel \n"
                        f"{data}"
                        "--------------------\n"
                    )
                save_log(self.sci_cli.sci_ref.logfilePath, data)
                await asyncio.sleep(1)
                continue
                
    
    async def related_main_node_is_alive_check__gw(
        self,
        node_data: dict,
        last_delay: int
    ) -> None:
        """
        Meta
        ---
        Patterns:
            [__gw lvl 1]
            log-save
            asyncio background
            ecsaddo
           
        Arguments
        ---
        `node_data: dict` - Данные авторизованного `main` узла.
        
        ```python
        {
            "interface": "remote-rq",
            "node_name": "some_node_name",
            "node_conf": {
                "node_rq": "sci_rq_name",
                "wsBridgeBroker": (,),
            }
        }
        ```
        
        `delay: int` - прошлое значение таймера. По умолчанию для 
        lifespanMainNodeSentinel все таймеры `ping-pong` опросов устанавливаются
        на 20 секунд.
        
        Description
        ----
        Метод `self.related_main_node_is_alive_check__gw` запускается как async
        background задача и отвечает за `ping-pong` опрос `node_data` узла.
        
        Задача отправляет `ping-pong` в `node` согласно `node_data`
        Если `node` отвечает, тогда задача зарегистрирует задачу-таймер
        на следующий опрос (`ping-pong`) в `self.related_main_nodes`
        и пеерзапустит `self.waitWhenAnyTimerPingRelatedMainNodesIsReady`
        для подхвата новой задачи.
        Если опрашиваемый `node` не отвечает, тогда задача добавляет
        задачу-таймер на реконект в список `self.recovery_nodes` с
        начальным промежутком в 2 секунды, и перезапускает задачу
        `self.waitWhenAnyTimerReconnectionNodeIsReady`
        что-бы она подхватила новую задачу-таймер.
        
        Return
        ---
        None
        """
        try:
            ecsaddo_related_main_node_is_alive_check__pl: ecsaddo = (
                await self.related_main_node_is_alive_check__pl(
                    node_data, last_delay
                )
            )
            if ecsaddo_related_main_node_is_alive_check__pl["status"] != "ok":
                # Если опрашиваемый node не отвечает, тогда задача добавляет
                # задачу-таймер на реконект в список self.recovery_nodes с
                # начальным промежутком в 2 секунды, и перезапускает задачу
                # self.waitWhenAnyTimerReconnectionNodeIsReady
                # что-бы она подхватила новую задачу-таймер.
                ecsaddo_delete_non_active_node: dict = (
                    self.delete_non_active_node(
                        interface=node_data["interface"], 
                        node_name=node_data["node_name"]
                    )
                )
                self.recovery_nodes.add(
                    asyncio.create_task(self.wrap_to_timer(node_data, 2))
                )
                self.reload_timerManager(
                    self.waitWhenAnyTimerReconnectionNodeIsReady
                )
                if ecsaddo_delete_non_active_node["status"] != "ok":
                    raise ValueError(ecsaddo_delete_non_active_node)
                ecsaddo_related_main_node_is_alive_check__pl["data"].setdefault(
                    "node_data", node_data
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        f"{self.__class__.__name__}"
                        ".related_main_node_is_alive_check__gw \n"
                        "Во время проверки активности related main node "
                        "Возникла ошибка или исключение: \n"
                        f"{ecsaddo_related_main_node_is_alive_check__pl}"
                        "--------------------\n"
                    )
                save_log(
                    self.sci_cli.sci_ref.logfilePath, 
                    ecsaddo_related_main_node_is_alive_check__pl
                )
            elif ecsaddo_related_main_node_is_alive_check__pl["status"] == "ok":
                self.related_main_nodes.add(
                    asyncio.create_task(
                        self.wrap_to_timer(
                            node_data,
                            sci_settings.pp_polling_related_main_nodes_time
                        )
                    )
                )
                self.reload_timerManager(
                    self.waitWhenAnyTimerPingRelatedMainNodesIsReady
                )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            data = create_ecsaddo(
                "ex",
                "related_main_node_is_alive_check__gw (ex)",
                "exception occurred in related_main_node_is_alive_check__gw",
                location=True,
                traceback=trc,
                node_data=node_data,
            )
            if DEBUG:
                pprint(
                    "--------------------\n"
                    f"{self.__class__.__name__}"
                    ".related_main_node_is_alive_check__gw \n"
                    "Во время проверки активности related main node "
                    "Возникла ошибка или исключение: \n"
                    f"{data}"
                    "--------------------\n"
                )
            save_log(self.sci_cli.sci_ref.logfilePath, data)
    
    
    async def related_main_node_is_alive_check__pl(
        self,
        node_data: dict,
        last_delay: int
    ):
        """
        Meta
        ---
        Patterns:
            [__pl lvl 1]
            ecsaddo

        Arguments
        ---
        `node_data: dict` - Данные авторизованного `main` узла.
        ```python
        {
            "interface": "remote-rq",
            "node_name": "some_node_name",
            "node_conf": {
                "node_rq": "sci_rq_name",
                "wsBridgeBroker": (,),
            }
        }
        ```
            
        `delay: int` - прошлое значение таймера. По умолчанию для 
        lifespanMainNodeSentinel все таймеры `ping-pong` опросов устанавливаются
        на 20 секунд.

        Description:
        ---
        Полное описание процедуры `ping-pong` опроса смотри в 
        self.related_main_node_is_alive_check__gw
        """
        try:
            EventMessage = {
                "sender": self.app_name,
                "action": "ping-pong",
                "address_section": {
                    "recipient": f"{node_data['node_name']}:{self.app_name}",
                    "interface": node_data["interface"]
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {
                        "background": True
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5
                }
            }
            if node_data["interface"] == "ws":
                EventMessage["address_section"].setdefault(
                    "wsbridge", 
                    node_data["node_conf"]["wsbridge"]
                )
            ecsaddo_send_message = (
                await self.sci_cli.send_message(
                    EventMessage, ping_pong=False
                )
            )
            if ecsaddo_send_message["status"] != "ok":
                return ecsaddo_send_message         
            awaitable_response: Callable[..., Awaitable] = (
                ecsaddo_send_message["data"]["awaitable_response"]
            )
            # asyncio.TimeoutError
            result = await asyncio.wait_for(awaitable_response(), 6)
            if result.status_code != 200:
                return create_ecsaddo(
                    "error",
                    "node is not alive",
                    "node is not alive"
                )
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "related_main_node_is_alive_check__pl (ex)",
                "exception occurred in related_main_node_is_alive_check__pl",
                location=True,
                traceback=trc,
            )
        
        
    def reload_timerManager(
        self, 
        timerManager: asyncio.Task
    ):
        """
        Arguments
        ---
        `timerManager: asyncio.Task` - 
        `asyncio.wait(aws, return_when=FIRST_COMPLETED)` задача которая ожидает
        завершения какой либо задачи из коллекции `aws`. Задачи из коллекции
        `aws` являются таймерами, которые возвращают `payload` результат
        по истечению своего внутреннего таймера.
        
        Description
        ---
        Вспомогательный метод `reload_timerManager` вызывается когда нужно
        перезапустить какой либо `timerManager` для подхвата новых задач.
        
        `reload_timerManager` помечает указынный `timerManager` как завершенный 
        с помощью `timerManager.cancel("reload")`.
        После чего вызывающий код может создать новый `timerManager` на основе 
        актуальных данных.
        
        Return
        ---
        None
        """
        try:
            timerManager.cancel("reload")
        except asyncio.InvalidStateError as ex:
            pass
        
        
    async def lifespanSubNodeSentinel(self):
        """
        Meta
        ---
        Patterns:
            [__gw__pl lvl 1]
            infinity-loop
            save-log
            timerManager
            asyncio background task
            ecsaddo
            
        Description
        ---
        Метод `lifespanSubNodeSentinel` является async background задачей которая
        в бесконечном цикле создает `timerManager`
        `self.waitWhenAnyTimerCheckRelatedSubNodesIsReady` на основе коллекции
        `self.related_sub_nodes` в которую входят отложенные задачи-таймеры
        возвращающие кортеж (node_data, delay) данные какого либо 
        `related_sub_node` который нужно проверить на активность.
        
        `node_data: dict` - Данные авторизованного `sub` узла.
            {
                "interface": "remote-rq",
                "node_name": "some_node_name",
                "node_conf": {
                    "node_rq": "sci_rq_name",
                    "wsBridgeBroker": (,),
                }
            }
            
        `delay: int` - прошлое значение таймера. По умолчанию для 
        lifespanSubNodeSentinel все таймеры проверки активности устанавливаются
        на 20 секунд.
        
        Проверка активности осуществляется на основе значения ключа
        `time_last_activity` который есть в кажом узле
        `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / 
        "remote_ws_nodes"`
        
        Если `time_last_activity` превышает `latency_limit` настройка 
        `max_related_sub_nodes_latency_activity`, это означает что `sub` узел 
        больше не активен и его можно удалить из
        `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / "remote_ws_nodes"`
        
        Для для возобновления общения, `sub` узлу предется снова проходить
        аутентификацию в текущем `main` `SCI` узле.
        """
        start_flag = True
        while True:
            try:
                self.waitWhenAnyTimerCheckRelatedSubNodesIsReady = (
                    asyncio.create_task(
                        asyncio.wait(
                            self.related_sub_nodes,
                            return_when=asyncio.FIRST_COMPLETED
                        )
                    )
                )
                if start_flag:
                    self.lifespanSubNodeSentinel_readyEvent.set()
                    await self.node_lifespan_tasks_is_ready
                    start_flag = False
                timerManager_result = await (
                    self.waitWhenAnyTimerCheckRelatedSubNodesIsReady
                )
                done, pending = timerManager_result
                for task in done:
                    self.related_sub_nodes.discard(task)
                    node_data, delay = await task
                    if node_data["interface"] == "local-rq":
                        node_section = "local_nodes"
                    elif node_data["interface"] == "remote-rq":
                        node_section = "remote_nodes"
                    elif node_data["interface"] == "ws":
                        node_section = "remote_ws_nodes"
                    actual_node_conf: dict = (
                        self.sci_cli.SCI_SETTINGS["nodes"][node_section].get(
                            node_data["node_name"]
                        )
                    )
                    if node_data["node_conf"] is not actual_node_conf:
                        # Если `sub` узел по какой либо причине выполнил не удачный
                        # ping-pong, например, если он использовал дополнительный
                        # промежуточный `wsBridgeBroker` узел, но этот узел в
                        # определенный момент отключился, то `sub` узел отправит
                        # Еще один запрос аутентификации в текущий `SCI node`,
                        # При том что в текущем `SCI node`, `sub` узел все еще
                        # может считаться активным, и иметь свой таймер в
                        # self.related_sub_nodes.
                        # В таком случае возникает ситуация, что после повторной
                        # аутентификации у `sub` узла остаются два таймера в
                        # self.related_sub_nodes.
                        # Для того что-бы старый таймер не удалил `sub` узел
                        # из `SCI_SETTING -> "nodes"`, старый таймер следует 
                        # Завершить.
                        continue
                    time_last_activity: int = (
                        node_data["node_conf"]["time_last_activity"]
                    )
                    latency = int(time.time()) - time_last_activity
                    if latency > sci_settings.max_related_sub_nodes_latency_activity:
                        ecsaddo_delete_non_active_node: dict = (
                            self.delete_non_active_node(
                                interface=node_data["interface"],
                                node_name=node_data["node_name"]
                            )
                        )
                        if ecsaddo_delete_non_active_node["status"] != "ok":
                            raise ValueError(ecsaddo_delete_non_active_node)
                    else:
                        self.related_sub_nodes.add(
                            asyncio.create_task(
                                self.wrap_to_timer(
                                    node_data,
                                    sci_settings.polling_related_sub_nodes_time
                                )
                            )
                        )
                        self.reload_timerManager(
                            self.waitWhenAnyTimerCheckRelatedSubNodesIsReady
                        )
            except asyncio.CancelledError as ex:
                cancel_action = ex.args[0] if len(ex.args) else None
                if cancel_action == "reload":
                    continue
                raise ex
            except Exception as ex:
                trc = str(traceback.format_exception(ex))
                data = create_ecsaddo(
                    "ex",
                    "lifespanSubNodeSentinel (ex)",
                    "exception occurred in lifespanSubNodeSentinel",
                    location=True,
                    traceback=trc
                )
                if DEBUG:
                    pprint(
                        "--------------------\n"
                        f"{self.__class__.__name__}: произошло исключение в "
                        "background задаче lifespanSubNodeSentinel \n"
                        f"{data}"
                        "--------------------\n"
                    )
                save_log(self.sci_cli.sci_ref.logfilePath, data)
                await asyncio.sleep(1)
                continue
            
            
    def delete_non_active_node(
        self, 
        interface: str, 
        node_name: str
    ) -> dict:
        """
        Meta
        ---
        Patterns:
            `ecsaddo`
           
        Arguments
        ---
        - `interface` - `local-rq`, `remote-rq`, `ws`
        - `node_name` - Имя удаляемого `SCI` узла.
            
        Description
        ---
        Метод `delete_non_active_node` отвечает за удаление `node_name` узла
        из `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / "remote_ws_nodes"`.
                
        Return
        ---
        Если `node_name` удалось успешно удалить из `SCI_SETTINGS -> "nodes"`,
        или на текущий момент ключ `node_name` уже отсутствует в
        `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / "remote_ws_nodes"`,
        то возвращается `ecsaddo`
        ```python
        {
            "status": "ok",
            "action": "",
            "data": {
                "description": "",
            }
        }
        ```
        
        Если во время удаления ключа `node_name` возникло исключение, то 
        возвращается соответствующий `ecsaddo`
        ```python
        {
            "status": "ex",
            "action": "delete_non_active_node (ex)",
            "data": {
                "description": "exception occurred in delete_non_active_node",
                "location": "...",
                "traceback": "[...]"
            }
        }
        ```
        """
        try:
            if interface == "local-rq":
                node_key = "local_nodes"
            elif interface == "remote-rq":
                node_key = "remote_nodes"
            elif interface == "ws":
                node_key = "remote_ws_nodes"
            if node_name in self.sci_cli.SCI_SETTINGS["nodes"][node_key]:
                del self.sci_cli.SCI_SETTINGS["nodes"][node_key][node_name]
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "delete_non_active_node (ex)",
                "exception occurred in delete_non_active_node",
                location=True,
                traceback=trc
            )
            
            
    def context_validate(self):
        """
        Description
        ----
        Валидация `self.context`
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        
        """
        ecsaddo: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context, 
            sci_mode=self.sci_cli.sci_mode, 
            SCI_SETTINGS=self.sci_cli.SCI_SETTINGS
        ).start_validation()
        return ecsaddo