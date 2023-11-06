import asyncio
import unittest
import traceback
import queue

from typing import Awaitable, Optional

from sci.app_controllers.base_controller import SCI_BaseAppController
from sci.lib.patterns import create_ecsaddo, isecsaddo
from sci.sci_base.sci_base import SCI
from sci.network.utils import create_response_payload
from sci.sci_settings import TEST_LOG_FILE_PATH


ref_q = queue.Queue()


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
        
    
class SCI_node_test_wIQcfmhrhVfEnqasTGWdmRMFwAxKvocLK(unittest.TestCase):
    """
    - `"sci_mode": "only_local"`
    - `without await response`
    - `"interface": "local-aq"`
    """

    def get_settings(self):
        SCI_SETTINGS = {
            "node_name": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (GenericTest_SCIApp, "generic_test_app", {})
            ],
        }
        return SCI_SETTINGS
    
    
    def setUp(self):
        SCI_SETTINGS = self.get_settings()
        sci = SCI(sci_mode="only_local", SCI_SETTINGS=SCI_SETTINGS)
        sci_cli, sci_core = sci.start()
        self.sci_cli = sci_cli
        self.sci_core = sci_core
        
        
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
        # Запуск sci_core
        sci_core_task = asyncio.create_task(self.sci_core())
        # Запуск пользовательских test_async_payload
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(sci_core_task)
        for future in asyncio.as_completed(futures):
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            return res
        
    
    def test_BUjhcAxYiWfbuPKqrY(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        - `ping-pong` не отправляется.
        
        Проверяется:
        Это тест нормальной работы.
        `actionHandler` должен успешно отработать.
        `sci_cli.send_message()` должен вернуть
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': ''
            }
        }
        """
        msg = self.test_BUjhcAxYiWfbuPKqrY.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
                    "isAwaiting": False,
                }
            }
            send_result = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)], 
            waiting_after=0.1
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertEqual(1, ref_q.qsize(), msg=msg)
        
        
    def test_EzBDOrUyzjQbJyHjEFTwuQdxFxbpqyfs(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        `actionHandler` должен успешно отработать.
        `sci_cli.send_message()` должен вернуть
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': ''
            }
        }
        """
        msg = self.test_EzBDOrUyzjQbJyHjEFTwuQdxFxbpqyfs.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
                    "isAwaiting": False,
                }
            }
            send_result = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)], 
            waiting_after=0.1
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertEqual(1, ref_q.qsize(), msg=msg)
        
        
    def test_nShByoChmekcJnbiXOPsKQUilJfkRu(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - неизвестный `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        `EventMessage` не пройдет валидацию в `SCI_cli.destination_check()`
        
        `sci_cli.send_message()` должен вернуть
        {
            'status': 'error', 
            'action': 'recipient not found', 
            'data': {
                'description': 'recipient not found'
            }
        }
        """
        msg = self.test_nShByoChmekcJnbiXOPsKQUilJfkRu.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "wrong_test_node:generic_test_app",
                    "interface": "local-aq",
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
                    "isAwaiting": False,
                }
            }
            send_result = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)], 
            waiting_after=0.1
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("recipient not found", result["action"], msg=msg)
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_ELRzfnafgajHutgkSrbhOUpiMTKcoRj(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель НЕ зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        `EventMessage` не пройдет валидацию в `SCI_cli.destination_check()`
        
        `sci_cli.send_message()` должен вернуть
        {
            'status': 'error', 
            'action': 'recipient not found', 
            'data': {
                'description': 'recipient not found'
            }
        }
        """
        msg = self.test_ELRzfnafgajHutgkSrbhOUpiMTKcoRj.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:wrong_test_app",
                    "interface": "local-aq",
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
                    "isAwaiting": False,
                }
            }
            send_result = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)], 
            waiting_after=0.1
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("recipient not found", result["action"], msg=msg)
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_uEZnOmifLdrUMZyllIjeQhFsuuT(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан НЕ поддерживаемым `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        
        `sci_cli.send_message()` успешно отправляет `EventMessage`
        но `MyApplication.actionDispatcher()` не найдет `actionHandler` для
        переданного `action`, вернет и залогирует отрицательный `ecsaddo`.
        
        `sci_cli.send_message()` должен вернуть:
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': ''
            }
        }
        """
        msg = self.test_uEZnOmifLdrUMZyllIjeQhFsuuT.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "wrong-generic-test",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
                    "isAwaiting": False,
                }
            }
            send_result = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)], 
            waiting_after=0.1
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
    
    def test_qyCtsVAtZSCPscTbOuyVaxuzCreU(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Возможность переопределить `"max_execution_time"` через
        `EventMessage -> "message_payload" -> "meta"`
        
        Если `actionHandler` превышает время обработки `"max_execution_time"`
        то задача должна завершиться отменой.
        """
        msg = self.test_qyCtsVAtZSCPscTbOuyVaxuzCreU.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 0.7,
                        "work_check": True    
                    },
                    "meta": {
                        "expire_time": 20,
                        "max_execution_time": 0.5
                    }
                },
                "response_settings": {
                    "isAwaiting": False,
                }
            }
            send_result = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)], 
            waiting_after=0.1
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_SohBfYfHKSAlEyBUDIxUuObbCR(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        
        Проверяется:
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(3)` (по умолчанию `"background": False`)
        в следствии чего `actionHandler` займет весь `AppController`.
        
        Сразу отправляется второй запрос (по умолчанию `"background": False`) 
        с `"ping-pong": True`, который (`ping-pong`) завершится в 
        `SCI_core.ResponseSession` по `timeout` через 2 секунды.
        Основной `EventMessage` второго запроса не отправится.
        
        
        `AppController` должен самостоятельно завершить `actionHandler`
        обработки первого запроса через `"max_execution_time"` (3с)
    
        `sci_cli.send_message()` возвращет:
        {
            'status': 'error', 
            'action': 'ping-pong timeout', 
            'data': {
                'description': 'ping-pong timeout'
            }
        }
        """
        msg = self.test_SohBfYfHKSAlEyBUDIxUuObbCR.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "work_check": True,
                        "sleep": 3, 
                    },
                    "meta": {
                        "expire_time": 20,
                        "max_execution_time": 2.5
                    }
                },
                "response_settings": {
                    "isAwaiting": False,
                }
            }
            EventMessage_second = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
                    "isAwaiting": False,
                }
            }
            send_result_first = await self.sci_cli.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_result_second = await self.sci_cli.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            return send_result_second
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)], 
            waiting_after=1.1
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("ping-pong timeout", result["action"], msg=msg)
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_GDzHPVbmTIVBHFdCwntHMEZhON(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        
        Проверяется:
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(2.1)` (`"background": True`), 
        в следствии чего `actionHandler` не блокирует `AppController`. 
        
        Сразу отправляется второй запрос с `"ping-pong": True`, 
        `"await_timeout": 1`, `"expire_time": 1` 
        (по умолчанию `"background": False`) который должен сразу успешно 
        выполниться.
        
        Первый запрос - самостоятельно успешно завершиться через 2.1 с.
        Второй запрос - сразу успешно выполняется.
        
        `sci_cli.send_message()` возвращает:
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': ''
            }
        }
        """
        msg = self.test_GDzHPVbmTIVBHFdCwntHMEZhON.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 2.1,
                         "work_check": True,
                    },
                    "meta": {
                        "background": True,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": False,
                }
            }
            EventMessage_second = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": False,
                }
            }
            send_result_first = await self.sci_cli.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_result_second = await self.sci_cli.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            return send_result_second
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)], 
            waiting_after=2.1
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertEqual(2, ref_q.qsize(), msg=msg)
        
        
    def test_YcMJymLAtvYIkzdFPP(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        
        Проверяется:
        Сначала отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(0.5)` (по умолчанию `"background": False`)
        в следствии чего `actionHandler` займет весь `AppController`.
        
        Сразу отправляется второй запрос (по умолчанию `"background": False`) 
        `expire_time = 0.2`
        
        Первый запрос успешно выполниться через `0.5` c.
        Второй запрос будет отменен согласно `expire_time = 0.2`.
            
        `sci_cli.send_message()` возвращает "ok", так оба сообщения успешно
        отправляются:
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': ''
            }
        }
        """
        msg = self.test_YcMJymLAtvYIkzdFPP.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 0.5,
                    },
                    "meta": {
                        "background": False,
                        "expire_time": 20,
                    }
                },
                "response_settings": {
                    "isAwaiting": False,
                }
            }
            EventMessage_second = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
                        "expire_time": 0.2,
                    }
                },
                "response_settings": {
                    "isAwaiting": False,
                }
            }
            send_result_first = await self.sci_cli.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_result_second = await self.sci_cli.send_message(
                EventMessage_second,
                ping_pong=ping_pong
            )
            return send_result_second
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=False)], 
            waiting_after=0.6
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_TxCtSBsnvizXCZCGf(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемым `Application`
        
        Проверяется:
        
        Отправляется `EventMessage` указывающий `actionHandler`
        совершить `await asyncio.sleep(0.5)` (`"background": True`),
        `"max_execution_time": 0.2`
        
        Обработка `actionHandler` будет отменена согласно 
        `"max_execution_time": 0.2`
        
        Так как сообщение успешно отправляется, то `sci_cli.send_message()`
        возвращает `"status": "ok"`
        {
            'status': 'ok', 
            'action': '', 
            'data': {
                'description': ''
            }
        }
        """
        msg = self.test_TxCtSBsnvizXCZCGf.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage_first = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
                },
                "meta": {
                    "mType": "request",
                },
                "message_payload": {
                    "data": {
                        "sleep": 0.5,
                        "work_check": True,
                    },
                    "meta": {
                        "expire_time": 20,
                        "background": True,
                        "max_execution_time": 0.2,
                    }
                },
                "response_settings": {
                    "isAwaiting": False,
                }
            }
            send_result_first = await self.sci_cli.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            return send_result_first
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message(ping_pong=True)], 
            waiting_after=0.3
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertEqual(0, ref_q.qsize(), msg=msg)
        
        
    def test_KmBKXdWsHwhmsVMobuABZPtrBllnlDvdobCRAtHMnAVWdfenfu(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": False`.
        - `"interface"` - "remote-rq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        При `"sci_mode": "only_local"`, отправляется `EventMessage`
        `"interface": "remote-rq".`
        
        `sci_cli` возвращает отрицательный `ecsaddo` ответ от валидации.
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'interface'], 'structure error', '`EventMessage -> "address_section" -> "interface"` Если текущий `SCI node` запущен в режиме `"only_local"`, то единственное допустимое значение `"interfcae"` это - `"local-aq"`.')
                ]
            }
        } 
        """
        msg = self.test_KmBKXdWsHwhmsVMobuABZPtrBllnlDvdobCRAtHMnAVWdfenfu.__doc__
        async def send_message(ping_pong: bool = False):
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
                    },
                    "meta": {
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_result_first = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result_first
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner(
                [send_message(ping_pong=True)], 
            )
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("error", result["status"], msg=msg)
        self.assertEqual("failed validation", result["action"], msg=msg)
        
        
if __name__ == '__main__':
    unittest.main()