---
layout: home
title: SiLA Raspberry Pi Workshop
permalink: /
nav_order: 0
---

![SiLA logo](/assets/images/sila_logo.png){: style="height:100px"}
![Big Chemistry logo](/assets/images/logo.svg){: style="height:100px; float: right"}

# SiLA Raspberry Pi Workshop

Build a real laboratory instrument interface from the ground up. Connect a Raspberry Pi to a simple LED and sensor setup, then expose its functionality through a SiLA connector.

This project is designed as a hands-on workshop for learning how to bridge physical hardware to the SiLA ecosystem using Python.

## Why this project?

Modern lab equipment often exposes its capabilities through a device API, not directly through a standardized interface. This workshop shows how to:

- connect to a Raspberry Pi over HTTP
- read sensor data and control an actuator
- wrap device behavior in a reusable SiLA connector
- expose instrument functionality as structured features and commands

## Prerequisites

Before starting, make sure you have the following installed:

 * [Python](https://www.python.org/) 3.10 or newer
 * [UV](https://docs.astral.sh/uv/)
