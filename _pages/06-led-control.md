---
layout: default
title: 6. LED Control Logic
permalink: /led-control/
---


# Get LED State Logic

## 1. Add `is_led_on` function to the `src\unitelabs\raspberrypi_connector\io\raspberrypi_connector_protocol.py`:

This function first prepares a get request to be sent to the `/led`. Then reads the state from the payload in the response and converts the 0 or 1 into a boolean value True or False.

```diff
from unitelabs.bus import Protocol, create_tcp_connection
+from unitelabs.bus import HTTPCommand
+from unitelabs.bus.commands.http_command import HTTPResponse
+import json


class RaspberrypiConnectorProtocol(Protocol):
    """Underlying communication protocol for raspberrypi-connector."""

    def __init__(self, **kwargs):
        super().__init__(create_tcp_connection, **kwargs)

+    async def is_led_on(self) -> bool:
+        """Check whether the LED is currently switched on."""
+        command = HTTPCommand(path="/led")
+        response: HTTPResponse = await self.execute(command)
+        if not response.payload:
+            raise Exception
+        state = json.loads(response.payload)
+        return bool(state["state"])
```

## 2. Add unobservable property to `src\unitelabs\raspberrypi_connector\features\raspberry_controller\raspberry_controller.py`:

Because all the logic is handled in the protocol the property only has to call and return its value. And describe the propertie's metadata, like the name, identifier, description and return value.

```diff
...

class RaspberryPiController(sila.Feature):
    """Controller for the Raspberry PI."""

    # Inject the Raspberry PI protocol 
    def __init__(self, protocol: RaspberrypiConnectorProtocol):
        super().__init__(
            originator="bigchemistry",
            category="demo",
            version="1.0",
            maturity_level="Draft",
        )
        self._protocol = protocol

+    @sila.UnobservableProperty(name="Is LED on", identifier="IsLedOn")
+    async def open_method(self) -> bool:
+        """
+        Check if LED is on or off.
+
+        Returns:
+            ledOn: True if LED is on, false otherwise
+
+        """
+        return await self._protocol.is_led_on()
```

# Turn LED on/off Logic

## 1. Add `set_led_state` function to the `src\unitelabs\raspberrypi_connector\io\raspberrypi_connector_protocol.py`: