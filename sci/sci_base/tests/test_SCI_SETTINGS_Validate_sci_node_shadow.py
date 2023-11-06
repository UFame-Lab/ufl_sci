import unittest
import asyncio

from sci.sci_base.validators import SCI_SETTINGS_Validate
from sci.lib.patterns import isecsaddo


class SCI_SETTINGS_Validate_sci_node_shadow(unittest.TestCase):
    
    def setUp(self):
        SCI_SETTINGS = {
            "related_node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "logfilePath": "/home/paul/Dev/ufame-lab/ufl_SCI_dev/SCI_0.1/sci/tests/test.log",
            "local_broker_connection_settings": {
                "redis": {
                    "host": {
                        "local": "localhost",
                        "local-tetwork": "localhost",
                        "external": "localhost",
                    },
                    "port": 6379,
                    "password": None,
                    "db": 0,
                }
            },
        }
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = "shadow"
        
        
    def test_PSywIIoitkJXcaTEXddQAraPGbTYCGvCnGIZvdf(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS -> "related_node_rq"`
        
        В качестве значения ключа `"related_node_rq"` передается валидное значение
        
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
        self.SCI_SETTINGS["related_node_rq"] = "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ"
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
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS -> "related_node_rq"`
        
        Ключ `"related_node_rq"` не передан
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['related_node_rq'], 'structure error', '`SCI_SETTINGS -> "related_node_rq"` Значение ключа `"related_node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_BzGfMlyhMxGkSPGvdoNNlozoAergEPEzRzeHe.__doc__
        del self.SCI_SETTINGS["related_node_rq"]
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
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS -> "related_node_rq"`
        
        В качестве значения ключа `"related_node_rq"` передается не валидный 
        тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['related_node_rq'], 'structure error', '`SCI_SETTINGS -> "related_node_rq"` Значение ключа `"related_node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_sNRCTEgCfkXxOZbfNDiRYIKSbUAnPdLkIRRSrJW.__doc__
        self.SCI_SETTINGS["related_node_rq"] = []
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
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS -> "related_node_rq"`
        
        В качестве значения ключа `"related_node_rq"` передается строка "hello"
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['related_node_rq'], 'structure error', '`SCI_SETTINGS -> "related_node_rq"` Значение ключа `"related_node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_kJYRshEWdkMLzdWESlIwocHbCNdr.__doc__
        self.SCI_SETTINGS["related_node_rq"] = "hello"
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
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS -> "related_node_rq"`
        
        В качестве значения ключа `"related_node_rq"` передается строка `> 50` 
        символов, но без префикса `SCI_NODE_RQ_PREFIX`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['related_node_rq'], 'structure error', '`SCI_SETTINGS -> "related_node_rq"` Значение ключа `"related_node_rq"` должно иметь тип `str`, начинаться с префикса `SCI_NODE_RQ_PREFIX`, и иметь длину `>=` 50 символам не включая SCI_NODE_RQ_PREFIX.')
                ]
            }
        }
        """
        msg = self.test_buzUDnEMShSZaxDUXwVngyjyGv.__doc__
        self.SCI_SETTINGS["related_node_rq"] = "sci_sci_sci_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        
        
    def test_JOQoqXhOcqqmKObXPHNThYanqxgmxyAVsjvFee(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
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
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ `node_name`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_name'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` (при `"sci_mode" - "standart", "only_local"`) - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_uJRVCAErHXSCRQxuNxQwJXgcFksc.__doc__
        self.SCI_SETTINGS["node_name"] = "alfa_node_aCtn4R2k3qPtzrGzxNhcZTrkfMCXJqHLwLwIvIcKtgrAscodORjfhYQeaBBiI"
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
        
        
    def test_KCOQRYEgndDogvBAYcFWfEkglLBiHXz(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ `node_rq`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_rq'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` (при `"sci_mode" - "standart", "only_local"`) - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_KCOQRYEgndDogvBAYcFWfEkglLBiHXz.__doc__
        self.SCI_SETTINGS["node_rq"] = "sci_rq_alfa_node_aCtn4R2k3qPtzrGzxNhcZTrkfMCXJqHLwLwIvIcKtgrAscodORjfhYQeaBBiI"
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
        
        
    def test_TRUrjBakHYMYqRBUZAlPSMeWBsiyPtEYYqvgJOzYKCg(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ `node_aq`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['node_aq'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` (при `"sci_mode" - "standart", "only_local"`) - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_TRUrjBakHYMYqRBUZAlPSMeWBsiyPtEYYqvgJOzYKCg.__doc__
        self.SCI_SETTINGS["node_aq"] = asyncio.Queue()
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
        
        
    def test_yWkAsDCkwgPtFLGJLdRbihDvnJIxHgWwkUftdWq(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ `AppConf`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` (при `"sci_mode" - "standart", "only_local"`) - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_yWkAsDCkwgPtFLGJLdRbihDvnJIxHgWwkUftdWq.__doc__
        self.SCI_SETTINGS["AppConf"] = ""
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
        
        
    def test_QLBfuVRCBJGuBpzROgKtFwrJmhMBYFaILLzUV(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ `nodes`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['nodes'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` (при `"sci_mode" - "standart", "only_local"`) - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_QLBfuVRCBJGuBpzROgKtFwrJmhMBYFaILLzUV.__doc__
        self.SCI_SETTINGS["nodes"] = ""
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
        
        
    def test_joNaWLDgEIiJuqZTfuJMXwRkvKngEItAqRROIHGgqy(self):
        """
        Основные условия:
        - `"sci_mode" - "shadow"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ `websocket_connections`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['websocket_connections'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` (при `"sci_mode" - "standart", "only_local"`) - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_joNaWLDgEIiJuqZTfuJMXwRkvKngEItAqRROIHGgqy.__doc__
        self.SCI_SETTINGS["websocket_connections"] = ""
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