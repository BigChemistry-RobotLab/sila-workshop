---
layout: default
title: 1. The Instrument
permalink: /workshop/instrument/
parent: SiLA Raspberry Pi Workshop
nav_order: 1
---

# Raspberry PI Instrument

![Wiring Diagram]({{ '/assets/images/circuit_image.png' | relative_url }})

The device is a Raspberry Pi 4 connected to:
* An LED with a 220 Ω resistor
* A BME280 sensor for temperature, humidity, and pressure

On the Raspberry Pi there is a server through which you can control the LED and get the sensor data. This server can be called through an HTTP API.

Make sure the Pi is connected to your computer through a USB-C cable.

## 1. Check the Raspberry Pi connection

{: .note }
> Windows users need to install a special driver from the Raspberry Pi Github page to enable their computer to connect to the Raspberry Pi. 
> You can download the driver from [here](https://github.com/raspberrypi/rpi-usb-gadget/releases/download/v1.0.6/rpi-usb-gadget-driver-setup.exe). 
> Run the installer and follow the instructions.

First, check that the Raspberry Pi is reachable from your computer:

```bash
ping raspberrypi.local
```

If this does not work try using the IP Address: 

```bash
ping 10.12.194.1
```
If `raspberrypi.local` does not work, but the IP address (`10.12.194.1`) works, substitute `raspberrypi.local` for `10.12.194.1` in all subsequent commands.


## 2. Call the server

The Raspberry Pi runs an HTTP server on port `5000`.

### Get LED state

```bash
curl http://raspberrypi.local:5000/led
```

Response (0=off, 1=on):

```json
{
  "state": 0
}
```

## Set LED state

**Turn the LED on:**

```bash
curl -X POST http://raspberrypi.local:5000/led -H "Content-Type: application/json" -d "{\"state\":1}"
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