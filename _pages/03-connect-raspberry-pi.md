---
layout: default
title: 3. Connecting to the Raspberry Pi
permalink: /workshop/connect-raspberry-pi/
parent: SiLA Raspberry Pi Workshop
nav_order: 3
---

# Connect the Connector to the Raspberry Pi

In this step, we will configure the connector to communicate with the Raspberry Pi.

The Raspberry Pi exposes an HTTP API. Instead of hard-coding the Raspberry Pi's address and port in the communication protocol, we will make them part of the connector configuration.

## 1. Remove the hard-coded host and port

Open:

```text
src/unitelabs/raspberrypi_connector/io/raspberrypi_connector_protocol.py
```

The generated protocol currently contains a hard-coded host and port:

```diff
...

class RaspberrypiConnectorProtocol(Protocol):
    """Underlying communication protocol for raspberrypi-connector."""

    def __init__(self, **kwargs):
-        kwargs["host"] = "localhost"  # FIXME: set device host
-        kwargs["port"] = 80  # FIXME: set device port
        super().__init__(create_tcp_connection, **kwargs)
```

Remove these two assignments.

The `host` and `port` will instead be passed to the protocol through `kwargs`. This keeps the protocol independent of a specific device and allows the connection settings to be provided by the connector configuration.

The SiLA connector framework will use these values when establishing the connection to the device.

## 2. Add the Raspberry Pi connection settings to the connector configuration

Open:

```text
src/unitelabs/raspberrypi_connector/__init__.py
```

The connector configuration is defined by the `RaspberrypiConnectorConfig` dataclass.

Add `host` and `port` to the configuration:

```diff
...

@dataclasses.dataclass
class RaspberrypiConnectorConfig(ConnectorBaseConfig):
    """Configuration for the raspberrypi-connector."""

+    "Address of the Raspberry Pi"
+    host: str = "raspberrypi.local"

+    "Port on which the server is running"
+    port: int = 5000

    sila_server: SiLAServerConfig = dataclasses.field(
        default_factory=lambda: SiLAServerConfig(
            name="raspberrypi-connector",
            type="Example",
            description=(
                """
                A connector for the raspberrypi-connector built with the UniteLabs CDK.
                """
            ),
            version=str(__version__),
            vendor_url="https://unitelabs.io/",
        )
    )


async def create_app(
    config: RaspberrypiConnectorConfig,
) -> collections.abc.AsyncGenerator[Connector, None]:
    """Create the connector application."""

    app = Connector(config)

-    protocol = RaspberrypiConnectorProtocol()
+    protocol = RaspberrypiConnectorProtocol(
+        host=config.host,
+        port=config.port,
+    )
    await protocol.open()

    yield app

    protocol.close()
```

The connector now gets the Raspberry Pi's address and port from its configuration.

This allows the connection settings to be changed through `config.json` without modifying the connector's source code.

## 3. Regenerate the configuration file

The new configuration fields need to be included in the connector's configuration file.

Run:

```bash
uv run config create --app unitelabs.raspberrypi_connector:create_app --force
```

This generates a `config.json` file in the root of the project.

The file now contains the `host` and `port` settings that were added to `RaspberrypiConnectorConfig`.

You should see these values:

```json
{
    "host": "raspberrypi.local",
    "port": 5000
}
```

{: .note }
> If the Raspberry Pi is running at a different address or port, update these values in `config.json`.

## 4. Start the connector

Start the connector with:

```bash
uv run connector start --app unitelabs.raspberrypi_connector:create_app
```

The connector will initialize, establish a connection to the Raspberry Pi, and start its SiLA server.

If the connection is successful, you should see log messages similar to:

```text
2026-09-22T13:18:08.570332Z [info     ] Starting application           [unitelabs.cdk.main]
2026-09-22T13:18:09.861838Z [info     ] Connection made to transport <_ProactorSocketTransport ...> [unitelabs.bus.protocols.protocol]
2026-09-22T13:18:09.861838Z [info     ] Validating device connection.  [unitelabs.bus.protocols.protocol]
2026-09-22T13:18:09.861838Z [info     ] We're connected to the correct device. [unitelabs.bus.protocols.protocol]
2026-09-22T13:18:09.861838Z [info     ] Starting Server...             [sila.server.server]
2026-09-22T13:18:09.906037Z [info     ] Server bound to '0.0.0.0:60509'. [sila.server.server]
2026-09-22T13:18:11.161379Z [info     ] Registering service 'raspberrypi-connector' (...) [sila.server.discovery]
```
