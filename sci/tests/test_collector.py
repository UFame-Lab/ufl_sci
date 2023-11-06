import unittest

from sci.tests.interface_local_aq import (
    test_SCI_node_only_local_with_await_response_interface_local_aq,
    test_SCI_node_only_local_without_await_response_interface_local_aq,
    test_SCI_node_shadow_with_await_response_interface_local_aq,
    test_SCI_node_shadow_without_await_response_interface_local_aq,
    test_SCI_node_standart_with_await_response_interface_local_aq,
    test_SCI_node_standart_without_await_response_interface_local_aq
)
from sci.tests.interface_local_rq import (
    test_SCI_node_shadow_with_await_response_interface_local_rq,
    test_SCI_node_shadow_without_awaot_response_interface_local_rq,
    test_SCI_node_standart_with_await_resposne_interface_local_rq,
    test_SCI_node_standart_without_await_response_interfcae_local_rq
)
from sci.tests.interface_remote_rq import (
    test_SCI_node_shadow_with_await_response_interface_remote_rq,
    test_SCI_node_shadow_without_await_response_interface_remote_rq,
    test_SCI_node_standart_with_await_response_interface_remote_rq,
    test_SCI_node_standart_without_await_response_interface_remote_rq
)
from sci.tests.interface_ws import (
    test_SCI_node_shadow_with_await_response_interface_ws,
    test_SCI_node_shadow_without_await_response_interface_ws,
    test_SCI_node_standart_with_await_response_interface_ws,
    test_SCI_node_standart_without_await_response_interface_ws
)
from sci.tests.interface_ws.interface_ws_use_wsBridgeBroker_via_local_rq import (
    test_SCI_node_shadow_with_await_response_interface_ws_use_wsBridgeBroker_via_local_rq,
    test_SCI_node_shadow_without_await_response_interface_ws_use_wsBridgeBroker_via_local_rq,
    test_SCI_node_standart_with_await_response_interface_ws_use_wsBridgeBroker_via_local_rq,
    test_SCI_node_standart_without_await_response_interface_ws_use_wsBridgeBroker_via_local_rq,
)
from sci.tests.interface_ws.interface_ws_use_wsBridgeBroker_via_remote_rq import (
    test_SCI_node_shadow_with_await_response_interface_ws_use_wsBridgeBroker_via_remote_rq,
    test_SCI_node_shadow_without_await_resposne_interface_ws_use_wsBridgeBroker_via_remote_rq,
    test_SCI_node_standart_with_await_response_interface_ws_use_wsBridgeBroker_via_remote_rq,
    test_SCI_node_standart_without_await_response_interface_ws_use_wsBridgeBroker_via_remote_rq
)
from sci.apps.nodeLifespanSystemSCIApp.tests import (
    test_NodeLifespanSystemSCIAppContext_Validate
)
from sci.apps.nodeLifespanSystemSCIApp.tests.all_interfaces import (
    test_NodeLifespanSystemSCIApp_all_interfaces
)
from sci.apps.nodeLifespanSystemSCIApp.tests.interface_local_rq import (
    test_NodeLifespanSystemSCIApp_local_rq
)
from sci.apps.nodeLifespanSystemSCIApp.tests.interface_remote_rq import (
    test_NodeLifespanSystemSCIApp_remote_rq,
    test_NodeLifespanSystemSCIApp_remote_rq_use_differents_back_address,
)
from sci.apps.nodeLifespanSystemSCIApp.tests.interface_ws import (
    test_NodeLifespanSystemSCIApp_ws,
    test_NodeLifespanSystemSCIApp_ws_use_wsBridgeBroker_via_local_rq,
    test_NodeLifespanSystemSCIApp_ws_use_wsBridgeBroker_via_remote_rq,
)
from sci.sci_cli.tests import (
    test_EventMessage_Validate_sci_node_only_local_mType_request,
    test_EventMessage_Validate_sci_node_only_local_mType_response,
    test_EventMessage_Validate_sci_node_shadow_mType_request,
    test_EventMessage_Validate_sci_node_shadow_response,
    test_EventMessage_Validate_sci_node_standart_mType_request,
    test_EventMessage_Validate_sci_node_standart_mType_response,
)
from sci.sci_base.tests import (
    test_SCI_SETTINGS_Validate_sci_node_only_local,
    test_SCI_SETTINGS_Validate_sci_node_shadow,
    test_SCI_SETTINGS_Validate_sci_node_standart
)


def load_tests() -> None:
    """
    Total: 1160 tests in 3791.107s
    """
    test_loader = unittest.TestLoader()
    test_suite = unittest.TestSuite()
    test_modules = [
        test_SCI_node_only_local_with_await_response_interface_local_aq, # 24 tests in 24.781s
        test_SCI_node_only_local_without_await_response_interface_local_aq, # 11 tests in 10.346s
        test_SCI_node_shadow_with_await_response_interface_local_aq, # 23 tests in 24.831s
        test_SCI_node_shadow_without_await_response_interface_local_aq, # 10 tests in 8.112s
        test_SCI_node_standart_with_await_response_interface_local_aq, # 23 tests in 24.709s
        test_SCI_node_standart_without_await_response_interface_local_aq, # 10 tests in 8.055s
        ###
        test_SCI_node_shadow_with_await_response_interface_local_rq, # 46 tests in 104.895s
        test_SCI_node_shadow_without_awaot_response_interface_local_rq, # 20 tests in 41.498s
        test_SCI_node_standart_with_await_resposne_interface_local_rq, # 41 tests in 90.297s
        test_SCI_node_standart_without_await_response_interfcae_local_rq, # 20 tests in 36.183s
        ###
        test_SCI_node_shadow_with_await_response_interface_remote_rq, # 46 tests in 109.046s
        test_SCI_node_shadow_without_await_response_interface_remote_rq, # 20 tests in 41.507s
        test_SCI_node_standart_with_await_response_interface_remote_rq, # 41 tests in 90.440s
        test_SCI_node_standart_without_await_response_interface_remote_rq, # 20 tests in 36.265s
        ###
        test_SCI_node_shadow_with_await_response_interface_ws, # 46 tests in 132.580s
        test_SCI_node_shadow_without_await_response_interface_ws, # 20 tests in 55.732s
        test_SCI_node_standart_with_await_response_interface_ws, # 41 tests in 115.372s
        test_SCI_node_standart_without_await_response_interface_ws, # 20 tests in 50.438s
        ###
        test_SCI_node_shadow_with_await_response_interface_ws_use_wsBridgeBroker_via_local_rq, # 32 tests in 154.094s
        test_SCI_node_shadow_without_await_response_interface_ws_use_wsBridgeBroker_via_local_rq, # 20 tests in 85.834s
        test_SCI_node_standart_with_await_response_interface_ws_use_wsBridgeBroker_via_local_rq, # 32 tests in 148.668s
        test_SCI_node_standart_without_await_response_interface_ws_use_wsBridgeBroker_via_local_rq, # 20 tests in 80.490s
        ###
        test_SCI_node_shadow_with_await_response_interface_ws_use_wsBridgeBroker_via_remote_rq, # 32 tests in 154.200s
        test_SCI_node_shadow_without_await_resposne_interface_ws_use_wsBridgeBroker_via_remote_rq, # 20 tests in 85.881s
        test_SCI_node_standart_with_await_response_interface_ws_use_wsBridgeBroker_via_remote_rq, # 32 tests in 148.789s
        test_SCI_node_standart_without_await_response_interface_ws_use_wsBridgeBroker_via_remote_rq, # 20 tests in 80.601s
        ###
        test_NodeLifespanSystemSCIAppContext_Validate, # 59 tests in 0.005s
        ###
        test_NodeLifespanSystemSCIApp_all_interfaces, # 1 tests in 65.112s
        ###
        test_NodeLifespanSystemSCIApp_local_rq, # 8 tests in 289.471s
        ###
        test_NodeLifespanSystemSCIApp_remote_rq, # Ran 8 tests in 289.469s
        test_NodeLifespanSystemSCIApp_remote_rq_use_differents_back_address, # Ran 12 tests in 13.359s
        ###
        test_NodeLifespanSystemSCIApp_ws, # 8 tests in 289.471s
        test_NodeLifespanSystemSCIApp_ws_use_wsBridgeBroker_via_local_rq, # 12 tests in 449.795s
        test_NodeLifespanSystemSCIApp_ws_use_wsBridgeBroker_via_remote_rq, # 12 tests in 449.810s
        ###
        test_EventMessage_Validate_sci_node_only_local_mType_request, # 60 tests in 0.006s
        test_EventMessage_Validate_sci_node_only_local_mType_response, # 42 tests in 0.003s
        test_EventMessage_Validate_sci_node_shadow_mType_request, # 0 tests in 0.000s
        test_EventMessage_Validate_sci_node_shadow_response, # 0 tests in 0.000s
        test_EventMessage_Validate_sci_node_standart_mType_request, # 65 tests in 0.005s
        test_EventMessage_Validate_sci_node_standart_mType_response, # 47 tests in 0.003s
        ###
        test_SCI_SETTINGS_Validate_sci_node_only_local, # 27 tests in 0.002s
        test_SCI_SETTINGS_Validate_sci_node_shadow, # 38 tests in 0.002s
        test_SCI_SETTINGS_Validate_sci_node_standart, # 71 tests in 0.005s
    ]
    for t_module in test_modules:
        package_tests = test_loader.loadTestsFromModule(t_module)
        test_suite.addTests(package_tests)
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)


if __name__ == "__main__":
    load_tests()
