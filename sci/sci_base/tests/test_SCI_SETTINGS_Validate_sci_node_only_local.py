import unittest
import asyncio

from sci.sci_base.validators import SCI_SETTINGS_Validate
from sci.lib.patterns import isecsaddo
from sci.app_controllers.base_controller import SCI_BaseAppController
from sci.apps.nodeLifespanSystemSCIApp.application import (
    NodeLifespanSystemSCIApp
)
from sci.sci_settings import TEST_LOG_FILE_PATH


class FakeSCIApp:
    pass


class TestSCIApp(SCI_BaseAppController):
    pass


class SCI_SETTINGS_Validate_sci_node_only_local(unittest.TestCase):
    
    def setUp(self):
        SCI_SETTINGS = {
            "node_name": "appolo_node",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [
                (TestSCIApp, "TestSCIApp", {})
            ],
        }
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = "only_local"
        
        
    def test_bsnkOhrlbgypmLCXriJidCjekXrO(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
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
        self.SCI_SETTINGS["node_name"] = "appolo_node"
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        
        
    # def test_CTVvaYGYfBmndrcOONbIEzcKGNrBWeTZfbB(self):
    #     """
    #     Основные условия:
    #     - `"sci_mode" - "only_local"`
        
    #     Проверяется:
    #     `SCI_SETTINGS -> "node_name"`
        
    #     В качестве значения ключа `"node_name"` передана строка `hello`
        
    #     Ожидаемый ответ:
    #     {
    #         'status': 'error', 
    #         'action': 'failed validation', 
    #         'data': {
    #             'description': 'failed validation', 
    #             'error_list': [
    #                 (['node_name'], 'structure error', '`SCI_SETTINGS -> "node_name"` Значение ключа `"node_name"` должно иметь тип `str`, и быть длиной `>=` 50 символов.')
    #             ]
    #         }
    #     }
    #     """
    #     msg = self.test_CTVvaYGYfBmndrcOONbIEzcKGNrBWeTZfbB.__doc__
    #     self.SCI_SETTINGS["node_name"] = "hello"
    #     ecsaddo_validate: dict = SCI_SETTINGS_Validate(
    #         validation_data=self.SCI_SETTINGS,
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
        
        
    def test_opRCISMhZfTrIDWSbdChDHTZBR(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        self.SCI_SETTINGS["logfilePath"] = TEST_LOG_FILE_PATH
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
            (TestSCIApp, "TestSCIApp", {}),
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        
        
    def test_BdrDQTwdtLFLleBjOeTOPUWHcIjUTrifWJyR(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
        Проверяется:
        `SCI_SETTINGS -> "AppConf" -> 0 -> 0`
        
        В качестве первого значения в кортеже с настройками конкретного 
        приложения, передается класс `NodeLifespanSystemSCIApp`, приложение
        которого не поддерживается при `"sci_mode": "only_local"`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['AppConf', 0, 0], 'structure error', '`SCI_SETTINGS -> "AppConf" -> 0 -> 0` Приложение `NodeLifespanSystemSCIApp` доступно к использованию только при `"sci_mode": "standart"`.')
                ]
            }
        }
        """
        msg = self.test_BdrDQTwdtLFLleBjOeTOPUWHcIjUTrifWJyR.__doc__
        
        AppConf = [
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
        
        
    def test_nlhgilBIFtWKSRlPiNiqIQCxE(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
        - `"sci_mode" - "only_local"`
        
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
            (TestSCIApp, "TestSCIApp_first", {}),
            (TestSCIApp, "TestSCIApp_second", {}),
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
        
    
    def test_uJRVCAErHXSCRQxuNxQwJXgcFksc(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
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
                    (['node_rq'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_uJRVCAErHXSCRQxuNxQwJXgcFksc.__doc__
        node_rq = ""
        self.SCI_SETTINGS["node_rq"] = node_rq
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
        
        
    def test_fKmedPuNinomReKnUuEgfGrdCk(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
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
                    (['nodes'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_fKmedPuNinomReKnUuEgfGrdCk.__doc__
        nodes = ""
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
        
    
    def test_ycHFwQiUzkmAjiAUCMpSLjDAdSYLwWYBmKQmtmbFWiOAQUx(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
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
                    (['websocket_connections'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_ycHFwQiUzkmAjiAUCMpSLjDAdSYLwWYBmKQmtmbFWiOAQUx.__doc__
        websocket_connections = ""
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
        
        
    def test_FWTuNbwmWyLhREHVHbcBzBXFBtAqeUAMbpMRgfgwYeeFe(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ `local_broker_connection_settings`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['local_broker_connection_settings'], 'structure error', '`EventMessage` Допустимые ключи словаря `SCI_SETTINGS`: - `node_name` - `node_rq` (при `"sci_mode" - "standart"`) - `node_aq` (при `"sci_mode" - "standart", "only_local"`) - `logfilePath` - `AppConf` (при `"sci_mode" - "standart", "only_local"`) - `nodes` (при `"sci_mode" - "standart"`) - `websocket_connections` (при `"sci_mode" - "standart"`) - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`) - `related_node_rq` (при `"sci_mode" - "only_local"`)')
                ]
            }
        }
        """
        msg = self.test_FWTuNbwmWyLhREHVHbcBzBXFBtAqeUAMbpMRgfgwYeeFe.__doc__
        self.SCI_SETTINGS["local_broker_connection_settings"] = ""
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
        
        
    def test_xxnGNwObtsfNYBnhRAnhABoYksptzkRnlbiXiOoDLVcQYb(self):
        """
        Основные условия:
        - `"sci_mode" - "only_local"`
        
        Проверяется:
        `SCI_SETTINGS`
        
        В `SCI_SETTINGS` передается лишний ключ `related_node_rq`
        
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
        msg = self.test_xxnGNwObtsfNYBnhRAnhABoYksptzkRnlbiXiOoDLVcQYb.__doc__
        self.SCI_SETTINGS["related_node_rq"] = ""
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
    