import time

from typing import Any

from sci.lib.validation import BaseValidate, ValidationError
from sci.app_controllers.base_controller import AUTH_SERVICE_ACTIONS


class EventMessage_Validate(BaseValidate):
    
    def __init__(
        self, 
        validation_data: dict, 
        sci_mode: str, 
        SCI_SETTINGS: dict
    ) -> None:
        self.validation_data: dict = validation_data
        self.sci_mode: str = sci_mode
        self.SCI_SETTINGS: dict = SCI_SETTINGS
        
        
    def build_validation_plan(self) -> list:
        validation_plan = [
            ("sender_check", {"required": True}),
            ("action_check", {"required": True}),
            ("address_section_check", {"required": True}),
            ("meta_check", {"required": True}),
            ("message_payload_check", {"required": True}), # Обязательно после meta_check
            ("response_settings_check", {"required": True}),
        ]
        return validation_plan
    
    
    def pre_validation(self):
        """
        Description
        ---
        Валидатор `pre_validation` совершает проверки:
        
        id:RPeOCINFgKZwoGMSDpbwordLfdoVjb
            `EventMessage`
            `EventMessage` должен иметь тип `dict`
        """
        if not isinstance(self.validation_data, dict):
            raise ValidationError(
                [], "structure error",
                self.extract_alert(
                    self.pre_validation.__doc__,
                    "RPeOCINFgKZwoGMSDpbwordLfdoVjb"
                )
            )
    
    
    def full_validation(self):
        """
        Description
        ---
        Валидатор `full_validation` совершает проверки:
        
        id:qCYhjdnVZkWwvguSaEhfyDqmVxNxOJk
            `EventMessage`
            Допустимые ключи  словаря `EventMessage`:
            - `sender`
            - `action`
            - `address_section`
            - `meta`
            - `message_payload`
            - `response_settings` (при `"mType": "request"`)
        """
        allowed_keys = (
            "sender",
            "action",
            "address_section",
            "meta",
            "message_payload",
            "response_settings" if self.validation_data["meta"]["mType"] == "request" else None
        )
        allowed_keys = tuple(filter(None, allowed_keys))
        for key in tuple(self.validation_data.keys()):
            if key not in allowed_keys:
                raise ValidationError(
                    [key], 
                    "structure error",
                    self.extract_alert(
                        self.full_validation.__doc__,
                        "qCYhjdnVZkWwvguSaEhfyDqmVxNxOJk"
                    )
                )
    
    
    def sender_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - False
            
        Description
        ---
        Валидатор `sender_check` совершает проверки:
        
        id:jCXoKCtvZDtBddYvIm
            `EventMessage -> "sender"`
            Значение ключа `"sender"` должно иметь тип `str`, быть длиной
            `>=` 3 символам.
        """
        key_check = "sender"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        sender: str = self.validation_data.get(key_check)
        if (
            not isinstance(sender, str) or
            not len(sender) >= 3 or
            sender.find(":") != -1
        ):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.sender_check.__doc__,
                    "jCXoKCtvZDtBddYvIm"
                )
            )
        
    
    def action_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - False
            
        Description
        ---
        Валидатор `action_check` совершает проверки:
        
        id:OBFEIktEWFHxpAbSro
            `EventMessage -> "action"`
            Значение ключа `"action"` должно иметь тип `str`, быть длиной
            `>=` 3 символам.
        """
        key_check = "action"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        action: str = self.validation_data.get(key_check)
        if (
            not isinstance(action, str) or
            not len(action) >= 3
        ):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.action_check.__doc__, "OBFEIktEWFHxpAbSro"
                )
            )
    
    
    def address_section_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - False
            
        Description
        ---
        Валидатор `address_section_check` совершает проверки:
        
        id:oQpOnrXUXxPHkNMno33
            `EventMessage -> "address_section"`
            Значение ключа `"address_section"` должно иметь тип `dict`.
        
        id:aXZrFtKRAqdyhdNMwXYtJzV
            `EventMessage -> "address_section"`
            Допустимые ключи  словаря `"address_section"`:
            - `recipient`
            - `interface`
            - `wsbidge` (при `"interfcae": "ws"`).
        
        id:hhlKgEqZyumzZyJrAn
            `EventMessage -> "address_section" -> "recipient"`
            Значение ключа `"recipient"` должно иметь тип `str`, и иметь
            символ разделитель `":"`.
            
        id:zObQtAqxVhCoJnNUnEK
            `EventMessage -> "address_section" -> "interface"`
            Значение ключа `"interface"` должно иметь тип `str`, и входит в
            допустимые интерфейсы: `("local-aq", "local-rq", "remote-rq", "ws")`
            
        id:jRqBskCKKBCDsfKTyhSx
            `EventMessage -> "address_section" -> "interface"`
            Если текущий `SCI node` запущен в режиме `"only_local"`, то
            единственное допустимое значение `"interfcae"` это - `"local-aq"`.
            
        id:RpiIvetYuuCWdxdvgJQEa
            `EventMessage -> "address_section" -> "wsbridge"`
            При `"interface": "ws"`, значение ключа `"wsbridge"` должно иметь
            тип `str`, и быть `>=` 3 символам.
        """
        key_check = "address_section"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        address_section: dict = self.validation_data.get(key_check)
        if not isinstance(address_section, dict):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.address_section_check.__doc__, "oQpOnrXUXxPHkNMno33"
                )
            )
        allowed_keys = (
            "recipient", 
            "interface", 
            "wsbridge" if address_section.get("interface") == "ws" else None
        )
        allowed_keys = tuple(filter(None, allowed_keys))
        for key in tuple(address_section.keys()):
            if key not in allowed_keys:
                raise ValidationError(
                    [key_check, key],
                    "structure error",
                    self.extract_alert(
                        self.address_section_check.__doc__,
                        "aXZrFtKRAqdyhdNMwXYtJzV"
                    )
                )
        recipient: str = address_section.get("recipient")
        if (
            not isinstance(recipient, str) or
            recipient.find(":") == -1
        ):
            raise ValidationError(
                [key_check, "recipient"], "structure error",
                self.extract_alert(
                    self.address_section_check.__doc__, "hhlKgEqZyumzZyJrAn"
                )
            )
        available_interfaces = ("local-aq", "local-rq", "remote-rq", "ws") 
        interface: str = address_section.get("interface")
        if interface not in available_interfaces:
            raise ValidationError(
                [key_check, "interface"], "structure error",
                self.extract_alert(
                    self.address_section_check.__doc__, "zObQtAqxVhCoJnNUnEK"
                )
            )
        if self.sci_mode == "only_local" and interface != "local-aq":
            raise ValidationError(
                [key_check, "interface"], "structure error",
                self.extract_alert(
                    self.address_section_check.__doc__, "jRqBskCKKBCDsfKTyhSx"
                )
            )
        if interface == "ws":
            wsbridge: str = address_section.get("wsbridge")
            if (
                not isinstance(wsbridge, str) or
                not len(wsbridge) >= 3
            ):
                raise ValidationError(
                    [key_check, "wsbridge"], "structure error",
                    self.extract_alert(
                        self.address_section_check.__doc__, 
                        "RpiIvetYuuCWdxdvgJQEa"
                    )
                )
        
    
    def meta_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - False
            
        Description
        ---
        Валидатор `meta_check` совершает проверки:
        
        id:CuAsPrDcGnSfCKh
            `EventMessage -> "meta"`
            Значение ключа `"meta"` должно иметь тип `dict`
            
        id:gDaEWfSPZgtGAZPEhlgElQlvoSfjpiNG
            `EventMessage -> "meta"`
            Допустимые ключи  словаря `"meta"`:
            - `mType`
            - `session_id` (при `"mType": "response"`)
            
        id:QpWDPIeDijNbPyUieaW
            `EventMessage -> "meta" -> "mType"`
            Значение ключа `"mType"` должно иметь тип `str`, и входить в
            ("request", "response").
            
        id:mBsXpITxYthrOjmGEZ
            `EventMessage -> "meta" -> "session_id"`
            При `"mType": "response"`, значение ключа `"session_id"` должно
            иметь тип `str`.
        """
        key_check = "meta"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        meta: dict = self.validation_data.get(key_check)
        if not isinstance(meta, dict):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.meta_check.__doc__, "CuAsPrDcGnSfCKh"
                )
            )
        allowed_keys = (
            "mType", 
            "session_id" if meta.get("mType") == "response" else None,
            "to_node_addr" if self.validation_data.get("action") in AUTH_SERVICE_ACTIONS else None,
            "back_node_addr" if self.validation_data.get("action") in AUTH_SERVICE_ACTIONS else None,
        )
        allowed_keys = tuple(filter(None, allowed_keys))
        for key in tuple(meta.keys()):
            if key not in allowed_keys:
                raise ValidationError(
                    [key_check, key],
                    "structure error",
                    self.extract_alert(
                        self.meta_check.__doc__,
                        "gDaEWfSPZgtGAZPEhlgElQlvoSfjpiNG"
                    )
                )
        mType: str = meta.get("mType")
        if not isinstance(mType, str) or mType not in ("request", "response"):
            raise ValidationError(
                [key_check, "mType"], "structure error",
                self.extract_alert(
                    self.meta_check.__doc__, "QpWDPIeDijNbPyUieaW"
                )
            )
        if mType == "response":
            session_id: str = meta.get("session_id")
            if not isinstance(session_id, str):
                raise ValidationError(
                    [key_check, "session_id"], "structure error",
                    self.extract_alert(
                        self.meta_check.__doc__, "mBsXpITxYthrOjmGEZ"
                    )
                )
        elif mType == "request":
            pass
        
    
    def message_payload_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - False
            
        Description
        ---
        Валидатор `message_payload_check` совершает проверки:
        
        id:jfvIrtZSVirGTFhlOG
            `EventMessage -> "message_payload"`
            Значение ключа `"message_payload"` должно иметь тип `dict`.
            
        id:kCBTbzYulyUyHiiOfkRDlwTwuBuCLfvX
            `EventMessage -> "message_payload"`
            Допустимые ключи  словаря `"message_payload"`:
            - `data`
            - `meta`
            
        id:GylUUkslKWmHGKtZwk
            `EventMessage -> "message_payload" -> "data"`
            Значение ключа `"data"` должно иметь тип `dict`.
            
        id:uDQzsHfQupVhdlCEdr
            `EventMessage -> "message_payload" -> "meta"`
            Значение ключа `"meta"` должно иметь тип `dict`.
        
        id:nesGfLMiEscTUuCZPXNEpGWrXUO
            `EventMessage -> "message_payload" -> "meta"`
            Допустимые ключи словаря `"meta"`:
            - `expire_time` (при `"mType": "request"`)
            - `background` (при `"mType": "request"`)
            - `max_execution_time` (при `"mType": "request"`)
            - `status_code` (при `"mType": "response"`)
        
        id:tRqerKyJHOhzOIjCngF
            `EventMessage -> "message_payload" -> "meta" -> "expire_time"`
            При `"mType": "request"` значение ключа `expire_time` должно иметь
            тип `int` / `float`.
            
        id:qQxlevznRZBSWWswIB
            `EventMessage -> "message_payload" -> "meta" -> "background"`
            При `"mType": "request"` значение ключа `"background"` должно иметь
            тип `bool`.
            
        id:wSPapfOYXahnLLoDSe
            `EventMessage -> "message_payload" -> "meta" -> "max_execution_time"`
            При `"mType": "request"` значение ключа `"max_execution_time"`
            должно иметь тип `int` / `float`.
            
        id:WKafpSIKjuISaKzyxXpE
            EventMessage -> "message_payload" -> "meta" -> "status_code"`
            При `"mType": "response"` значение ключа `"status_code"` должно
            иметь тип `int`
        """
        key_check = "message_payload"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        message_payload: dict = self.validation_data.get(key_check)
        mType: str = self.validation_data.get("meta", {}).get("mType")
        if not isinstance(message_payload, dict):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.message_payload_check.__doc__, "jfvIrtZSVirGTFhlOG"
                )
            )
        allowed_keys = ("data", "meta")
        for key in tuple(message_payload.keys()):
            if key not in allowed_keys:
                raise ValidationError(
                    [key_check, key],
                    "structure error",
                    self.extract_alert(
                        self.message_payload_check.__doc__,
                        "kCBTbzYulyUyHiiOfkRDlwTwuBuCLfvX"
                    )
                )
        data: dict = message_payload.get("data")
        if not isinstance(data, dict):
            raise ValidationError(
                [key_check, "data"], "structure error",
                self.extract_alert(
                    self.message_payload_check.__doc__, "GylUUkslKWmHGKtZwk"
                )
            )
        meta: dict = message_payload.get("meta")
        if not isinstance(meta, dict):
            raise ValidationError(
                [key_check, "meta"], "structure error",
                self.extract_alert(
                    self.message_payload_check.__doc__, "uDQzsHfQupVhdlCEdr"
                )
            )
        allowed_keys = (
            "expire_time" if mType == "request" else None, 
            "background" if mType == "request" else None,
            "max_execution_time" if mType == "request" else None,
            "status_code" if mType == "response" else None,
        )
        allowed_keys = tuple(filter(None, allowed_keys))
        for key in tuple(meta.keys()):
            if key not in allowed_keys:
                raise ValidationError(
                    [key_check, key],
                    "structure error",
                    self.extract_alert(
                        self.message_payload_check.__doc__,
                        "nesGfLMiEscTUuCZPXNEpGWrXUO"
                    )
                )
        if mType == "request":
            if "expire_time" not in meta:
                expire_time = int(time.time() * 2)
            else:
                expire_time: int = meta.get("expire_time")
                if not isinstance(expire_time, (int, float)):
                    raise ValidationError(
                        [key_check, "meta", "expire_time"], "structure error",
                        self.extract_alert(
                            self.message_payload_check.__doc__, 
                            "tRqerKyJHOhzOIjCngF"
                        )
                    )
                expire_time += time.time()
            self.validation_data["message_payload"]["meta"]["expire_time"] = expire_time
            if "background" in meta:
                background: bool = meta.get("background")
                if not isinstance(background, bool):
                    raise ValidationError(
                        [key_check, "meta", "background"], "structure error",
                        self.extract_alert(
                            self.message_payload_check.__doc__, 
                            "qQxlevznRZBSWWswIB"
                        )
                    )
            if "max_execution_time" in meta:
                max_execution_time: int = meta.get("max_execution_time")
                if not isinstance(max_execution_time, (int, float)):
                    raise ValidationError(
                        [key_check, "meta", "max_execution_time"], "structure error",
                        self.extract_alert(
                            self.message_payload_check.__doc__, 
                            "wSPapfOYXahnLLoDSe"
                        )
                    )
        elif mType == "response":
            status_code: int = meta.get("status_code")
            if not isinstance(status_code, int):
                raise ValidationError(
                    [key_check, "meta", "status_code"], "structure error",
                    self.extract_alert(
                        self.message_payload_check.__doc__, 
                        "WKafpSIKjuISaKzyxXpE"
                    )
                )
            
    
    def response_settings_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - False
            
        Description
        ---
        Валидатор `response_settings_check` совершает проверки:
        
        id:UEgeeXWliGSWpmklUYIy
            `EventMessage -> "response_settings"`
            При `"mType": "request"` значение ключа `"response_settings"`
            должно иметь тип `dict`.
            
        id:OGKgodxTDdvvxQtLbSmqGflMn
            `EventMessage -> "response_settings"`
            Допустимые ключи словаря `"response_settings"`:
            - `isAwaiting` (при `"mType": "request"`)
            - `await_timeout` (при `"mType": "request"`, `"isAwaiting": True`).
            
        id:tRAiAZPIiwagVSfTbNxW
            `EventMessage -> "response_settings" -> "isAwaiting"`
            При `"mType": "request"`, значение ключа `"isAwaiting"` должно
            иметь тип `bool`.
            
        id:UGBybhiAGyxQjtbNUrrJi
            `EventMessage -> "response_settings" -> "await_timeout"`
            При `"mType": "request"`, `"isAwaiting": True`, значение ключа
            `await_timeout` должно иметь тип `int` / `float`, и быть `>` 0.
        """
        key_check = "response_settings"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        mType: str = self.validation_data.get("meta", {}).get("mType")
        response_settings: dict = self.validation_data.get(key_check)
        if mType == "request":
            if not isinstance(response_settings, dict):
                raise ValidationError(
                    [key_check], "structure error",
                    self.extract_alert(
                        self.response_settings_check.__doc__, "UEgeeXWliGSWpmklUYIy"
                    )
                )
            allowed_keys = (
                "isAwaiting",
                "await_timeout" if response_settings.get("isAwaiting") else None
            )    
            allowed_keys = tuple(filter(None, allowed_keys))
            for key in tuple(response_settings.keys()):
                if key not in allowed_keys:
                    raise ValidationError(
                        [key_check, key],
                        "structure error",
                        self.extract_alert(
                            self.response_settings_check.__doc__,
                            "OGKgodxTDdvvxQtLbSmqGflMn"
                        )
                    )
            isAwaiting: bool = response_settings.get("isAwaiting")
            if not isinstance(isAwaiting, bool):
                raise ValidationError(
                    [key_check, "isAwaiting"], "structure error",
                    self.extract_alert(
                        self.response_settings_check.__doc__, 
                        "tRAiAZPIiwagVSfTbNxW"
                    )
                )
            if isAwaiting:
                await_timeout: int = response_settings.get("await_timeout")
                if (
                    not isinstance(await_timeout, (int, float)) or 
                    not await_timeout > 0
                ):
                    raise ValidationError(
                        [key_check, "await_timeout"], "structure error",
                        self.extract_alert(
                            self.response_settings_check.__doc__,
                            "UGBybhiAGyxQjtbNUrrJi"
                        )
                    )
            