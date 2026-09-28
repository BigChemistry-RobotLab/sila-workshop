---
layout: default
title: 6. LED Control
permalink: /workshop/led-control/
parent: SiLA Raspberry Pi Workshop
nav_order: 6
---

# Add LED State and Control Logic

In this step, we will connect the Raspberry Pi's LED API to the SiLA Feature.

## 1. Read the LED state from the Raspberry Pi

First, we need a method in the protocol that can determine whether the LED is currently on or off.

Open:

```text
src/unitelabs/raspberrypi_connector/io/raspberrypi_connector_protocol.py
```

Add the required imports:

```diff
+from unitelabs.bus import HTTPCommand
+import json

-from unitelabs.bus import Protocol, create_tcp_connection
+from unitelabs.bus import HTTPCommand, Protocol, create_tcp_connection
+from unitelabs.bus.commands.http_command import HTTPResponse, _Method

...
```

Then add the `is_led_on` method to `RaspberrypiConnectorProtocol`:

```python
    async def is_led_on(self) -> bool:
        """Check whether the LED is currently switched on."""
        command = HTTPCommand(path="/led")
        response: HTTPResponse = await self.execute(command)
        if not response.payload:
            raise Exception
        state = json.loads(response.payload)
        return bool(state["state"])
```

1. The method creates an HTTP request to the Raspberry Pi's `/led` endpoint. 
2. The command is then sent through the existing connection. 
3. The Raspberry Pi returns the LED state in the response payload. The payload contains a value representing the state of the LED.
4. The response is decoded from JSON.
5. Finally, the numeric state is converted to a Python boolean:

The feature can use this method without needing to know how the Raspberry Pi's HTTP API works.

## 2. Expose the LED state as a SiLA property

Now that the protocol can read the LED state, we can expose it through the `RaspberryPiController` feature.

Open:

```text
src/unitelabs/raspberrypi_connector/features/raspberry_controller/raspberry_controller.py
```

Add the following property to `RaspberryPiController`:

```python
    @sila.UnobservableProperty(name="Is LED on", identifier="IsLedOn")
    async def is_led_on(self) -> bool:
        """
        Check if the LED is on or off.

        Returns:
            True if the LED is on, false otherwise.
        """
        return await self._protocol.is_led_on()
```

The `@sila.UnobservableProperty` decorator tells the SiLA framework that this method should be exposed as a **SiLA property**, and adds metadata like a unique identifier and a human readable name.

## 3. Test the LED state

Start the connector:

```bash
uv run connector start --app unitelabs.raspberrypi_connector:create_app
```

The connector will now expose the `Is LED on` property through the `RaspberryPiController` feature.

---

# Turn the LED On and Off

Next, we will add the ability to change the LED state.

The Raspberry Pi API provides an endpoint that can be used to change the LED state. We will first implement this operation in the protocol and then expose it as a SiLA command.

## 1. Add `set_led_state` to the Raspberry Pi protocol

Open:

```text
src/unitelabs/raspberrypi_connector/io/raspberrypi_connector_protocol.py
```

Add a `set_led_state` method to `RaspberrypiConnectorProtocol`.

The method will be responsible for creating and sending the HTTP request to the Raspberry Pi.

```python
    async def set_led_state(self, led_on: bool) -> None:
        """Turn led on of off."""
        body = {"state": int(led_on)}

        command = HTTPCommand(
            path="/led",
            method=_Method.POST,
            message=json.dumps(body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
        )
        await self.execute(command)
```

## 2. Expose a Command to Set the LED State

Now that the protocol can set the LED state, we can expose it through the `RaspberryPiController` feature.

Open:

```text
src/unitelabs/raspberrypi_connector/features/raspberry_controller/raspberry_controller.py
```

Add the following property to `RaspberryPiController`:

```python
    @sila.UnobservableCommand(name="Set LED state", identifier="SetLedState")
    async def set_led_state(self, led_on: bool) -> None:
        """
        Set state of led.

        Args:
            led_on: True to turn led on, false otherwise
        """

        await self._protocol.set_led_state(led_on=led_on)
```

## 3. Test setting the LED state

Restart the connector:
```bash
ctrl+C
```

```bash
uv run connector start --app unitelabs.raspberrypi_connector:create_app
```


The connector will now expose the `Is LED on` property through the `RaspberryPiController` feature.
