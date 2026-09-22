from flask import Flask, request, jsonify
from gpiozero import LED
import bme280
import smbus2

# -------------------------
# Configuration
# -------------------------

LED_PIN = 17
BME280_ADDRESS = 0x76

# -------------------------
# Setup
# -------------------------

app = Flask(__name__)

# LED
led = LED(LED_PIN)
led.off()

# I2C / BME280
bus = smbus2.SMBus(1)
bme280.load_calibration_params(bus, BME280_ADDRESS)


# -------------------------
# LED endpoints
# -------------------------

@app.route("/led", methods=["POST"])
def set_led():
    """
    POST /led
    JSON body:
        {"state": 1}  -> LED on
        {"state": 0}  -> LED off
    """

    data = request.get_json()

    if not data or "state" not in data:
        return jsonify({
            "error": "Missing 'state'. Use 1 for on or 0 for off."
        }), 400

    state = data["state"]

    if state == 1:
        led.on()
    elif state == 0:
        led.off()
    else:
        return jsonify({
            "error": "'state' must be 1 or 0."
        }), 400

    return jsonify({
        "state": int(led.is_lit)
    })


@app.route("/led", methods=["GET"])
def get_led():
    """
    GET /led
    Returns the current LED state.
    """

    return jsonify({
        "state": int(led.is_lit)
    })


# -------------------------
# BME280 endpoint
# -------------------------

@app.route("/bme280", methods=["GET"])
def get_bme280():
    """
    GET /bme280
    Returns the current sensor readings.
    """

    data = bme280.sample(bus, BME280_ADDRESS)

    return jsonify({
        "temperature_c": round(data.temperature, 2),
        "humidity_percent": round(data.humidity, 2),
        "pressure_hpa": round(data.pressure, 2)
    })


# -------------------------
# Run server
# -------------------------

if __name__ == "__main__":
    # Listen on all interfaces so you can access it from your PC
    app.run(host="0.0.0.0", port=5000)
