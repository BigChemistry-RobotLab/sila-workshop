# Connecting the SiLA connector to the Raspberry PI

1. Open `src\unitelabs\raspberrypi_connector\io\raspberrypi_connector_protocol.py` and remove setting the of the host and port. This is because these variables will be caried through the kwargs. These arguments are passed into the `create_tcp_connection` method, and the SiLA connector will handle all network configuration and handling in the background.

```diff
...

class RaspberrypiConnectorProtocol(Protocol):
    """Underlying communication protocol for raspberrypi-connector."""

    def __init__(self, **kwargs):
-        kwargs["host"] = "localhost"  # FIXME: set device host
-        kwargs["port"] = 80  # FIXME: set device port
        super().__init__(create_tcp_connection, **kwargs)
```

2. Open `src\unitelabs\raspberrypi_connector\__init__.py` and add host and port to the configuration.
```diff
...

@dataclasses.dataclass
class RaspberrypiConnectorConfig(ConnectorBaseConfig):
    """Configuration for the raspberrypi-connector."""

+    "Address of the raspberry pi"
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


async def create_app(config: RaspberrypiConnectorConfig) -> collections.abc.AsyncGenerator[Connector, None]:
    """Create the connector application."""

    app = Connector(config)

-    protocol = RaspberrypiConnectorProtocol()
+    protocol = RaspberrypiConnectorProtocol(host=config.host, port=config.port)
    await protocol.open()

    yield app

    protocol.close()
```

3. Generate config file. A file `config.json` will be created in the root of the project containing the new parameters and default values that were added in the `RaspberrypiConnectorConfig` class.
```bash
uv run config create --app unitelabs.raspberrypi_connector:create_app
```

4. Start the connector:
```bash
uv run connector start --app unitelabs.raspberrypi_connector:create_app
```

```bash
2026-09-22T13:18:08.570332Z [info     ] Starting application           [unitelabs.cdk.main]
2026-09-22T13:18:09.861838Z [info     ] Connection made to transport <_ProactorSocketTransport fd=1348 read=<_OverlappedFuture pending cb=[_ProactorReadPipeTransport._loop_reading()]>>. [unitelabs.bus.protocols.protocol]
2026-09-22T13:18:09.861838Z [info     ] Validating device connection.  [unitelabs.bus.protocols.protocol]
2026-09-22T13:18:09.861838Z [info     ] We're connected to the correct device. [unitelabs.bus.protocols.protocol]
2026-09-22T13:18:09.861838Z [info     ] Starting Server...             [sila.server.server]
2026-09-22T13:18:09.906037Z [info     ] Server bound to '0.0.0.0:60509'. [sila.server.server]
2026-09-22T13:18:11.161379Z [info     ] Registering service 'raspberrypi-connector' (771d28b0-6f91-4080-9333-30d6b48e537e) [sila.server.discovery]
```