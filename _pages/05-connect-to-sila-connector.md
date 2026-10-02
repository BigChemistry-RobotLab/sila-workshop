---
layout: default
title: 5. Inspect the SiLA Connector
permalink: /workshop/connect-to-sila-connector/
parent: SiLA Raspberry Pi Workshop
nav_order: 5
---

# Inspect the SiLA Connector

Now that the connector is connected to the Raspberry Pi and the `RaspberryPiController` feature has been registered, we can connect to the SiLA server and inspect the available functionality. This can be done through the SiLA Browser, which is a graphical client that can discover SiLA servers on the network and interact with their Features.

At this stage, the feature does not contain any custom commands yet. Therefore, the SiLA Browser can be used mainly to verify that the connector is running and discoverable. 

## 1. Download SiLA Browser

Download [SiLA Browser](https://gitlab.com/unitelabs/sila2/sila-browser/#stable-releases) for your platform.

## 2. Start the SiLA Browser

Open SiLA Browser.

The connector should appear in the list of available SiLA servers.

![available SiLA Browsers](/assets/images/sila_browser_home.png)

Select:

```text
raspberrypi-connector
```

## 3. Inspect the available Features

After selecting `raspberrypi-connector`, SiLA Browser displays the features exposed by the connector.

The connector already exposes some functionality provided by the SiLA framework. For example, the `SiLAService` feature provides information about the SiLA server.

The `SiLAService` feature can be used to inspect information such as the server identity and the features available on the server.

## 4. Inspect the Raspberry Pi Feature

You should also see the feature that we created in the previous step:

```text
RaspberryPiController
```

{: .highlight }
> At the moment, this feature does not expose any custom commands or properties. This is expected. 
> In the previous step, we created and registered the feature, but we have not yet defined any SiLA commands or properties for it.
