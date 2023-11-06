from sci.lib.patterns import create_ecsaddo
from sci.network.utils import create_response_payload
from sci.sci_typing import ecsaddo


class PingPong_Handler:

    async def ping_pong(
        self, 
        EventMessage: dict
    ) -> ecsaddo:
        """
        Description
        ---
        ActionHandler обработки ping-pong запроса.
        
        Return
        ---
        {
            "status": "ok",
            "action": "",
            "data": {
                "description" : "",
                "response_payload": SCI_ResposnePayload, # status_code 200
            }
        }
        """
        response_payload = (
            create_response_payload({}, 200)
        )
        return create_ecsaddo(
            "ok",
            response_payload = response_payload
        )


class BasicActionHandlers(PingPong_Handler):
    """
    `BasicActionHandlers` включает в себя все стандартные классы `ActionHandler`
    """
    pass