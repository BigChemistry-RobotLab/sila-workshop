# Create and Register new Feature

1. Add the file `src\unitelabs\raspberrypi_connector\features\raspberry_controller\raspberry_controller.py`.

This file defines the API that the SiLA connector will expose. The Raspberry PI protocol is injected into this file. And some parameters are set through the `super.__init__()` function.

```diff
+from unitelabs.cdk import sila
+
+from unitelabs.raspberrypi_connector.io.raspberrypi_connector_protocol import RaspberrypiConnectorProtocol
+
+
+class RaspberryPiController(sila.Feature):
+    """Controller for the Raspberry PI."""
+
+    # Inject the Raspberry PI protocol 
+    def __init__(self, protocol: RaspberrypiConnectorProtocol):
+        super().__init__(
+            originator="bigchemistry",
+            category="demo",
+            version="1.0",
+            maturity_level="Draft",
+        )
+        self._protocol = protocol
```

2. Register the feature in `src\unitelabs\raspberrypi_connector\__init__.py`:

Register the feature in the app, so that it can automatically expose it as a feature.

```diff
import dataclasses
import collections.abc
from importlib.metadata import version

from unitelabs.cdk import Connector, ConnectorBaseConfig, SiLAServerConfig

+ from .features.raspberry_controller.raspberry_controller import RaspberryPiController
from .io.raspberrypi_connector_protocol import RaspberrypiConnectorProtocol

...

async def create_app(config: RaspberrypiConnectorConfig) -> collections.abc.AsyncGenerator[Connector, None]:
    """Create the connector application."""

    app = Connector(config)

    protocol = RaspberrypiConnectorProtocol(host=config.host, port=config.port)
    await protocol.open()

+    app.register(RaspberryPiController(protocol=protocol))

    yield app

    protocol.close()

```