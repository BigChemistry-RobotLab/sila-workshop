# SiLA Raspberry Pi Workshop

This project is a hands-on workshop for building a simple laboratory instrument interface using a Raspberry Pi and the [SiLA standard](https://sila-standard.com/).

The goal is to connect a physical device to software in a structured and reusable way: read sensor data, control a connected LED, and expose the device functionality through a SiLA connector.

## Built with

This workshop is built using:

- [Jekyll](https://jekyllrb.com/) for the site and workshop documentation
- [Docker Compose](https://docs.docker.com/compose/) for local previewing/development of the site

The example setup combines a Raspberry Pi running a small HTTP API with a Python-based SiLA connector that makes the sensor and actuator functionality available in a standard way.

## Requirements

For this project thsese supplies are required.

1. USB A to C cable
2. Raspberry PI 4, or similar (with the [server](./server/server.py) installed on it)
3. LED
4. BME280 sensor
5. 220 Ω resistor
6. 6 male to female jumper wires

## Installation

Clone the repo
```bash
git clone https://github.com/BigChemistry-RobotLab/sila-workshop.git
```

Move into project directory
```bash
cd sila-workshop
```

## Getting started

To preview the site locally, run:

```bash
docker compose up -d
```

Then open:

```text
http://localhost:4000
```

To refresh the site, run:
```bash
docker compose restart jekyll
```