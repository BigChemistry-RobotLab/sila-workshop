---
layout: default
title: 4. Create and Register Feature
permalink: /workshop/create-feature/
parent: SiLA Raspberry Pi Workshop
nav_order: 4
---

# Create and Register a Feature

A **SiLA Feature** defines the functionality that the connector exposes to SiLA clients. The feature acts as the public API of the connector, while the Raspberry Pi protocol is responsible for communicating with the physical device through the built-in omnibus.

![sila-connector-architecture](/assets/images/sila_connector_arch.png)

{: .note }
> This diagram shows multiple feature implementations because a single SiLA connector can register multiple features.
> The user determines how commands and properties are divided between these features. However, it is recommended to organize features according to the instrument’s functionality. For example, one feature for measurement and another for sample transport.

## 1. Create the Feature Implementation

Create the following file:

```text
src/unitelabs/raspberrypi_connector/features/raspberry_controller/raspberry_controller.py
```

Add the following code:

```python
from unitelabs.cdk import sila

from unitelabs.raspberrypi_connector.io.raspberrypi_connector_protocol import (
    RaspberrypiConnectorProtocol,
)


class RaspberryPiController(sila.Feature):
    """Controller for the Raspberry Pi."""

    def __init__(self, protocol: RaspberrypiConnectorProtocol):
        super().__init__(
            originator="bigchemistry",
            category="demo",
            version="1.0",
            maturity_level="Draft",
        )

        self._protocol = protocol
```

The `RaspberryPiController` class inherits from `sila.Feature`. This makes it a SiLA feature that can be registered with the connector. The feature is initialized with several pieces of metadata that describe the organization or prject that created the feature, the category of feature, the version and the maturity level.

The `RaspberrypiConnectorProtocol` is passed into the feature through the constructor. This is an example of [dependency injection](https://www.geeksforgeeks.org/system-design/dependency-injectiondi-design-pattern/). The feature does not create or configure the connection to the Raspberry Pi itself. Instead, the already-configured protocol is provided to it by another class.

## 2. Register the Feature with the connector

Creating the feature class is not enough. It must also be registered with the connector application so that the SiLA server knows that the feature exists.

Open:

```text
src/unitelabs/raspberrypi_connector/__init__.py
```

First, import the new feature:

```diff
import dataclasses
import collections.abc
from importlib.metadata import version

from unitelabs.cdk import Connector, ConnectorBaseConfig, SiLAServerConfig

+from .features.raspberry_controller.raspberry_controller import RaspberryPiController
from .io.raspberrypi_connector_protocol import RaspberrypiConnectorProtocol

...
```

Then register the feature after opening the protocol connection:

```diff
...

async def create_app(
    config: RaspberrypiConnectorConfig,
) -> collections.abc.AsyncGenerator[Connector, None]:
    """Create the connector application."""

    app = Connector(config)

    protocol = RaspberrypiConnectorProtocol(
        host=config.host,
        port=config.port,
    )
    await protocol.open()

+    app.register(RaspberryPiController(protocol=protocol))

    yield app

    protocol.close()
```

Once registered, the connector can expose the feature through its SiLA server.
