import asyncio
import unittest
import traceback
import inspect
import queue

from typing import Awaitable, Optional

from sci.app_controllers.base_controller import SCI_BaseAppController
from sci.lib.patterns import create_ecsaddo, isecsaddo
from sci.sci_base.sci_base import SCI
from sci.network.utils import create_response_payload
from sci.sci_cli.sci_cli import SCI_Response
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
        
    
class SCI_node_test_ogHaJScKiSdKTfgOVEhwMWeSyXAMvWbadiYHS(unittest.TestCase):
    """
    - `"sci_mode": "only_local"`
    - `with await response`
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
        task_sci_core = asyncio.create_task(self.sci_core())
        while True:
            if not all([self.sci_core.is_working]):
                await asyncio.sleep(0.1)
                continue
            break
        # Запуск пользовательских test_async_payload
        futures = [asyncio.create_task(i) for i in test_async_payload]
        futures.append(task_sci_core)
        for future in asyncio.as_completed(futures):
            res = await future
            # Первая задача которая завершилась
            await asyncio.sleep(waiting_after)
            return res
        
    
    def test_yeahvtIOxzNTxSMLz(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_yeahvtIOxzNTxSMLz.__doc__
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
                    "data": {},
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            return send_result
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message()])
        )
        self.assertEqual(True, isecsaddo(result), msg=msg)
        self.assertEqual("ok", result["status"], msg=msg)
        self.assertIn("awaitable_response", result["data"], msg=msg)
        self.assertEqual(
            True, 
            inspect.isfunction(result["data"]["awaitable_response"]),
            msg=msg
        )
        
    
    def test_cEfZinepgtRdwIPmhX(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
            
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым `Application`
        - `ping-pong`  используется
        
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
        msg = self.test_cEfZinepgtRdwIPmhX.__doc__
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
                    "data": {},
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli.send_message(
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
        
        
    def test_NRumkFOMgdmYeaCiWj(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        - `ping-pong` используется
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
                            'recipient': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'local-aq'
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
        msg = self.test_NRumkFOMgdmYeaCiWj.__doc__
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
                        "work_check": True,    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli.send_message(
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
        
        
    def test_XtCUdZjDbuQDKgMghgdxBFo(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        - `ping-pong` используется
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
                            'recipient': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'local-aq'
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
        msg = self.test_XtCUdZjDbuQDKgMghgdxBFo.__doc__
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
                        "work_check": True,    
                    },
                    "meta": {}
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 5,
                }
            }
            send_result = await self.sci_cli.send_message(
                EventMessage,
                ping_pong=ping_pong
            )
            awaitable_response = send_result["data"]["awaitable_response"]
            return await awaitable_response()
        # Запускает сперва sci_core, затем *send_message
        result = asyncio.run(
            self.async_test_runner([send_message()])
        )
        self.assertIsInstance(result, SCI_Response, msg=msg)
        self.assertEqual(200, result.status_code, msg=msg)
        self.assertIsInstance(result.response_data, dict, msg=msg)
        self.assertIn("work", result.response_data, msg=msg)
        self.assertEqual(True, result.response_data["work"], msg=msg)
        self.assertEqual(True, isecsaddo(result.session_result), msg=msg)
        self.assertEqual("ok", result.session_result["status"], msg=msg)
        self.assertEqual(ref_q.qsize(), 1, msg=msg)  
        
        
    def test_FzdoUCWhmmpYRjZjqPieL(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - неизвестный `SCI` node
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
        msg = self.test_FzdoUCWhmmpYRjZjqPieL.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "some_wrong_node_aCtn4R2k3qPtziyBfdEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
            send_result = await self.sci_cli.send_message(
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
        
    
    def test_sHjncUHIodCqzTFojbxZYs(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель НЕ зарегистрировано в `SCI_SETTINGS -> "AppConf"`
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
        msg = self.test_sHjncUHIodCqzTFojbxZYs.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "test-generic",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:wrong_app",
                    "interface": "local-aq",
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
            send_result = await self.sci_cli.send_message(
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
        
        
    def test_ywfMtqKXetOBLkRXfsS(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_ywfMtqKXetOBLkRXfsS.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "wrong-test-action",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
            send_result = await self.sci_cli.send_message(
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
        
    
    def test_DHfulUiHhLjWozJMYxcHKvdKJ(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_DHfulUiHhLjWozJMYxcHKvdKJ.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage = {
                "sender": "anonim",
                "action": "wrong-test-action",
                "address_section": {
                    "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
                    "interface": "local-aq",
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
            send_result = await self.sci_cli.send_message(
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
        
        
    def test_VOdQdRacAZqNSPMqWnkMwsdjJ(self):
        """
        Конфигурация:
         - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_VOdQdRacAZqNSPMqWnkMwsdjJ.__doc__
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
                    "interface": "local-aq",
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
            send_first_result = await self.sci_cli.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli.send_message(
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
        
        
    def test_WhcUyHNNFjJAfmvaHZoiMbkbkAPNQU(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        Сессия ожидания ответа от второго запроса завершится по `timeout`
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
        msg = self.test_WhcUyHNNFjJAfmvaHZoiMbkbkAPNQU.__doc__
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
                        "expire_time": 3,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 3,
                }
            }
            send_first_result = await self.sci_cli.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli.send_message(
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
        
        
    def test_CKdlPDdjPCQcohxKOao(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        
        Первый и вторый запрос успешно выполняются, хотя сессия ожидания ответа
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
        msg = self.test_CKdlPDdjPCQcohxKOao.__doc__
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
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_first_result = await self.sci_cli.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli.send_message(
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
        
        
    def test_xeQYvPjmmcdLoDpAWLLvuccJcC(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_xeQYvPjmmcdLoDpAWLLvuccJcC.__doc__
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
                        "expire_time": 2,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 2,
                }
            }
            send_first_result = await self.sci_cli.send_message(
                EventMessage_first,
                ping_pong=ping_pong
            )
            await asyncio.sleep(0.1)
            send_second_result = await self.sci_cli.send_message(
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
        
        
    def test_ELzhZsUTdjQvUGORtFwXOlBjKrIUl(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_ELzhZsUTdjQvUGORtFwXOlBjKrIUl.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage_block = {
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
            send_result = await self.sci_cli.send_message(
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
        
        
    def test_AxUDlLVuQzUwnRyxLbWGrMXYhI(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_AxUDlLVuQzUwnRyxLbWGrMXYhI.__doc__
        async def send_message(ping_pong: bool = False):
            EventMessage_block = {
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
            send_result = await self.sci_cli.send_message(
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
        
        
    def test_EuSYzFSYNRgBbTVLWjIotwTq(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
                            'recipient': 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:anonim', 
                            'interface': 'local-aq'
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
        msg = self.test_EuSYzFSYNRgBbTVLWjIotwTq.__doc__
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
                        "expire_time": 1,
                    }
                },
                "response_settings": {
                    "isAwaiting": True,
                    "await_timeout": 1,
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
        
    
    def test_QWEsYIWzuykNNxvONDTkAka(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` не отправляется.
        
        Проверяется:
        
        Оотправляется `EventMessage` `"await_timeout": 0.6`, `"expire_time": 20`,
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
        msg = self.test_QWEsYIWzuykNNxvONDTkAka.__doc__
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
            send_result_first = await self.sci_cli.send_message(
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
        
        
    def test_IrfPwRbwtGHvDqEhfvwe(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_IrfPwRbwtGHvDqEhfvwe.__doc__
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
            send_result_first = await self.sci_cli.send_message(
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
        
        
    def test_OhhRkEudsVaGTFzAfbGWosdDsvcTGIwi(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_OhhRkEudsVaGTFzAfbGWosdDsvcTGIwi.__doc__
        async def send_message(ping_pong: bool = False):
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
                    "interface": "local-aq",
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
            send_result_first = await self.sci_cli.send_message(
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
        
        
    def test_TnwqYPuGqNjwxehCZqSZrghdP(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_TnwqYPuGqNjwxehCZqSZrghdP.__doc__
        async def send_message(ping_pong: bool = False):
            error_ecsaddo = create_ecsaddo(
                "ok",
                response_payload = 200
            )
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
            send_result_first = await self.sci_cli.send_message(
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
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
            error_ecsaddo = create_ecsaddo("ok")
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
            send_result_first = await self.sci_cli.send_message(
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
        
        
    def test_NXspzzbyAEJiqHamD(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
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
        msg = self.test_NXspzzbyAEJiqHamD.__doc__
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
            send_result_first = await self.sci_cli.send_message(
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
        
        
    def test_SItKDCbLxuPwdikLIknoSgz(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Если `actionHandler` при создании экземпляра `SCI_ResponsePayload`
        передал невалидный `status_code`, то возникает исключение.
        `actionHandler` возвращает `ecsaddo` "status": "ex
        тогда `messageHandler__pl` логирует этот этот `ecsaddo` "status": "ex"
        и отправляет `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии.
        """
        msg = self.test_SItKDCbLxuPwdikLIknoSgz.__doc__
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
            send_result_first = await self.sci_cli.send_message(
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
        
        
    def test_ngzxYMNbpnhBmasBWYJrO(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
        - `"interface"` - "local-aq"
        
        Особенности:
        - Узел получатель - текущий `SCI` node
        - Приложение получатель зарегистрировано в `SCI_SETTINGS -> "AppConf"`
        - `EventMessage -> "action"` передан поддерживаемый целевым 
            `Application`
        - `ping-pong` отправляется.
        
        Проверяется:
        Если `actionHandler` при создании экземпляра `SCI_ResponsePayload`
        передал невалидный `response_data`, то возникает исключение.
        `actionHandler` возвращает `ecsaddo` "status": "ex
        
        тогда `messageHandler__pl` логирует этот этот `ecsaddo` "status": "ex"
        и отправляет `EventMessage` "response" `SCI_Response`:
        - `response.status_code` - 500
        - `resposne.response_data` - `{}`
        - `response.session_result` - `ecsaddo` "ok" `response` сессии.
        """
        msg = self.test_ngzxYMNbpnhBmasBWYJrO.__doc__
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
            send_result_first = await self.sci_cli.send_message(
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
        
        
    def test_ltHVJZGfCbjVQJkhrovOOtDSqhLiheSnDfDraWWIDupn(self):
        """
        Конфигурация:
        - `"sci_mode" - "only_local"`
        - `"mType": "request"` 
        - `"isAwaiting": True`.
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
        msg = self.test_ltHVJZGfCbjVQJkhrovOOtDSqhLiheSnDfDraWWIDupn.__doc__
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