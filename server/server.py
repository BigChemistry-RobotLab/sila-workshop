import atexit
import logging
import threading

from flask import Flask, jsonify, request
from gpiozero import LED
import bme280
import smbus2
from waitress import serve


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

HOST = "0.0.0.0"
PORT = 5000

LED_PIN = 17
BME280_ADDRESS = 0x76
I2C_BUS = 1


# -----------------------------------------------------------------------------
# Logging
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Application and hardware setup
# -----------------------------------------------------------------------------

app = Flask(__name__)

led = LED(LED_PIN)
led.off()

i2c_bus = smbus2.SMBus(I2C_BUS)
bme280.load_calibration_params(i2c_bus, BME280_ADDRESS)

# Protect hardware access if multiple HTTP requests arrive simultaneously.
hardware_lock = threading.Lock()

# -----------------------------------------------------------------------------
# Cleanup
# -----------------------------------------------------------------------------

def cleanup() -> None:
    logger.info("Cleaning up hardware")

    try:
        led.off()
        led.close()
    except Exception:
        logger.exception("Could not close LED")

    try:
        i2c_bus.close()
    except Exception:
        logger.exception("Could not close I2C bus")


atexit.register(cleanup)


# -----------------------------------------------------------------------------
# Request logging
# -----------------------------------------------------------------------------

@app.before_request
def log_request() -> None:
    logger.info(
        "HTTP %s %s from %s Host=%s",
        request.method,
        request.path,
        request.remote_addr,
        request.host,
    )

# -----------------------------------------------------------------------------
# LED endpoints
# -----------------------------------------------------------------------------

@app.route("/led", methods=["GET"])
def get_led():
    """Return the current LED state."""

    with hardware_lock:
        state = int(led.is_lit)

    return jsonify({
        "state": state,
    })


@app.route("/led", methods=["POST"])
def set_led():
    """
    Set the LED state.

    Expected JSON:

        {"state": 1}

    or:

        {"state": 0}
    """

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Request body must be a JSON object.",
        }), 400

    if "state" not in data:
        return jsonify({
            "error": "Missing 'state'. Use 1 for on or 0 for off.",
        }), 400

    state = data["state"]

    if state not in (0, 1):
        return jsonify({
            "error": "'state' must be 1 or 0.",
        }), 400

    with hardware_lock:
        if state == 1:
            led.on()
        else:
            led.off()

        actual_state = int(led.is_lit)

    return jsonify({
        "state": actual_state,
    })

# -----------------------------------------------------------------------------
# BME280 endpoint
# -----------------------------------------------------------------------------

@app.route("/bme280", methods=["GET"])
def get_bme280():
    """Return the current BME280 readings."""

    with hardware_lock:
        reading = bme280.sample(
            i2c_bus,
            BME280_ADDRESS,
        )

    return jsonify({
        "temperature": round(reading.temperature, 2),
        "humidity": round(reading.humidity, 2),
        "pressure": round(reading.pressure, 2),
    })

# -----------------------------------------------------------------------------
# Error handlers
# -----------------------------------------------------------------------------

@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({
        "error": "Bad request",
    }), 400


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({
        "error": "Endpoint not found",
    }), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    return jsonify({
        "error": "HTTP method not allowed",
    }), 405


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    logger.exception("Unhandled server error")

    return jsonify({
        "error": "Internal server error",
    }), 500

# -----------------------------------------------------------------------------
# Start server
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    logger.info("Starting Raspberry Pi server on %s:%s", HOST, PORT)

    serve(
        app,
        host=HOST,
        port=PORT,
        threads=4,
        channel_timeout=120,
    )
