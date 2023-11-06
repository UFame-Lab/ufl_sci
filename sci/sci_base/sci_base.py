import traceback
import asyncio

from typing import Awaitable

import redis.asyncio as redis

from sci.sci_core.sci_core import SCI_core
from sci.sci_cli.sci_cli import SCI_cli
from sci.lib.patterns import create_ecsaddo
from sci.sci_base.validators import SCI_SETTINGS_Validate
from sci.sci_typing import ecsaddo


class SCI:
    """
    Класс инициализации `sci node`
    """
    def __init__(
        self,
        sci_mode: str,
        SCI_SETTINGS: dict,
    ):
        """
        Meta
        ---
        Patterns:
            [__gw__pl lvl 1]
            
        Arguments
        ---
        - `sci_mode: str` - Режим инициализации `sci node`. 
        "shadow", "only_local", "standart".
        
        - `SCI_SETTINGS: dict` - Настройки для `sci node`
        """
        if sci_mode not in ("shadow", "only_local", "standart"):
            raise ValueError(
                "sci_mode должен быть 'shadow' / 'only_local' / 'standart'"
            )
        if not isinstance(SCI_SETTINGS, dict):
            raise ValueError(
                "Значение аргумент SCI_SETTINGS должно иметь тип `dict`" 
            )
        self.SCI_SETTINGS: dict = SCI_SETTINGS
        self.sci_mode: str = sci_mode
        ecsaddo_validate: dict = SCI_SETTINGS_Validate(
            validation_data=self.SCI_SETTINGS,
            sci_mode=self.sci_mode,
        ).start_validation()
        if ecsaddo_validate["status"] != "ok":
            raise ValueError(ecsaddo_validate)
        if self.sci_mode in ("shadow", "standart"):
            connection_settings: dict = (
                self.SCI_SETTINGS["local_broker_connection_settings"]["redis"]
            )
            redis_conn = redis.Redis(
                host=connection_settings["host"]["local"],
                port=connection_settings["port"],
                password=connection_settings["password"],
                db=connection_settings["db"]
            )
            connection_settings.setdefault("redis_conn", redis_conn)
        self.logfilePath: str = self.SCI_SETTINGS["logfilePath"]
        self.sci_cli = self._get_sci_cli()
        self.sci_core = self._get_sci_core()
        if self.sci_mode in ("standart", "only_local"):
            ecsaddo_reg_apps: dict = self.appConfHandler()
            if ecsaddo_reg_apps["status"] != "ok":
                raise ValueError(ecsaddo_reg_apps)
            self.awaitableAppControllers: list[Awaitable] = (
                ecsaddo_reg_apps["data"]["awaitableAppControllers"]
            )
    

    def start(self) -> tuple:
        """ 
        Description
        ---
        Точка получения `sci_cli`, `sci_core`.
        
        Return
        ---
        `(self.sci_cli, self.sci_core)`
        """
        return (self.sci_cli, self.sci_core)
    

    def core_is_ready(self) -> bool:
        """            
        Description
        ---
        Метод `core_is_ready()` проверяет готов ли `sci_core` принимать
        запросы.

        P.S: В режиме "shadow", метод `core.is_ready()` всегда будет 
        возвращать `True`.
        """
        if self.sci_mode == "shadow":
            return True
        else:
            result = self.sci_core.is_working
            return result


    def _get_sci_cli(self) -> SCI_cli:
        """
        Description
        ---
        `_get_sci_cli` совершает инициализацию `sci_cli`
        
        Return
        ---
        `sci_cli` - Экземпляр `SCI_cli`
        """
        sci_cli = SCI_cli(
            SCI_SETTINGS=self.SCI_SETTINGS, 
            sci_mode=self.sci_mode,
            sci_ref=self,
        )
        return sci_cli
    

    def _get_sci_core(self) -> SCI_core:
        """
        Description
        ---
        `_get_sci_core` совершает инициализацию `sci_core`
        
        Return
        ---
        `sci_core` - Экземпляр `SCI_core`
        """
        sci_core = SCI_core(
            SCI_SETTINGS=self.SCI_SETTINGS,
            sci_mode=self.sci_mode,
            sci_ref=self
        )
        return sci_core


    def appConfHandler(self) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            [__pl lvl 2]
            ecsaddo

        Description
        ---
        Метод `SCI_core.appConfHandler` регистрирует все `application` из списка 
        `SCI_SETTINGS -> "AppConf"` в `SCI_SETTINGS -> "app_controllers"`.

        Если при регистрации какого либо `application` возникает ошибка, 
        то `SCI_core.appConfHandler` вернет соответствующий 
        `ecsaddo` в `"data" -> "error_message"` в котором будет указанно 
        какой `application` из `AppConf` и почему не удалось зарегистрировать 
        в `SCI_SETTINGS -> "app_controllers"`

        Если удалось зарегистрировать все `application` из `AppConf` в 
        `app_controllers`, тогда возвращается `ecsaddo` в 
        `"data" -> "awaitableAppControllers"` содержится список с уже 
        сконфигурированными сопрограммами всех `app_controllers`, 
        которые нужно будет запустить в качестве `background` `asyncio.Task`
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        F.E:
        ```python
        {
            "status": "ok",
            "action": "",
            "data": {
                "description": "",
                "awaitableAppControllers": [
                    <awaitable app_controller1>,
                    <awaitable app_controller2>,
                    <awaitable app_controller3>,
                ]
            }
        }
        ```
        """
        try:
            error_message = []
            awaitableAppControllers = []
            # Доверяем валидации SCI_SETTINGS["AppConf"]
            self.SCI_SETTINGS.setdefault("app_controllers", {})
            for SCIApp, app_name, context in self.SCI_SETTINGS["AppConf"]:
                app_instance = (
                    SCIApp(app_name, self.sci_cli, context)
                )
                ecsaddo_get_register_data: dict = (
                    app_instance.get_register_data()
                )
                if ecsaddo_get_register_data["status"] != "ok":
                    error_message.append(ecsaddo_get_register_data)
                    continue
                queue: asyncio.Queue = (
                    ecsaddo_get_register_data.get("data").get("queue")
                )
                awaitableAppController: Awaitable = (
                    ecsaddo_get_register_data.get("data").get(
                        "awaitableAppController"
                    )
                )
                ecsaddo_register_app: dict = (
                    self._register_app(app_name=app_name, queue=queue)
                )
                if ecsaddo_register_app["status"] != "ok":
                    error_message.append(ecsaddo_register_app)
                    continue
                awaitableAppControllers.append(awaitableAppController)
            if error_message:
                return create_ecsaddo(
                    "error",
                    "register app_controllers error",
                    ("error occurred during registrations apps "
                    "from 'AppConf' in 'app_controllers'"),
                    error_message=error_message
                )
            return create_ecsaddo(
                "ok", 
                awaitableAppControllers=awaitableAppControllers
            )
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "appConfHandler (ex)",
                ("exception occurred during registrations apps "
                "from 'AppConf' in 'app_controllers'"),
                location=True,
                traceback=trc,
            )
           

    def _register_app(
        self, 
        app_name: str, 
        queue: asyncio.Queue
    ) -> ecsaddo:
        """
        Meta
        ---
        Patterns:
            ecsaddo
           
        Arguments
        ---
        - `app_name: str` - имя приложения.
        - `queue: asyncio.Queue` - `asyncio.Queue` очередь которую прослушивет
        `app_controller` (ядро) приложения.
            
        Description
        ---
        Метод `_register_app` добавляет в `SCI_SETTINGS -> "app_controllers"` 
        запись `"app_name": asyncio.Queue`

        Если запись с таким `app_name` уже есть в `"app_controllers"`, то 
        `SCI._register_app()` возвращает отрицательный `ecsaddo`.
        
        Return
        ---
        `ecsaddo` "ok", "error", "ex"
        """
        try:
            if app_name in self.SCI_SETTINGS["app_controllers"]:
                raise ValueError(f"{app_name} already exists")
            self.SCI_SETTINGS["app_controllers"].setdefault(
                app_name, 
                queue
            )
            return create_ecsaddo("ok")
        except Exception as ex:
            trc = str(traceback.format_exception(ex))
            return create_ecsaddo(
                "ex",
                "_register_app (ex)",
                "exception occurred in _register_app",
                location=True,
                traceback=trc,
            )