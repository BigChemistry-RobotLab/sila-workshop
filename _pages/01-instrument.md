---
layout: default
title: 1. The Instrument
permalink: /workshop/instrument/
parent: Workshop
---

# Raspberry PI Instrument

![Wiring Diagram](/assets/images/circuit_image.png)

The device is a Raspberry Pi 4 connected to:
* An LED
* A BME280 sensor for temperature, humidity, and pressure

On the Raspoberry PI there is a server through which you can control the LED and get the sensor data. This server can be called through HTTP.

## 1. Check the Raspberry Pi connection

First, check that the Raspberry Pi is reachable from your computer:

```bash
ping raspberrypi.local
```

## 2. Call the server

The Raspberry Pi runs an HTTP server on port `5000`.

### Get LED state

```bash
curl http://raspberrypi.local:5000/led
```

Response:

```json
{
  "state": 0
}
```

- 0 = off
- 1 = on

## Set LED state

**Turn the LED on:**

```bash
curl -X POST http://raspberrypi.local:5000/led -H "Content-Type: application/kson" -d "{\"state\":1}"
```

**Turn the LED off:**

```bash
curl -X POST http://raspberrypi.local:5000/led -H "Content-Type: application/json" -d "{\"state\":0}"
```

## 3. Read sensor data

Get the current measurements from the BME280 sensor:

```bash
curl http://raspberrypi.local:5000/bme280
```

Example response:

```json
{
  "humidity_percent": 56.26,
  "pressure_hpa": 1026.77,
  "temperature_c": 19.55
}
```