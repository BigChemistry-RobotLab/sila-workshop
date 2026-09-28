---
layout: default
title: 2. Create SiLA Connector
permalink: /workshop/create-sila-connector/
parent: SiLA Raspberry Pi Workshop
nav_order: 2
---

# Create SiLA Connector

## 1. Generate a new connector project

Open a terminal in the directory where you want to create the connector and run:

```bash
cruft create https://gitlab.com/unitelabs/cdk/connector-factory.git
```

Cruft will ask you several questions about the connector. For this workshop, use the following values:

```text
[1/9] Select your connector name: raspberrypi-connector
[8/9] What type of communication does your device use?: 5
[9/9] Select your environment management tool: 1
```

The important choice here is the communication type. Select option `5` because the Raspberry Pi exposes an HTTP API that the connector will communicate with.

Select UV as the environment management tool (`1`). UV will create and manage the project's Python virtual environment and dependencies.

## 2. Open the project in VS Code

Once Cruft has finished generating the project, change into the new project directory and open it in VS Code:

```bash
cd raspberrypi-connector
```

You should see a project structure similar to:

```text
raspberrypi-connector/
├── src/
│   └── unitelabs/
│       └── raspberrypi_connector/
│           ├── __init__.py
│           ├── __main__.py
│           └── io/
│               ├── __init__.py
│               └── raspberrypi_connector_protocol.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   └── test_version.py
│
├── .gitignore
├── README.md
├── pyproject.toml
└── uv.lock
```

The most important directories are:

* **`src/`** — contains the connector implementation.
* **`src/unitelabs/raspberrypi_connector/`** — contains the Python package for your connector.
* **`src/.../io/`** — contains the device communication layer. Since this connector communicates with the Raspberry Pi over HTTP, this is where the communication implementation will be developed.
* **`tests/`** — contains automated tests for the connector.
* **`pyproject.toml`** — defines the project metadata and Python dependencies.
* **`uv.lock`** — records the exact dependency versions used by the project.

## 3. Activate the Virtual Environment

**Windows**
```bash
.venv/Scripts/Activate
```

**Linux**
```bash
source .venv/bin/activate
```

## 4. Generate the connector configuration

Before starting the connector, generate its default configuration file.

Run:

```bash
uv run config create --app unitelabs.raspberrypi_connector:create_app
```

This creates a `config.json` file in the project root.

The generated configuration provides the default settings required to run the connector.Later this will be customized based on our needs.
