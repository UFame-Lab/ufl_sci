import json
import datetime

from sci.lib.common_utils import json_safe


def save_log(
    logfilePath: str, 
    ecsaddo_data: dict,
    date: bool = True,
    timezone: int = 0 # 0 - UTC, 3 - UTC+3
):
    """
    Arguments
    ---
    - `logfilePath: str` - Путь к `log` журналу
    - `ecsaddo_data: dict` - `ecsaddo` которую нужно залогировать.
    - `date: bool = True` - Нужно ли добавлять поле с датой сохранения лога.
    - `timezone: int = 0`- 0 - UTC, 3 - UTC+3 и тд.
    
    Description
    ---
    Функция `save_log` отвечает за логирование `ecsaddo` в указаный `log` журнал.
    
    Return
    ---
    `True` - успешное сохранение.
    `False` - не успешное сохранение.
    """
    try:
        if date:
            current_time = datetime.datetime.fromisoformat(
                datetime.datetime.now(
                    datetime.timezone(
                        datetime.timedelta(
                            hours=timezone
                        )
                    )
                ).strftime("%Y-%m-%d %H:%M:%S")
            )
            timestamp = int(current_time.timestamp())
            timestring = str(current_time)
            add_date = {
                "timezone": timezone,
                "timestamp": timestamp,
                "timestring": timestring
            }
            ecsaddo_data["data"].setdefault(
                "date",
                add_date
            )
        data_json: str = json.dumps(ecsaddo_data, default=json_safe)
        with open(logfilePath, "a+", encoding='utf-8') as file:
            file.write(data_json + "\n")
        return True
    except Exception as ex:
        return False
