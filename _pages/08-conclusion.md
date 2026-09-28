---
layout: default
title: 8. Conclusion
permalink: /workshop/conclusion/
parent: SiLA Raspberry Pi Workshop
nav_order: 8
---

# Conclusion

You have now built a small but realistic example of an instrument interface by writing a SiLA connector for an Raspberry PI instrument with an LED and a BME280 sensor.

## What you learned

Throughout this workshop, you worked through the full flow of instrument integration:

- Creating a new connector
- Connecting to a device over HTTP using the built in omnibus
- structuring device functionality in protocol and feature layers
- exposing capabilities through SiLA properties and commands

This pattern can be applied to any instrument in a self driving lab that exposes a supported API. And a standardized software layer makes it usable in a cleaner, more interoperable way.

## Extra Challenges *(Optional)*

- add a blinking pattern command for the LED
- average temperature readings over a 10-second window
- add an automatic warning when pressure or humidity is out of range

Back to the [home page](/).
