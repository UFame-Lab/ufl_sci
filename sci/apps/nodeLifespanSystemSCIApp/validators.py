from typing import Optional, Any

from sci.lib.validation import BaseValidate, ValidationError
from sci.sci_settings import SCI_NODE_RQ_PREFIX


class NodeLifespanSystemSCIAppContext_Validate(BaseValidate):
    """    
    context = {
        "auth_nodes_settings": {
            "local_nodes": {
                "node_name1": {
                    "node_rq": "sci_rq_name",
                    "wsBridgeBroker": tuple(),
                },
                "node_name2": {
                    "node_rq": "sci_rq_name",
                    "wsBridgeBroker": tuple(),
                },
            },
            "remote_nodes": {
                "node_name1": {
                    "node_rq": "sci_rq_name",
                    "wsBridgeBroker": tuple(),
                    "broker_connection_settings": {
                        "redis": {
                            "host": "localhost",
                            "port": 6379,
                            "password": None,
                            "db": 0,
                        },
                    },
                    "back_address": "local" / "local-network" / "external"
                },
            },
            "remote_ws_nodes": {
                "node_name": {
                    "wsbridge": "bridge_name",
                    "dependent": True / False
                }
            }
        }
    }
    """
    
    def __init__(
        self, 
        validation_data: dict,
        SCI_SETTINGS: dict,
        sci_mode: str,
    ) -> None:
        self.validation_data: dict = validation_data
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = sci_mode
        
        
    def build_validation_plan(self) -> list:
        validation_plan = [
            ("auth_nodes_settings_check", {"required": False}),
        ]
        return validation_plan
        
    
    def pre_validation(self):
        """
        Description
        ---
        Валидатор `pre_validation` совершает проверки:
        
        id:gyYxUhUAzSwweErcLgRLWegMCFxKfx
            `context`
            `context` должен иметь тип `dict`
        """
        if not isinstance(self.validation_data, dict):
            raise ValidationError(
                [], "structure error",
                self.extract_alert(
                    self.pre_validation.__doc__,
                    "gyYxUhUAzSwweErcLgRLWegMCFxKfx"
                )
            )
        
    
    def auth_nodes_settings_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - False
            
        Description
        ---
        Валидатор `auth_nodes_settings_check` совершает проверки:
        
        id:LhCxqYfczcp
            `context -> "auth_nodes_settings: dict"`
            Значение ключа `auth_nodes_settings` должно быть `dict`.
            
        id:PtIbIYGgMdWqU
            `context -> "auth_nodes_settings" -> "local_nodes"`
            `context -> "auth_nodes_settings" -> "remote_nodes"`
            `context -> "auth_nodes_settings" -> "remote_ws_nodes"`
            Словарь `auth_nodes_settings` должен содержать хотя-бы 1 не пустой
            словарь с настройками.
            
        id:IxSkgrXlRyv
            `context -> "auth_nodes_settings" -> "local_nodes: dict"`
            Значение ключа `"local_nodes"` должен быть тип `dict`.
            
        id:UDEddJQhnPSqArxV
            `context -> "auth_nodes_settings" -> "local_nodes" -> "node_name"`
            Ключ `"node_name"` должен иметь тип `str`.
            
        id:xNBGkytRhCMSiic
            `context -> "auth_nodes_settings" -> "remote_nodes: dict"`
            Значение ключа `"remote_nodes"` должен быть тип `dict`.
            
        id:LIaoOlnpAfLo
            `context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name"`
            Ключ `"node_name"` должен иметь тип `str`.
            
        id:zUHgjrJICvEekfRFZH
            `context -> "auth_nodes_settings" -> "remote_ws_nodes: dict"`
            Значение ключа `"remote_ws_nodes"` должен быть тип `dict`.
            
        id:SFrePFbRKzfvcAQISk
            `context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "node_name"`
            Ключ `"node_name"` должен иметь тип `str`.
        """
        key_check = "auth_nodes_settings"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        auth_nodes_settings: dict = self.validation_data.get(key_check)
        if not isinstance(auth_nodes_settings, dict):
            raise ValidationError(
                [key_check], 
                "type error", 
                self.extract_alert(
                    self.auth_nodes_settings_check.__doc__, "LhCxqYfczcp"
                )
            )
        local_nodes: Optional[dict] = (
            auth_nodes_settings.get("local_nodes")
        )
        remote_nodes: Optional[dict] = (
            auth_nodes_settings.get("remote_nodes")
        )
        remote_ws_nodes: Optional[dict] = (
            auth_nodes_settings.get("remote_ws_nodes")
        )
        if not any([local_nodes, remote_nodes, remote_ws_nodes]):
            raise ValidationError(
                [key_check], 
                "structure error",
                self.extract_alert(
                    self.auth_nodes_settings_check.__doc__, "PtIbIYGgMdWqU"
                )
            )
        if local_nodes:
            if not isinstance(local_nodes, dict):
                raise ValidationError(
                    [key_check, "local_nodes"], 
                    "type error",
                    self.extract_alert(
                        self.auth_nodes_settings_check.__doc__, "IxSkgrXlRyv"
                    )
                )
            for local_node in local_nodes:
                if not isinstance(local_node, str):
                    raise ValidationError(
                        [key_check, "local_nodes", local_node], 
                        "structure error",
                        self.extract_alert(
                            self.auth_nodes_settings_check.__doc__, 
                            "UDEddJQhnPSqArxV"
                        )
                    )
                ecsaddo: dict = LocalNodes_SubValidate(
                    validation_data=local_nodes[local_node],
                    SCI_SETTINGS=self.SCI_SETTINGS,
                    sci_mode=self.sci_mode,
                ).start_validation()
                if ecsaddo["status"] != "ok":
                    inner_error_list: list[tuple[list[str | int], str]] = (
                        self.join(
                            ecsaddo["data"]["error_list"], 
                            key_check,
                            "local_nodes",
                            local_node,
                        )
                    )
                    self.error_list += inner_error_list
                    if ecsaddo["status"] == "ex":
                        self.traceback_list += ecsaddo["data"]["traceback_list"]
        if remote_nodes:
            if not isinstance(remote_nodes, dict):
                raise ValidationError(
                    [key_check, "remote_nodes"], 
                    "type error",
                    self.extract_alert(
                        self.auth_nodes_settings_check.__doc__, 
                        "xNBGkytRhCMSiic"
                    )
                )
            for remote_node in remote_nodes:
                if not isinstance(remote_node, str):
                    raise ValidationError(
                        [key_check, "remote_nodes", remote_node], 
                        "structure error",
                        self.extract_alert(
                            self.auth_nodes_settings_check.__doc__, 
                            "LIaoOlnpAfLo"
                        )
                    )
                ecsaddo: dict = RemoteNodes_SubValidate(
                    validation_data=remote_nodes[remote_node],
                    SCI_SETTINGS=self.SCI_SETTINGS,
                    sci_mode=self.sci_mode,
                ).start_validation()
                if ecsaddo["status"] != "ok":
                    inner_error_list: list[tuple[list[str | int], str]] = (
                        self.join(
                            ecsaddo["data"]["error_list"],
                            key_check,
                            "remote_nodes",
                            remote_node
                        )
                    )
                    self.error_list += inner_error_list
                    if ecsaddo["status"] == "ex":
                        self.traceback_list += ecsaddo["data"]["traceback_list"]
        if remote_ws_nodes:
            if not isinstance(remote_ws_nodes, dict):
                raise ValidationError(
                    [key_check, "remote_ws_nodes"], 
                    "type_error",
                    self.extract_alert(
                        self.auth_nodes_settings_check.__doc__, 
                        "zUHgjrJICvEekfRFZH"
                    )
                )
            for remote_ws_node in remote_ws_nodes:
                if not isinstance(remote_ws_node, str):
                    raise ValidationError(
                        [key_check, "remote_ws_nodes", remote_ws_node], 
                        "structure error",
                        self.extract_alert(
                            self.auth_nodes_settings_check.__doc__, 
                            "SFrePFbRKzfvcAQISk"
                        )
                    )
                ecsaddo: dict = RemoteWsNodes_SubValidate(
                    validation_data=remote_ws_nodes[remote_ws_node],
                    SCI_SETTINGS=self.SCI_SETTINGS,
                    sci_mode=self.sci_mode,
                ).start_validation()
                if ecsaddo["status"] != "ok":
                    inner_error_list: list[tuple[list[str | int], str]] = (
                        self.join(
                            ecsaddo["data"]["error_list"],
                            key_check,
                            "remote_ws_nodes",
                            remote_ws_node
                        )
                    )
                    self.error_list += inner_error_list
                    if ecsaddo["status"] == "ex":
                        self.traceback_list += ecsaddo["data"]["traceback_list"]
        
            
class LocalNodes_SubValidate(BaseValidate):
    """
    {
        "node_rq": "sci_rq_name",
        "wsBridgeBroker": tuple(),
    }
    """
    def __init__(
        self, 
        validation_data: dict,
        SCI_SETTINGS: dict,
        sci_mode: str,
    ) -> None:
        self.validation_data: dict = validation_data
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = sci_mode
        
    
    def build_validation_plan(self) -> list:
        validation_plan = [
            ("node_rq_check", {"required": True}),
            ("wsBridgeBroker_check", {"required": True}),
        ]
        return validation_plan
        
       
    def node_rq_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required
        
        Description
        ---
        Валидатор `node_rq_check` совершает проверки:
        
        id:nJjLSGQoNHwAK
            `context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" ->
            "node_rq"`
            Значение ключа `"node_rq"` должно иметь тип `str`, начинаться с
            префикса `SCI_NODE_RQ_PREFIX`.
        """
        key_check = "node_rq"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        node_rq: str = self.validation_data.get(key_check)
        if (
            not isinstance(node_rq, str) or 
            not node_rq.startswith(SCI_NODE_RQ_PREFIX)
        ):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.node_rq_check.__doc__, "nJjLSGQoNHwAK"
                )
            )
        
    
    def wsBridgeBroker_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required
            
        Description
        ---
        Валидатор `wsBridgeBroker_check` совершает проверки:
        
        id:nyHYVJUhGAkFk
            `context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" ->
            "wsBridgeBroker"`
            Значением ключа `"wsBridgeBroker"` должен иметь тип `tuple` или `list`
            
        id:YGUOQsUnrrZWrtBa
            `context -> "auth_nodes_settings" -> "local_nodes" -> "node_name" ->
            "wsBridgeBroker"`
            Каждое значение кортежа - имя (str) `wsBridge`, должно быть `>=` 3 
            символам.
        """
        key_check = "wsBridgeBroker"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        wsBridgeBroker: tuple[str] = self.validation_data.get(key_check)
        if not isinstance(wsBridgeBroker, (tuple, list)):
            raise ValidationError(
                [key_check], 
                "type error",
                self.extract_alert(
                    self.wsBridgeBroker_check.__doc__, "nyHYVJUhGAkFk"
                )
            )
        for wsBridge in wsBridgeBroker:
            if not isinstance(wsBridge, str) or not len(wsBridge) >= 3:
                raise ValidationError(
                    [key_check], 
                    "structure error",
                    self.extract_alert(
                        self.wsBridgeBroker_check.__doc__, "YGUOQsUnrrZWrtBa"
                    )
                )
        
        
class RemoteNodes_SubValidate(LocalNodes_SubValidate):
    
    def __init__(
        self, 
        validation_data: dict,
        SCI_SETTINGS: dict,
        sci_mode: str,
    ) -> None:
        self.validation_data: dict = validation_data
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = sci_mode
        
        
    def build_validation_plan(self) -> list:
        validation_plan = [
            ("node_rq_check", {"required": True}),
            ("wsBridgeBroker_check", {"required": True}),
            ("broker_connection_settings_check", {"required": True}),
            ("back_address_check", {"required": True})
        ]
        return validation_plan
    
        
    def broker_connection_settings_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required
            
        Description
        ---
        Валидатор `broker_connection_settings_check` совершает проверки:
    
        id:auglcXTYhVfufOB
            `context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" ->
            "broker_connection_settings"`
            Значение ключа `"broker_connection_settings"` должен быть тип `dict`,
            который должен содержать ключ `"redis"`.
    
        id:EUumxqCCGLspxkSyG
            `context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" ->
            "broker_connection_settings" -> "redis"`
            Словарь `"redis"` должен содержать ключи:
            `host, 'port', 'password', 'db`.
    
        id:WEoCIttbVOWsFtoLjH
            `context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" ->
            "broker_connection_settings" -> "redis" -> "host"`
            Значение ключа `"host"` должно иметь тип `str`.
            
        id:tdcdfoZLaHEvAslrDaWO
            `context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" ->
            "broker_connection_settings" -> "redis" -> "port"`
            Значение ключа `"port"` должно иметь тип `int`.
            
        id:ZVPLLNfffXFjpuViIfscfh
            `context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" ->
            "broker_connection_settings" -> "redis" -> "password"`
            Значение ключа `"password"` должно иметь тип `str` и быть длиной
            `>=` 3 символам, или быть `None`.
                        
        id:AxbocNskgSkqNYVqQh
            `context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" ->
            "broker_connection_settings" -> "redis" -> "db"`
            Значение ключа `"db"` должно иметь тип `int`.
        """
        key_check = "broker_connection_settings"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        broker_connection_settings: dict = self.validation_data.get(key_check)
        if (
            not isinstance(broker_connection_settings, dict) or 
            "redis" not in broker_connection_settings
        ):
            raise ValidationError(
                [key_check], 
                "structure error",
                self.extract_alert(
                    self.broker_connection_settings_check.__doc__,
                    "auglcXTYhVfufOB"
                )
            )
        redis_settings: dict = broker_connection_settings["redis"]
        if (
            not isinstance(redis_settings, dict) or 
            "host" not in redis_settings or 
            "port" not in redis_settings or 
            "password" not in redis_settings or 
            "db" not in redis_settings
        ):
            raise ValidationError(
                [key_check, "redis"], 
                "structure error",
                self.extract_alert(
                    self.broker_connection_settings_check.__doc__,
                    "EUumxqCCGLspxkSyG"
                )
            )
        redis_host: str = redis_settings.get("host")
        if not isinstance(redis_host, str):
            raise ValidationError(
                [key_check, "redis", "host"], 
                "type error",
                self.extract_alert(
                    self.broker_connection_settings_check.__doc__,
                    "WEoCIttbVOWsFtoLjH"
                )
            )
        redis_port: int = redis_settings.get("port")
        if not isinstance(redis_port, int):
            raise ValidationError(
                [key_check, "redis", "port"], 
                "type error",
                self.extract_alert(
                    self.broker_connection_settings_check.__doc__,
                    "tdcdfoZLaHEvAslrDaWO"
                )
            )
        redis_password: Optional[int | str] = (
            redis_settings.get("password", tuple())
        )
        if (
            (not isinstance(redis_password, str) or 
             not len(redis_password) >= 3) and 
            (not redis_password is None)
        ):
            raise ValidationError(
                [key_check, "redis", "password"],
                "structure error",
                self.extract_alert(
                    self.broker_connection_settings_check.__doc__,
                    "ZVPLLNfffXFjpuViIfscfh"
                )
            )
        redis_db: int = redis_settings.get("db")
        if not isinstance(redis_db, int):
            raise ValidationError(
                [key_check, "redis", "db"], 
                "type error",
                self.extract_alert(
                    self.broker_connection_settings_check.__doc__,
                    "AxbocNskgSkqNYVqQh"
                )
            )
            
            
    def back_address_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required
            
        Description
        ---
        Валидатор `back_address_check` совершает проверки:
        
        id:KpSPOPTLRYHvASxSR
            `context -> "auth_nodes_settings" -> "remote_nodes" -> "node_name" ->
            "back_address"`
            Значение ключа `"back_address"` должно иметь тип `str`, и
            входить в `["local", "local-network", "external"]`
        """
        key_check = "back_address"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        back_address: str = self.validation_data.get(key_check)
        available_values = [
            "local", "local-network", "external"
        ]
        if (
            not isinstance(back_address, str) or 
            back_address not in available_values
        ):
            raise ValidationError(
                [key_check], 
                "structure error",
                self.extract_alert(
                    self.back_address_check.__doc__, 
                    "KpSPOPTLRYHvASxSR"
                )
            )
        
    
class RemoteWsNodes_SubValidate(BaseValidate):
    
    def __init__(
        self, 
        validation_data: dict,
        SCI_SETTINGS: dict,
        sci_mode: str,
    ) -> None:
        self.validation_data: dict = validation_data
        self.SCI_SETTINGS = SCI_SETTINGS
        self.sci_mode = sci_mode
    
   
    def build_validation_plan(self) -> list:
        validation_plan = [
            ("wsbridge_check", {"required": True}),
            ("dependent_check", {"required": False},)
        ]
        return validation_plan
    
    
    def wsbridge_check(self, num: int, **kwargs) -> Optional[bool]:
        """
        Meta
        ---
        Patterns:
            required
            
        Description
        ---
        Валидатор `wsbridge_check` совершает проверки:
        
        id:dQnphMlhITbDhEMnPNqDn
            `context -> "auth_nodes_settings" -> "remote_ws_nodes" -> "node_name" ->
            "wsbridge"`
            Значение ключа `"wsbridge"` должно иметь тип `str`.
        """
        key_check = "wsbridge"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        wsbridge: str = self.validation_data.get(key_check)
        if not isinstance(wsbridge, str):
            raise ValidationError(
                [key_check], 
                "structure error",
                self.extract_alert(
                    self.wsbridge_check.__doc__, "dQnphMlhITbDhEMnPNqDn"
                )
            )
        # if wsbridge not in self.SCI_SETTINGS["websocket_connections"]:
        #     raise ValidationError(
        #         [key_check],
        #         "structure error",
        #         self.extract_alert(
        #             self.wsbridge_check.__doc__, "RsIbkgJvMYOufsJfXRJzOhzob"
        #         )
        #     )
        
        
    def dependent_check(self, num: int, **kwargs):
        """
        Meta
        ---
        Patterns:
            non required
            
        Description
        ---
        Валидатор `dependent_check` совершает проверки:
        
        id:iYRbmWwJqzvkuuYaBxboAIjfbvSDlKnd
            `context -> "auth_nodes_settings" -> "remote_ws_nodes" -> 
            "node_name" -> "dependent"`
            Значение ключа `"dependent"` должно иметь тип bool.
        """
        key_check = "dependent"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        dependent: bool = self.validation_data.get(key_check)
        if not isinstance(dependent, bool):
            raise ValidationError(
                [key_check],
                "structure error",
                self.extract_alert(
                    self.dependent_check.__doc__, 
                    "iYRbmWwJqzvkuuYaBxboAIjfbvSDlKnd"
                )
            )
        