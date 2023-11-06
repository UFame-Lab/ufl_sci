import unittest
import asyncio

from sci.sci_base.validators import SCI_SETTINGS_Validate
from sci.lib.patterns import isecsaddo
from sci.apps.nodeLifespanSystemSCIApp.application import (
    NodeLifespanSystemSCIApp
)


class FakeSCIApp:
    pass


class SCI_SETTINGS_Validate_sci_node_standart(unittest.TestCase):
    
    def setUp(self):
        SCI_SETTINGS = {
            "node_name": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": "/home/paul/Dev/ufame-lab/ufl_SCI_dev/SCI_0.1/sci/tests/test.log",
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
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = "standart"
        
    
    def test_bsnkOhrlbgypmLCXriJidCjekXrO(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_name"`
        
        Значение ключа `"node_name"` передается валидным.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_bsnkOhrlbgypmLCXriJidCjekXrO.__doc__
        self.SCI_SETTINGS["node_name"] = "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_yKVzIfGActMVrJXhushpmCwGXiovJGbLPXOh(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_name"`
        
        Ключ `"node_name"` не передан.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_name'], 'structure error', '`SCI_SETTINGS -> "node_name"` Значение ключа `"node_name"` должно иметь тип `str`, и быть длиной `>=` 50 символов.')
                ]
            }
        }
        """
        msg = self.test_yKVzIfGActMVrJXhushpmCwGXiovJGbLPXOh.__doc__
        del self.SCI_SETTINGS["node_name"]
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_aTQmSnGnwexEpMaJUErftUYBbiRQaevYSjpwtoJY(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_name"`
        
        В качестве значения ключа `"node_name"` передан не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_name'], 'structure error', '`SCI_SETTINGS -> "node_name"` Значение ключа `"node_name"` должно иметь тип `str`, и быть длиной `>=` 50 символов.')
                ]
            }
        }
        """
        msg = self.test_aTQmSnGnwexEpMaJUErftUYBbiRQaevYSjpwtoJY.__doc__
        self.SCI_SETTINGS["node_name"] = []
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_CTVvaYGYfBmndrcOONbIEzcKGNrBWeTZfbB(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_name"`
        
        В качестве значения ключа `"node_name"` передана строка `hello`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_name'], 'structure error', '`SCI_SETTINGS -> "node_name"` Значение ключа `"node_name"` должно иметь тип `str`, и быть длиной `>=` 50 символов.')
                ]
            }
        }
        """
        msg = self.test_CTVvaYGYfBmndrcOONbIEzcKGNrBWeTZfbB.__doc__
        self.SCI_SETTINGS["node_name"] = "hello"
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_PSywIIoitkJXcaTEXddQAraPGbTYCGvCnGIZvdf(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается валидное значение
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_PSywIIoitkJXcaTEXddQAraPGbTYCGvCnGIZvdf.__doc__
        self.SCI_SETTINGS["node_rq"] = "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_BzGfMlyhMxGkSPGvdoNNlozoAergEPEzRzeHe(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_rq"`
        
        Ключ `"node_rq"` не передан
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_rq'], 'structure error', '`SCI_SETTINGS -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_BzGfMlyhMxGkSPGvdoNNlozoAergEPEzRzeHe.__doc__
        del self.SCI_SETTINGS["node_rq"]
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_sNRCTEgCfkXxOZbfNDiRYIKSbUAnPdLkIRRSrJW(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_rq'], 'structure error', '`SCI_SETTINGS -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_sNRCTEgCfkXxOZbfNDiRYIKSbUAnPdLkIRRSrJW.__doc__
        self.SCI_SETTINGS["node_rq"] = []
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_kJYRshEWdkMLzdWESlIwocHbCNdr(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается строка "hello"
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_rq'], 'structure error', '`SCI_SETTINGS -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_kJYRshEWdkMLzdWESlIwocHbCNdr.__doc__
        self.SCI_SETTINGS["node_rq"] = "hello"
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
    
    
    def test_buzUDnEMShSZaxDUXwVngyjyGv(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_rq"`
        
        В качестве значения ключа `"node_rq"` передается строка `> 50` символов,
        но без префикса `SCI_NODE_RQ_PREFIX`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_rq'], 'structure error', '`SCI_SETTINGS -> "node_rq"` Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_buzUDnEMShSZaxDUXwVngyjyGv.__doc__
        self.SCI_SETTINGS["node_rq"] = "sci_sci_sci_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_opRCISMhZfTrIDWSbdChDHTZBR(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_aq"`
        
        В качестве значения ключа `"node_aq"` передается валидное значение
        `asyncio.Queue()` 
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_opRCISMhZfTrIDWSbdChDHTZBR.__doc__
        self.SCI_SETTINGS["node_aq"] = asyncio.Queue()
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_JuBtuQOcWKzeeDYZWBqvkJSexxQshK(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_aq"`
        
        Ключ `"node_aq"` не передается. 
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_aq'], 'structure error', '`SCI_SETTINGS -> "node_aq"` Значение ключа `"node_aq"` должно иметь тип `asyncio.Queue()`')
                ]
            }
        }
        """
        msg = self.test_JuBtuQOcWKzeeDYZWBqvkJSexxQshK.__doc__
        del self.SCI_SETTINGS["node_aq"]
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_CMcckiqQyxGXNmJgGrSDuKvHGWwVCrkB(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "node_aq"`
        
        В качестве значения ключа `"node_aq"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_aq'], 'structure error', '`SCI_SETTINGS -> "node_aq"` Значение ключа `"node_aq"` должно иметь тип `asyncio.Queue()`')
                ]
            }
        }
        """
        msg = self.test_CMcckiqQyxGXNmJgGrSDuKvHGWwVCrkB.__doc__
        self.SCI_SETTINGS["node_aq"] = []
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_vEKQQjaDzDToUdtVtXUarZFWhSxxufWNmJiOnpTyWChvPeSoEnSmu(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "logfilePath"`
        
        В качестве значения ключа `"logfilePath"` передается валидное значение.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_vEKQQjaDzDToUdtVtXUarZFWhSxxufWNmJiOnpTyWChvPeSoEnSmu.__doc__
        self.SCI_SETTINGS["logfilePath"] = "/home/paul/Dev/ufame-lab/ufl_SCI_dev/SCI_0.1/sci/tests/test.log"
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_UFoQWyYpRkKaZiJuEQiVkoeNXdVUoU(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "logfilePath"`
        
        Ключ `"logfilePath"` не передается
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['logfilePath'], 'structure error', '`SCI_SETTINGS -> "logfilePath"` Значение ключа `"logfilePath"` должно иметь тип `str` и указывать путь к существующему `log` файлу. `log` файл должен быть доступен для записи.')
                ]
            }
        }
        """
        msg = self.test_UFoQWyYpRkKaZiJuEQiVkoeNXdVUoU.__doc__
        del self.SCI_SETTINGS["logfilePath"]
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_iIYJTdgUTltUWYjuKSBlTnteYuwAVgkAXKCfOTlLq(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "logfilePath"`
        
        В качестве значения ключа `"logfilePath"` передается не валидный тип
        `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['logfilePath'], 'structure error', '`SCI_SETTINGS -> "logfilePath"` Значение ключа `"logfilePath"` должно иметь тип `str` и указывать путь к существующему `log` файлу. `log` файл должен быть доступен для записи.')
                ]
            }
        }
        """
        msg = self.test_iIYJTdgUTltUWYjuKSBlTnteYuwAVgkAXKCfOTlLq.__doc__
        self.SCI_SETTINGS["logfilePath"] = []
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_TbwcHEYNUxdNushDuuqsh(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf"`
        
        В качестве значения ключа `"AppConf"` передается валидное значение.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_TbwcHEYNUxdNushDuuqsh.__doc__
        AppConf = [
            (NodeLifespanSystemSCIApp, "nodeLifespanSystemSCIApp", {}),
        ]
        self.SCI_SETTINGS["AppConf"] = AppConf
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_DBryFLElGXVgBjRhNdmXNuYmUwCffATehfFG(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf"`
        
        Ключ `"AppConf"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf'], 'structure error', '`SCI_SETTINGS -> "AppConf"` Значение ключа `"AppConf"` должно иметь тип `list`. В качестве содержимого `"AppConf"` выступают кортежи с настройками приложений. `"AppConf"` должен содержать настройку как минимум 1 приложения.')
                ]
            }
        }
        """
        msg = self.test_DBryFLElGXVgBjRhNdmXNuYmUwCffATehfFG.__doc__
        del self.SCI_SETTINGS["AppConf"]
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_NiNmUGUYnubhmmXqFSKVmwzDmNSHORuTIEICP(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf"`
        
        В качестве значения ключа `"AppConf"` передается не валидный тип `{}`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf'], 'structure error', '`SCI_SETTINGS -> "AppConf"` Значение ключа `"AppConf"` должно иметь тип `list`. В качестве содержимого `"AppConf"` выступают кортежи с настройками приложений. `"AppConf"` должен содержать настройку как минимум 1 приложения.')
                ]
            }
        }
        """
        msg = self.test_NiNmUGUYnubhmmXqFSKVmwzDmNSHORuTIEICP.__doc__
        self.SCI_SETTINGS["AppConf"] = {}
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_gYLGdtVNaLknyFxPSPhLahLjq(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf"`
        
        В качестве значения ключа `"AppConf"` передается пустой список.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf'], 'structure error', '`SCI_SETTINGS -> "AppConf"` Значение ключа `"AppConf"` должно иметь тип `list`. В качестве содержимого `"AppConf"` выступают кортежи с настройками приложений. `"AppConf"` должен содержать настройку как минимум 1 приложения.')
                ]
            }
        }
        """
        msg = self.test_gYLGdtVNaLknyFxPSPhLahLjq.__doc__
        self.SCI_SETTINGS["AppConf"] = []
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_ljxLMTDwOLzrXJUuJIUAbzsRNgE(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf" -> 0 -> 0`
        
        В качестве первого значения в кортеже с настройками конкретного 
        приложения передается не валидное значение (`FakeSCIApp`).
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf', 0], 'structure error', '`SCI_SETTINGS -> "AppConf" -> 0` Кортеж с настройками приложения должен иметь структуру: Первый элемент - класс SCIAPP пользовательского приложения производный от базового `SCI_BaseAppController`. Второй элемент - `app_name` имя приложения в виде строки. Третий элемент - словарь с дополнительными, опциональными переменными.')
                ]
            }
        }
        """
        msg = self.test_ljxLMTDwOLzrXJUuJIUAbzsRNgE.__doc__
        
        AppConf = [
            (FakeSCIApp, "FakeSCIApp", {}),
        ]
        self.SCI_SETTINGS["AppConf"] = AppConf
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_nlhgilBIFtWKSRlPiNiqIQCxE(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf" -> 0 -> 1`
        
        В качестве второго значения в кортеже с настройками конкретного 
        приложения передается не валидный тип `dict`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf', 0], 'structure error', '`SCI_SETTINGS -> "AppConf" -> 0` Кортеж с настройками приложения должен иметь структуру: Первый элемент - класс SCIAPP пользовательского приложения производный от базового `SCI_BaseAppController`. Второй элемент - `app_name` имя приложения в виде строки. Третий элемент - словарь с дополнительными, опциональными переменными.')
                ]
            }
        }
        """
        msg = self.test_nlhgilBIFtWKSRlPiNiqIQCxE.__doc__
        
        AppConf = [
            (NodeLifespanSystemSCIApp, {}, {}),
        ]
        self.SCI_SETTINGS["AppConf"] = AppConf
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_UYgPeGMaMZHBUGnZhCRfORli(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf" -> 0 -> 1`
        
        В качестве второго значения в кортеже с настройками конкретного 
        приложения передается не валидная строка `hi`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf', 0, 0], 'structure error', '`SCI_SETTINGS -> "AppConf" -> 0 -> 1` `app_name` должен быть уникальным и состоянть `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_UYgPeGMaMZHBUGnZhCRfORli.__doc__
        
        AppConf = [
            (NodeLifespanSystemSCIApp, "hi", {}),
        ]
        self.SCI_SETTINGS["AppConf"] = AppConf
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_tkTMjlpyBQRbfHqvjoWodxfbL(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf" -> 0 -> 2`
        
        В качестве третьего значения котрежа с настройками конкретного
        приложения, ничего не передается
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf', 0], 'structure error', '`SCI_SETTINGS -> "AppConf" -> 0` Кортеж с настройками приложения должен иметь структуру: Первый элемент - класс SCIAPP пользовательского приложения производный от базового `SCI_BaseAppController`. Второй элемент - `app_name` имя приложения в виде строки. Третий элемент - словарь с дополнительными, опциональными переменными.')
                ]
            }
        }
        """
        msg = self.test_tkTMjlpyBQRbfHqvjoWodxfbL.__doc__
        
        AppConf = [
            (NodeLifespanSystemSCIApp, "NodeLifespanSystemSCIApp"),
        ]
        self.SCI_SETTINGS["AppConf"] = AppConf
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_qFdgrNnzHEBLcNJvPFHBlUUxLWJOgPdzoNZav(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf" -> 0 -> 1`
        
        В качестве второго значения котрежа с настройками конкретного
        приложения, передается не уникальное значение.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf', 1, 0], 'structure error', '`SCI_SETTINGS -> "AppConf" -> 0 -> 1` `app_name` должен быть уникальным и состоянть `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_qFdgrNnzHEBLcNJvPFHBlUUxLWJOgPdzoNZav.__doc__
        
        AppConf = [
            (NodeLifespanSystemSCIApp, "NodeLifespanSystemSCIApp", {}),
            (NodeLifespanSystemSCIApp, "NodeLifespanSystemSCIApp", {}),
        ]
        self.SCI_SETTINGS["AppConf"] = AppConf
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_vrUnVYjRMklHPPeJMbOMQtiAvjiZZ(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf" -> 0 -> 2`
        
        В качестве третьего значения котрежа с настройками конкретного
        приложения, передается значение с не валидным типом `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf', 0], 'structure error', '`SCI_SETTINGS -> "AppConf" -> 0` Кортеж с настройками приложения должен иметь структуру: Первый элемент - класс SCIAPP пользовательского приложения производный от базового `SCI_BaseAppController`. Второй элемент - `app_name` имя приложения в виде строки. Третий элемент - словарь с дополнительными, опциональными переменными.'
                ]
            }
        }
        """
        msg = self.test_vrUnVYjRMklHPPeJMbOMQtiAvjiZZ.__doc__
        
        AppConf = [
            (NodeLifespanSystemSCIApp, "NodeLifespanSystemSCIApp", []),
        ]
        self.SCI_SETTINGS["AppConf"] = AppConf
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_rmoKFhxJexeuWJojfqnEOHhPJE(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf" -> 0`
        
        В качестве значения `AppConf` передается 2 валидных кортежа с
        настройками приложений.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_rmoKFhxJexeuWJojfqnEOHhPJE.__doc__
        
        AppConf = [
            (NodeLifespanSystemSCIApp, "NodeLifespanSystemSCIApp", {}),
            (NodeLifespanSystemSCIApp, "second_NodeLifespanSystemSCIApp", {}),
        ]
        self.SCI_SETTINGS["AppConf"] = AppConf
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_ZhyaGCHImZciUfJWseMLpVsKAkTcgINHVVhTUfuSe(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes"`
        
        В качестве значения ключа `nodes` передается валидное значение.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_ZhyaGCHImZciUfJWseMLpVsKAkTcgINHVVhTUfuSe.__doc__
        
        nodes = {
            "local_nodes": {},
            "remote_nodes": {},
            "remote_ws_nodes": {},
        }
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_kYmabzfjDoQqEFYTvvYaPzl(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes"`
        
        Ключ `"nodes"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes"` Значение ключа `"nodes"` должен иметь тип `dict`')
                ]
            }
        }
        """
        msg = self.test_kYmabzfjDoQqEFYTvvYaPzl.__doc__
        del self.SCI_SETTINGS["nodes"]
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_mwNkOklMrAhuUzlevWtEatT(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes"`
        
        В качестве значения ключа `"nodes"` передается пустой `dict`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes" -> "local_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_ws_nodes"` `"nodes"` должен содержать обязательные ключи "local_nodes", "remote_nodes", "remote_ws_nodes", значением которых должен быть `dict`.')
            }
        }
        """
        msg = self.test_mwNkOklMrAhuUzlevWtEatT.__doc__
        nodes = {}
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_JWNNWJHCwlUEiORDiNupQkhfTTLKUhlMVjSc(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes"`
        
        В качестве значения ключа `"nodes"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes"` Значение ключа `"nodes"` должен иметь тип `dict`')
            }
        }
        """
        msg = self.test_JWNNWJHCwlUEiORDiNupQkhfTTLKUhlMVjSc.__doc__
        nodes = []
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_TkxHsKtNxsIzUNHSvRtILjBFNTewJJLitClSVCT(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes" -> "local_nodes"`
        
        В качестве значения ключа `"local_nodes"` передается не валидный тип 
        `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes" -> "local_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_ws_nodes"` `"nodes"` должен содержать обязательные ключи "local_nodes", "remote_nodes", "remote_ws_nodes", значением которых должен быть `dict`.')
            }
        }
        """
        msg = self.test_TkxHsKtNxsIzUNHSvRtILjBFNTewJJLitClSVCT.__doc__
        nodes = {
            "local_nodes": [],
            "remote_nodes": {},
            "remote_ws_nodes": {},
        }
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_fsFSMPLIrVaPMatIlGYrxZxBnC(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes" -> "local_nodes"`
        
        Ключ `"local_nodes"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes" -> "local_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_ws_nodes"` `"nodes"` должен содержать обязательные ключи "local_nodes", "remote_nodes", "remote_ws_nodes", значением которых должен быть `dict`.')
            }
        }
        """
        msg = self.test_fsFSMPLIrVaPMatIlGYrxZxBnC.__doc__
        nodes = {
            "remote_nodes": {},
            "remote_ws_nodes": {},
        }
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_cnnyILUEdxcfkpZFNRIJAeFwmpVSf(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes" -> "remote_nodes"`
        
        В качестве значения ключа `"remote_nodes"` передается не валидный тип
        `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes" -> "local_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_ws_nodes"` `"nodes"` должен содержать обязательные ключи "local_nodes", "remote_nodes", "remote_ws_nodes", значением которых должен быть `dict`.')
            }
        }
        """
        msg = self.test_cnnyILUEdxcfkpZFNRIJAeFwmpVSf.__doc__
        nodes = {
            "local_nodes": {},
            "remote_nodes": [],
            "remote_ws_nodes": {},
        }
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_ydYHyyHlJVuRzmadjYkpOuDCnsDJUzBRKqtaL(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes" -> "remote_nodes"`
        
        Ключ `"remote_nodes"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes" -> "local_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_ws_nodes"` `"nodes"` должен содержать обязательные ключи "local_nodes", "remote_nodes", "remote_ws_nodes", значением которых должен быть `dict`.')
            }
        }
        """
        msg = self.test_ydYHyyHlJVuRzmadjYkpOuDCnsDJUzBRKqtaL.__doc__
        nodes = {
            "local_nodes": {},
            "remote_ws_nodes": {},
        }
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_RdLKcwodqXWuAnivXbqiRvWMUjHQGQRqDEuspXS(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes" -> "remote_ws_nodes"`
        
        В качестве значения ключа `"remote_ws_nodes"` передается не валидный тип
        `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes" -> "local_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_ws_nodes"` `"nodes"` должен содержать обязательные ключи "local_nodes", "remote_nodes", "remote_ws_nodes", значением которых должен быть `dict`.')
            }
        }
        """
        msg = self.test_RdLKcwodqXWuAnivXbqiRvWMUjHQGQRqDEuspXS.__doc__
        nodes = {
            "local_nodes": {},
            "remote_nodes": {},
            "remote_ws_nodes": [],
        }
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_CftaGfyQvejbikNAvZRMgosNOXAonNJOgLk(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "nodes" -> "remote_ws_nodes"`
        
        Ключ `"remote_ws_nodes"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "nodes" -> "local_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_nodes"` `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_ws_nodes"` `"nodes"` должен содержать обязательные ключи "local_nodes", "remote_nodes", "remote_ws_nodes", значением которых должен быть `dict`.')
            }
        }
        """
        msg = self.test_CftaGfyQvejbikNAvZRMgosNOXAonNJOgLk.__doc__
        nodes = {
            "local_nodes": {},
            "remote_nodes": {},
        }
        self.SCI_SETTINGS["nodes"] = nodes
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_ZBzQIsFDlcdYkePcCutNvcuEFMGWTapSa(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections"`
        
        В качестве значения ключа`"websocket_connections"` передается 
        валидное значение.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_ZBzQIsFDlcdYkePcCutNvcuEFMGWTapSa.__doc__
        websocket_connections = {
            "someWsBridge": {
                "url": "ws://localhost:8555/ws/chat/100/",
                "headers": {},
                "wsBridgeBroker_aq": asyncio.Queue(),
            }
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_DjJuKrodAnTmRCVhMuvKlECZxwzZ(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections"`
        
        В качестве значения ключа `"websocket_connections"` передается не
        валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "websocket_connections"` Значение ключа `"websocket_connections"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_DjJuKrodAnTmRCVhMuvKlECZxwzZ.__doc__
        websocket_connections = []
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_cUrOtSUzWUsLQAMsmOXOdRerKBlBFklJJD(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections"`
        
        В качестве имени ключа `wsBridge` передается не валидный тип `tuple`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections', (1, 2, 3)], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "websocket_connections"` Ключи словаря `"websocket_connections" это `str` имена `wsBridge` сервисов, а значения ключей - словари с настройками `ws` подключения. id:RlfosdZKBUKFURmDxcCZ `SCI_SETTINGS -> "AppConf" -> "websocket_connections" ->')
                ]
            }
        }
        """
        msg = self.test_cUrOtSUzWUsLQAMsmOXOdRerKBlBFklJJD.__doc__
        websocket_connections = {
            (1,2,3): {
                "url": "ws://localhost:8555/ws/chat/100/",
                "headers": {},
                "wsBridgeBroker_aq": asyncio.Queue(),
            }
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_WezcczVgsueoQGfhLrqaommBBFKCPjiWkNDV(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections" -> "someWsBridge" -> "url"`
        
        Ключ `"url"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections', 'someWsBridge', 'url'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "websocket_connections" -> "wsBridgeName" -> "url"`. Ключ `"url"` должен иметь значение типа `str`.')
                ]
            }
        }
        """
        msg = self.test_WezcczVgsueoQGfhLrqaommBBFKCPjiWkNDV.__doc__
        websocket_connections = {
            "someWsBridge": {
                "headers": {},
                "wsBridgeBroker_aq": asyncio.Queue(),
            }
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_MunCBuDcnOaIZoGrJScLFdNvPOJFiSg(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections" -> "someWsBridge" -> "url"`
        
        В качестве значения ключа `"url"` передается не валидный тип `list` 
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections', 'someWsBridge', 'url'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "websocket_connections" -> "wsBridgeName" -> "url"`. Ключ `"url"` должен иметь значение типа `str`.')
                ]
            }
        }
        """
        msg = self.test_MunCBuDcnOaIZoGrJScLFdNvPOJFiSg.__doc__
        websocket_connections = {
            "someWsBridge": {
                "url": [],
                "headers": {},
                "wsBridgeBroker_aq": asyncio.Queue(),
            }
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_jMvTXXIFiQrXhjmDYIRSTxVYXoQrCCIz(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections" -> "someWsBridge" -> "headers"`
        
        Ключ `"headers"` не передается. 
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections', 'someWsBridge', 'headers'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "websocket_connections" -> "wsBridgeName" -> "headers"`. Ключ `"headers"` должен иметь значение типа `dict`.')
                ]
            }
        }
        """
        msg = self.test_jMvTXXIFiQrXhjmDYIRSTxVYXoQrCCIz.__doc__
        websocket_connections = {
            "someWsBridge": {
                "url": "ws://localhost:8555/ws/chat/100/",
                "wsBridgeBroker_aq": asyncio.Queue(),
            }
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_LdRZIvFKJshVFSVydppQKOFULqzkk(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections" -> "someWsBridge" -> "headers"`
        
        В качестве значения ключа `"headers"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections', 'someWsBridge', 'headers'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "websocket_connections" -> "wsBridgeName" -> "headers"`. Ключ `"headers"` должен иметь значение типа `dict`.')
                ]
            }
        }
        """
        msg = self.test_LdRZIvFKJshVFSVydppQKOFULqzkk.__doc__
        websocket_connections = {
            "someWsBridge": {
                "url": "ws://localhost:8555/ws/chat/100/",
                "headers": [],
                "wsBridgeBroker_aq": asyncio.Queue(),
            }
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_tFAlnAsFCNHLBchTnKOiFKuefncDAb(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections" -> "someWsBridge" -> 
        "wsBridgeBroker_aq"`
        
        Ключ `"wsBridgeBroker_aq"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections', 'someWsBridge', 'wsBridgeBroker_aq'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "websocket_connections" -> "wsBridgeName" -> "wsBridgeBroker_aq"`. Ключ `"wsBridgeBroker_aq"` должен иметь значение типа `asyncio.Queue`.')
                ]
            }
        }
        """
        msg = self.test_tFAlnAsFCNHLBchTnKOiFKuefncDAb.__doc__
        websocket_connections = {
            "someWsBridge": {
                "url": "ws://localhost:8555/ws/chat/100/",
                "headers": {},
            }
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_oHauUroyStRWoPIsmNCsosDybt(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections" -> "someWsBridge" -> 
        "wsBridgeBroker_aq"`
        
        В качестве значения ключа `"wsBridgeBroker_aq"` передается не валидный
        тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections', 'someWsBridge', 'wsBridgeBroker_aq'], 'structure error', '`SCI_SETTINGS -> "AppConf" -> "websocket_connections" -> "wsBridgeName" -> "wsBridgeBroker_aq"`. Ключ `"wsBridgeBroker_aq"` должен иметь значение типа `asyncio.Queue`.')
                ]
            }
        }
        """
        msg = self.test_oHauUroyStRWoPIsmNCsosDybt.__doc__
        websocket_connections = {
            "someWsBridge": {
                "url": "ws://localhost:8555/ws/chat/100/",
                "headers": {},
                "wsBridgeBroker_aq": [],
            }
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_YRTGWhOzinIwTnvczbPgskGiensKAEAOYaPF(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "websocket_connections" -> "someWsBridge" -> 
        "wsBridgeBroker_aq"`
        
        В качестве значения ключа `"wsBridgeBroker_aq"` передается не валидный
        тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_YRTGWhOzinIwTnvczbPgskGiensKAEAOYaPF.__doc__
        websocket_connections = {
            "someWsBridge_first": {
                "url": "ws://localhost:8555/ws/chat/100/",
                "headers": {},
                "wsBridgeBroker_aq": asyncio.Queue(),
            },
            "someWsBridge_second": {
                "url": "ws://localhost:8555/ws/chat/100/",
                "headers": {},
                "wsBridgeBroker_aq": asyncio.Queue(),
            },
        }
        self.SCI_SETTINGS["websocket_connections"] = websocket_connections
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_JOQoqXhOcqqmKObXPHNThYanqxgmxyAVsjvFee(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings"`
        
        В качестве значения ключа `"local_broker_connection_settings"`
        передается валидное значение.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_JOQoqXhOcqqmKObXPHNThYanqxgmxyAVsjvFee.__doc__
        local_broker_connection_settings = {
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
        }
        self.SCI_SETTINGS["local_broker_connection_settings"] = (
            local_broker_connection_settings
        )
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_szoYAYwhomKOXXuMgcjiWWQnLlKtxcMSiXKhKT(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings"`
        
        Ключ `"local_broker_connection_settings"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings"` Значение ключа `"broker_connection_settings"` должен быть тип `dict`, который должен содержать ключ `"redis"`.')
                ]
            }
        }
        """
        msg = self.test_szoYAYwhomKOXXuMgcjiWWQnLlKtxcMSiXKhKT.__doc__
        del self.SCI_SETTINGS["local_broker_connection_settings"]
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_fqthMnJXIwHfusuTrncElapUZYehlGIuuAz(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings"`
        
        В качестве значения ключа `"local_broker_connection_settings"`
        передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings"` Значение ключа `"broker_connection_settings"` должен быть тип `dict`, который должен содержать ключ `"redis"`.')
                ]
            }
        }
        """
        msg = self.test_fqthMnJXIwHfusuTrncElapUZYehlGIuuAz.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = []
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_qJfQmUeWmHDOlkMkvBaPHsioECZx(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings"`
        
        В качестве значения ключа `"local_broker_connection_settings"`
        передается пустой `dict`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings"` Значение ключа `"broker_connection_settings"` должен быть тип `dict`, который должен содержать ключ `"redis"`.')
                ]
            }
        }
        """
        msg = self.test_qJfQmUeWmHDOlkMkvBaPHsioECZx.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {}
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_jKaSPKXeujmtjRRTWxAJsAJoNEvsOBk(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis"`
        
        В качестве значения ключа `"redis"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host`, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_jKaSPKXeujmtjRRTWxAJsAJoNEvsOBk.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": []
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_ivGqVzsHVFuyAHEaIxtoSwPiPPPsoov(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis"`
        
        В качестве значения ключа `"redis"` передается пустой `dict`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host`, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_ivGqVzsHVFuyAHEaIxtoSwPiPPPsoov.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {}
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_NhCcwAObRdnCAmqnXlOatiqgOjIFAGxdO(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> "host"`
        
        Ключ `"host"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host`, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_NhCcwAObRdnCAmqnXlOatiqgOjIFAGxdO.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_MmeMfhsTbrSiePRxxmJNdgkdOsJNNjzukU(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> "host"`
        
        В качестве значения ключа `"host"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'host'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "host"` Значение ключа `"host"` должно иметь тип `dict`')
                ]
            }
        }
        """
        msg = self.test_MmeMfhsTbrSiePRxxmJNdgkdOsJNNjzukU.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": [],
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_aZskeNiVcfgVunXUtREjxmfYqXXgRUeYeqdA(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> "host"`
        
        В качестве значения ключа `"host"` передается пустой `dict`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'host', 'local'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "host" -> "local"` Значение ключа `"local"` должно иметь тип `str`')
                ]
            }
        }
        """
        msg = self.test_aZskeNiVcfgVunXUtREjxmfYqXXgRUeYeqdA.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {},
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_sdFutqngObIHhkPlbuXXSBYaZGnEPtt(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "host" -> "local"`
        
        В качестве значения ключа `"local"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'host', 'local'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "host" -> "local"` Значение ключа `"local"` должно иметь тип `str`')
                ]
            }
        }
        """
        msg = self.test_sdFutqngObIHhkPlbuXXSBYaZGnEPtt.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": [],
                },
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_AmfBOyHxMDvpnwdjFFOGgoYeLmzZzRuWc(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "host" -> "local"`
        
        В качестве значения ключа `"local"` передается валидное значение.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_AmfBOyHxMDvpnwdjFFOGgoYeLmzZzRuWc.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                },
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_ZIlFsvbDSyFDRbsVqLkJZbymaidQbSJTj(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "host" -> "local-network"`
        
        В качестве значения ключа `"local-network"` передается не валидный 
        тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'host', 'local-network'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "host" -> "local-network"` Значение ключа `"local-network"` должно иметь тип `str`.')
                ]
            }
        }
        """
        msg = self.test_ZIlFsvbDSyFDRbsVqLkJZbymaidQbSJTj.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": [],
                },
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_hySYMhiLCUzsBxTGWwTYnhUghJPoncogcfgXko(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "host" -> "local-network"`
        
        В качестве значения ключа `"local-network"` передается валидное
        значение.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_hySYMhiLCUzsBxTGWwTYnhUghJPoncogcfgXko.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                },
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_ctEtMrRjfKcqfZAWZBZbJaSGlzKGNfJLXDrCHh(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "host" -> "external"`
        
        В качестве значения ключа `"external"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'host', 'external'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "host" -> "external"` Значение ключа `"external"` должно иметь тип `str`.')
                ]
            }
        }
        """
        msg = self.test_ctEtMrRjfKcqfZAWZBZbJaSGlzKGNfJLXDrCHh.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "external": [],
                },
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
    
    def test_fZZAznVhyPdoTLbFtmQLwcJjwMUslyGmVIUJBdIyMNtynG(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "host" -> "external"`
        
        В качестве значения ключа `"external"` передается валидное
        значение.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_fZZAznVhyPdoTLbFtmQLwcJjwMUslyGmVIUJBdIyMNtynG.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "external": "localhost",
                },
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_UTrHUzcEGgXwJxzTVEFRzLUulzDtgH(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "port"`
        
        Ключ `"port"` не указывается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host`, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_UTrHUzcEGgXwJxzTVEFRzLUulzDtgH.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_uQpgKIYDUiZkLFBNFHDLGxRcXLvEhEGREiQNMApx(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "port"`
        
        В качестве значения ключа `"port"` указывается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'port'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "port"` Значение ключа `"port"` должно иметь тип `int`')
                ]
            }
        }
        """
        msg = self.test_uQpgKIYDUiZkLFBNFHDLGxRcXLvEhEGREiQNMApx.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "port": [],
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_NIPXZbSMxNiARQnxRJmSgLpWHJFkUdHFCljkEqNO(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "password"`
        
        Ключ `"password"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host`, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_NIPXZbSMxNiARQnxRJmSgLpWHJFkUdHFCljkEqNO.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "port": 6379,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_KEafcEcKPTbxaGnbyPVIUXkV(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "password"`
        
        В качестве значения ключа `"password"` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'password'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "password"` Значение ключа `"password"` должно иметь тип `str` и быть длиной `>=` 3 символам, или быть `None`.')
                ]
            }
        }
        """
        msg = self.test_KEafcEcKPTbxaGnbyPVIUXkV.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "port": 6379,
                "password": [],
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_WjycJmpIAHYYzsFlPHlCttKCrWYn(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "password"`
        
        В качестве значения ключа `"password"` передается не валидное значение
        `hi`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'password'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "password"` Значение ключа `"password"` должно иметь тип `str` и быть длиной `>=` 3 символам, или быть `None`.')
                ]
            }
        }
        """
        msg = self.test_WjycJmpIAHYYzsFlPHlCttKCrWYn.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "port": 6379,
                "password": "hi",
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_UwEZofSIEYMMjvvDZXORKbRzABqOxoI(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "password"`
        
        В качестве значения ключа `"password"` передается валидное значение
        `"mypassword"`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_UwEZofSIEYMMjvvDZXORKbRzABqOxoI.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "port": 6379,
                "password": "mypassword",
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_DzjYJKFRZZtkitwrGQduylpfHNZeU(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "password"`
        
        В качестве значения ключа `"password"` передается валидное значение
        `None`.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_DzjYJKFRZZtkitwrGQduylpfHNZeU.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "port": 6379,
                "password": None,
                "db": 0
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_SjiAicdpgLXuyEfEiCSyGVaTMWGZlrZQHnJi(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> 
        "db"`
        
        Ключ `db` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis"` Словарь `"redis"` должен содержать ключи: `host`, \'port\', \'password\', \'db`.')
                ]
            }
        }
        """
        msg = self.test_SjiAicdpgLXuyEfEiCSyGVaTMWGZlrZQHnJi.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "port": 6379,
                "password": None,
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_OyeQqPhciTRgDgpDCLOtmPcVqYnTUeiiKTTpmihua(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS -> "local_broker_connection_settings" -> "redis" -> "db"`
        
        В качестве значения ключа `db` передается не валидный тип `list`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings', 'redis', 'db'], 'structure error', '`SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "db"` Значение ключа `"db"` должно иметь тип `int`.')
                ]
            }
        }
        """
        msg = self.test_OyeQqPhciTRgDgpDCLOtmPcVqYnTUeiiKTTpmihua.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = {
            "redis": {
                "host": {
                    "local": "localhost",
                    "local-network": "localhost",
                    "external": "localhost",
                },
                "port": 6379,
                "password": None,
                "db": []
            }
        }
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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
        
        
    def test_uJRVCAErHXSCRQxuNxQwJXgcFksc(self):
        """
        Основные условия:
        - `"sci_mode" - "standart"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['related_node_rq'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_uJRVCAErHXSCRQxuNxQwJXgcFksc.__doc__
        self.SCI_SETTINGS.setdefault(
            "related_node_rq", 
            "sci_rq_alfa_node_aCtn4R2k3qPtzrGzxNhcZTrkfMCXJqHLwLwIvIcKtgrAscodORjfhYQeaBBiI"
        )
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
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