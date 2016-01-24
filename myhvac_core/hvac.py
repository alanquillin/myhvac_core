import cfg
import logging
import RPi.GPIO as GPIO
import system_state as state

LOG = logging.getLogger(__name__)

io_opts = [
    cfg.IntOpt('green_pin_out', required=True, help='GPIO BCM pin output number for green (FAN) wire'),
    cfg.IntOpt('green_pin_in', required=True, help='GPIO BCM pin input number for green (FAN) wire'),
    cfg.IntOpt('white_pin_out', required=True, help='GPIO BCM pin output number for white (HEAT) wire'),
    cfg.IntOpt('white_pin_in', required=True, help='GPIO BCM pin input number for white (HEAT) wire'),
    cfg.IntOpt('yellow_pin_out', required=True, help='GPIO BCM pin output number for yellow (COOL) wire'),
    cfg.IntOpt('yellow_pin_in', required=True, help='GPIO BCM pin input number for yellow (COOL) wire')
]

cfg.CONF.register_opts(io_opts, 'io')


def init_gpio():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(cfg.CONF.io.green_pin_out, GPIO.OUT)
    GPIO.setup(cfg.CONF.io.green_pin_in, GPIO.IN)
    GPIO.setup(cfg.CONF.io.white_pin_out, GPIO.OUT)
    GPIO.setup(cfg.CONF.io.white_pin_in, GPIO.IN)
    GPIO.setup(cfg.CONF.io.yellow_pin_out, GPIO.OUT)
    GPIO.setup(cfg.CONF.io.yellow_pin_in, GPIO.IN)


def get_system_state():
    is_green_on = GPIO.input(cfg.CONF.io.green_pin_in)
    is_white_on = GPIO.input(cfg.CONF.io.green_pin_in)
    is_yellow_on = GPIO.input(cfg.CONF.io.green_pin_in)

    if is_green_on and is_white_on and is_yellow_on:
        return state.COOL

    if is_green_on and is_white_on and not is_yellow_on:
        return state.HEAT

    if is_green_on and not is_white_on and not is_yellow_on:
        return state.FAN_ONLY

    return state.UNKNOWN


def heat_on():
    GPIO.output(cfg.CONF.io.green_pin_out, True)
    GPIO.output(cfg.CONF.io.white_pin_out, True)
    GPIO.output(cfg.CONF.io.yellow_pin_out, False)


def cool_on():
    GPIO.output(cfg.CONF.io.green_pin_out, True)
    GPIO.output(cfg.CONF.io.white_pin_out, True)
    GPIO.output(cfg.CONF.io.yellow_pin_out, True)


def fan_only():
    GPIO.output(cfg.CONF.io.green_pin_out, True)
    GPIO.output(cfg.CONF.io.white_pin_out, False)
    GPIO.output(cfg.CONF.io.yellow_pin_out, False)
