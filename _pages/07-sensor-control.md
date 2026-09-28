---
layout: default
title: 7. BME280 Sensor Control
permalink: /workshop/sensor-control/
parent: SiLA Raspberry Pi Workshop
nav_order: 7
---

# Add BME280 Sensor Control

In this step, we will connect the Raspberry Pi's BME280 Sensor API to the SiLA Feature.

## 1. Read the Sensor state from the Raspberry Pi

First, we need a method in the protocol that can retrieve the sensor data and return it as a python object.

Open:

```text
src/unitelabs/raspberrypi_connector/io/raspberrypi_connector_protocol.py
```


Add the required imports:

```diff
import json
+from dataclasses import dataclass

from unitelabs.bus import HTTPCommand, Protocol, create_tcp_connection
from unitelabs.bus.commands.http_command import HTTPResponse, _Method

...
```

Add the data object to carry the sensor data:

```diff
...
from unitelabs.bus.commands.http_command import HTTPResponse, _Method


+@dataclass
+class SensorData:
+    """BME280 sensor readings from the Raspberry Pi device."""
+
+    humidity: float
+    pressure: float
+    temperature: float


class RaspberrypiConnectorProtocol(Protocol):
...
```

Add the `get_sensor_data` function to the `RaspberrypiConnectorProtocol`:
```python
async def get_sensor_data(self) -> SensorData:
    """Get data of sensor."""
    command = HTTPCommand(path="/bme280")
    response: HTTPResponse = await self.execute(command)
    if not response.payload:
        raise Exception
    state = json.loads(response.payload)
    return SensorData(
        humidity=state["humidity"],
        pressure=state["pressure"],
        temperature=state["temperature"],
    )
```

1. The method creates an HTTP request to the Raspberry Pi’s /bme280 endpoint.
2. The command is then sent through the existing connection.
3. The Raspberry Pi returns the BME280 data in the response payload.
4. The response is decoded from JSON
5. The response is converted to the `SensorData` object and returned.

## 2. Expose the Data Points as SiLA Properties

Now that the protocol can read the BME280 state, we can expose it through the RaspberryPiController feature. Instead of returning the entire SensorData object, each value is returned separately because SiLA properties represent independent data points.

Each property is observable, allowing clients to subscribe to updates and monitor the sensor readings over time. 

Open:

```text
src/unitelabs/raspberrypi_connector/features/raspberry_controller/raspberry_controller.py
```

Add the following observable properties to the `RaspberryPiController`:

### Temperature

```python
@sila.ObservableProperty(name="Temperature", identifier="Temperature")
async def get_temperature(self) -> sila.Stream[float]:
    """
    Read temperature.

    Returns:
        Temperature: Environmental temperature in celcius.
    """
    while True:
        data = await self._protocol.get_sensor_data()
        yield data.temperature
        await asyncio.sleep(1)
```

### Humidity

```python
@sila.ObservableProperty(name="Humidity", identifier="Humidity")
async def get_humidity(self) -> sila.Stream[float]:
    """
    Read humidity.

    Returns:
        Humidity: Environmental humidity.
    """
    while True:
        data = await self._protocol.get_sensor_data()
        yield data.humidity
        await asyncio.sleep(1)
```

### Pressure

```python
@sila.ObservableProperty(name="Pressure", identifier="Pressure")
async def get_pressure(self) -> sila.Stream[float]:
    """
    Read pressure.

    Returns:
        Pressure: Environmental pressure.
    """
    while True:
        data = await self._protocol.get_sensor_data()
        yield data.pressure
        await asyncio.sleep(1)
```

## 3. Test setting the LED state

Restart the connector:
```bash
ctrl+C
```

```bash
uv run connector start --app unitelabs.raspberrypi_connector:create_app
```

The connector will now expose the `Temperature`, `Humidity` and `Pressure`   properties through the `RaspberryPiController` feature.