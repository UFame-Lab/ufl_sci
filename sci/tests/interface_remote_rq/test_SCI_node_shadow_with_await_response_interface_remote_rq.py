import asyncio
import unittest
import traceback
import inspect
import queue

from typing import Awaitable, Optional

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
            
    
class SCI_node_test_lxECsFzBbxrmgtsSNcOMLmhlDBRYMBqCYWkNENXCAwBrqYF(unittest.TestCase):
    """
    - `"sci_mode": "shadow"`
    - `with await response`
    - `"interface": "remote-rq"`
    - `EventMessage` `proxy` отправляется от `jupiter` к `appolo` 
    """
    def get_settings(self) -> dict:
       pass
    
    
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
        SCI_SETTINGS_shadow = {
            "related_node_rq": "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "logfilePath": TEST_LOG_FILE_PATH,
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
        sci_shadow = SCI(sci_mode="shadow", SCI_SETTINGS=SCI_SETTINGS_shadow)
        self.sci_cli_shadow, self.sci_core_shadow = sci_shadow.start()
        
        
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
        # Запуск sci_core_appolo
        task_sci_core_appolo = asyncio.create_task(self.sci_core_appolo())
        # Запуск sci_core_jupiter
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
        # Завершаем все задачи (в том числе sci_core)
        # Кроме текущей.
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
        redis_conn_shadow = (
            self.sci_core_shadow.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_shadow.close()
        # Возвращаем результат первой завершенной задачи
        return res
    
    
    def test_cyPzANdstHkaKfLVkGrZcvBzHfoJtwzvfmsQx(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
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
        msg = self.test_cyPzANdstHkaKfLVkGrZcvBzHfoJtwzvfmsQx.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq", 
                },
                "meta" : {
                    "mType": "request"
                },
                "message_payload": {
                    "data": {
                        "work_check": True
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage, ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва `sci_core`, затем `*send_message`
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
        
        
    def test_kXZBZganHpAXhftbzAfUSPKUTeIggg(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
       - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
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
        msg = self.test_kXZBZganHpAXhftbzAfUSPKUTeIggg.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq", 
                },
                "meta" : {
                    "mType": "request"
                },
                "message_payload": {
                    "data": {
                        "work_check": True
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
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
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
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
                            'session_id': 'sci_session:1kAdZWvhFFQwGgukhetRzJ1', 
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
        async def send_message(ping_pong: bool = True):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq", 
                },
                "meta" : {
                    "mType": "request"
                },
                "message_payload": {
                    "data": {
                        "work_check": True
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
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
        
        
    def test_mxhynPKgByDlANLd(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` НЕ используется
        
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
                            'session_id': 'sci_session:1kAdZWvhFFQwGgukhetRzJ1', 
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
            send_result = await self.sci_cli_shadow.send_message(
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
        
        
    def test_UtPwYATxU(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в неизвестный `SCI` node.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется (до отправки `ping-pong` дело не дойдет)
        
        Проверка:
        (Это деградационный тест.)
        `EventMessage` должен не пройти проверку назначения в 
        `sci_cli.destination_check()`.
        `sci_cli.send_message()` должен вернуть:
        {
            'status': 'error', 
            'action': 'recipient not found', 
            'data': {
                'description': 'recipient not found'
            }
        }
        """
        msg = self.test_UtPwYATxU.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "some_wrong_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
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
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("recipient not found", result["action"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_mppOHwpaZiIzjBgKhYM(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель НЕ зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется.
        
        Проверка:
        (Это деградационный тест.)
        `EventMessage` должен не пройти проверку назначения в 
        `sci_cli.destination_check()`.
        `sci_cli.send_message()` должен вернуть:
        {
            'status': 'error', 
            'action': 'recipient not found', 
            'data': {
                'description': 'recipient not found'
            }
        }
        """
        msg = self.test_mppOHwpaZiIzjBgKhYM.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:wrong_app",
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
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("recipient not found", result["action"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_bRTClXvixdyOwJtiV(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан НЕ поддерживаемый целевым 
            `Application`
        - `ping-pong` используется.
        
        Проверка:    
        (Это деградационный тест.)
        `EventMessage` успешно отправляется.
        `sci_cli.send_message()` должен вернуть `ecssaddo` "status": "ok",
        Поддерживается ли переданный `action` проверяется непосредственно
        в самом `AppController` целевого приложения, поэтому что-бы узнать
        как запрос был обработан в `AppController`, нужно дополнительно
        совершить `await awaitable_response()`
        
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': '', 
                'awaitable_response': <function SCI_cli.convert_to_sci_response.<locals>.wrapper at 0x7f22c605b2e0>
            }
        }
        """
        msg = self.test_bRTClXvixdyOwJtiV.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "wrong-test-action",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
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
        
        
    def test_nvmDiNHOhKVXHJwJNwLr(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан НЕ поддерживаемый целевым 
            `Application`
        - `ping-pong` используется.
        
        Проверка:
        (Это деградационный тест.)
        `EventMessage` успешно отправляется.
        `sci_cli.send_message()` должен вернуть `ecssaddo` "status": "ok",
        Поддерживается ли переданный `action` проверяется непосредственно
        в самом `AppController` целевого приложения, поэтому что-бы узнать
        как запрос был обраьотан в `AppController`, нужно дополнительно
        совершить `await awaitable_response()`
        
        response.status_code - `404`
        response.response_data - `{}`
        response.session_result - Вся сессия `("status": "ok")`
        """
        msg = self.test_nvmDiNHOhKVXHJwJNwLr.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "wrong-test-action",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True,
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
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
        self.assertEqual(404, result.status_code)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_NWFolhHLEUmzpavni(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` используется. 
        - `AppController` искусственно занят, и не может обработать `ping-pong` 
        запрос.
            
        Проверка:
        (Это деградационный тест.)
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(20)` (по умолчанию `"background": False`), 
        в следствии чего `actionHandler`займет весь `AppController`. 
        
        Сразу отправляется второй запрос (по умолчанию `"background": False`)
        с `"ping-pong": True`,  который завершится в `SCI_core.ResponseSession` 
        по `timeout` через 2 секунды.
        Основной `EventMessage` второго запроса не отправится.
        
        `AppController` должен самостоятельно завершить `actionHandler`
        обработки первого запроса через `"max_execution_time"` (5с)
        Настройка установленная в `GenericTest_SCIApp.ACTIONS`
        
        `sci_cli.send_message() отвечает`
        {
            'status': 'error', 
            'action': 'ping-pong timeout', 
            'data': {
                'description': 'ping-pong timeout'
            }
        }
        """
        msg = self.test_NWFolhHLEUmzpavni.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
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
                        "sleep": 20,
                        "work_check": True,    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            EventMessage_second = {
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
                        "work_check": True,      
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 3,
                }
            }
            send_first_result = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            return send_second_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=3.1)
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("ping-pong timeout", result["action"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_wNpyPOtKRPIGM(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` НЕ отправляется.
        - `AppController` искусственно занят, основной `EventMessage` будет
            проигнорирован
            
        Проверка:
        (Это деградационный тест.)
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(20)` (по умолчанию `"background": False`), 
        в следствии чего `actionHandler`займет весь `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": False`, 
        `"await_timeout": 3`, `"expire_time": 3` 
        (по умолчанию `"background": False`) который
        попадет в очередь ожидания `AppController`.
        Сессия ожидания ответа от второго запроса завершиться по `timeout`
        в `SCI_core.ResponseSession` через 3 секунды.
        
        `AppController` должен самостоятельно завершить `actionHandler`
        обработки первого запроса через `"max_execution_time"` (5с)
        Настройка установленная в `GenericTest_SCIApp.ACTIONS`
        
        `EventMessage` второго запроса имеет `"expire_time": 3`, это означает 
        что когда `AppController` все-таки возьмет второй `EventMessage` из 
        очереди, то он его проигнорирует так как истек `expire_time`.
       
        `sci_cli.send_message()` вернет `ecsaddo`: "ok", так как основной
        `EventMessage` был отправлен.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_wNpyPOtKRPIGM.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
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
                        "sleep": 20,
                        "work_check": True    
                    },
                    "meta": {
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            EventMessage_second = {
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
                    "meta": {
                        "expire_time": 3,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 3,
                }
            }
            send_first_result = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            awaitable_response: dict = (
                send_second_result["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=2.1
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_sQJEAowOfxYnVmJV(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверка:
        (Это деградационный тест.)
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(3)` (по умолчанию `"background": False`), 
        в следствии чего `actionHandler`займет весь `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": False`, 
        `"await_timeout": 2`, `"expire_time": 20` 
        (по умолчанию `"background": False`) который
        попадет в очередь ожидания `AppController`.
        Сессия ожидания ответа от второго запроса завершиться по `timeout`
        в `SCI_core.ResponseSession` через 2 секунды.
        
        Первый запрос самостоятельно успешно завершиться через 3 с.
        
        `EventMessage` второго запроса имеет `"expire_time": 20`, это означает 
        что когда `AppController` все-таки возьмет второй `EventMessage` из 
        очереди, то он его успешно выполнит.
        
        Первый и вторый запрос успешно выполняются, хоть сессия ожидания ответа
        2-го запроса завершается по `timeout`.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_sQJEAowOfxYnVmJV.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
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
                        "sleep": 3,
                        "work_check": True    
                    },
                    "meta": {
                        "max_execution_time": 5
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            EventMessage_second = {
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
                    "meta": {
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_first_result = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            awaitable_response: dict = (
                send_second_result["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)], 
                waiting_after=1.1
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(2, ref_q.qsize(), msg=msg)
        
        
    def test_kJXVSGQPvpKCUrFo(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверка:
        (Это деградационный тест.)
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(3)` (по умолчанию `"background": False`), 
        в следствии чего `actionHandler` займет весь `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": False`, 
        `"await_timeout": 2`, `"expire_time": 2` 
        (по умолчанию `"background": False`) который
        попадет в очередь ожидания `AppController`.
        Сессия ожидания ответа от второго запроса завершиться по `timeout`
        в `SCI_core.ResponseSession` через 2 секунды.
        
        Первый запрос самостоятельно успешно завершиться через 3 с.
        
        `EventMessage` второго запроса имеет `"expire_time": 2`, это означает 
        что когда `AppController` все-таки возьмет второй `EventMessage` из 
        очереди, то он его проигнорирует.
        
        Первый и вторый запрос успешно выполняются.
        Второй запрос не будет выполнен. Сессия ожидания ответа 2-го запроса
        завершиться по `timeout`
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_kJXVSGQPvpKCUrFo.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
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
                        "sleep": 3,
                        "work_check": True    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            EventMessage_second = {
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
                    "meta": {
                        "expire_time": 2,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_first_result = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            awaitable_response: dict = (
                send_second_result["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)], 
                waiting_after=1.1
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(1, ref_q.qsize(), msg=msg)
        
        
    def test_DchxWnGJEhwUduWneBtXD(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверяется:
        
        Оотправляется `EventMessage` `"await_timeout": 2`, `"expire_time": 20`,
        `"max_execution_time": 3`, указывающий `actionHandler` совершить 
        `await asyncio.sleep(20)` (по умолчанию `"background": False`), в 
        следствии чего `actionHandler` займет весь `AppController`.
        
        Запрос не будет (полностью) выполнен, так как `AppController` отменит 
        его через `"max_execution_time": 3` 
        Сессия ожидания ответа запроса завершиться по `timeout`.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_DchxWnGJEhwUduWneBtXD.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_block = {
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
                        "sleep": 20,
                        "work_check": True    
                    },
                    "meta": {
                        "max_execution_time": 2,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2.1,
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage_block,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_yUBNhTffjlzurFXU(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не используется.
        
        Проверяется:
        
        Отправляется `EventMessage` `"await_timeout": 1`, `"expire_time": 20`,
        `"max_execution_time": 0.5`, указывающий `actionHandler` совершить 
        `await asyncio.sleep(1.3)` ("background": True`).
        
        Запрос не будет (полностью) выполнен, так как `AppController` отменит 
        его через `"max_execution_time": 0.5`.
         
        Сессия ожидания ответа запроса завершиться по `timeout`.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_yUBNhTffjlzurFXU.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_block = {
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
                        "sleep": 1.3,
                        "work_check": True
                    },
                    "meta": {
                        "background": True,
                        "max_execution_time": 0.5,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 1,
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage_block,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=0.4 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_sLxJsyrHrjxMJirKz(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
    
        Проверка:
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(1.2)` (`"background": True`), 
        в следствии чего `actionHandler` не блокирует `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": False`, 
        `"await_timeout": 1`, `"expire_time": 1` 
        (по умолчанию `"background": False`) который должен сразу успешно 
        выполниться.
        
        Первый запрос - самостоятельно успешно завершиться через 1.2 с.
        Второй запрос - сразу успешно выполняется.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 200
        - response.resposne_data - `{'work': True}`
        - response.session_result - `ecsaddo` всей сессии.
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
                            'session_id': 'sci_session:PHZ9KCM4y7xciyAnb2OfnRr', 
                            'sci_mode': 'standart'
                        }, 
                        'message_payload': {
                            'data': {
                                'work': True
                            }, 
                            'meta': {
                                'status_code': 200
                            }
                        }
                    }
                }
            }
        """
        msg = self.test_sLxJsyrHrjxMJirKz.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
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
                        "sleep": 1.2,
                        "work_check": True 
                    },
                    "meta": {
                        "background": True,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            EventMessage_second = {
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
                    "meta": {
                        "background": False,
                        "expire_time": 1,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 1,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_result_second = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_second["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=1.3
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 2, msg=msg)
        
        
    def test_JbxhyQCWJxVrlbdDP(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверяется:
        
        Отправляется `EventMessage` `"await_timeout": 0.6`, `"expire_time": 20`,
        `"max_execution_time": 0.3`, указывающий `actionHandler` совершить 
        `await asyncio.sleep(0.5)` ("background": False`).
        
        Запрос не будет (полностью) выполнен, так как `AppController` отменит 
        его через `"max_execution_time": 0.3`.
         
        Сессия ожидания ответа запроса завершиться по `timeout`.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_JbxhyQCWJxVrlbdDP.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
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
                        "sleep": 0.5,
                        "work_check": True 
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 0.3,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 0.6,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)], 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"],
            msg=msg
        )
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_sTBIZzDZfLFbrkb(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
       - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        Если `actionHandler` отвечает не `ecsaddo`, тогда `messageHandler__pl`
        должен обернуть ответ в `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_sTBIZzDZfLFbrkb.__doc__
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
                        "work_check": True,
                        "return_data": [1, 2, 3, 4]
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 10,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_LwpQCVldlekAB(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Если `actionHandler` отвечает `ecsaddo` "status" != "ok"
        тогда `messageHandler__pl` логирует этот `ecsaddo` и отправляет
        `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_LwpQCVldlekAB.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            error_ecsaddo = create_ecsaddo(
                "error",
                "oops error",
                "oops error test"
            )
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
                        "return_data": error_ecsaddo
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                         "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
        
    def test_HBMnaXTcpajNNHkRBj(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        Если `actionHandler` отвечает `ecsaddo` "status" == "ok"
        но в `ecsaddo["data"]` отсутствует ключ `"response_payload"`, или
        значение ключа `"response_payload" не является экземпляром 
        `SCI_ResponsePayload`
        
        тогда `messageHandler__pl` логирует этот `ecsaddo` и отправляет
        `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_HBMnaXTcpajNNHkRBj.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            error_ecsaddo = create_ecsaddo(
                "ok",
                response_payload = 200
            )
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
                        "return_data": error_ecsaddo
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                         "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
        
    def test_wFQNUhUBWUfqSXWNDbYktPdoZBDiWYybUrGSfQR(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        Если `actionHandler` отвечает `ecsaddo` "status" == "ok"
        но в `ecsaddo["data"]` отсутствует ключ `"response_payload"`, или
        значение ключа `"response_payload" не является экземпляром 
        `SCI_ResponsePayload`
        
        тогда `messageHandler__pl` логирует этот `ecsaddo` и отправляет
        `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_wFQNUhUBWUfqSXWNDbYktPdoZBDiWYybUrGSfQR.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            error_ecsaddo = create_ecsaddo("ok")
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
                        "return_data": error_ecsaddo
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
    
    def test_uvNLEsKOT(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        Если в `actionHandler` возникает исключенеи.
        тогда `messageHandler__pl` логирует этот это исключение в виде
        `ecsaddo` и отправляет `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_uvNLEsKOT.__doc__
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
                        "return_exception": True
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
        ####
        ####
        
    def test_YvTvDRBfsZc(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Если `actionHandler` при создании экземпляра `SCI_ResponsePayload`
        передал невалидный `status_code`, то возникает исключение.
        `actionHandler` возвращает `ecsaddo` "status": "ex"
        тогда `messageHandler__pl` логирует этот этот `ecsaddo` "status": "ex"
        и отправляет `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии.
        """
        msg = self.test_YvTvDRBfsZc.__doc__
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
                        "wrong_status_code": True,
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
    
    def test_ccxvoqHCPZBMqZoeho(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_jupiter` отправляет сообщение в `sci_node_appolo`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Если `actionHandler` при создании экземпляра `SCI_ResponsePayload`
        передал невалидный `response_data`, то возникает исключение.
        `actionHandler` возвращает `ecsaddo` "status": "ex"
        
        тогда `messageHandler__pl` логирует этот этот `ecsaddo` "status": "ex"
        и отправляет `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии.
        """
        msg = self.test_ccxvoqHCPZBMqZoeho.__doc__
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
                        "wrong_response_data": True,
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
        
        
class SCI_node_test_HJItkNWeSeOFrihWUAgyjyttEqDMIgYEkMndtoCHruFY(unittest.TestCase):
    """
    - `"sci_mode": "shadow"`
    - `with await response`
    - `"interface": "remote-rq"`
    - `EventMessage` `proxy` отправляется от `appolo` к `jupiter` 
    """
    def get_settings(self) -> dict:
       pass
    
    
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
        SCI_SETTINGS_shadow = {
            "related_node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "logfilePath": TEST_LOG_FILE_PATH,
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
        sci_shadow = SCI(sci_mode="shadow", SCI_SETTINGS=SCI_SETTINGS_shadow)
        self.sci_cli_shadow, self.sci_core_shadow = sci_shadow.start()
        
        
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
        # Запуск sci_core_appolo
        task_sci_core_appolo = asyncio.create_task(self.sci_core_appolo())
        # Запуск sci_core_jupiter
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
        # Завершаем все задачи (в том числе sci_core)
        # Кроме текущей.
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
        redis_conn_shadow = (
            self.sci_core_shadow.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_shadow.close()
        # Возвращаем результат первой завершенной задачи
        return res
    
    
    def test_cyPzANdstHkaKfLVkGrZcvBzHfoJtwzvfmsQx(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
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
        msg = self.test_cyPzANdstHkaKfLVkGrZcvBzHfoJtwzvfmsQx.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq", 
                },
                "meta" : {
                    "mType": "request"
                },
                "message_payload": {
                    "data": {
                        "work_check": True
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage, ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва `sci_core`, затем `*send_message`
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)], 
                waiting_after=0.5
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]),
            msg=msg
        )
        
        
    def test_kXZBZganHpAXhftbzAfUSPKUTeIggg(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
       - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
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
        msg = self.test_kXZBZganHpAXhftbzAfUSPKUTeIggg.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq", 
                },
                "meta" : {
                    "mType": "request"
                },
                "message_payload": {
                    "data": {
                        "work_check": True
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
                waiting_after=0.5
            )
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
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
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
                        'sender': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:1kAdZWvhFFQwGgukhetRzJ1', 
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
        async def send_message(ping_pong: bool = True):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq", 
                },
                "meta" : {
                    "mType": "request"
                },
                "message_payload": {
                    "data": {
                        "work_check": True
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=0.5
            )
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
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` НЕ используется
        
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
                        'sender': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:1kAdZWvhFFQwGgukhetRzJ1', 
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
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
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
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=0.5
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 1, msg=msg)
        
        
    def test_UtPwYATxU(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в неизвестный `SCI` node.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется (до отправки `ping-pong` дело не дойдет)
        
        Проверка:
        (Это деградационный тест.)
        `EventMessage` должен не пройти проверку назначения в 
        `sci_cli.destination_check()`.
        `sci_cli.send_message()` должен вернуть:
        {
            'status': 'error', 
            'action': 'recipient not found', 
            'data': {
                'description': 'recipient not found'
            }
        }
        """
        msg = self.test_UtPwYATxU.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "some_wrong_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
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
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("recipient not found", result["action"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_mppOHwpaZiIzjBgKhYM(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель НЕ зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong` используется.
        
        Проверка:
        (Это деградационный тест.)
        `EventMessage` должен не пройти проверку назначения в 
        `sci_cli.destination_check()`.
        `sci_cli.send_message()` должен вернуть:
        {
            'status': 'error', 
            'action': 'recipient not found', 
            'data': {
                'description': 'recipient not found'
            }
        }
        """
        msg = self.test_mppOHwpaZiIzjBgKhYM.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:wrong_app",
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
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("recipient not found", result["action"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
    
    def test_bRTClXvixdyOwJtiV(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан НЕ поддерживаемый целевым 
            `Application`
        - `ping-pong` используется.
        
        Проверка:    
        (Это деградационный тест.)
        `EventMessage` успешно отправляется.
        `sci_cli.send_message()` должен вернуть `ecssaddo` "status": "ok",
        Поддерживается ли переданный `action` проверяется непосредственно
        в самом `AppController` целевого приложения, поэтому что-бы узнать
        как запрос был обработан в `AppController`, нужно дополнительно
        совершить `await awaitable_response()`
        
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': '', 
                'awaitable_response': <function SCI_cli.convert_to_sci_response.<locals>.wrapper at 0x7f22c605b2e0>
            }
        }
        """
        msg = self.test_bRTClXvixdyOwJtiV.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "wrong-test-action",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {},
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5,
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]), 
            msg=msg
        )
        
        
    def test_nvmDiNHOhKVXHJwJNwLr(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан НЕ поддерживаемый целевым 
            `Application`
        - `ping-pong` используется.
        
        Проверка:
        (Это деградационный тест.)
        `EventMessage` успешно отправляется.
        `sci_cli.send_message()` должен вернуть `ecssaddo` "status": "ok",
        Поддерживается ли переданный `action` проверяется непосредственно
        в самом `AppController` целевого приложения, поэтому что-бы узнать
        как запрос был обраьотан в `AppController`, нужно дополнительно
        совершить `await awaitable_response()`
        
        response.status_code - `404`
        response.response_data - `{}`
        response.session_result - Вся сессия `("status": "ok")`
        """
        msg = self.test_nvmDiNHOhKVXHJwJNwLr.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "wrong-test-action",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True,
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5,
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(404, result.status_code)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_NWFolhHLEUmzpavni(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` используется. 
        - `AppController` искусственно занят, и не может обработать `ping-pong` 
        запрос.
            
        Проверка:
        (Это деградационный тест.)
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(20)` (по умолчанию `"background": False`), 
        в следствии чего `actionHandler`займет весь `AppController`. 
        
        Сразу отправляется второй запрос (по умолчанию `"background": False`)
        с `"ping-pong": True`,  который завершится в `SCI_core.ResponseSession` 
        по `timeout` через 2 секунды.
        Основной `EventMessage` второго запроса не отправится.
        
        `AppController` должен самостоятельно завершить `actionHandler`
        обработки первого запроса через `"max_execution_time"` (5с)
        Настройка установленная в `GenericTest_SCIApp.ACTIONS`
        
        `sci_cli.send_message() отвечает`
        {
            'status': 'error', 
            'action': 'ping-pong timeout', 
            'data': {
                'description': 'ping-pong timeout'
            }
        }
        """
        msg = self.test_NWFolhHLEUmzpavni.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 20,
                        "work_check": True,    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            EventMessage_second = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True,      
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 3,
                }
            }
            send_first_result = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            return send_second_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=3.5)
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("ping-pong timeout", result["action"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_wNpyPOtKRPIGM(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` НЕ отправляется.
        - `AppController` искусственно занят, основной `EventMessage` будет
            проигнорирован
            
        Проверка:
        (Это деградационный тест.)
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(20)` (по умолчанию `"background": False`), 
        в следствии чего `actionHandler`займет весь `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": False`, 
        `"await_timeout": 3`, `"expire_time": 3` 
        (по умолчанию `"background": False`) который
        попадет в очередь ожидания `AppController`.
        Сессия ожидания ответа от второго запроса завершиться по `timeout`
        в `SCI_core.ResponseSession` через 3 секунды.
        
        `AppController` должен самостоятельно завершить `actionHandler`
        обработки первого запроса через `"max_execution_time"` (5с)
        Настройка установленная в `GenericTest_SCIApp.ACTIONS`
        
        `EventMessage` второго запроса имеет `"expire_time": 3`, это означает 
        что когда `AppController` все-таки возьмет второй `EventMessage` из 
        очереди, то он его проигнорирует так как истек `expire_time`.
       
        `sci_cli.send_message()` вернет `ecsaddo`: "ok", так как основной
        `EventMessage` был отправлен.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_wNpyPOtKRPIGM.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 20,
                        "work_check": True    
                    },
                    "meta": {
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            EventMessage_second = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {
                        "expire_time": 3,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 3,
                }
            }
            send_first_result = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            awaitable_response: dict = (
                send_second_result["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=2.1
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
        
        
    def test_sQJEAowOfxYnVmJV(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверка:
        (Это деградационный тест.)
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(3)` (по умолчанию `"background": False`), 
        в следствии чего `actionHandler`займет весь `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": False`, 
        `"await_timeout": 2`, `"expire_time": 20` 
        (по умолчанию `"background": False`) который
        попадет в очередь ожидания `AppController`.
        Сессия ожидания ответа от второго запроса завершиться по `timeout`
        в `SCI_core.ResponseSession` через 2 секунды.
        
        Первый запрос самостоятельно успешно завершиться через 3 с.
        
        `EventMessage` второго запроса имеет `"expire_time": 20`, это означает 
        что когда `AppController` все-таки возьмет второй `EventMessage` из 
        очереди, то он его успешно выполнит.
        
        Первый и вторый запрос успешно выполняются, хоть сессия ожидания ответа
        2-го запроса завершается по `timeout`.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_sQJEAowOfxYnVmJV.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 3,
                        "work_check": True    
                    },
                    "meta": {
                        "max_execution_time": 5
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            EventMessage_second = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_first_result = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            awaitable_response: dict = (
                send_second_result["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)], 
                waiting_after=1.1
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(2, ref_q.qsize(), msg=msg)
        
        
    def test_kJXVSGQPvpKCUrFo(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверка:
        (Это деградационный тест.)
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(3)` (по умолчанию `"background": False`), 
        в следствии чего `actionHandler` займет весь `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": False`, 
        `"await_timeout": 2`, `"expire_time": 2` 
        (по умолчанию `"background": False`) который
        попадет в очередь ожидания `AppController`.
        Сессия ожидания ответа от второго запроса завершиться по `timeout`
        в `SCI_core.ResponseSession` через 2 секунды.
        
        Первый запрос самостоятельно успешно завершиться через 3 с.
        
        `EventMessage` второго запроса имеет `"expire_time": 2`, это означает 
        что когда `AppController` все-таки возьмет второй `EventMessage` из 
        очереди, то он его проигнорирует.
        
        Первый и вторый запрос успешно выполняются.
        Второй запрос не будет выполнен. Сессия ожидания ответа 2-го запроса
        завершиться по `timeout`
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_kJXVSGQPvpKCUrFo.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 3,
                        "work_check": True    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            EventMessage_second = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True    
                    },
                    "meta": {
                        "expire_time": 2,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_first_result = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            awaitable_response: dict = (
                send_second_result["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)], 
                waiting_after=1.1
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(1, ref_q.qsize(), msg=msg)
        
        
    def test_DchxWnGJEhwUduWneBtXD(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверяется:
        
        Оотправляется `EventMessage` `"await_timeout": 2`, `"expire_time": 20`,
        `"max_execution_time": 3`, указывающий `actionHandler` совершить 
        `await asyncio.sleep(20)` (по умолчанию `"background": False`), в 
        следствии чего `actionHandler` займет весь `AppController`.
        
        Запрос не будет (полностью) выполнен, так как `AppController` отменит 
        его через `"max_execution_time": 3` 
        Сессия ожидания ответа запроса завершиться по `timeout`.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_DchxWnGJEhwUduWneBtXD.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_block = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 20,
                        "work_check": True    
                    },
                    "meta": {
                        "max_execution_time": 2,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2.1,
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage_block,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=0.5
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_yUBNhTffjlzurFXU(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не используется.
        
        Проверяется:
        
        Отправляется `EventMessage` `"await_timeout": 1`, `"expire_time": 20`,
        `"max_execution_time": 0.5`, указывающий `actionHandler` совершить 
        `await asyncio.sleep(1.3)` ("background": True`).
        
        Запрос не будет (полностью) выполнен, так как `AppController` отменит 
        его через `"max_execution_time": 0.5`.
         
        Сессия ожидания ответа запроса завершиться по `timeout`.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_yUBNhTffjlzurFXU.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_block = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 1.3,
                        "work_check": True
                    },
                    "meta": {
                        "background": True,
                        "max_execution_time": 0.5,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 1,
                }
            }
            send_result = await self.sci_cli_shadow.send_message(
                EventMessage_block,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=0.5 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"], 
            msg=msg
        )
        self.assertIn("response", result.session_result["data"], msg=msg)
        self.assertEqual(
            None, 
            result.session_result["data"]["response"], 
            msg=msg
        )
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_sLxJsyrHrjxMJirKz(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
    
        Проверка:
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(1.2)` (`"background": True`), 
        в следствии чего `actionHandler` не блокирует `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": False`, 
        `"await_timeout": 1`, `"expire_time": 1` 
        (по умолчанию `"background": False`) который должен сразу успешно 
        выполниться.
        
        Первый запрос - самостоятельно успешно завершиться через 1.2 с.
        Второй запрос - сразу успешно выполняется.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 200
        - response.resposne_data - `{'work': True}`
        - response.session_result - `ecsaddo` всей сессии.
            {
                'status': 'ok', 
                'action': '', 
                'data': {
                    'description': '', 
                    'response': {
                        'sender': 'jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app', 
                        'action': 'test-generic', 
                        'address_section': {
                            'recipient': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'remote-rq'
                        }, 
                        'meta': {
                            'mType': 'response', 
                            'session_id': 'sci_session:PHZ9KCM4y7xciyAnb2OfnRr', 
                            'sci_mode': 'standart'
                        }, 
                        'message_payload': {
                            'data': {
                                'work': True
                            }, 
                            'meta': {
                                'status_code': 200
                            }
                        }
                    }
                }
            }
        """
        msg = self.test_sLxJsyrHrjxMJirKz.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 1.2,
                        "work_check": True 
                    },
                    "meta": {
                        "background": True,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            EventMessage_second = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True
                    },
                    "meta": {
                        "background": False,
                        "expire_time": 1,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 1,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_result_second = await self.sci_cli_shadow.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_second["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=1.3
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 2, msg=msg)
        
        
    def test_JbxhyQCWJxVrlbdDP(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверяется:
        
        Отправляется `EventMessage` `"await_timeout": 0.6`, `"expire_time": 20`,
        `"max_execution_time": 0.3`, указывающий `actionHandler` совершить 
        `await asyncio.sleep(0.5)` ("background": False`).
        
        Запрос не будет (полностью) выполнен, так как `AppController` отменит 
        его через `"max_execution_time": 0.3`.
         
        Сессия ожидания ответа запроса завершиться по `timeout`.
        
        Для получения результата нужно `await awaitable_resposne()`
        - response.status_code - 524
        - response.resposne_data - `{}`
        - response.session_result - `ecsaddo` всей сессии.
        {
            'status': 'error', 
            'action': 'session timeout error', 
            'data': {
                'description': 'session timeout error', 
                'response': None
            }
        }
        """
        msg = self.test_JbxhyQCWJxVrlbdDP.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(5)
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 0.5,
                        "work_check": True 
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 0.3,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 0.6,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=False)],
                waiting_after=0.5
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(524, result.status_code, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("error", result.session_result["status"], msg=msg)
        self.assertEqual(
            "session timeout error", 
            result.session_result["action"],
            msg=msg
        )
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_sTBIZzDZfLFbrkb(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
       - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        Если `actionHandler` отвечает не `ecsaddo`, тогда `messageHandler__pl`
        должен обернуть ответ в `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_sTBIZzDZfLFbrkb.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True,
                        "return_data": [1, 2, 3, 4]
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 10,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5 
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 0, msg=msg)
    
    
    def test_LwpQCVldlekAB(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Если `actionHandler` отвечает `ecsaddo` "status" != "ok"
        тогда `messageHandler__pl` логирует этот `ecsaddo` и отправляет
        `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_LwpQCVldlekAB.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            error_ecsaddo = create_ecsaddo(
                "error",
                "oops error",
                "oops error test"
            )
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "return_data": error_ecsaddo
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                         "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
    
    def test_HBMnaXTcpajNNHkRBj(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        Если `actionHandler` отвечает `ecsaddo` "status" == "ok"
        но в `ecsaddo["data"]` отсутствует ключ `"response_payload"`, или
        значение ключа `"response_payload" не является экземпляром 
        `SCI_ResponsePayload`
        
        тогда `messageHandler__pl` логирует этот `ecsaddo` и отправляет
        `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_HBMnaXTcpajNNHkRBj.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            error_ecsaddo = create_ecsaddo(
                "ok",
                response_payload = 200
            )
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "return_data": error_ecsaddo
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                         "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
        
    def test_wFQNUhUBWUfqSXWNDbYktPdoZBDiWYybUrGSfQR(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        Если `actionHandler` отвечает `ecsaddo` "status" == "ok"
        но в `ecsaddo["data"]` отсутствует ключ `"response_payload"`, или
        значение ключа `"response_payload" не является экземпляром 
        `SCI_ResponsePayload`
        
        тогда `messageHandler__pl` логирует этот `ecsaddo` и отправляет
        `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_wFQNUhUBWUfqSXWNDbYktPdoZBDiWYybUrGSfQR.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            error_ecsaddo = create_ecsaddo("ok")
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "return_data": error_ecsaddo
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                         "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
        
    def test_uvNLEsKOT(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        Если в `actionHandler` возникает исключенеи.
        тогда `messageHandler__pl` логирует этот это исключение в виде
        `ecsaddo` и отправляет `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии. 
        """
        msg = self.test_uvNLEsKOT.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "return_exception": True
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5,
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
        
    def test_YvTvDRBfsZc(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Если `actionHandler` при создании экземпляра `SCI_ResponsePayload`
        передал невалидный `status_code`, то возникает исключение.
        `actionHandler` возвращает `ecsaddo` "status": "ex"
        тогда `messageHandler__pl` логирует этот этот `ecsaddo` "status": "ex"
        и отправляет `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии.
        """
        msg = self.test_YvTvDRBfsZc.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "wrong_status_code": True,
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
    
    def test_ccxvoqHCPZBMqZoeho(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - (`proxy`) 
        `sci_node_appolo` отправляет сообщение в `sci_node_jupiter`.
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Если `actionHandler` при создании экземпляра `SCI_ResponsePayload`
        передал невалидный `response_data`, то возникает исключение.
        `actionHandler` возвращает `ecsaddo` "status": "ex"
        
        тогда `messageHandler__pl` логирует этот этот `ecsaddo` "status": "ex"
        и отправляет `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии.
        """
        msg = self.test_ccxvoqHCPZBMqZoeho.__doc__
        async def send_message(ping_pong: bool = False):
            await asyncio.sleep(WAIT_AUTH)
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "remote-rq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "wrong_response_data": True,
                    },
                    "meta": {
                        "background": False,
                        "max_execution_time": 5,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli_shadow.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = (
                send_result_first["data"]["awaitable_response"]
            )
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)],
                waiting_after=0.5
            )
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(500, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        
        
if __name__ == "__main__":
    unittest.main()