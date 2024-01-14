import unittest
import asyncio

from sci.sci_cli.validators import EventMessage_Validate
from sci.lib.patterns import isecsaddo
from sci.sci_settings import TEST_LOG_FILE_PATH


class EventMessage_Validate_sci_node_standart_mType_response(unittest.TestCase):

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
                "mType": "response",
                "session_id": "WrAdlJvCpkexXtXvvorGBtPCopmycrBAtsNmnoQ",
            },
            "message_payload": {
                "data": {},
                "meta": {
                    "status_code": 200
                }
            },
        }
        self.template_validation_data = template_validation_data
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = "standart"
        
        
    def test_wzFdATztALqqDcfUhZVSUhGYACLIPqPb(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_wzFdATztALqqDcfUhZVSUhGYACLIPqPb.__doc__
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
        
    
    def test_ScWDwNTDeGoXZjdlOUKDeJpez(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_ScWDwNTDeGoXZjdlOUKDeJpez.__doc__
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
        
    
    def test_HvaRYePNjdzsvEjbVHNldYCeuTHEn(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_HvaRYePNjdzsvEjbVHNldYCeuTHEn.__doc__
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
        
        
    def test_eiQIgZLoTCOEpTGfXjRmasShepUxbvk(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_eiQIgZLoTCOEpTGfXjRmasShepUxbvk.__doc__
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
        
        
    def test_pMVYUtYfyziIJSewaqFaKfIdiJHZpAxXqz(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_pMVYUtYfyziIJSewaqFaKfIdiJHZpAxXqz.__doc__
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
        
        
    def test_MTzQXPztlEecEypExhbTllVjrsmlvUSSF(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_MTzQXPztlEecEypExhbTllVjrsmlvUSSF.__doc__
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
        
        
    def test_YxknIkgTgkNSxXLHmOsysClcHHZVOl(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_YxknIkgTgkNSxXLHmOsysClcHHZVOl.__doc__
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
        
        
    def test_smjWOXdxcntAWPzIFBvGkeuIKWkwyJeGNqxS(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_smjWOXdxcntAWPzIFBvGkeuIKWkwyJeGNqxS.__doc__
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
        
        
    def test_zmyXpMYyLHLyQvhiDjcFbUHezgrjhIilyC(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_zmyXpMYyLHLyQvhiDjcFbUHezgrjhIilyC.__doc__
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
        
        
    def test_RPEFdwfIHIalTUpPBGYSLqrnbOunGws(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_RPEFdwfIHIalTUpPBGYSLqrnbOunGws.__doc__
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
        
    
    def test_pCXqzRXynpawQoRnlDWqQJuZiNIEnijFTEBe(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_pCXqzRXynpawQoRnlDWqQJuZiNIEnijFTEBe.__doc__
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
        
        
    def test_CrZXVkDaWZihmLIQIGUTvxeHauJiVlrh(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_CrZXVkDaWZihmLIQIGUTvxeHauJiVlrh.__doc__
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
        
        
    def test_gaxmChbAyumYiDQuohdIelpFJshWrTv(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_gaxmChbAyumYiDQuohdIelpFJshWrTv.__doc__
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
        
        
    def test_EhhSGYPDKrKsLMCQqKWSDvcEtDKEMvHTTvH(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_EhhSGYPDKrKsLMCQqKWSDvcEtDKEMvHTTvH.__doc__
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
        
        
    def test_jMEfJPAAghfBtQaxOeSOnkllWZVCTfB(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_jMEfJPAAghfBtQaxOeSOnkllWZVCTfB.__doc__
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
        
        
    def test_cdqWqOXKXbetPZSihvcfrBtbz(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_cdqWqOXKXbetPZSihvcfrBtbz.__doc__
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
        
        
    def test_dweJMpMtvuLaWKnBrpzOHkvFEXDgavylHcOoD(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_dweJMpMtvuLaWKnBrpzOHkvFEXDgavylHcOoD.__doc__
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
        
        
    def test_vRHCcxRATCrGjjtuHrvsmpKnIEZvq(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_vRHCcxRATCrGjjtuHrvsmpKnIEZvq.__doc__
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
        
        
    def test_OoLHagmFAeMiLNADpRmPGSLghSBCZl(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_OoLHagmFAeMiLNADpRmPGSLghSBCZl.__doc__
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
        
        
    def test_ZKndjTJCkSTKTFnmHhOfvDEq(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_ZKndjTJCkSTKTFnmHhOfvDEq.__doc__
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
        
    
    def test_NJpSasijHnCgzQASGRPwVtTUwvMXB(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_NJpSasijHnCgzQASGRPwVtTUwvMXB.__doc__
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
        
        
    def test_VCGayeVbGcQjSlgqNXooYptDYPhR(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_VCGayeVbGcQjSlgqNXooYptDYPhR.__doc__
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
        
        
    def test_MmAagTYMHdwfyQHSucxUivDIEhSHdYRugSIl(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_MmAagTYMHdwfyQHSucxUivDIEhSHdYRugSIl.__doc__
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
        
    
    def test_IqqRpQTIwtksTZnooCCEgUbSVIHVosPEBgzvtFD(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_IqqRpQTIwtksTZnooCCEgUbSVIHVosPEBgzvtFD.__doc__
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
        
        
    def test_BxIntfJbIMABwXcpRciEBSokSkZZHNOSoTWBecUlhH(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_BxIntfJbIMABwXcpRciEBSokSkZZHNOSoTWBecUlhH.__doc__
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
        
        
    def test_RySYHWJHcDzBGLVjJZdGLYrupWcebleAQtoI(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_RySYHWJHcDzBGLVjJZdGLYrupWcebleAQtoI.__doc__
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
        
    
    def test_FZJTotqazDdYcBFPAEdtcjMCcgNUVZqfmz(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_FZJTotqazDdYcBFPAEdtcjMCcgNUVZqfmz.__doc__
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
        
        
    def test_RfCRahaYWxyvhTLoXhhFbxhFCstqKVMiLly(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_RfCRahaYWxyvhTLoXhhFbxhFCstqKVMiLly.__doc__
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
        
        
    def test_rXyRwrNuLPJduZfOhfLoKibzjkJSMpJpVubP(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_rXyRwrNuLPJduZfOhfLoKibzjkJSMpJpVubP.__doc__
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
        
        
    def test_VRyFPhFeuKohKUjklfNFuSIODbjxtbegdJ(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_VRyFPhFeuKohKUjklfNFuSIODbjxtbegdJ.__doc__
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
        
        
    def test_tqEVhrICHxQeQRSjRIwmuFYkn(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_tqEVhrICHxQeQRSjRIwmuFYkn.__doc__
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
        
        
    def test_pmNTtmegRzFdmwfJnCMLjtRmIW(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage -> "meta" -> "mType"`
        `EventMessage -> "meta" -> "session_id"`
        
        В качестве значения ключа `"mType"` передается валидный `"response"`
        Ключ `session_id` не передается.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['meta', 'session_id'], 'structure error', '`EventMessage -> "meta" -> "session_id"` При `"mType": "response"`, значение ключа `"session_id"` должно иметь тип `str`.')
                ]
            }
        }
        """
        msg = self.test_pmNTtmegRzFdmwfJnCMLjtRmIW.__doc__
        meta = {
            "mType": "response",
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
        
        
    def test_BtthwWQcpcIypJOyDeYmOgliREOtCNVVKFdV(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage -> "meta" -> "session_id"`
        
        В качестве значения ключа `"session_id"` передается не валидный тип 
        `list`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['meta', 'session_id'], 'structure error', '`EventMessage -> "meta" -> "session_id"` При `"mType": "response"`, значение ключа `"session_id"` должно иметь тип `str`.')
                ]
            }
        }
        """
        msg = self.test_BtthwWQcpcIypJOyDeYmOgliREOtCNVVKFdV.__doc__
        meta = {
            "mType": "response",
            "session_id": []
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
        
        
    def test_WqqMpswWLqBnpfFkhxryjATcpUZCOGEyacPxTOhCzDPaJPTmZSzUT(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage -> "meta" -> "session_id"`
        
        В качестве значения ключа `"session_id"` передается валидное значение.
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_WqqMpswWLqBnpfFkhxryjATcpUZCOGEyacPxTOhCzDPaJPTmZSzUT.__doc__
        meta = {
            "mType": "response",
            "session_id": "UoPmeAsPEJvwyfVPomETleSLVcVzfLRCauvxdFvjuIJQp"
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
        
        
    def test_lryiOfcZCcaurDueQdFnojbvxmJBhqNQzlLxifDMMBykcFij(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage -> "meta"`
        
        Передается лишний ключ `"optional"`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['meta', 'optional'], 'structure error', '`EventMessage -> "meta"` Допустимые ключи словаря `"meta"`: - `mType` - `session_id` (при `"mType": "response"`)')
                ]
            }
        }
        """
        msg = self.test_lryiOfcZCcaurDueQdFnojbvxmJBhqNQzlLxifDMMBykcFij.__doc__
        meta = {
            "mType": "response",
            "session_id": "UoPmeAsPEJvwyfVPomETleSLVcVzfLRCauvxdFvjuIJQp",
            "optional": []
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
        
        
    def test_UiCQxnWIzGJTLrkdTDoImQRZCBoYvPcuHp(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_UiCQxnWIzGJTLrkdTDoImQRZCBoYvPcuHp.__doc__
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
        
        
    def test_kQTAcdAivxESJDGjQfmEeTgGJJmPfVVs(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_kQTAcdAivxESJDGjQfmEeTgGJJmPfVVs.__doc__
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
    
    
    def test_IWWedVpAXyGkjzfmpZZlUKDJAOgvKphDw(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_IWWedVpAXyGkjzfmpZZlUKDJAOgvKphDw.__doc__
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
        
    
    def test_BMzrGjXMAubebTOsuPFQcAqINCfHlrVWdOrJzFD(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "data"`
        `EventMessage -> "message_payload" -> "data"`
        
        В качестве значения ключа `"data"` передается пустой `dict`
        В качестве значения ключа `"meta"` передается пустой `dict`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'meta', 'status_code'], 'structure error', 'EventMessage -> "message_payload" -> "meta" -> "status_code"` При `"mType": "response"` значение ключа `"status_code"` должно')
                ]
            }
        }
        """
        msg = self.test_BMzrGjXMAubebTOsuPFQcAqINCfHlrVWdOrJzFD.__doc__
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
        
        
    def test_LfqAPOqMlpNyflHTWDFhZzfwjaGwMJ(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_LfqAPOqMlpNyflHTWDFhZzfwjaGwMJ.__doc__
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
        
        
    def test_oQJmYrUkhkRkjtUjGRjLkYRtPNRrI(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_oQJmYrUkhkRkjtUjGRjLkYRtPNRrI.__doc__
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
        
        
    def test_tPeTBwEOaCktRntnJgDVcQAOofryQDraFDoWPURVIt(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_tPeTBwEOaCktRntnJgDVcQAOofryQDraFDoWPURVIt.__doc__
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
        
    
    def test_SbihBoCOgSMvJfFhSbeaLsRkgTaYEDeQgQjlItWFAOYh(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "status_code"`
        
        В качестве значения ключа `"status_code"` передается не валидный тип 
        `list`.
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                   (['message_payload', 'meta', 'status_code'], 'structure error', 'EventMessage -> "message_payload" -> "meta" -> "status_code"` При `"mType": "response"` значение ключа `"status_code"` должно иметь тип `int`')
                ]
            }
        }
        """
        msg = self.test_SbihBoCOgSMvJfFhSbeaLsRkgTaYEDeQgQjlItWFAOYh.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "status_code": []
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
        
        
    def test_YRoPaSlXCTybwVBBbELndDkiSKEpvtWlWMohmdFvu(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" -> "status_code"`
        
        В качестве значения ключа `"status_code"` передается валидное значение.
                
        Ожидаемый ответ:
        {
            'status': 'ok', 
            'action': 'successfully validation', 
            'data': {
                'description': 'successfully validation'
            }
        }
        """
        msg = self.test_YRoPaSlXCTybwVBBbELndDkiSKEpvtWlWMohmdFvu.__doc__
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
        
        
    def test_qIwLHbRnCwHsIpobpsexqcDWDaChvhm(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage -> "message_payload" -> "meta" ->`
        
        Передается лишний ключ `"expire_time"`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['message_payload', 'expire_time'], 'structure error', '`EventMessage -> "message_payload" -> "meta"` Допустимые ключи словаря `"meta"`: - `expire_time` (при `"mType": "request"`) - `background` (при `"mType": "request"`) - `max_execution_time` (при `"mType": "request"`) - `status_code` (при `"mType": "response"`)')
                ]
            }
        }
        """
        msg = self.test_qIwLHbRnCwHsIpobpsexqcDWDaChvhm.__doc__
        message_payload = {
            "data": {},
            "meta": {
                "status_code": 200,
                "expire_time": 10,
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
        
        
    def test_qnoCtodAEDXFGOjJHgtfSJXTlSV(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
        Проверяется:
        `EventMessage`
        
        Передается лишний ключ `response_settings`
                
        Ожидаемый ответ:
        {
            'status': 'error', 
            'action': 'failed validation', 
            'data': {
                'description': 'failed validation', 
                'error_list': [
                    (['response_settings'], 'structure error', '`EventMessage` Допустимые ключи словаря `EventMessage`: - `sender` - `action` - `address_section` - `meta` - `message_payload` - `response_settings` (при `"mType": "request"`)')
                ]
            }
        }
        """
        msg = self.test_qnoCtodAEDXFGOjJHgtfSJXTlSV.__doc__
        self.template_validation_data["response_settings"] = {}
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
        
    
    def test_sZIretQjVOensVAzUAOuryoflUbVpksJIYDiG(self):
        """    
        Основные условия:
        - `"sci_mode" - "standart"`
        - `"mType": "response"`
        
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
        msg = self.test_sZIretQjVOensVAzUAOuryoflUbVpksJIYDiG.__doc__
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