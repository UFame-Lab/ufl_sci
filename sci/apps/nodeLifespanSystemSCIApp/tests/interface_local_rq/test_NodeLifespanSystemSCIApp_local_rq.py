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
import subprocess
import asyncio
import unittest
import traceback
import queue
import time

from typing import Awaitable, Optional
from pathlib import Path

from sci.apps.nodeLifespanSystemSCIApp.application import (
    NodeLifespanSystemSCIApp
)
from sci.app_controllers.base_controller import SCI_BaseAppController
from sci.lib.patterns import create_ecsaddo
from sci.sci_base.sci_base import SCI
from sci.network.utils import create_response_payload
from sci.sci_settings import TEST_LOG_FILE_PATH


ref_q = queue.Queue()
WAIT_AUTH = 1.5

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
            
            
class NodeLifespanSystemSCIApp_UkFrfuBDHUeaWbeWUDHgC(unittest.TestCase):
    """
    Тесты нормальной работы аутентификации NodeLifespanSystemSCIApp
    - `"interface": "local-rq"`
    """
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
        # Завершаем все задачи (в том числе sci_core), кроме текущей.
        for task in asyncio.all_tasks(loop):
            if not task.done() and task.get_name() != current_task_name:
                task.cancel()
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
    
    
    def test_MRnMzqrHZbqXFbNqIrJxuArgGzWhsqndiTsY(self):
        """
        Основные конфигурации:
        - `sci_node_jupiter` - "standart" 
        - `sci_node_appolo` - "standart" 
        
        `sci_node_jupiter` `-(auth)>` `sci_node_appolo`
        
        Проверка:
        `sci_node_jupiter` должен успешно авторизовать `sci_node_appolo`.
        `sci_node_appolo` должен успешно авторизовать `sci_node_jupiter`.
        """
        msg = self.test_MRnMzqrHZbqXFbNqIrJxuArgGzWhsqndiTsY.__doc__
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
                "local_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
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
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            await asyncio.sleep(WAIT_AUTH)
            return True
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertIn(
            "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"], 
            msg=msg
        )        
        self.assertEqual(
            "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["wsBridgeBroker"],
                (tuple, list)
            ),
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            ),
            msg=msg
        )
        self.assertIn(
            "relation_type", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ),
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        ############
        self.assertIn(
            "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"], 
            msg=msg
        )        
        self.assertEqual(
            "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["wsBridgeBroker"],
                (tuple, list)
            ),
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            ),
            msg=msg
        )
        self.assertIn(
            "relation_type", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ),
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        
        
    def test_nRIedrgrpfZqOXEfoRJaoBJTQtgaxniavPUJISICM(self):
        """
        Основные конфигурации:
        - `sci_node_jupiter` - "standart" 
        - `sci_node_appolo` - "standart" 
        
        `sci_node_jupiter` `-(auth)>` `sci_node_appolo`
        
        Проверка:
        `sci_node_appolo` должен успешно авторизовать `sci_node_jupiter`.
        `sci_node_jupiter` должен успешно авторизовать `sci_node_appolo`.
        Тест длится 47 секунд:
        За это время, `sci_node_jupiter` должен 2 раза отправить `ping-pong` 
        в `sci_node_appolo`, при котором происходит обновление поля 
        'time_last_activity'.
        За это время, `sci_node_appolo` должен два раза проверить 
        `time_last_activity` - `sci_node_jupiter` `sub` узла.
        Тест проверяет обновляется ли поле `time_last_activity`
        """
        msg = self.test_nRIedrgrpfZqOXEfoRJaoBJTQtgaxniavPUJISICM.__doc__
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
                "local_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
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
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            start_time = time.time()
            await asyncio.sleep(47)
            return start_time
        start_test = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        time_end_test = time.time()
        self.assertIn(
            "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"], 
            msg=msg
        )        
        self.assertEqual(
            "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["wsBridgeBroker"],
                (tuple, list)
            ),
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            ),
            msg=msg
        )
        self.assertEqual(
            True,             
            (time_end_test - SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertIn(
            "relation_type", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ),
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        ############
        self.assertIn(
            "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"], 
            msg=msg
        )        
        self.assertEqual(
            "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["wsBridgeBroker"],
                (tuple, list)
            ),
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            ),
            msg=msg
        )
        self.assertEqual(
            True,             
            (time_end_test - SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertIn(
            "relation_type", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ),
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        
        
    def test_lokwFusMzaaWpRiUxXsaqKrBrvrRZkVNmfRiQBfuGH(self):
        """
        Основные конфигурации:
        - `sci_node_jupiter` - "standart" 
        - `sci_node_appolo` - "standart" 
        
        Основные условия:
        - `sci_node_jupiter` отправлят запрос аутентификации в 
        неизвестный `sci node`
        
        Проверка:
        `SCI_SETTINGS -> "nodes" -> "local_nodes"` должен быть пустым.
        """
        msg = self.test_lokwFusMzaaWpRiUxXsaqKrBrvrRZkVNmfRiQBfuGH.__doc__
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
                "local_nodes": {
                    "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOdddZ": {
                        "node_rq": "sci_rq_saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOdddZ",
                        "wsBridgeBroker": tuple(),
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
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            start_time = time.time()
            await asyncio.sleep(WAIT_AUTH)
            return start_time
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertEqual(
            0,
            len(SCI_SETTINGS_jupiter["nodes"]["local_nodes"]),
            msg=msg
        )
        
        
    def test_VcyLXuwrFUDmXxeYajaqekjajkvTfufgLxF(self):
        """
        Основные конфигурации:
        - `sci_node_jupiter` - "standart" 
        - `sci_node_appolo` - "standart"
        
        `sci_node_jupiter` `-(auth)>` `sci_node_appolo`
        `sci_node_appolo` `-(auth)>` `sci_node_jupiter`
        
        Проверка:        
        Если два узла совершают перекрестную аутентификацию, то такая
        аутентификация будет выполнена (дважды), в 
        `SCI_SETTINGS -> "nodes" -> "local_nodes" / "remote_nodes" / "remote_ws_nodes"`
        будет добавлен соответствующий узел либо от `NodeLifespanSystemSCIApp` -
        `recovery`, либо от `NodeLifespanSystemSCIApp` `"node-authentication"`,
        Отличие будет только в поле 
        `"relation_type": "related_main" / "related_sub"`.
        Так же при перекрестной аутентификации, `sci_node_jupiter` будет 
        одновременно отправлять `ping-pong` запрос в `sci_node_appolo`, так и 
        совершать проверки активности `sci_node_appolo` на основе поля 
        `"time_last_activity"`, зеркально тоже самое будет делать и 
        `sci_node_appolo`.
        Перекрестная аутентификация не должна вызывать конфликт между 
        `NodeLifespanSystemSCIApp` - `recovery` (отправка запроса), и 
        `NodeLifespanSystemSCIApp` `"node-authentication"` (принятие запроса) 
        при удалении не активного узла из `SCI_SETTINGS -> "nodes"`.
        
        NOTE WARNING: Ситуация когда два узла совершают перекрестную аутентификацию 
        является ошибкой конфигурации `SCI` узлов и может привести к неожиданным
        последствиям.
        """
        msg = self.test_VcyLXuwrFUDmXxeYajaqekjajkvTfufgLxF.__doc__
        context_appolo = {
            "auth_nodes_settings": {
                "local_nodes": {
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
                    }
                }
            }
        }
        SCI_SETTINGS_appolo = {
            "node_name": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", context_appolo)
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
                "local_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
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
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            await asyncio.sleep(47)
            return True
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        time_end_test = time.time()
        self.assertIn(
            "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"], 
            msg=msg
        )        
        self.assertEqual(
            "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["wsBridgeBroker"],
                (tuple, list)
            ),
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            ),
            msg=msg
        )
        self.assertEqual(
            True,
            (time_end_test - 
             SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
             )["time_last_activity"] <= 26),
            msg=msg
        )
        self.assertIn(
            "relation_type", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ),
            msg=msg
        )
        ############
        self.assertIn(
            "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"], 
            msg=msg
        )        
        self.assertEqual(
            "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["wsBridgeBroker"],
                (tuple, list)
            ),
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            ),
            msg=msg
        )
        self.assertEqual(
            True,
            (time_end_test - 
             SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
             )["time_last_activity"] <= 26),
            msg=msg
        )
        self.assertIn(
            "relation_type", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ),
            msg=msg
        )
    
    
class NodeLifespanSystemSCIApp_nuIoWvkpknQCigOxf(unittest.TestCase):
    """
    Тесты нормальной работы аутентификации NodeLifespanSystemSCIApp
    - `"interface": "local-rq"`
    
    Данные тесты проверяют ситуации когда `sci_node_appolo` (который по отношению
    к `sci_node_jupiter` является `related_main`), в какой-то момент времени
    отключается.
    """
            
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
        self.background_processes = set()
        current_task_name = "async_test_runner"
        loop = asyncio.get_event_loop()
        asyncio.current_task(loop).set_name(current_task_name)
        # Запуск sci_core_appolo
        process_sci_node_appolo = self.start_sci_node_process()
        # Регистрация `callback` на остановку `sci_node_fn`
        loop.call_later(10, self.process_resolver, process_sci_node_appolo)
        # Запуск sci_core second_node
        task_sci_core_jupiter = asyncio.create_task(self.sci_core_jupiter())
        # Ожидание запуска всех `sci_node`.
        await asyncio.sleep(1)
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_core_jupiter)
        for future in asyncio.as_completed(futures):
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            break
        # Начинается очистка
        # Завершаем все задачи (в том числе sci_core), кроме текущей.
        for task in asyncio.all_tasks(loop):
            if not task.done() and task.get_name() != current_task_name:
                task.cancel()
        # Завершаем все дочернии процессы.
        for process in self.background_processes:
            process.terminate()
            code = process.wait()
        # Закрываем redis подключения всех `sci_core`
        redis_conn_jupiter = (
            self.sci_core_jupiter.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_jupiter.close()
        # Возвращаем результат первой завершенной задачи
        return res        
        
    
    def start_sci_node_process(self) -> subprocess.Popen:
        path_to_module = str(
            str(Path(__file__).resolve().parent) + 
            "/node_templates/sci_node_appolo.py"
        )
        process = subprocess.Popen(["python3.11", path_to_module])
        self.background_processes.add(process)
        return process


    def process_resolver(self, process: subprocess.Popen) -> None:
        process.terminate()
        code = process.wait()
        self.background_processes.discard(process)
        
        
    def test_wSyvhHEIlUCAcwXuzGFlPHDQKpjsgftLEpwgR(self):
        """
        Основные конфигурации:
        - `sci_node_jupiter` - "standart" 
        - `sci_node_appolo` - "standart"
        
        `sci_node_jupiter` `-(auth)>` `sci_node_appolo`
        
        Проверка:
        Через 10 секунд работы выключается `sci_node_appolo`.
        Еще через 10 секунд, (на 20 секунде) `sci_node_jupiter` должен отправить
        первый `ping_pong` запрос в `sci_node_appolo`, но так как 
        `sci_node_appolo` выключен, то `ping-pong` завершится неудачей.
        Так как `ping-pong` завершился неудачей, то `sci_node_jupiter` должен
        удалить узел `sci_node_appolo` из 
        `SCI_SETTINGS -> "nodes" -> "local_nodes"`.
        `sci_node_appolo` удалит `sci_node_jupiter` только на 40 секунде после
        2 проверки `time_last_activity`.
        
        Некоторые тесты создают дочерние процессы и самостоятельно завершают их 
        по завершению. NOTE: Поэтому не рекомендуется самостоятельно прерывать 
        тест в середине его выполнения с помощью `Ctrl + Z` (`KeyboardInterrupt`), 
        так это может привести к ситуации, когда дочерний процесс не сможет 
        автоматически завершиться, и придется вручную отправлять команду для 
        его завершения.
        """
        msg = self.test_wSyvhHEIlUCAcwXuzGFlPHDQKpjsgftLEpwgR.__doc__
        context_jupiter = {
            "auth_nodes_settings": {
                "local_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
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
        sci_jupiter = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_jupiter)
        self.sci_cli_jupiter, self.sci_core_jupiter = sci_jupiter.start()
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            time_start_test = time.time()
            await asyncio.sleep(26)
            return time_start_test
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        self.assertEqual(
            0,
            len(SCI_SETTINGS_jupiter["nodes"]["local_nodes"]),
            msg=msg
        )
        

class NodeLifespanSystemSCIApp_huqbuxryzRWpGFFPl(unittest.TestCase):
    """
    Тесты нормальной работы аутентификации NodeLifespanSystemSCIApp
    - `"interface": "local-rq"`
    
    Данные тесты проверяют ситуации когда `sci_node_appolo` (который по отношению
    к `sci_node_jupiter` является `related_main`), в какой-то момент времени
    отключается, и спустя некоторое время снова запускается.
    """         
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
        self.background_processes = set()
        current_task_name = "async_test_runner"
        loop = asyncio.get_event_loop()
        asyncio.current_task(loop).set_name(current_task_name)
        # Запуск sci_core_appolo
        process_sci_node_appolo = self.start_sci_node_process()
        # Регистрация `callback` на остановку `sci_node_fn`
        loop.call_later(10, self.process_resolver, process_sci_node_appolo)
        # Регистрация `callback` на запуск `sci_node_fn`
        loop.call_later(27, self.start_sci_node_process)
        # Запуск sci_core second_node
        task_sci_core_jupiter = asyncio.create_task(self.sci_core_jupiter())
        # Ожидание пока запустятся оба `sci_core`
        await asyncio.sleep(1) 
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_core_jupiter)
        for future in asyncio.as_completed(futures):       
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            break
        # Начинается очистка
        # Завершаем все задачи (в том числе sci_core), кроме текущей.
        for task in asyncio.all_tasks(loop):
            if not task.done() and task.get_name() != current_task_name:
                task.cancel()
        # Завершаем дочернии процессы.
        for process in self.background_processes:
            process.terminate()
            code = process.wait()
        # Закрываем redis подключения всех `sci_core`
        redis_conn_jupiter = (
            self.sci_core_jupiter.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_jupiter.close()
        # Возвращаем результат первой завершенной задачи
        return res        
    

    def start_sci_node_process(self) -> subprocess.Popen:
        path_to_module = str(
            str(Path(__file__).resolve().parent) + 
            "/node_templates/sci_node_appolo.py"
        )
        process = subprocess.Popen(["python3.11", path_to_module])
        self.background_processes.add(process)
        return process


    def process_resolver(self, process: subprocess.Popen) -> None:
        process.terminate()
        code = process.wait()
        self.background_processes.discard(process)
    

    def test_vGEDhVJXEtUjkQAaWOcSdwUEYvQDna(self):
        """
        Основные конфигурации:
        - `sci_node_jupiter` - "standart" 
            (В текущем процессе)
        - `sci_node_appolo` - "standart"
            (В дочернем процессе)
        
        `sci_node_jupiter` `-(auth)>` `sci_node_appolo`
        
        Проверка:
        На 10 секунде процесс `sci_node_appolo` принудительно завершается.
        На 20 секунде `sci_node_jupiter` отправляет первый `ping-pong` запрос
        в `sci_node_appolo`. Ответ на `ping-pong` запрос ожидается 5 секунд.
        На 26 секунде `sci_node_jupiter` удаляет `sci_node_appolo` из 
        `SCI_SETTINGS -> "nodes" -> "local_nodes"`.
        `NodeLifespanSystemSCI` добавляет `sci_node_appolo` в очередь на 
        `recovery`. На `27` секунде снова запускается `sci_node_appolo` 
        (в дочернем процессе)
        На 28 сеукунде `NodeLifespanSystemSCI` отправляет первый `recovery`
        запрос аутентификации в `sci_node_appolo`. Если `sci_node_appolo` успел
        запуститься, то он принимает этот запрос аутентификации.
        `sci_node_jupiter` добавляет `sci_node_appolo` в 
        `"SCI_SETTINGS" -> "nodes" -> "local_nodes"`.
        На ~47 секуде, `sci_node_jupiter` отправит `ping-pong` запрос в 
        `sci_node_appolo`,
        в следствии чего будет обновлено значение `"time_last_activity"`.
        P.S: Если к 28 секунде `sci_node_appolo` не успел запуститься, то 
        `sci_node_jupiter` отправит следующий `recovery` запрос на  32 секунде.
        
        Некоторые тесты создают дочерние процессы и самостоятельно завершают их 
        по завершению. NOTE: Поэтому не рекомендуется самостоятельно прерывать 
        тест в середине его выполнения с помощью `Ctrl + Z` (`KeyboardInterrupt`), 
        так это может привести к ситуации, когда дочерний процесс не сможет 
        автоматически завершиться, и придется вручную отправлять команду для 
        его завершения.
        """
        msg = self.test_vGEDhVJXEtUjkQAaWOcSdwUEYvQDna.__doc__
        context_jupiter = {
            "auth_nodes_settings": {
                "local_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
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
        sci_jupiter = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_jupiter)
        self.sci_cli_jupiter, self.sci_core_jupiter = sci_jupiter.start()
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            time_start_test = time.time()
            await asyncio.sleep(50) # 50
            return time_start_test
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        time_end_test = time.time()
        self.assertIn(
            "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"], 
            msg=msg
        )        
        self.assertEqual(
            "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["wsBridgeBroker"],
                (tuple, list)
            ),
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            ),
            msg=msg
        )
        self.assertEqual(
            True,
            (time_end_test - 
             SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
             )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main", 
            SCI_SETTINGS_jupiter["nodes"]["local_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        
        
class NodeLifespanSystemSCIApp_dTlHQOVtJRfiYtClocLuRHBAsy(unittest.TestCase):
    """
    Тесты нормальной работы аутентификации NodeLifespanSystemSCIApp
    - `"interface": "local-rq"`
    
    Данные тесты проверяют ситуации когда `sci_node_jupiter` 
    (который по отношению к `sci_node_appolo` является `related_sub`), 
    в какой-то момент времени
    отключается.
    """ 
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
        self.background_processes = set()
        current_task_name = "async_test_runner"
        loop = asyncio.get_event_loop()
        asyncio.current_task(loop).set_name(current_task_name)
        # Запуск `sci_node_jupiter`
        process_sci_node_jupiter = self.start_sci_node_process()
        # Регистрация `callback` на завершение `sci_node_sn`
        loop.call_later(10, self.process_resolver, process_sci_node_jupiter)
        # Запуск `sci_node_fn`
        task_sci_core_appolo = asyncio.create_task(self.sci_core_appolo())
        # Ожидание пока запустятся оба `sci_core`
        await asyncio.sleep(1) 
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_core_appolo)
        for future in asyncio.as_completed(futures):       
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            break
        # Начинается очистка
        # Завершаем все задачи (в том числе sci_core) кроме текущей.
        for task in asyncio.all_tasks(loop):
            if not task.done() and task.get_name() != current_task_name:
                task.cancel()
        # Завершаем все дочернии процессы.
        for process in self.background_processes:
            process.terminate()
            code = process.wait()
        # Закрываем redis подключения всех `sci_core`
        redis_conn_appolo = (
            self.sci_core_appolo.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_appolo.close()
        # Возвращаем результат первой завершенной задачи
        return res        
    

    def start_sci_node_process(self) -> subprocess.Popen:
        path_to_module = str(
            str(Path(__file__).resolve().parent) + 
            "/node_templates/sci_node_jupiter_auth_appolo_use_local_rq.py"
        )
        process = subprocess.Popen(["python3.11", path_to_module])
        self.background_processes.add(process)
        return process


    def process_resolver(self, process: subprocess.Popen) -> None:
        process.terminate()
        code = process.wait()
        self.background_processes.discard(process)
    

    def test_vGEDhVJXEtUjkQAaWOcSdwUEYvQDna(self):
        """
        Основные конфигурации:
        - `sci_node_jupiter` - "standart" / 
            (В дочернем процессе)
        - `sci_node_appolo` - "standart" /
            (В текущем процессе)
            
        `sci_node_jupiter` `-(auth)>` `sci_node_appolo`
        
        Проверка:
        На 10 секунде `sci_node_jupiter` принудительно завершается.
        На 20 секунде `sci_node_appolo` выполняет первую проверку активности 
        `sci_node_jupiter`. Разница между текущим временем и `time_last_activity`
        `sci_node_jupiter` не превысит 26 секунд 
        (настройка `max_related_sub_nodes_latency_activity`).
        На 40 секунде `sci_node_appolo` снова выполняет проверку активности 
        `sci_node_jupiter` узла. Разница между текущим временм и 
        `time_last_actibity` `sci_node_jupiter` превысит 26 секунд 
        (настройка `max_related_sub_nodes_latency_activity`), `sci_node_appolo`
        удаляет `sci_node_jupiter` из 
        `SCI_SETTINGS -> "nodes" -> "local_nodes"`.
        
        Некоторые тесты создают дочерние процессы и самостоятельно завершают их 
        по завершению. NOTE: Поэтому не рекомендуется самостоятельно прерывать 
        тест в середине его выполнения с помощью `Ctrl + Z` (`KeyboardInterrupt`), 
        так это может привести к ситуации, когда дочерний процесс не сможет 
        автоматически завершиться, и придется вручную отправлять команду для 
        его завершения.
        """
        msg = self.test_vGEDhVJXEtUjkQAaWOcSdwUEYvQDna.__doc__
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
        sci_appolo = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_appolo)
        self.sci_cli_appolo, self.sci_core_appolo = sci_appolo.start()
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            time_start_test = time.time()
            await asyncio.sleep(47)
            return time_start_test
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        time_end_test = time.time()
        self.assertEqual(
            0,
            len(SCI_SETTINGS_appolo["nodes"]["local_nodes"]),
            msg=msg
        )
        
        
class NodeLifespanSystemSCIApp_RNxYbJfemexPlmwCFnlt(unittest.TestCase):
    """
    Тесты нормальной работы аутентификации NodeLifespanSystemSCIApp
    - `"interface": "local-rq"`
    
    Данные тесты проверяют ситуации когда `sci_node_jupiter` (который по отношению
    к `sci_node_appolo` является `related_sub`), в какой-то момент времени
    отключается, и спустя некоторое время снова запускается.
    """     
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
        self.background_processes = set()
        current_task_name = "async_test_runner"
        loop = asyncio.get_event_loop()
        asyncio.current_task(loop).set_name(current_task_name)
        # Запуск `sci_node_jupiter`
        process_sci_node_jupiter = self.start_sci_node_process()
        # Регистрация `callback` на завершение `sci_node_sn`
        loop.call_later(10, self.process_resolver, process_sci_node_jupiter)
        # Регистрация `callback` на запуск `sci_node_sn`
        loop.call_later(43, self.start_sci_node_process)
        # Запуск `sci_node_fn`
        task_sci_core_appolo = asyncio.create_task(self.sci_core_appolo())
        # Ожидание пока запустятся оба `sci_core`
        await asyncio.sleep(1) 
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_core_appolo)
        for future in asyncio.as_completed(futures):       
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            break
        # Начинается очистка
        # Завершаем все задачи (в том числе sci_core), кроме текущей.
        for task in asyncio.all_tasks(loop):
            if not task.done() and task.get_name() != current_task_name:
                task.cancel()
        # Завершение всех дочерних процессов.
        for process in self.background_processes:
            process.terminate()
            code = process.wait()
        # Закрываем redis подключения всех `sci_core`
        redis_conn_appolo = (
            self.sci_core_appolo.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_appolo.close()
        # Возвращаем результат первой завершенной задачи
        return res        
    

    def start_sci_node_process(self) -> subprocess.Popen:
        path_to_module = str(
            str(Path(__file__).resolve().parent) + 
            "/node_templates/sci_node_jupiter_auth_appolo_use_local_rq.py"
        )
        process = subprocess.Popen(["python3.11", path_to_module])
        self.background_processes.add(process)
        return process


    def process_resolver(self, process: subprocess.Popen) -> None:
        process.terminate()
        code = process.wait()
        self.background_processes.discard(process)
    

    def test_vGEDhVJXEtUjkQAaWOcSdwUEYvQDna(self):
        """
        Основные конфигурации:
        - `sci_node_jupiter` - "standart" 
            (В дочернем процессе)
        - `sci_node_appolo` - "standart"
            (В текущем процессе)
        
        `sci_node_jupiter` `-(auth)>` `sci_node_appolo`
        
        Проверка:
        На 10 секунде `sci_node_jupiter` принудительно завершается.
        На 20 секунде `sci_node_appolo` выполняет первую проверку активности 
        `sci_node_jupiter`. Разница между текущим временем и `time_last_activity`
        `sci_node_jupiter` не превысит 26 секунд 
        (настройка `max_related_sub_nodes_latency_activity`).
        На 40 секунде `sci_node_appolo` снова выполняет проверку активности 
        `sci_node_jupiter` узла, разница между текущим временм и 
        `time_last_actibity` `sci_node_jupiter` превысит 26 секунд. 
        (настройка `max_related_sub_nodes_latency_activity`), `sci_node_appolo`
        удаляет `sci_node_jupiter` из 
        `SCI_SETTINGS -> "nodes" -> "local_nodes"`.
        На 43 секунде снова запускается `sci_node_jupiter` (В дочернем процессе).
        `sci_node_jupiter` отправляет запрос аутентификации в `sci_node_appolo`.
        Аутентификация успешно выполняется.
        `sci_node_appolo` возвращает 
        `sci_node_jupiter` в `SCI_SETTINGS -> "nodes" -> "local_nodes"`.
        На 63 секунде `sci_node_jupiter` отправляет `ping-pong` запрос в 
        `sci_node_appolo`.
        На 63 секунде `sci_node_appolo` выполняет проверку активности 
        `sci_node_jupiter` узла. 
        Разница между текущим временм и `time_last_actibity`
        `sci_node_jupiter` не превысит 26 секунд, `sci_node_jupiter` остается в
        `SCI_SETTINGS -> "nodes" -> "local_nodes"`.
        
        Некоторые тесты создают дочерние процессы и самостоятельно завершают их 
        по завершению. NOTE: Поэтому не рекомендуется самостоятельно прерывать 
        тест в середине его выполнения с помощью `Ctrl + Z` (`KeyboardInterrupt`), 
        так это может привести к ситуации, когда дочерний процесс не сможет 
        автоматически завершиться, и придется вручную отправлять команду для 
        его завершения.
        """
        msg = self.test_vGEDhVJXEtUjkQAaWOcSdwUEYvQDna.__doc__
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
        sci_appolo = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_appolo)
        self.sci_cli_appolo, self.sci_core_appolo = sci_appolo.start()
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            time_start_test = time.time()
            await asyncio.sleep(65) # 65
            return time_start_test
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        time_end_test = time.time()
        self.assertIn(
            "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"], 
            msg=msg
        )        
        self.assertEqual(
            "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["wsBridgeBroker"],
                (tuple, list)
            ),
            msg=msg
        )
        self.assertEqual(
            True, 
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            ),
            msg=msg
        )
        self.assertEqual(
            True,
            (time_end_test - 
             SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
             )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub", 
            SCI_SETTINGS_appolo["nodes"]["local_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        

if __name__ == "__main__":
    unittest.main()