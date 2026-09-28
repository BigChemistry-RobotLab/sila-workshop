---
layout: default
title: 8. Extra Challenges
permalink: /workshop/challenges/
parent: SiLA Raspberry Pi Workshop
nav_order: 8
---

## Extra Challenges *(Optional)*

### Average temperature property

Requirements:
- Read temperature every 1 second over 10 seconds

<details markdown="1">
<summary>Answer</summary>

```python
@sila.UnobservableProperty(name="Average Temperature", identifier="AverageTemperature")
async def avg_temp(self) -> float:
    """
    Average temperature over 10 seconds.

    Returns:
        Average: Average temperature.
    """
    temps = []

    for _ in range(10):
        data = await self._protocol.get_sensor_data()
        temps.append(data.temperature)
        await asyncio.sleep(1)

    return sum(temps) / len(temps)
```

</details>

### Add a blinking pattern command for the LED

- Add a `blinks` argument and use its value to determine the number of blink cycles.
- Add a `MinimalInclusive` constraint to require `blinks > 0` ([constraints](https://docs.unitelabs.io/connector-development/tutorial/data-types/#constraints)).
- Add a `MaximalInclusive` constraint to require `blinks <= 10` ([constraints](https://docs.unitelabs.io/connector-development/tutorial/data-types/#constraints)).
- Each blink cycle should take 1 second

<details markdown="1">
<summary>Answer</summary>

```python
import typing


@sila.UnobservableCommand(name="Blink", identifier="Blink")
async def blink(
    self,
    blinks: typing.Annotated[
        int,
        sila.constraints.MinimalExclusive(0),
        sila.constraints.MaximalInclusive(10),
    ],
) -> None:
    """
    Blink the LED.

    Args:
        Blinks: Number of times to blink.
    """
    for _ in range(abs(blinks)):
        await self._protocol.set_led_state(led_on=True)
        await asyncio.sleep(0.5)
        await self._protocol.set_led_state(led_on=False)
        await asyncio.sleep(0.5)
```

</details>