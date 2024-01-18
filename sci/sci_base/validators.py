import asyncio
import os

from typing import Any, Optional

from sci.lib.validation import BaseValidate, ValidationError
from sci.sci_settings import SCI_NODE_RQ_PREFIX
from sci.app_controllers.base_controller import SCI_BaseAppController
from sci.apps.nodeLifespanSystemSCIApp.application import NodeLifespanSystemSCIApp


class SCI_SETTINGS_Validate(BaseValidate):
    
    def __init__(
        self,
        validation_data: dict,
        sci_mode: str
    ) -> None:
        self.validation_data: dict = validation_data
        self.sci_mode: str = sci_mode
        
        
    def build_validation_plan(self) -> list:
        # Разный в зависимости от режима.
        match self.sci_mode:
            case 'standart':
                validation_plan = [
                    ("node_name_check", {"required": True}),
                    ("node_rq_check", {"required": True}), 
                    ("node_aq_check", {"required": True}),
                    ("logfilePath_check", {"required": True}),
                    ("AppConf_check", {"required": True}),
                    ("nodes_check", {"required": True}),
                    ("websocket_connections_check", {"required": True}),
                    ("local_broker_connection_settings_check", {"required": True})
                ]
            case "shadow":
                validation_plan = [
                    ("related_node_rq_check", {"required": True}),
                    ("logfilePath_check", {"required": True}),
                    ("local_broker_connection_settings_check", {"required": True}),
                ]
            case "only_local":
                validation_plan = [
                    ("node_name_check", {"required": True}),
                    ("node_aq_check", {"required": True}),
                    ("logfilePath_check", {"required": True}),
                    ("AppConf_check", {"required": True}),
                ]
        if not validation_plan:
            raise ValueError("validation is empty")
        return validation_plan


    def pre_validation(self):
        """
        Description
        ---
        Валидатор `pre_validation` совершает проверки:
        
        id:gyYxUhUAzSwweErcLgRLWegMCFxKfx
            `SCI_SETTINGS`
            `SCI_SETTINGS` должен иметь тип `dict`
        """
        if not isinstance(self.validation_data, dict):
            raise ValidationError(
                [], "structure error",
                self.extract_alert(
                    self.pre_validation.__doc__,
                    "gyYxUhUAzSwweErcLgRLWegMCFxKfx"
                )
            )
    
    
    def full_validation(self):
        """
        Description
        ---
        Валидатор `full_validation` совершает проверки:
        
        id:qCYhjdnVZkWwvguSaEhfyDqmVxNxOJk
            `EventMessage`
            Допустимые ключи  словаря `SCI_SETTINGS`:
            - `node_name` (при `"sci_mode" - "standart", "only_local"`)
            - `node_rq` (при `"sci_mode" - "standart"`)
            - `node_aq` (при `"sci_mode" - "standart", "only_local"`)
            - `logfilePath`
            - `AppConf` (при `"sci_mode" - "standart", "only_local"`)
            - `nodes` (при `"sci_mode" - "standart"`)
            - `websocket_connections` (при `"sci_mode" - "standart"`)
            - `local_broker_connection_settings` (при `"sci_mode" - "standart", "shadow"`)
            - `related_node_rq` (при `"sci_mode" - "only_local"`)
        """
        allowed_keys = (
            "node_name" if self.sci_mode in ("standart", "only_local") else None,
            "node_rq" if self.sci_mode == "standart" else None,
            "node_aq" if self.sci_mode in ("standart", "only_local") else None,
            "logfilePath",
            "AppConf" if self.sci_mode in ("standart", "only_local") else None,
            "nodes" if self.sci_mode == "standart" else None,
            "websocket_connections" if self.sci_mode == "standart" else None,
            "local_broker_connection_settings" if self.sci_mode in ("standart", "shadow") else None,
            "related_node_rq" if self.sci_mode == "shadow" else None
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


    def node_name_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `node_name_check` совершает проверки:
        
        id:hsMEfuJkkXmcpPBqFX
            `SCI_SETTINGS -> "node_name"`
            Значение ключа `"node_name"` должно иметь тип `str`.
        """
        key_check = "node_name"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        node_name: str = self.validation_data.get(key_check)
        if not isinstance(node_name, str):
            raise ValidationError(
                [key_check],
                "structure error",
                self.extract_alert(
                    self.node_name_check.__doc__,
                    "hsMEfuJkkXmcpPBqFX"
                )
            )
    
    
    def node_rq_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `node_rq_check` совершает проверки:
        
        id:GJResZnOZMTHPjdqzVNg
            `SCI_SETTINGS -> "node_rq"`
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
                    self.node_rq_check.__doc__, "GJResZnOZMTHPjdqzVNg"
                )
            )
        
    
    def node_aq_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `node_aq_check` совершает проверки:
        
        id:GJResZnOZMTHPjdqzVNg
            `SCI_SETTINGS -> "node_aq"`
            Значение ключа `"node_aq"` должно иметь тип `asyncio.Queue()`
        """
        key_check = "node_aq"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        node_aq: str = self.validation_data.get(key_check)
        if not isinstance(node_aq, asyncio.Queue):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.node_aq_check.__doc__, "GJResZnOZMTHPjdqzVNg"
                )
            )
            
    
    def logfilePath_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `logfilePath_check` совершает проверки:
        
        id:WeJyXnYWQGJYUkngAR
            `SCI_SETTINGS -> "logfilePath"`
            Значение ключа `"logfilePath"` должно иметь тип `str`.
        """
        key_check = "logfilePath"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        logfilePath: str = self.validation_data.get(key_check)
        # if (
        #     not isinstance(logfilePath, str) or
        #     not os.path.isfile(logfilePath) or
        #     os.path.isdir(logfilePath) or
        #     not os.access(logfilePath, os.W_OK)
        # ):
        if not isinstance(logfilePath, str):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.logfilePath_check.__doc__, "WeJyXnYWQGJYUkngAR"
                )
            )
            
    
    def AppConf_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `AppConf_check` совершает проверки:
        
        id:fYhFpwPlkLjeJxUpvTYk
            `SCI_SETTINGS -> "AppConf"`
            Значение ключа `"AppConf"` должно иметь тип `list`. В качестве
            содержимого `"AppConf"` выступают кортежи с настройками приложений.
            `"AppConf"` должен содержать настройку как минимум 1 приложения.
            
        id:VuEJFDDnSOJySYcSrH
            `SCI_SETTINGS -> "AppConf" -> 0`
            Кортеж с настройками приложения должен иметь структуру:
            Первый элемент - класс SCIAPP пользовательского приложения
            производный от базового `SCI_BaseAppController`.
            Второй элемент - `app_name` имя приложения в виде строки.
            Третий элемент - словарь с дополнительными, опциональными
            переменными.
            
        id:NWzWVonZSaGfxeeYQVcj
            `SCI_SETTINGS -> "AppConf" -> 0 -> 1`
            `app_name` должен быть уникальным и состоянть `>=` 3 символам.
            
        id:lXMDFPzcYcKCwgnokICScOf
            `SCI_SETTINGS -> "AppConf" -> 0 -> 0`
            Приложение `NodeLifespanSystemSCIApp` доступно к использованию
            только при `"sci_mode": "standart"`.
        """
        key_check = "AppConf"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        AppConf: list = self.validation_data.get(key_check)
        if (
            not isinstance(AppConf, list) or
            not len(AppConf)
        ):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.AppConf_check.__doc__, "fYhFpwPlkLjeJxUpvTYk"
                )
            )
        app_names = [] 
        for index, app in enumerate(AppConf):
            sciAppClass = app[0] if len(app) else None
            app_name = app[1] if len(app) >= 2 else None
            context = app[2] if len(app) >= 3 else None
            if (
                not issubclass(sciAppClass, SCI_BaseAppController) or
                not isinstance(app_name, str) or
                not isinstance(context, dict)
            ):
                raise ValidationError(
                    [key_check, index],
                    "structure error",
                    self.extract_alert(
                        self.AppConf_check.__doc__, "VuEJFDDnSOJySYcSrH"
                    )
                )
            if not len(app_name) >= 3 or app_name in app_names:
                raise ValidationError(
                    [key_check, index, 1],
                    "structure error",
                    self.extract_alert(
                        self.AppConf_check.__doc__, "NWzWVonZSaGfxeeYQVcj"
                    )
                )
            if (
                not self.sci_mode == "standart" and 
                issubclass(sciAppClass, NodeLifespanSystemSCIApp)
            ):
                raise ValidationError(
                    [key_check, index, 0],
                    "structure error",
                    self.extract_alert(
                        self.AppConf_check.__doc__,
                        "lXMDFPzcYcKCwgnokICScOf"
                    )
                )
            app_names.append(app_name)
    
    
    def nodes_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `nodes_check` совершает проверки:
        
        id:NfclLGQiWVgEWhJvWRRFH
            `SCI_SETTINGS -> "AppConf" -> "nodes"`
            Значение ключа `"nodes"` должен иметь тип `dict`
            
        id:PvFeamRMTLXxsQfqAqAwf
            `SCI_SETTINGS -> "AppConf" -> "nodes" -> "local_nodes"`
            `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_nodes"`
            `SCI_SETTINGS -> "AppConf" -> "nodes" -> "remote_ws_nodes"`
            `"nodes"` должен содержать обязательные ключи "local_nodes",
            "remote_nodes", "remote_ws_nodes", значением которых должен быть
            `dict`.
        """
        key_check = "nodes"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        nodes: dict = self.validation_data.get(key_check)
        if not isinstance(nodes, dict):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.nodes_check.__doc__, "NfclLGQiWVgEWhJvWRRFH"
                )
            )
        local_nodes: dict = nodes.get("local_nodes")
        remote_nodes: dict = nodes.get("remote_nodes")
        remote_ws_nodes: dict = nodes.get("remote_ws_nodes")
        if (
            not isinstance(local_nodes, dict) or 
            not isinstance(remote_nodes, dict) or 
            not isinstance(remote_ws_nodes, dict)
        ):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.nodes_check.__doc__, "PvFeamRMTLXxsQfqAqAwf"
                )
            )
    
    
    def websocket_connections_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `websocket_connections_check` совершает проверки:
        
        id:UzUoVuOtXnbAMRTnoaSX
            `SCI_SETTINGS -> "AppConf" -> "websocket_connections"`
            Значение ключа `"websocket_connections"` должно иметь тип `dict`.
            
        id:sjUlRjjlfcosOlyQXKge
            `SCI_SETTINGS -> "AppConf" -> "websocket_connections"`
            Ключи словаря `"websocket_connections" это `str` имена `wsBridge`
            сервисов, а значения ключей - словари с настройками `ws` подключения.

        id:RlfosdZKBUKFURmDxcCZ
            `SCI_SETTINGS -> "AppConf" -> "websocket_connections" ->
            "wsBridgeName" -> "url"`.
            Ключ `"url"` должен  иметь значение типа `str`.
            
        id:usiROwOMLRXrevpoDCh
            `SCI_SETTINGS -> "AppConf" -> "websocket_connections" ->
            "wsBridgeName" -> "headers"`.
            Ключ `"headers"` должен  иметь значение типа `dict`.
            
        id:vHHVBVgDfqsbNjfsfvctu
            `SCI_SETTINGS -> "AppConf" -> "websocket_connections" ->
            "wsBridgeName" -> "wsBridgeBroker_aq"`.
            Ключ `"wsBridgeBroker_aq"` должен  иметь значение типа `asyncio.Queue`.
        """
        key_check = "websocket_connections"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        websocket_connections: dict = self.validation_data.get(key_check)
        if not isinstance(websocket_connections, dict):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.websocket_connections_check.__doc__,
                    "UzUoVuOtXnbAMRTnoaSX"
                )
            )
        for wsBridge in websocket_connections:
            if not isinstance(wsBridge, str):
                raise ValidationError(
                    [key_check, wsBridge], "structure error",
                    self.extract_alert(
                        self.websocket_connections_check.__doc__,
                        "sjUlRjjlfcosOlyQXKge"
                    )
                )
            url: str = websocket_connections[wsBridge].get("url")
            headers: dict = websocket_connections[wsBridge].get("headers")
            wsBridgeBroker_aq: asyncio.Queue = (
                websocket_connections[wsBridge].get("wsBridgeBroker_aq")
            )
            if not isinstance(url, str):
                raise ValidationError(
                    [key_check, wsBridge, "url"], "structure error",
                    self.extract_alert(
                        self.websocket_connections_check.__doc__,
                        "RlfosdZKBUKFURmDxcCZ"
                    )
                )
            if not isinstance(headers, dict):
                raise ValidationError(
                    [key_check, wsBridge, "headers"], "structure error",
                    self.extract_alert(
                        self.websocket_connections_check.__doc__,
                        "usiROwOMLRXrevpoDCh"
                    )
                )
            if not isinstance(wsBridgeBroker_aq, asyncio.Queue):
                raise ValidationError(
                    [key_check, wsBridge, "wsBridgeBroker_aq"],
                    "structure error",
                    self.extract_alert(
                        self.websocket_connections_check.__doc__,
                        "vHHVBVgDfqsbNjfsfvctu"
                    )
                )
    
    
    def local_broker_connection_settings_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `local_broker_connection_settings_check` совершает проверки:
        
        id:mngmdypTFHqBfMKgegbkj
            `SCI_SETTINGS -> "broker_connection_settings"`
            Значение ключа `"broker_connection_settings"` должен быть тип `dict`,
            который должен содержать ключ `"redis"`.
            
        id:KCOhmJpPTHNwkKMHehu
            `SCI_SETTINGS -> "broker_connection_settings" -> "redis"`
            Словарь `"redis"` должен содержать ключи:
            `host`, 'port', 'password', 'db`.
            
        id:MiySYvZgOVsnlzDeMB
            `SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "host"`
            Значение ключа `"host"` должно иметь тип `dict`
            
        id:FzEEykfEWipycUkoBus
            `SCI_SETTINGS -> "broker_connection_settings" -> "redis" ->
            "host" -> "local"`
            Значение ключа `"local"` должно иметь тип `str`
            
        id:RynWfYDpkjeUINPAQDan
            `SCI_SETTINGS -> "broker_connection_settings" -> "redis" ->
            "host" -> "local-network"`
            Значение ключа `"local-network"` должно иметь тип `str`.
            
        id:sXscUmCDYPzeIqvKbbisqxi
            `SCI_SETTINGS -> "broker_connection_settings" -> "redis" ->
            "host" -> "external"`
            Значение ключа `"external"` должно иметь тип `str`.
            
        id:IGlBpjIaLezlPUhKiUUFIwZhFUSftno
            `SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "port"`
            Значение ключа `"port"` должно иметь тип `int`
            
        id:sbGlRjSdIFzxNrOztTsB
            `SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "password"`
            Значение ключа `"password"` должно иметь тип `str` и быть длиной
            `>=` 3 символам, или быть `None`.
            
        id:OsAFqMoFVqaJoKyBJXFF
            `SCI_SETTINGS -> "broker_connection_settings" -> "redis" -> "db"`
            Значение ключа `"db"` должно иметь тип `int`.
        """
        key_check = "local_broker_connection_settings"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        local_broker_connection_settings: dict = (
            self.validation_data.get(key_check)
        )
        if (
            not isinstance(local_broker_connection_settings, dict) or
            "redis" not in local_broker_connection_settings
        ):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.local_broker_connection_settings_check.__doc__,
                    "mngmdypTFHqBfMKgegbkj"
                )
            )
        redis_settings: dict = local_broker_connection_settings.get("redis")
        if (
            not isinstance(redis_settings, dict) or
            "host" not in redis_settings or
            "port" not in redis_settings or
            "password" not in redis_settings or
            "db" not in redis_settings
        ):
            raise ValidationError(
                [key_check, "redis"], "structure error",
                self.extract_alert(
                    self.local_broker_connection_settings_check.__doc__,
                    "KCOhmJpPTHNwkKMHehu"
                )
            )
        redis_host: dict = redis_settings.get("host")
        if not isinstance(redis_host, dict):
            raise ValidationError(
                [key_check, "redis", "host"], "structure error",
                self.extract_alert(
                    self.local_broker_connection_settings_check.__doc__,
                    "MiySYvZgOVsnlzDeMB"
                )
            )
        if not isinstance(redis_host.get("local"), str):
            raise ValidationError(
                [key_check, "redis", "host", "local"], "structure error",
                self.extract_alert(
                    self.local_broker_connection_settings_check.__doc__,
                    "FzEEykfEWipycUkoBus"
                )
            )
        if "local-network" in redis_host:
            if not isinstance(redis_host["local-network"], str):
                raise ValidationError(
                    [key_check, "redis", "host", "local-network"],
                    "structure error",
                    self.extract_alert(
                        self.local_broker_connection_settings_check.__doc__,
                        "RynWfYDpkjeUINPAQDan"
                    )
                )
        if "external" in redis_host:
            if not isinstance(redis_host["external"], str):
                raise ValidationError(
                    [key_check, "redis", "host", "external"],
                    "structure error",
                    self.extract_alert(
                        self.local_broker_connection_settings_check.__doc__,
                        "sXscUmCDYPzeIqvKbbisqxi"
                    )
                )
        redis_port: int = redis_settings.get("port")
        if not isinstance(redis_port, int):
            raise ValidationError(
                [key_check, "redis", "port"], "structure error",
                self.extract_alert(
                    self.local_broker_connection_settings_check.__doc__,
                    "IGlBpjIaLezlPUhKiUUFIwZhFUSftno"
                )
            )
        redis_password: Optional[str | int] = (
            redis_settings.get("password", tuple())
        )
        if (
            (not isinstance(redis_password, str) or
             not len(redis_password) >=3) and
            (not redis_password is None)
        ):
            raise ValidationError(
                [key_check, "redis", "password"], "structure error",
                self.extract_alert(
                    self.local_broker_connection_settings_check.__doc__,
                    "sbGlRjSdIFzxNrOztTsB"
                )
            )
        redis_db: int = redis_settings.get("db")
        if not isinstance(redis_db, int):
            raise ValidationError(
                [key_check, "redis", "db"], "structure error",
                self.extract_alert(
                    self.local_broker_connection_settings_check.__doc__,
                    "OsAFqMoFVqaJoKyBJXFF"
                )
            )
        
    
    def related_node_rq_check(self, num: int, **kwargs) -> Any:
        """
        Meta
        ---
        Patterns:
            required - True
            
        Description
        ---
        Валидатор `related_node_rq_check` совершает проверки:
        
        id:yrUGRIAtDcxIiwddFmAt
            `SCI_SETTINGS -> "related_node_rq"`
            Значение ключа `"related_node_rq"` должно иметь тип `str`, начинаться с
            префикса `SCI_NODE_RQ_PREFIX`.
        """
        key_check = "related_node_rq"
        if (
            key_check not in self.validation_data and
            kwargs.get("required") is False
        ):
            return True
        related_node_rq: str = self.validation_data.get(key_check)
        if (
            not isinstance(related_node_rq, str) or
            not related_node_rq.startswith(SCI_NODE_RQ_PREFIX)
        ):
            raise ValidationError(
                [key_check], "structure error",
                self.extract_alert(
                    self.related_node_rq_check.__doc__,
                    "yrUGRIAtDcxIiwddFmAt"
                )
            )