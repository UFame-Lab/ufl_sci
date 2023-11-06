import inspect

from sci.sci_exceptions import EcsaddoStructureError


def create_ecsaddo(
    status: str, # "ok", "error", "ex"
    action: str = "", # buDsTRAMdz
    description: str = "",
    *,
    location: bool = False,
    **kwargs
):
    try:
        ecsaddo = {
             "status": status,
             "action": action,
             "data": {
                  "description": description,

             }
        }

        def get_location_data():
            try:
                # Получаем frame вызывающего кода
                frame = inspect.currentframe().f_back.f_back
                path_to_module = frame.f_code.co_filename
                qual_name = frame.f_code.co_qualname
                return (path_to_module, qual_name)
            except Exception as ex:
                return ('empty', 'empty')

        if location:
            location_data = get_location_data()
            ecsaddo["data"].setdefault(
                "location",
                {
                     "path_to_module": location_data[0],
                     "qual_name": location_data[1],
                }
            )
        for i in kwargs:
            ecsaddo["data"].setdefault(i, kwargs[i])
        return ecsaddo
    except Exception as ex:
        return {}
    

def isecsaddo(ecsaddo: dict) -> bool:
    """
    Arguments
    ---
    - `ecsaddo: dict` - Словарь который нужно проверить на принадлежность
    соответствия паттерну `ecsaddo`
    
    Description
    ---
    Функция `isecsaddo` проверяет соответствует ли переданный аргумент паттерну
    `ecsaddo`
    
    Return
    ---
    `True` / `False`
    """
    try:
        if not isinstance(ecsaddo, dict):
            raise EcsaddoStructureError(
                "ecsaddo должен иметь тип dict" 
            )
        if (
            "status" not in ecsaddo or 
            ecsaddo["status"] not in ("ok", "error", "ex")
        ):
            raise EcsaddoStructureError(
                "ecsaddo должен иметь ключ 'status' с одним из возможных "
                "значений ('ok', 'error', 'ex)"
            )
        if "action" not in ecsaddo:
            raise EcsaddoStructureError(
                "ecsaddo должен иметь обязательный ключ 'action' с значением: "
                "любая python строка"
            )
        if ( 
            "data" not in ecsaddo or 
            not isinstance(ecsaddo["data"], dict)
        ):
            raise EcsaddoStructureError(
                "ecsaddo должен иметь обязательный ключ 'data', значением "
                "которого должен быть python тип dict"
            )
        if "description" not in ecsaddo["data"]:
            raise EcsaddoStructureError(
                "ecsaddo должен иметь обязательный ключ 'data' -> 'description' "
                "значением которого может быть любая python строка"
            )
        return True
    except Exception as ex:
        # trc = str(traceback.format_exception(ex))
        return False
    
