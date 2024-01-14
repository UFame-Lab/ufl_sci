import unittest
import asyncio

from sci.sci_cli.validators import EventMessage_Validate
from sci.lib.patterns import isecsaddo
from sci.sci_settings import TEST_LOG_FILE_PATH


class EventMessage_Validate_sci_node_standart_mType_request(unittest.TestCase):

    def setUp(self):
        SCI_SETTINGS = {
            "node_name": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_rq": "sci_rq_appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ",
            "node_aq": asyncio.Queue(),
            "logfilePath": TEST_LOG_FILE_PATH,
            "AppConf": [], # Намерено оставлено пустым
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
        template_validation_data = {
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
        self.template_validation_data = template_validation_data
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = "standart"


    def test_jYkdAhjJvCBHuTVgH(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        EventMessage -> "sender"`
        
        Значение ключа `"sender"` передается валидным
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_jYkdAhjJvCBHuTVgH.__doc__
        self.template_validation_data["sender"] = "some_app_name"
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_bXBRXjDjvRRLvyyHXwMqkvcKDUw(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "sender"`
        
        Значение ключа `"sender"` передается не валидным типом `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['sender'], 'structure error', '`EventMessage -> "sender"` Значение ключа `"sender"` должно иметь тип `str`, быть длиной `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_bXBRXjDjvRRLvyyHXwMqkvcKDUw.__doc__
        self.template_validation_data["sender"] = ["hello", "world"]
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_RidOwKFMAoKOCdUXmfpkoUHmIoHvwbkQ(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "sender"`
        
        Значение ключа `"sender"` передается длиной в 2 символа.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['sender'], 'structure error', '`EventMessage -> "sender"` Значение ключа `"sender"` должно иметь тип `str`, быть длиной `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_RidOwKFMAoKOCdUXmfpkoUHmIoHvwbkQ.__doc__
        self.template_validation_data["sender"] = "hi"
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_yKeFOmgGnYSRUyyUZsiBhJsFGsSILlT(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "sender"`
        
        Ключ `"sender" не передается`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['sender'], 'structure error', '`EventMessage -> "sender"` Значение ключа `"sender"` должно иметь тип `str`, быть длиной `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_yKeFOmgGnYSRUyyUZsiBhJsFGsSILlT.__doc__
        del self.template_validation_data["sender"]
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
            
        
    def test_sBRsiPTtAFciOWFrVKrkso(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "action"`
        
        Значение ключа `"action"` передается валидным.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_sBRsiPTtAFciOWFrVKrkso.__doc__
        self.template_validation_data["action"] = "some_action"
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_WLyIcKemRiARJcNWXUFQklITetBx(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "action"`
        
        Значение ключа `"action"` передается не валидным типом `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['action'], 'structure error', '`EventMessage -> "action"` Значение ключа `"action"` должно иметь тип `str`, быть длиной `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_WLyIcKemRiARJcNWXUFQklITetBx.__doc__
        self.template_validation_data["action"] = [1,2]
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_lQwNDNvrliMixoceobYyutxmwKSsmv(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "action"`
        
        Значение ключа `"action"` передается длиной в 2 символа.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['action'], 'structure error', '`EventMessage -> "action"` Значение ключа `"action"` должно иметь тип `str`, быть длиной `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_lQwNDNvrliMixoceobYyutxmwKSsmv.__doc__
        self.template_validation_data["action"] = "hi"
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_ftwVRYhWRfXcTHEEDpzlRRjHygunlNVBT(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "action"`
        
        Ключ `"action"` не передается
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['action'], 'structure error', '`EventMessage -> "action"` Значение ключа `"action"` должно иметь тип `str`, быть длиной `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_ftwVRYhWRfXcTHEEDpzlRRjHygunlNVBT.__doc__
        del self.template_validation_data["action"]
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_OPZtApZTWTSiPNplCbZOsGbCRiEoYxUv(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section"`
        
        Значение ключа `"address_section"` передается валидным.
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_OPZtApZTWTSiPNplCbZOsGbCRiEoYxUv.__doc__
        address_section = {
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "interface": "local-aq",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_MrRaHmpABsppJogNcCUxdXpykPegjF(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section"`
        
        Ключ "address_section"` не передан.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section'], 'structure error', '`EventMessage -> "address_section"` Значение ключа `"address_section"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_MrRaHmpABsppJogNcCUxdXpykPegjF.__doc__
        del self.template_validation_data["address_section"]
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_obrOfQwtIwMzyHvBOfCENO(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "recipient"`
        
        Значение ключа `"recipient"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'recipient'], 'structure error', '`EventMessage -> "address_section" -> "recipient"` Значение ключа `"recipient"` должно иметь тип `str`, и иметь символ разделитель `":"`.')
                ]
            }
        }
        """
        msg = self.test_obrOfQwtIwMzyHvBOfCENO.__doc__
        address_section = {
            "recipient": [],
            "interface": "local-aq",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_LfEisXbgMlmjAZGvPKmvVZmKtZdmb(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "recipient"`
        
        Значение ключа `"recipient"` не имеет обязательного символа 
        разделителя `":"`.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'recipient'], 'structure error', '`EventMessage -> "address_section" -> "recipient"` Значение ключа `"recipient"` должно иметь тип `str`, и иметь символ разделитель `":"`.')
                ]
            }
        }
        """
        msg = self.test_LfEisXbgMlmjAZGvPKmvVZmKtZdmb.__doc__
        address_section = {
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZgeneric_test_app",
            "interface": "local-aq",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_nJHVQVBzFbeThvdsGLUwcJOSsSdeL(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "recipient"`
        
        Ключ `"recipient"` не передается
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'recipient'], 'structure error', '`EventMessage -> "address_section" -> "recipient"` Значение ключа `"recipient"` должно иметь тип `str`, и иметь символ разделитель `":"`.')
                ]
            }
        }
        """
        msg = self.test_nJHVQVBzFbeThvdsGLUwcJOSsSdeL.__doc__
        address_section = {
            "interface": "local-aq",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_NuNeRjbLaHrhiFkdkURyVfBORMufwh(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        В качестве значения ключа `"interface"` передан не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'interface'], 'structure error', '`EventMessage -> "address_section" -> "interface"` Значение ключа `"interface"` должно иметь тип `str`, и входит в допустимые интерфейсы: `("local-aq", "local-rq", "remote-rq", "ws")`')
                ]
            }
        }
        """
        msg = self.test_NuNeRjbLaHrhiFkdkURyVfBORMufwh.__doc__
        address_section = {
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "interface": [],
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_JVmMPMkTSOEEmvdSkzNxnBSPQdpfPKjdKLJ(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        В `"interface"` передано значение не входящие в 
        `("local-aq", "local-rq", "remote-rq", "ws")`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'interface'], 'structure error', '`EventMessage -> "address_section" -> "interface"` Значение ключа `"interface"` должно иметь тип `str`, и входит в допустимые интерфейсы: `("local-aq", "local-rq", "remote-rq", "ws")`')
                ]
            }
        }
        """
        msg = self.test_JVmMPMkTSOEEmvdSkzNxnBSPQdpfPKjdKLJ.__doc__
        address_section = {
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "interface": "local-local",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_GodTiSOjvOqRynSCwSybAMea(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        Ключ `"interface"` не передается.
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'interface'], 'structure error', '`EventMessage -> "address_section" -> "interface"` Значение ключа `"interface"` должно иметь тип `str`, и входит в допустимые интерфейсы: `("local-aq", "local-rq", "remote-rq", "ws")`')
                ]
            }
        }
        """
        msg = self.test_GodTiSOjvOqRynSCwSybAMea.__doc__
        address_section = {
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_udERSwKpxlKJPiFiRYgacajVEIAPRXfGFs(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        Значение ключа `"interface"` - "local-aq"
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_udERSwKpxlKJPiFiRYgacajVEIAPRXfGFs.__doc__
        address_section = {
            "interface": "local-aq",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_XtOgkStbHBecqyXBpTCzmOnDZVittXxMTIXXcCeDvR(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        Значение ключа `"interface"` - "local-aq".
        Передается лишний ключ `wsbridge`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'wsbridge'], 'structure error', '`EventMessage -> "address_section"` Допустимые ключи словаря `"address_section"`: - `recipient` - `interface` - `wsbidge` (при `"interfcae": "ws"`).')
                ]
            }
        }
        """
        msg = self.test_XtOgkStbHBecqyXBpTCzmOnDZVittXxMTIXXcCeDvR.__doc__
        address_section = {
            "interface": "local-aq",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "wsbridge": "aVsXUHRrkkSBlJXSYtZvmFU"
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_LqcQfgSvkcFfhfKZIzXDVLWXsQCdTfrmWr(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        Значение ключа `"interface"` - "local-rq"
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_LqcQfgSvkcFfhfKZIzXDVLWXsQCdTfrmWr.__doc__
        address_section = {
            "interface": "local-rq",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_tylPvrOByOjznuOZAbugYDamaFeaHZNIZtWrDdc(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        Значение ключа `"interface"` - "local-rq".
        Передается лишний ключ `wsbridge`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'wsbridge'], 'structure error', '`EventMessage -> "address_section"` Допустимые ключи словаря `"address_section"`: - `recipient` - `interface` - `wsbidge` (при `"interfcae": "ws"`).')
                ]
            }
        }
        """
        msg = self.test_tylPvrOByOjznuOZAbugYDamaFeaHZNIZtWrDdc.__doc__
        address_section = {
            "interface": "local-rq",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "wsbridge": "aVsXUHRrkkSBlJXSYtZvmFU"
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_BQTiZPFUnbvvAuEcumoKGDPBZWYZIO(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        Значение ключа `"interface"` - "remote-rq"
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_BQTiZPFUnbvvAuEcumoKGDPBZWYZIO.__doc__
        address_section = {
            "interface": "remote-rq",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_srLTPiGsCVpYotQHKGEAIoJAXJ(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        Значение ключа `"interface"` - "remote-rq".
        Передается лишний ключ `wsbridge`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'wsbridge'], 'structure error', '`EventMessage -> "address_section"` Допустимые ключи словаря `"address_section"`: - `recipient` - `interface` - `wsbidge` (при `"interfcae": "ws"`).')
                ]
            }
        }
        """
        msg = self.test_srLTPiGsCVpYotQHKGEAIoJAXJ.__doc__
        address_section = {
            "interface": "remote-rq",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "wsbridge": "aVsXUHRrkkSBlJXSYtZvmFU"
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_VpzwPmltJCWlUTYiwoFhAUCblo(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        
        Значение ключа `"interface"` - "ws", без передачи дополнительного
        обязательного ключа `"wsbridge"`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'wsbridge'], 'structure error', '`EventMessage -> "address_section" -> "wsbridge"` При `"interface": "ws"`, значение ключа `"wsbridge"` должно иметь тип `str`, и быть `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_VpzwPmltJCWlUTYiwoFhAUCblo.__doc__
        address_section = {
            "interface": "ws",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_vKGaWdpRJJFIQsYtwCDEXGUjHBHdILlM(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        `EventMessage -> "address_section" -> "wsbridge"`
        
        При `"interface": "ws"`, должен присутствовать обязательный
        дополнительный ключ `"wsbridge"`
        
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_vKGaWdpRJJFIQsYtwCDEXGUjHBHdILlM.__doc__
        address_section = {
            "interface": "ws",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "wsbridge": "some_wsbridge"
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_sSowMDrHvMHNEyumnnTwJtNwLso(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        `EventMessage -> "address_section" -> "wsbridge"`
        
        В качестве значения `"wsbridge"` передается не валидный тип `list`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'wsbridge'], 'structure error', '`EventMessage -> "address_section" -> "wsbridge"` При `"interface": "ws"`, значение ключа `"wsbridge"` должно иметь тип `str`, и быть `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_sSowMDrHvMHNEyumnnTwJtNwLso.__doc__
        address_section = {
            "interface": "ws",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "wsbridge": []
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_EFpWbQNqKslATDWWBToejkraKqZctfm(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "address_section" -> "interface"`
        `EventMessage -> "address_section" -> "wsbridge"`
        
        В качестве значения `"wsbridge"` передается не валидное значение `"hi"`
        
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['address_section', 'wsbridge'], 'structure error', '`EventMessage -> "address_section" -> "wsbridge"` При `"interface": "ws"`, значение ключа `"wsbridge"` должно иметь тип `str`, и быть `>=` 3 символам.')
                ]
            }
        }
        """
        msg = self.test_EFpWbQNqKslATDWWBToejkraKqZctfm.__doc__
        address_section = {
            "interface": "ws",
            "recipient": "appolo_node_aCtn4R2k3qPtziyBEM6EwjdDr7ulRz5WQHDbOZ:generic_test_app",
            "wsbridge": "hi"
        }
        self.template_validation_data["address_section"] = address_section
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    def test_pCwoJMHdLAYpzXVCxEptPNpKnAhtX(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "meta"`
        
        Ключ `"meta"` не передается
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['meta'], 'structure error', '`EventMessage -> "meta"` Значение ключа `"meta"` должно иметь тип `dict`')
                ]
            }
        }
        """
        msg = self.test_pCwoJMHdLAYpzXVCxEptPNpKnAhtX.__doc__
        del self.template_validation_data["meta"]
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_GUpaQodmveSdSMkRcnNnrUCpz(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "meta"`
        
        В качестве значения ключа `"meta"` передается не валидный тип `list`
                
        Ожидаемый ответ:
        {
            'status': 'ex', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'location': {
                    'path_to_module': '/home/paul/Dev/ufame-lab/ufl_SCI_dev/SCI_0.1/sci/lib/validation.py', 
                    'qual_name': 'BaseValidate.complete_validation'
                }, 
                'error_list': [
                    (['meta'], 'structure error', '`EventMessage -> "meta"` Значение ключа `"meta"` должно иметь тип `dict`')
                ], 
                'traceback_list': [
                    '[\'Traceback (most recent call last):\\n\',...]', 
                    '[\'Traceback (most recent call last):\\n\',...]'
                ]
            }
        }
        """
        msg = self.test_GUpaQodmveSdSMkRcnNnrUCpz.__doc__
        self.template_validation_data["meta"] = []
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
        ).start_validation()
        self.assertEqual(True, isecsaddo(ecsaddo_validate), msg=msg)
        self.assertEqual("ex", ecsaddo_validate["status"],msg=msg)
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
        
        
    def test_FwHMmChMQxegYgRohEdnigezgijXM(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "meta"`
        
        Значение ключа `"meta"` - пустой `dict`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['meta', 'mType'], 'structure error', '`EventMessage -> "meta" -> "mType"` Значение ключа `"mType"` должно иметь тип `str`, и входить в ("request", "response").')
                ]
            }
        }
        """
        msg = self.test_FwHMmChMQxegYgRohEdnigezgijXM.__doc__
        meta = {}
        self.template_validation_data["meta"] = meta
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_NeqtYLmFvOMxWrurdrJJLIcvSlGotb(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "meta" -> "mType"`
        
        В качестве значения ключа `"mType"` передается не валидный тип `list`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['meta', 'mType'], 'structure error', '`EventMessage -> "meta" -> "mType"` Значение ключа `"mType"` должно иметь тип `str`, и входить в ("request", "response").')
                ]
            }
        }
        """
        msg = self.test_NeqtYLmFvOMxWrurdrJJLIcvSlGotb.__doc__
        meta = {
            "mType": [],
        }
        self.template_validation_data["meta"] = meta
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_NLbjdaemlyygCTQvxfTGhPzFjwluJkQnoG(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "meta" -> "mType"`
        
        В качестве значения ключа `"mType"` передается не валидное значение `"hi"`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['meta', 'mType'], 'structure error', '`EventMessage -> "meta" -> "mType"` Значение ключа `"mType"` должно иметь тип `str`, и входить в ("request", "response").')
                ]
            }
        }
        """
        msg = self.test_NLbjdaemlyygCTQvxfTGhPzFjwluJkQnoG.__doc__
        meta = {
            "mType": "hi",
        }
        self.template_validation_data["meta"] = meta
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_ZRWvyghdCFRzwzzRekkcLp(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "meta" -> "mType"`
        
        В качестве значения ключа `"mType"` передается валидный `"request"`
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_ZRWvyghdCFRzwzzRekkcLp.__doc__
        meta = {
            "mType": "request",
        }
        self.template_validation_data["meta"] = meta
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_XPQnYdvXJbDDPGoZtOsvKpBUFJhLTkLKKLJGpJzn(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "meta" -> "mType"`
        
        В качестве значения ключа `"mType"` передается валидный `"request"`.
        Передается лишний ключ `"session_id"`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['meta', 'session_id'], 'structure error', '`EventMessage -> "meta"` Допустимые ключи словаря `"meta"`: - `mType` - `session_id` (при `"mType": "response"`)')
                ]
            }
        }
        """
        msg = self.test_XPQnYdvXJbDDPGoZtOsvKpBUFJhLTkLKKLJGpJzn.__doc__
        meta = {
            "mType": "request",
            "session_id": "ksYqaDFOATRxKjarAwwnjxavaXY"
        }
        self.template_validation_data["meta"] = meta
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_jgAwtyVSvdLfVUDWdQePoRz(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload"`
        
        Ключ `"message_payload"` не передается.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload'], 'structure error', '`EventMessage -> "message_payload"` Значение ключа `"message_payload"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_jgAwtyVSvdLfVUDWdQePoRz.__doc__
        message_payload = []
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_BSmtQbUQtaKQUZAWrYSeFtsZn(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload"`
        
        В качестве значения ключа `"message_payload"` передается не валидный 
        тип `list`.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload'], 'structure error', '`EventMessage -> "message_payload"` Значение ключа `"message_payload"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_BSmtQbUQtaKQUZAWrYSeFtsZn.__doc__
        message_payload = []
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_CpIfcLXNLWTpaITLGRbVDHhOv(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload"`
        
        В качестве значения ключа `"message_payload"` передается пустой `dict`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'data'], 'structure error', '`EventMessage -> "message_payload" -> "data"` Значение ключа `"data"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_CpIfcLXNLWTpaITLGRbVDHhOv.__doc__
        message_payload = {}
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_gAVixtJalfaZasWOCgaUGPVenJj(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "data"`
        `EventMessage -> "message_payload" -> "data"`
        
        В качестве значения ключа `"data"` передается пустой `dict`
        В качестве значения ключа `"meta"` передается пустой `dict`
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_gAVixtJalfaZasWOCgaUGPVenJj.__doc__
        message_payload = {
            "data": {},
            "meta": {}
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    def test_gOFJjTpiVsFEJqyEYLzQJvJJ(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "data"`
        `EventMessage -> "message_payload" -> "data"`
        
        В качестве значения ключа `"data"` передается пустой `dict`
        В качестве значения ключа `"meta"` передается пустой `dict`
        Передается дополнительный лишний ключ `"options"`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'options'], 'structure error', '`EventMessage -> "message_payload"` Допустимые ключи словаря `"message_payload"`: - `data` - `meta`')
                ]
            }
        }
        """
        msg = self.test_gOFJjTpiVsFEJqyEYLzQJvJJ.__doc__
        message_payload = {
            "data": {},
            "meta": {},
            "options": []
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_cNUotzBgSXYApKXRdWkOYxwJFVxDlJwo(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "data"`
        
        Ключ `"data"` не передается
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'data'], 'structure error', '`EventMessage -> "message_payload" -> "data"` Значение ключа `"data"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_cNUotzBgSXYApKXRdWkOYxwJFVxDlJwo.__doc__
        message_payload = {
            "meta": {}
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_cCkfWUEYCPHdBdgAIOeJACtHoA(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "data"`
        
        В качестве значения ключа `"data"` передается не валидный тип `list`.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'data'], 'structure error', '`EventMessage -> "message_payload" -> "data"` Значение ключа `"data"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_cCkfWUEYCPHdBdgAIOeJACtHoA.__doc__
        message_payload = {
            "data": [],
            "meta": {}
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_XYKiqUNdDyHjOsceQVOhmxzDLXWpvdisHpPH(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta"`
        
        Ключ `meta` не передается.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'meta'], 'structure error', '`EventMessage -> "message_payload" -> "meta"` Значение ключа `"meta"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_XYKiqUNdDyHjOsceQVOhmxzDLXWpvdisHpPH.__doc__
        message_payload = {
            "data": {},
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_rbYiHEEVjhflJQDbsbgWgRBokvTBAVTLOZBhE(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "expire_time"`
        
        В качестве значения ключа `"expire_time"` передается не валидный тип 
        `str`.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                   (['message_payload', 'meta', 'expire_time'], 'structure error', '`EventMessage -> "message_payload" -> "meta" -> "expire_time"` При `"mType": "request"` значение ключа `expire_time` должно иметь тип `int` / `float`.')
                ]
            }
        }
        """
        msg = self.test_rbYiHEEVjhflJQDbsbgWgRBokvTBAVTLOZBhE.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "expire_time": ""
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_NVPLIfavUUfWgjrEgAPttlKPZo(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "expire_time"`
        
        В качестве значения ключа `"expire_time"` передается валидный тип 
        `int` (10)
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_NVPLIfavUUfWgjrEgAPttlKPZo.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "expire_time": 10
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_MskhVfVcoqIowXlSYvjKEzYHcLqIu(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "expire_time"`
        
        В качестве значения ключа `"expire_time"` передается валидный тип 
        `float` (10.5)
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_MskhVfVcoqIowXlSYvjKEzYHcLqIu.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "expire_time": 10.5
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_AuvAcJSrakWJSOvQVjfOoidDWLXDFmMD(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "background"`
        
        В качестве значения ключа `"background"` передается не валидный тип 
        `str`.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                   (['message_payload', 'meta', 'background'], 'structure error', '`EventMessage -> "message_payload" -> "meta" -> "background"` При `"mType": "request"` значение ключа `"background"` должно иметь тип `bool`.')
                ]
            }
        }
        """
        msg = self.test_AuvAcJSrakWJSOvQVjfOoidDWLXDFmMD.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "background": ""
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_zeglhwWrPjfCSZINHGdJZnVUF(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "background"`
        
        В качестве значения ключа `"background"` передается валидное значение
        `True`
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_zeglhwWrPjfCSZINHGdJZnVUF.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "background": True
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
    
    
    def test_TiRmfZStRsJEybvnjLZfcUtqEfzEcXNW(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "background"`
        
        В качестве значения ключа `"background"` передается валидное значение
        `False`
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_TiRmfZStRsJEybvnjLZfcUtqEfzEcXNW.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "background": False
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_DCqeBMOVpdEZAFRzbJupetkz(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "max_execution_time"`
        
        В качестве значения ключа `"max_execution_time"` передается не 
        валидный тип `str`.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'meta', 'max_execution_time'], 'structure error', '`EventMessage -> "message_payload" -> "meta" -> "max_execution_time"` При `"mType": "request"` значение ключа `"max_execution_time"` должно иметь тип `int` / `float`.')
                ]
            }
        }
        """
        msg = self.test_DCqeBMOVpdEZAFRzbJupetkz.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "max_execution_time": ""
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_JjMMydbnLBCiiWkTLnQbunvHutUfdCzjubEg(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "max_execution_time"`
        
        В качестве значения ключа `"max_execution_time"` передается валидное
        згачение `int` (10)
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_JjMMydbnLBCiiWkTLnQbunvHutUfdCzjubEg.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "max_execution_time": 10
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_qfqyzijZMrjKTPnLGLzYzefh(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "max_execution_time"`
        
        В качестве значения ключа `"max_execution_time"` передается валидное
        згачение `float` (10.5)
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_qfqyzijZMrjKTPnLGLzYzefh.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "max_execution_time": 10.5
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_YzSeCAiEIpmfkLTbJmncqZKtjlymfUssTkRzTfnu(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta"`
        
        Передается лишний ключ `"status_code"`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'status_code'], 'structure error', '`EventMessage -> "message_payload" -> "meta"` Допустимые ключи словаря `"meta"`: - `expire_time` (при `"mType": "request"`) - `background` (при `"mType": "request"`) - `max_execution_time` (при `"mType": "request"`) - `status_code` (при `"mType": "response"`)')
                ]
            }
        }
        """
        msg = self.test_YzSeCAiEIpmfkLTbJmncqZKtjlymfUssTkRzTfnu.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "status_code": 200
            }
        }
        self.template_validation_data["message_payload"] = message_payload
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_bJrHpUXpQdbjOZBdFmsEu(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings"`
        
        Ключ `"response_settings"` не передается.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['response_settings'], 'structure error', '`EventMessage -> "response_settings"` При `"mType": "request"` значение ключа `"response_settings"` должно иметь тип `dict`.')
                ]
            }
        }
        """
        msg = self.test_bJrHpUXpQdbjOZBdFmsEu.__doc__
        del self.template_validation_data["response_settings"]
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_yunXPSsFwdFIQdyNbTRdULmMdtfjw(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings"`
        
        В качестве значения ключа `"response_settings"` передается пустой `dict`.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                   (['response_settings', 'isAwaiting'], 'structure error', '`EventMessage -> "response_settings" -> "isAwaiting"` При `"mType": "request"`, значение ключа `"isAwaiting"` должно иметь тип `bool`.')
                ]
            }
        }
        """
        msg = self.test_yunXPSsFwdFIQdyNbTRdULmMdtfjw.__doc__
        response_settings = {}
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_WdntxqVtaxzLwftMICx(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        `EventMessage -> "message_payload" -> "response_settings" -> "await_timeout"`
        
        В качестве значения ключа `"isAwaiting"` передается `True`
        В качестве значения ключа `"await_timeout"` передается `10`
                
        Ожидаемый ответ:
        {
            'status': 'ok',
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_WdntxqVtaxzLwftMICx.__doc__
        response_settings = {
            "isAwaiting": True,
            "await_timeout": 10
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_fxgpsBPUDZrmicxbtZFSboEsAp(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        `EventMessage -> "message_payload" -> "response_settings" -> "await_timeout"`
        
        В качестве значения ключа `"isAwaiting"` передается не валидный тип `str`
        В качестве значения ключа `"await_timeout"` передается `10`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['response_settings', 'isAwaiting'], 'structure error', '`EventMessage -> "response_settings" -> "isAwaiting"` При `"mType": "request"`, значение ключа `"isAwaiting"` должно иметь тип `bool`.')
                ]
            }
        }
        """
        msg = self.test_fxgpsBPUDZrmicxbtZFSboEsAp.__doc__
        response_settings = {
            "isAwaiting": "",
            "await_timeout": 10
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_DbJjCsVwSDZwvQYDOhikQVlEmvOuMTH(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        
        В качестве значения ключа `"isAwaiting"` передается `False`
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_DbJjCsVwSDZwvQYDOhikQVlEmvOuMTH.__doc__
        response_settings = {
            "isAwaiting": False,
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_fYpjrJscczlCFLazCVQtNFsjWTTtetUVzza(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        
        В качестве значения ключа `"isAwaiting"` передается `False`.
        Передается лишний ключ `"await_timeout"`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['response_settings', 'await_timeout'], 'structure error', '`EventMessage -> "response_settings"` Допустимые ключи словаря `"response_settings"`: - `isAwaiting` (при `"mType": "request"`) - `await_timeout` (при `"mType": "request"`, `"isAwaiting": True`).')
                ]
            }
        }
        """
        msg = self.test_fYpjrJscczlCFLazCVQtNFsjWTTtetUVzza.__doc__
        response_settings = {
            "isAwaiting": False,
            "await_timeout": 10,
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
    
    def test_uzVsnOzJCNGdsUoYNlGmVLpmnEvwAAPFCgzR(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        `EventMessage -> "message_payload" -> "response_settings" -> "await_timeout"`
        
        В качестве значения ключа `"isAwaiting"` передается `True`
        Ключ `await_timeout` не передается.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['response_settings', 'await_timeout'], 'structure error', '`EventMessage -> "response_settings" -> "await_timeout"` При `"mType": "request"`, `"isAwaiting": True`, значение ключа `await_timeout` должно иметь тип `int` / `float`, и быть `>` 0.')
                ]
            }
        }
        """
        msg = self.test_uzVsnOzJCNGdsUoYNlGmVLpmnEvwAAPFCgzR.__doc__
        response_settings = {
            "isAwaiting": True,
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_REuYeBvabwpTVOAuziTQfzQAu(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        `EventMessage -> "message_payload" -> "response_settings" -> "await_timeout"`
        
        В качестве значения ключа `"isAwaiting"` передается `True`
        В качестве значения ключа `"await_timeout"` передается не валидный тип
        `str`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['response_settings', 'await_timeout'], 'structure error', '`EventMessage -> "response_settings" -> "await_timeout"` При `"mType": "request"`, `"isAwaiting": True`, значение ключа `await_timeout` должно иметь тип `int` / `float`, и быть `>` 0.')
                ]
            }
        }
        """
        msg = self.test_REuYeBvabwpTVOAuziTQfzQAu.__doc__
        response_settings = {
            "isAwaiting": True,
            "await_timeout": ""
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_xmzXiPyErglpeQLqkTLk(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        `EventMessage -> "message_payload" -> "response_settings" -> "await_timeout"`
        
        В качестве значения ключа `"isAwaiting"` передается `True`
        В качестве значения ключа `"await_timeout"` передается `int` (10)
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_xmzXiPyErglpeQLqkTLk.__doc__
        response_settings = {
            "isAwaiting": True,
            "await_timeout": 10
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_DfudfMjAiEblmwucyCNGGVYncaBQYD(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        `EventMessage -> "message_payload" -> "response_settings" -> "await_timeout"`
        
        В качестве значения ключа `"isAwaiting"` передается `True`
        В качестве значения ключа `"await_timeout"` передается `float` (10.5)
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_DfudfMjAiEblmwucyCNGGVYncaBQYD.__doc__
        response_settings = {
            "isAwaiting": True,
            "await_timeout": 10.5
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_dSofohbJpchOYpjFhfAkQxwSebzjUPaMJGZ(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        `EventMessage -> "message_payload" -> "response_settings" -> "await_timeout"`
        
        В качестве значения ключа `"isAwaiting"` передается `True`
        В качестве значения ключа `"await_timeout"` передается `int` (0)
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['response_settings', 'await_timeout'], 'structure error', '`EventMessage -> "response_settings" -> "await_timeout"` При `"mType": "request"`, `"isAwaiting": True`, значение ключа `await_timeout` должно иметь тип `int` / `float`, и быть `>` 0.')
                ]
            }
        }
        """
        msg = self.test_dSofohbJpchOYpjFhfAkQxwSebzjUPaMJGZ.__doc__
        response_settings = {
            "isAwaiting": True,
            "await_timeout": 0
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_BHYuBqGZCKIxwtgyHNJhXKlVjJiPWmI(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "response_settings" -> "isAwaiting"`
        `EventMessage -> "message_payload" -> "response_settings" -> "await_timeout"`
        
        В качестве значения ключа `"isAwaiting"` передается `True`
        В качестве значения ключа `"await_timeout"` передается `int` (-3)
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['response_settings', 'await_timeout'], 'structure error', '`EventMessage -> "response_settings" -> "await_timeout"` При `"mType": "request"`, `"isAwaiting": True`, значение ключа `await_timeout` должно иметь тип `int` / `float`, и быть `>` 0.')
                ]
            }
        }
        """
        msg = self.test_BHYuBqGZCKIxwtgyHNJhXKlVjJiPWmI.__doc__
        response_settings = {
            "isAwaiting": True,
            "await_timeout": -3
        }
        self.template_validation_data["response_settings"] = response_settings
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_tVmZnHXvaTqhKEJghiBStPOLmoxMyjNly(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage`
        
        Передается лишний ключ `optional`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['optional'], 'structure error', '`EventMessage` Допустимые ключи словаря `EventMessage`: - `sender` - `action` - `address_section` - `meta` - `message_payload` - `response_settings` (при `"mType": "request"`)')
                ]
            }
        }
        """
        msg = self.test_tVmZnHXvaTqhKEJghiBStPOLmoxMyjNly.__doc__
        self.template_validation_data["optional"] = {}
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=self.template_validation_data,
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
    def test_LUtikLlWCNngoXWKTbukIUuiFYxcAAqen(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "request"`
        
        Проверяется:
        `EventMessage`
        
        В качестве `EventMessage` передается не валидный тип `list`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    ([], 'structure error', '`EventMessage` `EventMessage` должен иметь тип `dict`')
                ]
            }
        }
        """
        msg = self.test_LUtikLlWCNngoXWKTbukIUuiFYxcAAqen.__doc__
        ecsaddo_validate: dict = EventMessage_Validate(
            validation_data=[],
            sci_mode=self.sci_mode,
            SCI_SETTINGS=self.SCI_SETTINGS
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
        
        
if __name__ == '__main__':
    unittest.main()