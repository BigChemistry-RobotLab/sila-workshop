import atexit
import logging
import threading

from flask import Flask, jsonify, request
from gpiozero import LED
import bme280
import smbus2
from waitress import serve

HOST = "0.0.0.0"
PORT = 5000

LED_PIN = 17
BME280_ADDRESS = 0x76
I2C_BUS = 1

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
hardware_lock = threading.Lock()

led = None
i2c_bus = None
bme280_calibration = None
bme280_error = None


def initialize_led():
    global led

    try:
        led = LED(LED_PIN)
        led.off()
        logger.info("LED initialized on GPIO %s", LED_PIN)
    except Exception:
        led = None
        logger.exception("LED unavailable; continuing without it")


def initialize_bme280():
    """Try to initialize the sensor without preventing server startup."""
    global i2c_bus, bme280_calibration, bme280_error

    # Close any previous bus before retrying.
    if i2c_bus is not None:
        try:
            i2c_bus.close()
        except Exception:
            logger.exception("Error closing previous I2C bus")

    i2c_bus = None
    bme280_calibration = None

    bus = None
    try:
        bus = smbus2.SMBus(I2C_BUS)

        # This is the API used by the common RPi bme280 package.
        calibration = bme280.load_calibration_params(
            bus, BME280_ADDRESS
        )

        i2c_bus = bus
        bme280_calibration = calibration
        bme280_error = None
        logger.info(
            "BME280 initialized at address 0x%02X", BME280_ADDRESS
        )
        return True

    except Exception as exc:
        bme280_error = str(exc)
        logger.warning("BME280 unavailable: %s", exc)

        if bus is not None:
            try:
                bus.close()
            except Exception:
                logger.exception("Could not close I2C bus")

        return False


def cleanup():
    logger.info("Cleaning up hardware")

    if led is not None:
        try:
            led.off()
            led.close()
        except Exception:
            logger.exception("Could not close LED")

    if i2c_bus is not None:
        try:
            i2c_bus.close()
        except Exception:
            logger.exception("Could not close I2C bus")


initialize_led()
initialize_bme280()
atexit.register(cleanup)


@app.before_request
def log_request():
    logger.info(
        "HTTP %s %s from %s Host=%s",
        request.method,
        request.path,
        request.remote_addr,
        request.host,
    )


@app.route("/led", methods=["GET"])
def get_led():
    if led is None:
        return jsonify({"error": "LED is unavailable"}), 503

    with hardware_lock:
        state = int(led.is_lit)

    return jsonify({"state": state})


@app.route("/led", methods=["POST"])
def set_led():
    if led is None:
        return jsonify({"error": "LED is unavailable"}), 503

    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({"error": "Request body must be a JSON object."}), 400

    state = data.get("state")
    if type(state) is not int or state not in (0, 1):
        return jsonify({"error": "'state' must be 1 or 0."}), 400

    with hardware_lock:
        if state:
            led.on()
        else:
            led.off()

        actual_state = int(led.is_lit)

    return jsonify({"state": actual_state})


@app.route("/bme280", methods=["GET"])
def get_bme280():
    global i2c_bus, bme280_calibration

    with hardware_lock:
        # Retry initialization if the sensor was unavailable at startup.
        if i2c_bus is None or bme280_calibration is None:
            if not initialize_bme280():
                return jsonify({
                    "error": "BME280 sensor is unavailable",
                    "detail": bme280_error,
                }), 503

        try:
            reading = bme280.sample(
                i2c_bus,
                BME280_ADDRESS,
                bme280_calibration,
            )

            return jsonify({
                "temperature": round(reading.temperature, 2),
                "humidity": round(reading.humidity, 2),
                "pressure": round(reading.pressure, 2),
            })

        except Exception as exc:
            logger.exception("Could not read BME280")
            return jsonify({
                "error": "Could not read BME280 sensor",
                "detail": str(exc),
            }), 503


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "ok",
        "led": "available" if led is not None else "unavailable",
        "bme280": "available" if i2c_bus is not None else "unavailable",
    })


@app.errorhandler(400)
def handle_bad_request(error):
    return jsonify({"error": "Bad request"}), 400


@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(405)
def handle_method_not_allowed(error):
    return jsonify({"error": "HTTP method not allowed"}), 405


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    logger.exception("Unhandled server error")
    return jsonify({"error": "Internal server error"}), 500


if __name__ == "__main__":
    logger.info("Starting Raspberry Pi server on %s:%s", HOST, PORT)
    serve(
        app,
        host=HOST,
        port=PORT,
        threads=4,
        channel_timeout=120,
    )
