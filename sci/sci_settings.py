import os

from pathlib import Path

BASE_PATH = str(Path(__file__).resolve().parent)

TEST_LOG_FILE_PATH = os.path.join(BASE_PATH, "tests/test.log")

DEBUG = True

SCI_NODE_RQ_PREFIX = "sci_rq_"

SCI_SESSION_PREFIX = "sci_session:"

# Промежуток отправки `ping-pong` запроса в `main` узел.
pp_polling_related_main_nodes_time = 20 # 20
# Промежуток проверки активности `sub` узла
polling_related_sub_nodes_time = 20 # 20
# Максимальное допустимое время не активности `sub` узла.
max_related_sub_nodes_latency_activity = 26 # 26

# Значение должно быть кратно 2.
# Максимальаня задержка перед попыткой отправить запрос аутентификации.
max_delay_btwn_try_reconnection_node = 128

# Задержка между проверками изменений в `SCI_SETTINGS -> "nodes"`
# Пока `transfer_current_node_chain` работает в режиме `startup`
await_startup_delay_to_check_update_nodeChain = 1.5 # 2 ?
# Промежуток через который `transfer_current_node_chain` должен 100% отправить
# данные об `SCI_SETTINGS -> "nodes"` в `wsBridge`, если в течении этого
# промежутка, данные SCI_SETTINGS -> "nodes" не были обновлены и отправлены.
await_delay_to_transfer_nodeChain = 120
# Задержка между проверками изменений в `SCI_SETTINGS -> "nodes"`
# Пока `transfer_current_node_chain` работает обычном режиме.
await_delay_to_check_update_nodeChain = 20
# Длительность работы `transfer_current_node_chain` в "startup" режиме.
startup_activity_time_for_transfer_nodeChain = 6

# Задержка перед тем как текущий `sci node` должен отправить первый запрос
# аутентификации в другой `sci node` по `ws` интерфейсу.
# Эта задержка дает время `sci node` установить websocket подключение с 
# `wsBridge`
wait_delay_for_ws_auth = 0.5
# Задержка перед тем как текущий `sci node` должен отправить первый запрос
# аутентификации в другой `sci node` по `ws` интерфейсу если текущий `sci node`
# не является `wsBridgeBroker`, и он рассчитывает использовать `wsBrodgeBroker`
# какого либо другого узла.
# Эта задержка дает время текущему `sci node` выполнить аутентификацию 
# какого либо `sci node` который сможет выполнять функцию `wsBridgeBroker` 
wait_delay_for_ws_auth_dependent = 2

# timeout ожидания ответа `ping-pong`
await_pp_timeout = 2
# expire_time `ping-pong` запроса.
pp_expire_time = 2