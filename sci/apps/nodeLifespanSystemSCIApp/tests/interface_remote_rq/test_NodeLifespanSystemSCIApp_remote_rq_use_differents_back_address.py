"""
Данный модуль предоставляет тесты проверяющие работоспособность `lifespan` цикла 
взаимодействия узлов от `NodeLifespanSystemSCIApp`.

Время выполнения многих тестов может превышать 30 секунд.

Некоторые тесты создают дочерние процессы и самостоятельно завершают их.
NOTE: Поэтому, не рекомендуется самостоятельно прерывать 
тест в середине его выполнения с помощью `Ctrl + Z` (`KeyboardInterrupt`), 
так-как это может привести к ситуации, когда дочерний процесс не сможет 
автоматически завершиться, и придется вручную отправлять команду для 
его завершения.

TBD:
Добавить автоматическую систему `terminate` / `startup` дочерних процессов 
на основе `PID` файлов.
"""
import asyncio
import unittest
import traceback
import inspect
import queue

from typing import Awaitable, Optional
from pathlib import Path

from sci.apps.nodeLifespanSystemSCIApp.application import (
    NodeLifespanSystemSCIApp
)
from sci.app_controllers.base_controller import SCI_BaseAppController
from sci.lib.patterns import create_ecsaddo, isecsaddo
from sci.sci_base.sci_base import SCI
from sci.network.utils import create_response_payload
from sci.sci_cli.sci_cli import SCI_Response
from sci.sci_settings import TEST_LOG_FILE_PATH


ref_q = queue.Queue()
WAIT_AUTH = 1


class GenericTest_SCIApp(SCI_BaseAppController):
    
    ACTIONS = {
        "test-generic": {
            "handler_name": "genericActionHandler",
            "background": False,
            "max_execution_time": 5,
        },
    }
            
                
    async def genericActionHandler(
        self, 
        EventMessage: dict
    ) -> dict:
        try:
            time_sleep: Optional[int] = (
                EventMessage["message_payload"]["data"].get("sleep")
            )
            if time_sleep:
                await asyncio.sleep(time_sleep)
            return_data: dict = (
                EventMessage["message_payload"]["data"].get("return_data")
            )
            if return_data:
                return return_data
            return_exception: Optional[bool] = (
                EventMessage["message_payload"]["data"].get("return_exception")
            )
            if return_exception:
                raise ValueError("oops")
            set_wrong_status_code: Optional[bool] = (
                EventMessage["message_payload"]["data"].get("wrong_status_code")
            )
            if set_wrong_status_code:
                response_payload = create_response_payload({"work": True}, "FF")
                return create_ecsaddo("ok", response_payload)
            set_wrong_response_data: Optional[bool] = (
                EventMessage["message_payload"]["data"].get("wrong_response_data")
            )
            if set_wrong_response_data:
                response_payload = create_response_payload(
                    response_data="6ftgyhbuj"
                )
                return create_ecsaddo("ok", response_payload=response_payload)
            work_check: Optional[bool] = (
                EventMessage["message_payload"]["data"].get("work_check")
            )
            if work_check:
                ref_q.put(True)
            response_payload = create_response_payload({"work": True}, 200)
            return create_ecsaddo("ok", response_payload=response_payload)
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "oHsRKKdUTcUaMGgGHMm",
                "exception occurred in node_authentication_local",
                location=True,
                traceback=trc
            )
            

class SCI_node_test_wfGadIqDLpgjmTNEUAzVUAdAVxGrInqHjji(unittest.TestCase):
    """
    Аутентификация "back_address": "local".
    """
    def setUp(self):
        SCI_SETTINGS_appolo = {
            "node_name": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", {})
            ],
            "nodes": {
                "local_nodes": {},
                "remote_nodes": {},
                "remote_ws_nodes": {},
            },
            "websocket_connections": {},
            "local_broker_connection_settings": {
                "redis": {
                    "host": {
                        "local": "localhost",
                    },
                    "port": 6379,
                    "password": None,
                    "db": 0,
                }
            }
        }
        context_jupiter = {
            "auth_nodes_settings": {
                "remote_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
                        "broker_connection_settings": {
                            "redis": {
                                "host": "localhost",
                                "port": 6379,
                                "password": None,
                                "db": 0
                            }
                        },
                        "back_address": "local"
                    }
                }
            }
        }
        SCI_SETTINGS_jupiter = {
            "node_name": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", context_jupiter)
            ],
            "nodes": {
                "local_nodes": {},
                "remote_nodes": {},
                "remote_ws_nodes": {},
            },
            "websocket_connections": {},
            "local_broker_connection_settings": {
                "redis": {
                    "host": {
                        "local": "localhost",
                    },
                    "port": 6379,
                    "password": None,
                    "db": 0,
                }
            }
        }
        sci_appolo = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_appolo)
        self.sci_cli_appolo, self.sci_core_appolo = sci_appolo.start()
        sci_jupiter = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_jupiter)
        self.sci_cli_jupiter, self.sci_core_jupiter = sci_jupiter.start()
        
        
    def tearDown(self) -> None:
        # Очищаем ref_q
        size = ref_q.qsize()
        for i in range(size):
            ref_q.get()
        

    async def async_test_runner(
        self, 
        test_async_payload: list[Awaitable],
        waiting_after: (int | float) = 0 
    ):
        """
        `async_test_runner` это вспомогательная асинхронная функция, которая
        позволяет сперва запустить `sci_core`, затем запустить пользовательские
        `awaitable` сопрограммы из `test_async_payload`
        
        `async_test_runner` возвращает результат первой завершенной задачи.
        """
        current_task_name = "async_test_runner"
        loop = asyncio.get_event_loop()
        asyncio.current_task(loop).set_name(current_task_name)
        # Запуск `sci_node_appolo`
        task_sci_core_appolo = asyncio.create_task(self.sci_core_appolo())
        # Запуск `sci_node_jupiter`
        task_sci_core_jupiter = asyncio.create_task(self.sci_core_jupiter())
        # Запуск пользовательских test_async_payload
        while True:
            core_is_ready = [
                self.sci_core_appolo.is_working, 
                self.sci_core_jupiter.is_working
            ]
            if not all(core_is_ready):
                await asyncio.sleep(0.1)
                continue
            break
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_core_appolo)
        futures.append(task_sci_core_jupiter)
        for future in asyncio.as_completed(futures):
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            break
        # Начинается очистка
        # Завершаем все задачи (в том числе sci_core), кроме текущей.
        [
            task.cancel() 
            for task in asyncio.all_tasks(loop) 
            if not task.done() and task.get_name() != current_task_name
        ]
        # Закрываем redis подключения всех `sci_core`
        redis_conn_appolo = (
            self.sci_core_appolo.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_appolo.close()
        redis_conn_jupiter = (
            self.sci_core_jupiter.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_jupiter.close()
        # Возвращаем результат первой завершенной задачи
        return res
    
    
    def test_kImkUBfrfXvNLDWhCYdrhhnexRlaHcOSftgQqYGNZAD(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "local".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` не используется
        
        Проверка:
        Это тест нормальной работы.
        `sci_cli.send_message()` должен вернуть `ecsaddo`
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': '', 
                'awaitable_response': <function SCI_cli.convert_to_sci_response.<locals>.wrapper at 0x7f96bd722de0>
            }
        }
        """
        msg = self.test_kImkUBfrfXvNLDWhCYdrhhnexRlaHcOSftgQqYGNZAD.__doc__
        async def send_message(ping_pong: bool = False) -> dict:
            # время на аутентификацию и handshake.
            await asyncio.sleep(WAIT_AUTH) 
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {},
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage, ping_pong=ping_pong
            )
            return send_result
        # Запуск сперва `sci_core`, затем `*send_message`
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]),
            msg=msg
        )
            
        
    def test_YsMLKpHqQIZYuWzX(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "local".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется
        
        Проверка:
        Это тест нормальной работы.
        `sci_cli.send_message()` должен вернуть `ecsaddo`
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': '', 
                'awaitable_response': <function SCI_cli.convert_to_sci_response.<locals>.wrapper at 0x7f96bd722de0>
            }
        }
        """
        msg = self.test_YsMLKpHqQIZYuWzX.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_from_sn = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {},
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage_from_sn,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]),
            msg=msg
        )
            
        
    def test_ZnecujFmPTcSQi(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "local".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется
        
        Проверка:
        (Это тест нормальной работы.)
        `await awaitable_response()` вернет экземпляр `SCI_Response`, где:
        - `response.status_code` - 200
        - `response.response_data` - `session_result -> "data" -> "response" ->
            "message_payload" -> "data"`
        - `response.session_result` - Все данные сессии.
            {
                'status': 'ok', 
                'action': '', 
                'data': {
                    'description': '', 
                    'response': {
                        'sender': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:gGn7FQQQeUmrODo9tEtJuIS',
                            'sci_mode': 'standart'
                        }, 
                        'message_payload': {
                            'data': {'work': True}, 
                            'meta': {'status_code': 200}
                        }
                    }
                }
            }
        """
        msg = self.test_ZnecujFmPTcSQi.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)])
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 1, msg=msg)
        
        
    def test_mxhynPKgByDlANLd(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        - Аутентификация "back_address": "local".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` не используется
        
        Проверка:
        (Это тест нормальной работы.)
        `await awaitable_response()` вернет экземпляр `SCI_Response`, где:
        - `response.status_code` - 200
        - `response.response_data` - `session_result -> "data" -> "response" ->
            "message_payload" -> "data"`
        - `response.session_result` - Все данные сессии.
            {
                'status': 'ok', 
                'action': '', 
                'data': {
                    'description': '', 
                    'response': {
                        'sender': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:rcSU1fON73z4iFUXwr0iM7L', 
                            'sci_mode': 'standart'
                        }, 
                        'message_payload': {
                            'data': {'work': True}, 
                            'meta': {'status_code': 200}
                        }
                    }
                }
            }
        """
        msg = self.test_mxhynPKgByDlANLd.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 1, msg=msg)
        
        
class SCI_node_test_UZQGbPPcMbYBvnArNKSdlvrPcAOgEAoqXRZvpaLlKuB(unittest.TestCase):
    """
    Аутентификация "back_address": "local-network"
    """
    def setUp(self):
        SCI_SETTINGS_appolo = {
            "node_name": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", {})
            ],
            "nodes": {
                "local_nodes": {},
                "remote_nodes": {},
                "remote_ws_nodes": {},
            },
            "websocket_connections": {},
            "local_broker_connection_settings": {
                "redis": {
                    "host": {
                        "local": "localhost",
                        "local-network": "localhost",
                    },
                    "port": 6379,
                    "password": None,
                    "db": 0,
                }
            }
        }
        context_jupiter = {
            "auth_nodes_settings": {
                "remote_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
                        "broker_connection_settings": {
                            "redis": {
                                "host": "localhost",
                                "port": 6379,
                                "password": None,
                                "db": 0
                            }
                        },
                        "back_address": "local-network"
                    }
                }
            }
        }
        SCI_SETTINGS_jupiter = {
            "node_name": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", context_jupiter)
            ],
            "nodes": {
                "local_nodes": {},
                "remote_nodes": {},
                "remote_ws_nodes": {},
            },
            "websocket_connections": {},
            "local_broker_connection_settings": {
                "redis": {
                    "host": {
                        "local": "localhost",
                        "local-network": "localhost"
                    },
                    "port": 6379,
                    "password": None,
                    "db": 0,
                }
            }
        }
        sci_appolo = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_appolo)
        self.sci_cli_appolo, self.sci_core_appolo = sci_appolo.start()
        sci_jupiter = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_jupiter)
        self.sci_cli_jupiter, self.sci_core_jupiter = sci_jupiter.start()
        
        
    def tearDown(self) -> None:
        # Очищаем ref_q
        size = ref_q.qsize()
        for i in range(size):
            ref_q.get()
        

    async def async_test_runner(
        self, 
        test_async_payload: list[Awaitable],
        waiting_after: (int | float) = 0 
    ):
        """
        `async_test_runner` это вспомогательная асинхронная функция, которая
        позволяет сперва запустить `sci_core`, затем запустить пользовательские
        `awaitable` сопрограммы из `test_async_payload`
        
        `async_test_runner` возвращает результат первой завершенной задачи.
        """
        current_task_name = "async_test_runner"
        loop = asyncio.get_event_loop()
        asyncio.current_task(loop).set_name(current_task_name)
        # Запуск `sci_node_appolo`
        task_sci_core_appolo = asyncio.create_task(self.sci_core_appolo())
        # Запуск `sci_node_jupiter`
        task_sci_core_jupiter = asyncio.create_task(self.sci_core_jupiter())
        # Запуск пользовательских test_async_payload
        while True:
            core_is_ready = [
                self.sci_core_appolo.is_working, 
                self.sci_core_jupiter.is_working
            ]
            if not all(core_is_ready):
                await asyncio.sleep(0.1)
                continue
            break
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_core_appolo)
        futures.append(task_sci_core_jupiter)
        for future in asyncio.as_completed(futures):
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            break
        # Начинается очистка
        # Завершаем все задачи (в том числе sci_core), кроме текущей.
        [
            task.cancel() 
            for task in asyncio.all_tasks(loop) 
            if not task.done() and task.get_name() != current_task_name
        ]
        # Закрываем redis подключения всех `sci_core`
        redis_conn_appolo = (
            self.sci_core_appolo.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_appolo.close()
        redis_conn_jupiter = (
            self.sci_core_jupiter.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_jupiter.close()
        # Возвращаем результат первой завершенной задачи
        return res
    
    
    def test_kImkUBfrfXvNLDWhCYdrhhnexRlaHcOSftgQqYGNZAD(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "local-network".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` не используется
        
        Проверка:
        Это тест нормальной работы.
        `sci_cli.send_message()` должен вернуть `ecsaddo`
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': '', 
                'awaitable_response': <function SCI_cli.convert_to_sci_response.<locals>.wrapper at 0x7f96bd722de0>
            }
        }
        """
        msg = self.test_kImkUBfrfXvNLDWhCYdrhhnexRlaHcOSftgQqYGNZAD.__doc__
        async def send_message(ping_pong: bool = False) -> dict:
            # время на аутентификацию и handshake.
            await asyncio.sleep(WAIT_AUTH) 
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {},
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage, ping_pong=ping_pong
            )
            return send_result
        # Запуск сперва `sci_core`, затем `*send_message`
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]),
            msg=msg
        )
            
        
    def test_YsMLKpHqQIZYuWzX(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "local-network".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется
        
        Проверка:
        Это тест нормальной работы.
        `sci_cli.send_message()` должен вернуть `ecsaddo`
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': '', 
                'awaitable_response': <function SCI_cli.convert_to_sci_response.<locals>.wrapper at 0x7f96bd722de0>
            }
        }
        """
        msg = self.test_YsMLKpHqQIZYuWzX.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_from_sn = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {},
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage_from_sn,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]),
            msg=msg
        )
            
        
    def test_ZnecujFmPTcSQi(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "local-network".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется
        
        Проверка:
        (Это тест нормальной работы.)
        `await awaitable_response()` вернет экземпляр `SCI_Response`, где:
        - `response.status_code` - 200
        - `response.response_data` - `session_result -> "data" -> "response" ->
            "message_payload" -> "data"`
        - `response.session_result` - Все данные сессии.
            {
                'status': 'ok', 
                'action': '', 
                'data': {
                    'description': '', 
                    'response': {
                        'sender': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:gGn7FQQQeUmrODo9tEtJuIS',
                            'sci_mode': 'standart'
                        }, 
                        'message_payload': {
                            'data': {'work': True}, 
                            'meta': {'status_code': 200}
                        }
                    }
                }
            }
        """
        msg = self.test_ZnecujFmPTcSQi.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)])
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 1, msg=msg)
        
        
    def test_mxhynPKgByDlANLd(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        - Аутентификация "back_address": "local-network".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` не используется
        
        Проверка:
        (Это тест нормальной работы.)
        `await awaitable_response()` вернет экземпляр `SCI_Response`, где:
        - `response.status_code` - 200
        - `response.response_data` - `session_result -> "data" -> "response" ->
            "message_payload" -> "data"`
        - `response.session_result` - Все данные сессии.
            {
                'status': 'ok', 
                'action': '', 
                'data': {
                    'description': '', 
                    'response': {
                        'sender': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:rcSU1fON73z4iFUXwr0iM7L', 
                            'sci_mode': 'standart'
                        }, 
                        'message_payload': {
                            'data': {'work': True}, 
                            'meta': {'status_code': 200}
                        }
                    }
                }
            }
        """
        msg = self.test_mxhynPKgByDlANLd.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 1, msg=msg)
        
        
class SCI_node_standart_with_await_response_interface_remote_rq_use_external_address(unittest.TestCase):
    """
    Аутентификация "back_address": "external".
    """
    def setUp(self):
        SCI_SETTINGS_appolo = {
            "node_name": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", {})
            ],
            "nodes": {
                "local_nodes": {},
                "remote_nodes": {},
                "remote_ws_nodes": {},
            },
            "websocket_connections": {},
            "local_broker_connection_settings": {
                "redis": {
                    "host": {
                        "local": "localhost",
                        "local-network": "localhost",
                        "external": "localhost"
                    },
                    "port": 6379,
                    "password": None,
                    "db": 0,
                }
            }
        }
        context_jupiter = {
            "auth_nodes_settings": {
                "remote_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
                        "broker_connection_settings": {
                            "redis": {
                                "host": "localhost",
                                "port": 6379,
                                "password": None,
                                "db": 0
                            }
                        },
                        "back_address": "local-network"
                    }
                }
            }
        }
        SCI_SETTINGS_jupiter = {
            "node_name": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", context_jupiter)
            ],
            "nodes": {
                "local_nodes": {},
                "remote_nodes": {},
                "remote_ws_nodes": {},
            },
            "websocket_connections": {},
            "local_broker_connection_settings": {
                "redis": {
                    "host": {
                        "local": "localhost",
                        "local-network": "localhost",
                        "external": "localhost",
                    },
                    "port": 6379,
                    "password": None,
                    "db": 0,
                }
            }
        }
        sci_appolo = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_appolo)
        self.sci_cli_appolo, self.sci_core_appolo = sci_appolo.start()
        sci_jupiter = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_jupiter)
        self.sci_cli_jupiter, self.sci_core_jupiter = sci_jupiter.start()
        
        
    def tearDown(self) -> None:
        # Очищаем ref_q
        size = ref_q.qsize()
        for i in range(size):
            ref_q.get()
        

    async def async_test_runner(
        self, 
        test_async_payload: list[Awaitable],
        waiting_after: (int | float) = 0 
    ):
        """
        `async_test_runner` это вспомогательная асинхронная функция, которая
        позволяет сперва запустить `sci_core`, затем запустить пользовательские
        `awaitable` сопрограммы из `test_async_payload`
        
        `async_test_runner` возвращает результат первой завершенной задачи.
        """
        current_task_name = "async_test_runner"
        loop = asyncio.get_event_loop()
        asyncio.current_task(loop).set_name(current_task_name)
        # Запуск `sci_node_appolo`
        task_sci_core_appolo = asyncio.create_task(self.sci_core_appolo())
        # Запуск `sci_node_jupiter`
        task_sci_core_jupiter = asyncio.create_task(self.sci_core_jupiter())
        # Запуск пользовательских test_async_payload
        while True:
            core_is_ready = [
                self.sci_core_appolo.is_working, 
                self.sci_core_jupiter.is_working
            ]
            if not all(core_is_ready):
                await asyncio.sleep(0.1)
                continue
            break
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_core_appolo)
        futures.append(task_sci_core_jupiter)
        for future in asyncio.as_completed(futures):
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            break
        # Начинается очистка
        # Завершаем все задачи (в том числе sci_core), кроме текущей.
        [
            task.cancel() 
            for task in asyncio.all_tasks(loop) 
            if not task.done() and task.get_name() != current_task_name
        ]
        # Закрываем redis подключения всех `sci_core`
        redis_conn_appolo = (
            self.sci_core_appolo.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_appolo.close()
        redis_conn_jupiter = (
            self.sci_core_jupiter.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_jupiter.close()
        # Возвращаем результат первой завершенной задачи
        return res
    
    
    def test_kImkUBfrfXvNLDWhCYdrhhnexRlaHcOSftgQqYGNZAD(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "external".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` не используется
        
        Проверка:
        Это тест нормальной работы.
        `sci_cli.send_message()` должен вернуть `ecsaddo`
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': '', 
                'awaitable_response': <function SCI_cli.convert_to_sci_response.<locals>.wrapper at 0x7f96bd722de0>
            }
        }
        """
        msg = self.test_kImkUBfrfXvNLDWhCYdrhhnexRlaHcOSftgQqYGNZAD.__doc__
        async def send_message(ping_pong: bool = False) -> dict:
            # время на аутентификацию и handshake.
            await asyncio.sleep(WAIT_AUTH) 
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {},
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage, ping_pong=ping_pong
            )
            return send_result
        # Запуск сперва `sci_core`, затем `*send_message`
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]),
            msg=msg
        )
            
        
    def test_YsMLKpHqQIZYuWzX(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "external".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется
        
        Проверка:
        Это тест нормальной работы.
        `sci_cli.send_message()` должен вернуть `ecsaddo`
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': '', 
                'awaitable_response': <function SCI_cli.convert_to_sci_response.<locals>.wrapper at 0x7f96bd722de0>
            }
        }
        """
        msg = self.test_YsMLKpHqQIZYuWzX.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_from_sn = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {},
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage_from_sn,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]),
            msg=msg
        )
            
        
    def test_ZnecujFmPTcSQi(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        - `"isAwaiting" - True`
        - `"interface" - "remote-rq"`
        - Аутентификация "back_address": "external".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется
        
        Проверка:
        (Это тест нормальной работы.)
        `await awaitable_response()` вернет экземпляр `SCI_Response`, где:
        - `response.status_code` - 200
        - `response.response_data` - `session_result -> "data" -> "response" ->
            "message_payload" -> "data"`
        - `response.session_result` - Все данные сессии.
            {
                'status': 'ok', 
                'action': '', 
                'data': {
                    'description': '', 
                    'response': {
                        'sender': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:gGn7FQQQeUmrODo9tEtJuIS',
                            'sci_mode': 'standart'
                        }, 
                        'message_payload': {
                            'data': {'work': True}, 
                            'meta': {'status_code': 200}
                        }
                    }
                }
            }
        """
        msg = self.test_ZnecujFmPTcSQi.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)])
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 1, msg=msg)
        
        
    def test_mxhynPKgByDlANLd(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        - Аутентификация "back_address": "external".
        
        Особенности:
        - Сообщение передается от `jupiter` узла, в `appolo` узел.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` не используется
        
        Проверка:
        (Это тест нормальной работы.)
        `await awaitable_response()` вернет экземпляр `SCI_Response`, где:
        - `response.status_code` - 200
        - `response.response_data` - `session_result -> "data" -> "response" ->
            "message_payload" -> "data"`
        - `response.session_result` - Все данные сессии.
            {
                'status': 'ok', 
                'action': '', 
                'data': {
                    'description': '', 
                    'response': {
                        'sender': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:rcSU1fON73z4iFUXwr0iM7L', 
                            'sci_mode': 'standart'
                        }, 
                        'message_payload': {
                            'data': {'work': True}, 
                            'meta': {'status_code': 200}
                        }
                    }
                }
            }
        """
        msg = self.test_mxhynPKgByDlANLd.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_jupiter.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 1, msg=msg)
        
        
if __name__ == "__main__":
    unittest.main()
        
        