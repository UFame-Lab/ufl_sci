import unittest
import asyncio

from sci.apps.nodeLifespanSystemSCIApp.validators import (
    NodeLifespanSystemSCIAppContext_Validate
)
from sci.apps.nodeLifespanSystemSCIApp.application import (
    NodeLifespanSystemSCIApp
)
from sci.lib.patterns import isecsaddo
from sci.sci_settings import TEST_LOG_FILE_PATH


class NodeLifespanSystemSCIAppContect_Validate(unittest.TestCase):
    
    def setUp(self) -> None:
        context = {
            "auth_nodes_settings": {
                "local_nodes": {
                    "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                        "wsBridgeBroker": tuple(),
                    },
                },
                "remote_nodes": {
                    "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                        "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                        "wsBridgeBroker": tuple(),
                        "broker_connection_settings": {
                            "redis": {
                                "host": "localhost",
                                "port": 6379,
                                "password": None,
                                "db": 0,
                            },
                        },
                        "back_address": "external",
                    },
                },
                "remote_ws_nodes": {
                    "moscow_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                        "wsbridge": "someWsBridge"
                    }
                },
            }
        }
        SCI_SETTINGS = {
            "node_name": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (NodeLifespanSystemSCIApp, "nodeLifespanSystemSCIApp", {})
            ],
            "nodes": {
                "local_nodes": {},
                "remote_nodes": {},
                "remote_ws_nodes": {},
            },
            "websocket_connections": {
                "someWsBridge": {
                    "url": "ws://localhost:8555/ws/chat/100/",
                    "headers": {},
                    "wsBridgeBroker_aq": asyncio.Queue(),
                }
            },
            "local_broker_connection_settings": {
                "redis": {
                    "host": {
                        "local": "localhost",
                        "local-tetwork": "",
                        "external": "",
                    },
                    "port": 6379,
                    "password": None,
                    "db": 0,
                }
            },
        }
        self.context = context
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = "standart"
        
        
    def test_oMjwDsJuWskItagpgaxFcVsTGiCbLQhdh(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context`
        
        `context` передается валидным.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_oMjwDsJuWskItagpgaxFcVsTGiCbLQhdh.__doc__
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_VAsOcxpFMgiNBvUpKYzJrEwXFjmTcNAdsLM(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings"`
        
        Ключ `"auth_nodes_settings"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_VAsOcxpFMgiNBvUpKYzJrEwXFjmTcNAdsLM.__doc__
        del self.context["auth_nodes_settings"]
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_ZPCZKcCTzOSYJsrgtpbLwuQCePXfVQgjxMt(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings"`
        
        В качестве значения ключа `"auth_nodes_settings"` передается не
        валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings'], 'type error', '`context -> "auth_nodes_settings: dict"` Значение ключа `auth_nodes_settings` должно быть `dict`.')
                ]
            }
        }
        """
        msg = self.test_ZPCZKcCTzOSYJsrgtpbLwuQCePXfVQgjxMt.__doc__
        self.context["auth_nodes_settings"] = []
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_haphPJPoBgSLBvOmfzYBZIkmpBFnYaSKUy(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings"`
        
        В качестве значения ключа `"auth_nodes_settings"` передается пустой
        `dict`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes"` `context -> "auth_nodes_settings" -> "remote_nodes"` `context -> "auth_nodes_settings" -> "remote_ws_nodes"` Словарь `auth_nodes_settings` должен содержать хотя-бы 1 не пустой словарь с настройками.')
                ]
            }
        }
        """
        msg = self.test_haphPJPoBgSLBvOmfzYBZIkmpBFnYaSKUy.__doc__
        self.context["auth_nodes_settings"] = {}
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_ldQRwWAYkTYaDanpAlWzLxRTJFMPTSzCyHeYPyoz(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes"`
        
        В качестве значения ключа `"auth_nodes_settings"` передается словарь
        с настройками только для `"local_nodes"`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_ldQRwWAYkTYaDanpAlWzLxRTJFMPTSzCyHeYPyoz.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    "wsBridgeBroker": tuple(),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_jFRChfPsUCgxtsYvqhAFwZcOBIUbFqCQ(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes"`
        
        В качестве значения ключа `"local_nodes"` передается не валидный тип
        `str`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'local_nodes'], 'type error', '`context -> "auth_nodes_settings" -> "local_nodes: dict"` Значение ключа `"local_nodes"` должен быть тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_jFRChfPsUCgxtsYvqhAFwZcOBIUbFqCQ.__doc__
        auth_nodes_settings = {
            "local_nodes": "ff",
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_BbccEyMRbCBxhmssbYWCMmCPmZidwybDrojFQWWuOQctIx(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "key"`
        
        В качестве имени ключа значений `"local_nodes"` используется не
        валидный тип `tuple`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', "local_nodes", (1, 2)], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name"` Ключ `"node_name"` должен иметь тип `str`, и быть длиной `>=` 50 символов.')
                ]
            }
        }
        """
        msg = self.test_BbccEyMRbCBxhmssbYWCMmCPmZidwybDrojFQWWuOQctIx.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                (1, 2): {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    "wsBridgeBroker": tuple(),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_xfRgvmNyWSbhRmQUINUYochGRZmexjUbeDvqY(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "key"`
        
        В качестве имени ключа значений `"local_nodes"` используется
        короткая строка `hello`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_xfRgvmNyWSbhRmQUINUYochGRZmexjUbeDvqY.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "hello": {
                    "node_rq": "sci_rq_hello_xTUwoiqkabbyYVvhOtSuUBcVZzMKPZkOfoOhA",
                    "wsBridgeBroker": tuple(),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"],
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_YfBclMSswWFVtQeGVNNZfxVTBKWuobTNvWGCAFeW(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "node_rq"`
        
        Ключ `"node_rq"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ', 'node_rq'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_YfBclMSswWFVtQeGVNNZfxVTBKWuobTNvWGCAFeW.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "wsBridgeBroker": tuple(),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_AqPHKvalJHIZrZSShbfxFmFgMdezSQWqMxQpaLjX(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ', 'node_rq'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_AqPHKvalJHIZrZSShbfxFmFgMdezSQWqMxQpaLjX.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq":[],
                    "wsBridgeBroker": tuple(),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_jkhRjGaXYFhYyoFHGPpnXBTMxlsrjHqvOLkoTi(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается короткая строка.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_jkhRjGaXYFhYyoFHGPpnXBTMxlsrjHqvOLkoTi.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "hello": {
                    "node_rq": "sci_rq_hello",
                    "wsBridgeBroker": tuple(),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_rSqyUqMRocJmXlvMGAGsVsQFEfkpxoph(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается строка нормальной
        длины, но без префикса `SCI_NODE_RQ_PREFIX`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ', 'node_rq'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_rSqyUqMRocJmXlvMGAGsVsQFEfkpxoph.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "HiBqSQGvtZizazVqZJPpMcOUvSKugpeoBjtsGCAhtMOadbILxsYokegNmdapCgNqHJ",
                    "wsBridgeBroker": tuple(),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_UmFnZfVmXwbtfCMSWZkiQajeDeBVeDlYAuFljgYOdQ(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        Ключ `"wsBridgeBroker"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ', 'wsBridgeBroker'], 'type error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "wsBridgeBroker"` Значением ключа `"wsBridgeBroker"` должен быть тип `tuple`')
                ]
            }
        }
        """
        msg = self.test_UmFnZfVmXwbtfCMSWZkiQajeDeBVeDlYAuFljgYOdQ.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_QknREvsteEhlVLAVCttvfsknikpUNsrVdWOHQeEj(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        В качестве значения ключа `"wsBridgeBroker"` передается не валидный
        тип `set`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'local_nodes', 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ', 'wsBridgeBroker'], 'type error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "wsBridgeBroker"` Значением ключа `"wsBridgeBroker"` должен иметь тип `tuple` или `list`')
                ]
            }
        }
        """
        msg = self.test_QknREvsteEhlVLAVCttvfsknikpUNsrVdWOHQeEj.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    "wsBridgeBroker": set(),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_VEFWpYtGOYHlaiLLdciCHjlWSeulqHBszen(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        В качестве значения ключа `"wsBridgeBroker"` передается `("hi",)`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ', 'wsBridgeBroker'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "wsBridgeBroker"` Каждое значение кортежа - имя (str) `wsBridge`, должно быть `>=` 3')
                ]
            }
        }
        """
        msg = self.test_VEFWpYtGOYHlaiLLdciCHjlWSeulqHBszen.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    "wsBridgeBroker": ("hi",),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_QzqkvjyfevIiFnirjRHNjMAapDYlHEusenGczFOL(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        В качестве значения ключа `"wsBridgeBroker"` передается не валидный
        `([1,2,3,4,5,], )`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ', 'wsBridgeBroker'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "wsBridgeBroker"` Каждое значение кортежа - имя (str) `wsBridge`, должно быть `>=` 3')
                ]
            }
        }
        """
        msg = self.test_QzqkvjyfevIiFnirjRHNjMAapDYlHEusenGczFOL.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    "wsBridgeBroker": ([1,2,3,4,5,], ),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_QVAIcKFFnCLqwUgUjqOcWpzcRBKqYvaTpDv(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "local_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        В качестве значения ключа `"wsBridgeBroker"` передается валидный
        `("some1_wsBridge", "some2_wsBridge")`
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_QVAIcKFFnCLqwUgUjqOcWpzcRBKqYvaTpDv.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
##################
##################

    def test_wmRGoaLdzqbtCcYyOXBpsEqzFRiGgZZStgVnhEAsSfZhP(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes"`
        
        В качестве значения ключа `"auth_nodes_settings"` передается словарь
        с настройками только для `"remote_nodes"`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_wmRGoaLdzqbtCcYyOXBpsEqzFRiGgZZStgVnhEAsSfZhP.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": tuple(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_oQofEuDbvLIOyWhzMpTocjtIDZUdjbIHrvRrfZqXCHpSy(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes"`
        
        В качестве значения ключа `"remote_nodes"` передается не валидный тип
        `str`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes'], 'type error', '`context -> "auth_nodes_settings" -> "remote_nodes: dict"` Значение ключа `"remote_nodes"` должен быть тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_oQofEuDbvLIOyWhzMpTocjtIDZUdjbIHrvRrfZqXCHpSy.__doc__
        auth_nodes_settings = {
            "remote_nodes": "ffddd",
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_FVRRgCSMQtkvlDdweFKrJOdyvphrdSGtLvaAIWYQFBp(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "key"`
        
        В качестве имени ключа значений `"remote_nodes"` используется не
        валидный тип `tuple`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', (1, 2)], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name"` Ключ `"node_name"` должен иметь тип `str`, и быть длиной `>=` 50 символов.')
                ]
            }
        }
        """
        msg = self.test_FVRRgCSMQtkvlDdweFKrJOdyvphrdSGtLvaAIWYQFBp.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                (1, 2): {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": tuple(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        

    def test_AorYJUXVxYZHJxAooNmRfWfaFCYpFvBikCFLUUxrc(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "key"`
        
        В качестве имени ключа значений `"remote_nodes"` используется
        короткая строка `hello`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_AorYJUXVxYZHJxAooNmRfWfaFCYpFvBikCFLUUxrc.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "hello": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": tuple(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        

    def test_zEYcPvrIbWLYhDcuNvubZCChxLCvWvgXsGdCPIwbqAESk(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "node_rq"`
        
        Ключ `"node_rq"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'node_rq'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_zEYcPvrIbWLYhDcuNvubZCChxLCvWvgXsGdCPIwbqAESk.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "wsBridgeBroker": tuple(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_asANQuHwdnsedTftnRkiXbkATqeEOrzRYGKoVvlJgC(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'node_rq'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_asANQuHwdnsedTftnRkiXbkATqeEOrzRYGKoVvlJgC.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": [],
                    "wsBridgeBroker": tuple(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_WYhMVKRKKijtLSRjeKfiGRvfkISMlIfzNpZBRrdxId(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается короткая строка.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_WYhMVKRKKijtLSRjeKfiGRvfkISMlIfzNpZBRrdxId.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_hello",
                    "wsBridgeBroker": tuple(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_FePVvmKonAzkSJJeoyndnsFHprxfDViqJioVuFwJ(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается строка нормальной
        длины, но без префикса `SCI_NODE_RQ_PREFIX`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'node_rq'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_FePVvmKonAzkSJJeoyndnsFHprxfDViqJioVuFwJ.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "HiBqSQGvtZizazVqZJPpMcOUvSKugpeoBjtsGCAhtMOadbILxsYokegNmdapCgNqHJ",
                    "wsBridgeBroker": tuple(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_wnPkAMjJClIByYisjTthbBkntBxDuGdPzZQrRV(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        Ключ `"wsBridgeBroker"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'wsBridgeBroker'], 'type error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "wsBridgeBroker"` Значением ключа `"wsBridgeBroker"` должен быть тип `tuple`')
                ]
            }
        }
        """
        msg = self.test_wnPkAMjJClIByYisjTthbBkntBxDuGdPzZQrRV.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_dWEiCbzvreXPTQJuMTlFoCxbUvlrbfmWQDOhpJdBekbJ(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        В качестве значения ключа `"wsBridgeBroker"` передается не валидный
        тип `set`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'wsBridgeBroker'], 'type error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "wsBridgeBroker"` Значением ключа `"wsBridgeBroker"` должен быть тип `tuple`')
                ]
            }
        }
        """
        msg = self.test_dWEiCbzvreXPTQJuMTlFoCxbUvlrbfmWQDOhpJdBekbJ.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": set(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_WjptdMPxfzmtmpzSERYgvTUSwkwJFNBRvno(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        В качестве значения ключа `"wsBridgeBroker"` передается `("hi",)`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'wsBridgeBroker'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "wsBridgeBroker"` Каждое значение кортежа - имя (str) `wsBridge`, должно быть `>=` 3')
                ]
            }
        }
        """
        msg = self.test_WjptdMPxfzmtmpzSERYgvTUSwkwJFNBRvno.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("hi",),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_oGOVNpiAQQGznJcqdTfYcIwSYSHuIGfjQBNPSDyFClLe(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        В качестве значения ключа `"wsBridgeBroker"` передается не валидный
        `([1,2,3,4,5,], )`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'wsBridgeBroker'], 'structure error', '`context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" -> "wsBridgeBroker"` Каждое значение кортежа - имя (str) `wsBridge`, должно быть `>=` 3')
                ]
            }
        }
        """
        msg = self.test_oGOVNpiAQQGznJcqdTfYcIwSYSHuIGfjQBNPSDyFClLe.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ([1,2,3,4,5,], ),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_TjcascsXWDsdRCZpNqfFGHlQuVcxqkWpcZkslOoRGPJTnAwg(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "wsBridgeBroker"`
        
        В качестве значения ключа `"wsBridgeBroker"` передается валидный
        `("some1_wsBridge", "some2_wsBridge")`
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_TjcascsXWDsdRCZpNqfFGHlQuVcxqkWpcZkslOoRGPJTnAwg.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_SZQJjpoTUsdOhVNASDpmkNmfAShEnutVewndYKqg(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings"`
        
        Ключ `"broker_connection_settings"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings"` Значение ключа `"broker_connection_settings"` должен быть тип `dict`, который должен содержать ключ `"redis"`.')
                ]
            }
        }
        """
        msg = self.test_SZQJjpoTUsdOhVNASDpmkNmfAShEnutVewndYKqg.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    # "broker_connection_settings": {
                    #     "redis": {
                    #         "host": "localhost",
                    #         "port": 6379,
                    #         "password": None,
                    #         "db": 0,
                    #     },
                    # },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_knuwkDyWKdaKMDjvuRoVbVsffsEpCutuyHJnp(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings"`
        
        В качестве значения ключа `"broker_connection_settings"` передается не
        валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings"` Значение ключа `"broker_connection_settings"` должен быть тип `dict`, который должен содержать ключ `"redis"`.')
                ]
            }
        }
        """
        msg = self.test_knuwkDyWKdaKMDjvuRoVbVsffsEpCutuyHJnp.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": [],
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_gfQEpUXUvxrTVlKMsyOFQMeGDPXDUsjLbDDRVGaEwwUr(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings"`
        
        В качестве значения ключа `"broker_connection_settings"` передается
        пустой `dict`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings"` Значение ключа `"broker_connection_settings"` должен быть тип `dict`, который должен содержать ключ `"redis"`.')
                ]
            }
        }
        """
        msg = self.test_gfQEpUXUvxrTVlKMsyOFQMeGDPXDUsjLbDDRVGaEwwUr.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {},
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_ghvhnOFlPGxjobDuXHJuCXWSTmWkqRV(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis"`
        
        В качестве значения ключа `"redis"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'redis', 'broker_connection_settings'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_ghvhnOFlPGxjobDuXHJuCXWSTmWkqRV.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": []    
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_UkxLxaGUAamImksQQUBXSrKOzIUPLHDlTHnTCWyyQH(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis"`
        
        В качестве значения ключа `"redis"` передается пустой `dict`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings', 'redis'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_UkxLxaGUAamImksQQUBXSrKOzIUPLHDlTHnTCWyyQH.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {}  
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_sMcwxniFGUnmiaxGInHQENfOatJqIBvxGYkuKKVgWnNfILRN(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "host"`
        
        Ключ `host` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings', 'redis'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_sMcwxniFGUnmiaxGInHQENfOatJqIBvxGYkuKKVgWnNfILRN.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_sJbZDrcTYEDSUxueMYcsJHeoFRllKEsDN(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "host"`
        
        В качестве значения ключа `"host"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings', 'redis', 'host'], 'type error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis" -> "host"` Значение ключа `"host"` должно иметь тип `str`.')
                ]
            }
        }
        """
        msg = self.test_sJbZDrcTYEDSUxueMYcsJHeoFRllKEsDN.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": [],
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    def test_dzaCmudUBSiblHbDpVezNIJhWjgvLTSllUKjatzdTShCQdRX(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "port"`
        
        Ключ `port` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings', 'redis'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_dzaCmudUBSiblHbDpVezNIJhWjgvLTSllUKjatzdTShCQdRX.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": None,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_ndaZZmgQXfdxPEJaelZjyntcWbMMPHohKuxc(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "port"`
        
        В качестве значения ключа `"port"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings', 'redis', 'port'], 'type error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis" -> "port"` Значение ключа `"port"` должно иметь тип `int`.')
                ]
            }
        }
        """
        msg = self.test_ndaZZmgQXfdxPEJaelZjyntcWbMMPHohKuxc.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": [],
                            "password": None,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_otjDULDFoKNVVlOptOPMiIlcTCVPJK(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "password"`
        
        Ключ `"password"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings', 'redis'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_otjDULDFoKNVVlOptOPMiIlcTCVPJK.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_fXTbFUhwQNgvVMsaSOONoVvkZbsiaGAwYmgpUiGPZ(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "password"`
        
        В качестве значения ключа `"password"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings', 'redis', 'password'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis" -> "password"` Значение ключа `"password"` должно иметь тип `str` и быть длиной `>=` 3 символам, или быть `None`.')
                ]
            }
        }
        """
        msg = self.test_fXTbFUhwQNgvVMsaSOONoVvkZbsiaGAwYmgpUiGPZ.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": [],
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_ejdQWzUCnlLHSRJHHSzDnKunWvpjIGVZm(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "password"`
        
        В качестве значения ключа `"password"` передается не валидная строка
        `"hi"`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'broker_connection_settings', 'redis', 'password'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis" -> "password"` Значение ключа `"password"` должно иметь тип `str` и быть длиной `>=` 3 символам, или быть `None`.')
                ]
            }
        }
        """
        msg = self.test_ejdQWzUCnlLHSRJHHSzDnKunWvpjIGVZm.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": "hi",
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_ibzkySLIAinVxoVSPCWxHmxnTmPCaineDSyVV(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "password"`
        
        В качестве значения ключа `"password"` передается валидная строка
        `"hello"`
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_ibzkySLIAinVxoVSPCWxHmxnTmPCaineDSyVV.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": "hello",
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_jXptgdJYycVVjEEoEBuXkxTGIMtQlmKOAZpODWbsvqasiktukb(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "broker_connection_settings" -> "redis" -> "password"`
        
        В качестве значения ключа `"password"` передается `None`
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_jXptgdJYycVVjEEoEBuXkxTGIMtQlmKOAZpODWbsvqasiktukb.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": None,
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_NKWRqruTlKzPPZSGmrRVFIvHNDPKPTOJXEIhAYZmu(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "back_address"`
        
        Ключ `"back_address"` не пердается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'back_address'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "back_address"` Значение ключа `"back_address"` должно иметь тип `str`, и входить в `["local", "local-network", "external"]`')
                ]
            }
        }
        """
        msg = self.test_NKWRqruTlKzPPZSGmrRVFIvHNDPKPTOJXEIhAYZmu.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": None,
                            "port": 6379,
                            "db": 0,
                        }
                    },
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_SKDZxEKxmJUfHDbdhCCpBTZJNhHHBAVyO(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "back_address"`
        
        В качестве значения ключа `"back_address"` передается не валидный тип
        `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'back_address'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "back_address"` Значение ключа `"back_address"` должно иметь тип `str`, и входить в `["local", "local-network", "external"]`')
                ]
            }
        }
        """
        msg = self.test_SKDZxEKxmJUfHDbdhCCpBTZJNhHHBAVyO.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": None,
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": [],
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_yqcLnMJyDxqFBIixPwopbAcMVpsprxFbF(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "back_address"`
        
        В качестве значения ключа `"back_address"` передается не валидная строка
        `"hello"`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb', 'back_address'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "back_address"` Значение ключа `"back_address"` должно иметь тип `str`, и входить в `["local", "local-network", "external"]`')
                ]
            }
        }
        """
        msg = self.test_yqcLnMJyDxqFBIixPwopbAcMVpsprxFbF.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": None,
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "hello",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_jXNTHfYESchuInLUHNVsjqQhBIOxvxVUlUVhegD(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "back_address"`
        
        В качестве значения ключа `"back_address"` передается `"local"`
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_jXNTHfYESchuInLUHNVsjqQhBIOxvxVUlUVhegD.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": None,
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "local",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_iOjSGBsukgxsTwogPZXVbYNiWfNiuzkrxEaEyKkeDPPUC(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "back_address"`
        
        В качестве значения ключа `"back_address"` передается `"local-network"`
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_iOjSGBsukgxsTwogPZXVbYNiWfNiuzkrxEaEyKkeDPPUC.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": None,
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "local-network",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_UbhpeOtzAcNOggzCUrZQEtfRyYzcqqRDjgJhbmHSQyLqsMOXWpx(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_nodes" -> "?node_name" -> 
        "back_address"`
        
        В качестве значения ключа `"back_address"` передается `"external"`
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_UbhpeOtzAcNOggzCUrZQEtfRyYzcqqRDjgJhbmHSQyLqsMOXWpx.__doc__
        auth_nodes_settings = {
            "remote_nodes": {
                "alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_alfa_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("some1_wsBridge", "some2_wsBridge"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "password": None,
                            "port": 6379,
                            "db": 0,
                        }
                    },
                    "back_address": "external",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    ###
    def test_gISqxQYpsjXxajvDiidpyzcmobdiFhDYhEoFLszUtCiy(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_ws_nodes"`
        
        В качестве значения ключа `"auth_nodes_settings"` передается словарь
        с настройками только для `"remote_ws_nodes"`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_gISqxQYpsjXxajvDiidpyzcmobdiFhDYhEoFLszUtCiy.__doc__
        auth_nodes_settings = {
            "remote_ws_nodes": {
                "moscow_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "wsbridge": "someWsBridge"
                }
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_WOVlcLodvodhwaSbhcjubSzeenoOZGcbyvjRyIhA(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_ws_nodes"`
        
        В качестве значения ключа `"remote_nodes"` передается не валидный тип
        `str`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_ws_nodes'], 'type_error', '`context -> "auth_nodes_settings" -> "remote_ws_nodes: dict"` Значение ключа `"remote_ws_nodes"` должен быть тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_WOVlcLodvodhwaSbhcjubSzeenoOZGcbyvjRyIhA.__doc__
        auth_nodes_settings = {
            "remote_ws_nodes": "ffddd",
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_TjSuEWvmsRaCkrZMlBReWxuRiLhxizLrqpxAoiEsNdqcQk(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "key"`
        
        В качестве имени ключа значений `"remote_ws_nodes"` используется не
        валидный тип `tuple`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_ws_nodes', (1, 2)], 'structure error', '`context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "node_name"` Ключ `"node_name"` должен иметь тип `str`, и быть длиной `>=` 50 символов.')
                ]
            }
        }
        """
        msg = self.test_TjSuEWvmsRaCkrZMlBReWxuRiLhxizLrqpxAoiEsNdqcQk.__doc__
        auth_nodes_settings = {
            "remote_ws_nodes": {
                (1, 2): {
                    "wsbridge": "someWsBridge"
                }
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        

    def test_MklVUCAdpfihXLmhohLizkOfVcngMKkmbZflOiCuofC(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "key"`
        
        В качестве имени ключа значений `"remote_ws_nodes"` используется
        короткая строка `hello`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_MklVUCAdpfihXLmhohLizkOfVcngMKkmbZflOiCuofC.__doc__
        auth_nodes_settings = {
            "remote_ws_nodes": {
                "hello": {
                    "wsbridge": "someWsBridge"
                }
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_DsuijKImxGrwiHIyUaKRjdvNwtIgJCBATjjxkBfvwbsMnh(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "key" ->
        "wsbridge"`
        
        Ключ `wsbridge` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_ws_nodes', 'hello'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "node_name"` Ключ `"node_name"` должен иметь тип `str`, и быть длиной `>=` 50 символов.')
                ]
            }
        }
        """
        msg = self.test_DsuijKImxGrwiHIyUaKRjdvNwtIgJCBATjjxkBfvwbsMnh.__doc__
        auth_nodes_settings = {
            "remote_ws_nodes": {
                "hello": {
                }
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_xQlfTjWRdFqFHqnVBrPDsHJppgZpgYnJskQKaWzQeHzw(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "key" ->
        "wsbridge"`
        
        В качестве значения ключа `"wsbridge"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_ws_nodes', 'hello'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "node_name"` Ключ `"node_name"` должен иметь тип `str`, и быть длиной `>=` 50 символов.')
                ]
            }
        }
        """
        msg = self.test_xQlfTjWRdFqFHqnVBrPDsHJppgZpgYnJskQKaWzQeHzw.__doc__
        auth_nodes_settings = {
            "remote_ws_nodes": {
                "hello": {
                    "wsbridge": [],
                }
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
    
    # def test_LTGIvinfLeonVkPjygIBjybFZgiYzFLdTOccFxoBvpmW(self):
    #     """
    #     Основные условия:
    #     - `"sci_mode" - "standart"`
        
    #     Проверяется:
    #     `context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "key" ->
    #     "wsbridge"`
        
    #     В качестве значения ключа `"wsbridge"` передается не валидное имя
    #     которого нет в `SCI_SETTINGS["websocket_connections"]`
        
    #     Ожидаемый ответ:
    #     {
    #         'status': 'error', 
    #         'action': 'failed validation', 
    #         'data': {
    #             'description': 'failed validation', 
    #             'error_list': [
    #                 (['auth_nodes_settings', 'remote_ws_nodes', 'hello'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "node_name"` Ключ `"node_name"` должен иметь тип `str`, и быть длиной `>=` 50 символов.')
    #             ]
    #         }
    #     }
    #     """
    #     msg = self.test_LTGIvinfLeonVkPjygIBjybFZgiYzFLdTOccFxoBvpmW.__doc__
    #     auth_nodes_settings = {
    #         "remote_ws_nodes": {
    #             "hello": {
    #                 "wsbridge": "wrong_someWsBridge",
    #             }
    #         },
    #     }
    #     self.context["auth_nodes_settings"] = auth_nodes_settings
    #     ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
    #         validation_data=self.context,
    #         SCI_SETTINGS=self.SCI_SETTINGS,
    #         sci_mode=self.sci_mode
    #     ).start_validation()
    #     self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
    #     self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
    #     self.assertEqual(
    #         "failed validation", 
    #         ecsaddo_validate["action"], 
    #         msg=msg
    #     )
    #     self.assertEqual(
    #         "failed validation", 
    #         ecsaddo_validate["data"]["description"], 
    #         msg=msg
    #     )
        
        
    def test_ewyivIzsXzZgTAGcqjtHlmRMQceMgJYgokEPsvkuOdEp(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings"`
        
        2 `local_nodes` узла.
        2 `remote_nodes` узла.
        2 `remote_ws_nodes` узла.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_ewyivIzsXzZgTAGcqjtHlmRMQceMgJYgokEPsvkuOdEp.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    "wsBridgeBroker": ("wsBridge_one", "wsBridge_two"),
                },
                "gama_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZCoHZFkt": {
                    "node_rq": "sci_rq_gama_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZCoHZFkt",
                    "wsBridgeBroker": ("wsBridge_three",),
                },
            },
            "remote_nodes": {
                "charli_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_charli_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("wsBridge_three", "wsBridge_four"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
                "bravo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhbftygbhnjk": {
                    "node_rq": "sci_rq_bravo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhbftygbhnjk",
                    "wsBridgeBroker": ("wsBridge_five",),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "local-network",
                },
            },
            "remote_ws_nodes": {
                "moscow_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "wsbridge": "someWsBridge"
                },
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "wsbridge": "someWsBridge",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ok", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "successfully validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
    def test_MVDPfVMBxBaOPvMbJFnORUUTZYsXCzMNtdhlkwNKClH(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `context -> "auth_nodes_settings"`
        
        Два `local_nodes` узла.
        Два `remote_nodes` узла. (в 2 есть ошибка)
        Два `remote_ws_nodes` узла. (в 1 есть ошибка)
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['auth_nodes_settings', 'remote_nodes', 'bravo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhbftygbhnjk', 'broker_connection_settings', 'redis', 'port'], 'type error', '`context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" -> "broker_connection_settings" -> "redis" -> "port"` Значение ключа `"port"` должно иметь тип `int`.'), 
                    (['auth_nodes_settings', 'remote_ws_nodes', 'moscow_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ', 'wsbridge'], 'structure error', '`context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "node_name" -> "wsbridge"` Значение ключа `"wsbridge"` должно иметь тип `str`, и входить в `SCI_SETTINGS["websocket_connections"]`.')
                ]
            }
        }
        """
        msg = self.test_MVDPfVMBxBaOPvMbJFnORUUTZYsXCzMNtdhlkwNKClH.__doc__
        auth_nodes_settings = {
            "local_nodes": {
                "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
                    "wsBridgeBroker": ("wsBridge_one", "wsBridge_two"),
                },
                "gama_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZCoHZFkt": {
                    "node_rq": "sci_rq_gama_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZCoHZFkt",
                    "wsBridgeBroker": ("wsBridge_three",),
                },
            },
            "remote_nodes": {
                "charli_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb": {
                    "node_rq": "sci_rq_charli_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhb",
                    "wsBridgeBroker": ("wsBridge_three", "wsBridge_four"),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "external",
                },
                "bravo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhbftygbhnjk": {
                    "node_rq": "sci_rq_bravo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgdiuhbftygbhnjk",
                    "wsBridgeBroker": ("wsBridge_five",),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": "wrong_value",
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "local-network",
                },
            },
            "remote_ws_nodes": {
                "moscow_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "wsbridge": "wrong_value"
                },
                "jupiter_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ": {
                    "wsbridge": "someWsBridge",
                },
            },
        }
        self.context["auth_nodes_settings"] = auth_nodes_settings
        ecsaddo_validate: dict = NodeLifespanSystemSCIAppContext_Validate(
            validation_data=self.context,
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("error", ecsaddo_validate["status"],msg=msg)
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["action"], 
            msg=msg
        )
        self.assertEqual(
            "failed validation", 
            ecsaddo_validate["data"]["description"], 
            msg=msg
        )
        
        
if __name__ == "__main__":
    unittest.main()