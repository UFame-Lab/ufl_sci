"""
Данный модуль предоставляет тесты проверяющие работоспособность `lifespan` цикла 
взаимодействия узлов от `NodeLifespanSystemSCIApp`.

Время выполнения многих тестов может превышать 30 секунд.

Некоторые тесты создают дочерние процессы и самостоятельно завершают их 
по завершению. NOTE: Поэтому не рекомендуется самостоятельно прерывать 
тест в середине его выполнения с помощью `Ctrl + Z` (`KeyboardInterrupt`), 
так это может привести к ситуации, когда дочерний процесс не сможет 
автоматически завершиться, и придется вручную отправлять команду для 
его завершения.

TBD:
Добавить автоматическую систему `terminate` / `startup` дочерних процессов 
на основе `PID` файлов.
"""
import asyncio
import unittest
import traceback
import queue
import time

from typing import Awaitable, Optional

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
            
            
class NodeLifespanSystemSCIApp_ogAVOwUglrpWgNNIYUsuNZyIkkd(unittest.TestCase):
    """
    Тесты нормальной работы аутентификации NodeLifespanSystemSCIApp
    При использовании всех интерфейсов
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
        # Запуск sci_core first_node
        task_sci_node_sunny = asyncio.create_task(self.sci_core_sunny())
        task_sci_node_appolo = asyncio.create_task(self.sci_core_appolo())
        task_sci_node_jupiter = asyncio.create_task(self.sci_core_jupiter())
        task_sci_node_neptun = asyncio.create_task(self.sci_core_neptun())
        task_sci_node_saturn = asyncio.create_task(self.sci_core_saturn())
        # Запуск пользовательских test_async_payload
        while True:
            core_is_ready = [
                self.sci_core_sunny.is_working, 
                self.sci_core_appolo.is_working,
                self.sci_core_jupiter.is_working, 
                self.sci_core_neptun.is_working,
                self.sci_core_saturn.is_working,
            ]
            if not all(core_is_ready):
                await asyncio.sleep(0.1)
                continue
            break
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_node_sunny)
        futures.append(task_sci_node_appolo)
        futures.append(task_sci_node_jupiter)
        futures.append(task_sci_node_neptun)
        futures.append(task_sci_node_saturn)
        for future in asyncio.as_completed(futures):
            res = await future
            # Первая завершенная задача.
            await asyncio.sleep(waiting_after)
            break
        # Начинается очистка
        # Завершаем все задачи (в том числе sci_core), кроме текущей.
        for task in asyncio.all_tasks(loop):
            if not task.done() and task.get_name() != current_task_name:
                task.cancel()
        # Закрываем redis подключения всех `sci_core`
        redis_conn_sunny = (
            self.sci_core_sunny.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_sunny.close()
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
        redis_conn_neptun = (
            self.sci_core_neptun.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_neptun.close()
        redis_conn_saturn = (
            self.sci_core_saturn.SCI_SETTINGS.get(
                "local_broker_connection_settings"
            )["redis"]["redis_conn"]
        )
        await redis_conn_saturn.close()
        # Возвращаем результат первой завершенной задачи
        return res
    
    
    def test_kOkhnwpSDFTDpyxiwjQABGRGUgTbiOstaWBLuxl(self):
        """
        """   
        msg = self.test_kOkhnwpSDFTDpyxiwjQABGRGUgTbiOstaWBLuxl.__doc__
        SCI_SETTINGS_sunny = {
            "node_name": "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
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
            "websocket_connections": {
                "alfaBridge": {
                    "url": "ws://localhost:8555/wsbridge/",
                    "headers": {
                        "wsbridge-key": "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
                    },
                    "wsBridgeBroker_aq": asyncio.Queue(),
                },    
            },
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
        context_appolo = {
            "auth_nodes_settings": {
                "remote_nodes": {
                    "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
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
                },
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
            "websocket_connections": {
                "alfaBridge": {
                    "url": "ws://localhost:8555/wsbridge/",
                    "headers": {
                        "wsbridge-key": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    },
                    "wsBridgeBroker_aq": asyncio.Queue(),
                }    
            },
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
                "remote_ws_nodes": {
                    "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ": {
                        "wsbridge": "alfaBridge",
                    },
                    "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "wsbridge": "alfaBridge",
                    },
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
            "websocket_connections": {
                "alfaBridge": {
                    "url": "ws://localhost:8555/wsbridge/",
                    "headers": {
                        "wsbridge-key": "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    },
                    "wsBridgeBroker_aq": asyncio.Queue(),
                },    
            },
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
        context_saturn = {
            "auth_nodes_settings": {
                "local_nodes": {
                    "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
                    }
                },
            }
        }
        SCI_SETTINGS_saturn = {
            "node_name": "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", context_saturn)
            ],
            "nodes": {
                "local_nodes": {},
                "remote_nodes": {},
                "remote_ws_nodes": {},
            },
            "websocket_connections": {
                "alfaBridge": {
                    "url": "ws://localhost:8555/wsbridge/",
                    "headers": {
                        "wsbridge-key": "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    },
                    "wsBridgeBroker_aq": asyncio.Queue(),
                },    
            },
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
        context_neptun = {
            "auth_nodes_settings": {
                "remote_ws_nodes": {
                    "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ": {
                        "wsbridge": "alfaBridge",
                        "dependent": True,
                    },
                },
                "remote_nodes": {
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
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
                    },
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
                    },
                    "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
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
                    },
                },
            }
        }
        SCI_SETTINGS_neptun = {
            "node_name": "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {}),
                (NodeLifespanSystemSCIApp, "node_lifespan_system_app", context_neptun)
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
        sci_sunny = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_sunny)
        self.sci_cli_sunny, self.sci_core_sunny = sci_sunny.start()
        sci_appolo = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_appolo)
        self.sci_cli_appolo, self.sci_core_appolo = sci_appolo.start()
        sci_jupiter = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_jupiter)
        self.sci_cli_jupiter, self.sci_core_jupiter = sci_jupiter.start()
        sci_neptun = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_neptun)
        self.sci_cli_neptun, self.sci_core_neptun = sci_neptun.start()
        sci_saturn = SCI(sci_mode="standart", SCI_SETTINGS=SCI_SETTINGS_saturn)
        self.sci_cli_saturn, self.sci_core_saturn = sci_saturn.start()
        async def send_message(ping_pong: bool = False) -> dict:
            # Время на утентификацию и `handshake`
            await asyncio.sleep(65) # 60
            return True
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)])
        )
        time_end_test = time.time()
        #########
        # sunny #
        #########
        self.assertIn(
            "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_sunny["nodes"]["remote_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_sunny["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "alfaBridge",
            SCI_SETTINGS_sunny["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsBridgeBroker"],
            msg=msg
        )
        self.assertIn(
            "broker_connection_settings",
            SCI_SETTINGS_sunny["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_sunny["nodes"]["remote_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_sunny["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_sunny["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"],
            msg=msg
        )
        self.assertEqual(
            "alfaBridge",
            SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsbridge"],
            msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"],
            msg=msg
        )
        self.assertEqual(
            "alfaBridge",
            SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsbridge"],
            msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"].get(
                    "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_sunny["nodes"]["remote_ws_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_sunny["nodes"]["local_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_sunny["nodes"]["local_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "alfaBridge",
            SCI_SETTINGS_sunny["nodes"]["local_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsBridgeBroker"],
            msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_sunny["nodes"]["local_nodes"].get(
                    "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_sunny["nodes"]["local_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_sunny["nodes"]["local_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #########
        # appolo #
        #########
        self.assertIn(
            "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "wsBridgeBroker",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertIn(
            "broker_connection_settings",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                    "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "alfaBridge",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["wsBridgeBroker"], 
            msg=msg
        )
        self.assertIn(
            "broker_connection_settings",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                    "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_appolo["nodes"]["remote_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        ##########
        # jupiter #
        ##########
        self.assertIn(
            "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_jupiter["nodes"]["remote_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_jupiter["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "wsBridgeBroker",
            SCI_SETTINGS_jupiter["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertIn(
            "broker_connection_settings",
            SCI_SETTINGS_jupiter["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["remote_nodes"].get(
                    "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_jupiter["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_jupiter["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"],
            msg=msg
        )
        self.assertEqual(
            "alfaBridge",
            SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["wsbridge"], msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"].get(
                    "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"],
            msg=msg
        )
        self.assertEqual(
            "alfaBridge",
            SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsbridge"], msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"].get(
                    "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_jupiter["nodes"]["remote_ws_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        ##########
        # neptun #
        ##########
        self.assertIn(
            "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "alfaBridge",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsBridgeBroker"], msg=msg
        )
        self.assertIn(
            "broker_connection_settings",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                    "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "saturn_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "alfaBridge",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsBridgeBroker"], msg=msg
        )
        self.assertIn(
            "broker_connection_settings",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "alfaBridge",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsBridgeBroker"], msg=msg
        )
        self.assertIn(
            "broker_connection_settings",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_neptun["nodes"]["remote_nodes"].get(
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_neptun["nodes"]["remote_ws_nodes"],
            msg=msg
        )
        self.assertEqual(
            "alfaBridge",
            SCI_SETTINGS_neptun["nodes"]["remote_ws_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["wsbridge"], msg=msg
        )
        self.assertEqual(
            True,
            SCI_SETTINGS_neptun["nodes"]["remote_ws_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["dependent"], msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_neptun["nodes"]["remote_ws_nodes"].get(
                    "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_neptun["nodes"]["remote_ws_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_neptun["nodes"]["remote_ws_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        ##########
        # saturn #
        ##########
        self.assertIn(
            "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_saturn["nodes"]["remote_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_saturn["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["node_rq"],
            msg=msg
        )
        self.assertIn(
            "wsBridgeBroker",
            SCI_SETTINGS_saturn["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertIn(
            "broker_connection_settings",
            SCI_SETTINGS_saturn["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            ), msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_saturn["nodes"]["remote_nodes"].get(
                    "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_saturn["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_saturn["nodes"]["remote_nodes"].get(
                "neptun_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_saturn["nodes"]["remote_ws_nodes"],
            msg=msg
        )
        self.assertEqual(
            "alfaBridge",
            SCI_SETTINGS_saturn["nodes"]["remote_ws_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["wsbridge"], msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_saturn["nodes"]["remote_ws_nodes"].get(
                    "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_saturn["nodes"]["remote_ws_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_sub",
            SCI_SETTINGS_saturn["nodes"]["remote_ws_nodes"].get(
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        #
        self.assertIn(
            "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_saturn["nodes"]["local_nodes"],
            msg=msg
        )
        self.assertEqual(
            "sci_rq_sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ",
            SCI_SETTINGS_saturn["nodes"]["local_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["node_rq"], 
            msg=msg
        )
        self.assertIn(
            "alfaBridge",
            SCI_SETTINGS_saturn["nodes"]["local_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["wsBridgeBroker"], 
            msg=msg
        )
        self.assertEqual(
            True,
            isinstance(
                SCI_SETTINGS_saturn["nodes"]["local_nodes"].get(
                    "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
                )["time_last_activity"], (int, float)
            )
        )
        self.assertEqual(
            True,
            (time_end_test - SCI_SETTINGS_saturn["nodes"]["local_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["time_last_activity"]) <= 26,
            msg=msg
        )
        self.assertEqual(
            "related_main",
            SCI_SETTINGS_saturn["nodes"]["local_nodes"].get(
                "sunny_node_aCtn4R2k3qPtziyBEM6ntdvEwjdDr7ulRz5WQHDbOZ"
            )["relation_type"],
            msg=msg
        )
        

if __name__ == "__main__":
    unittest.main()
        
    