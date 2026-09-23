---
layout: default
title: 2. Create SiLA Connector
permalink: /workshop/create-sila-connector/
parent: Workshop
nav_order: 2
---

# Create SiLA Connector

*Open a terminal in a location where you want the SiLA connector to be created.*

## 1. Generate a new connector project using Cruft and fill in the variables:

```bash 
cruft create https://gitlab.com/unitelabs/cdk/connector-factory.git
```

Fill in the options

```bash
[1/9] Select your connector name: raspberrypi-connector
[8/9] What type of communication does your device use?: 5 # because the server on the Raspberry pi is exposing an http api
[9/9] Select your environment management tool: 1
```

## 2. Open VSCode in the location where you created your connector.

In the IDE the file structure will look like this:

```bash
raspberrypi-connector/
├── .venv/                      # Local Python environment
├── src/                        # Application source code
│   └── unitelabs/
│       └── raspberrypi_connector/
├── tests/                      # Automated tests
│
├── .gitignore                  # Defines what Git should ignore
├── README.md                   # Project overview and instructions
├── pyproject.toml              # Project configuration and dependencies
└── uv.lock                     # Exact dependency versions used by the project
```

## 3. Install the dependencies of the project with UV:

```bash
uv sync --all-extras
```