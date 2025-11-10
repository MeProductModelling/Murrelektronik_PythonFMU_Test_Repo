import numpy as np


def leds(sensor_voltage, actuator_voltage, current_time):
    """
    This method returns the LED status of the simulation module.

    :param sensor_voltage: Sensor Voltage that is regulated by user to check the behaviour of model.
    :param actuator_voltage: Actuator Voltage that is regulated by user to check the behaviour of model.
    :param current_time: Time at which the simulation steps are determined.
    :return: Returns the array of LED status of the device.
    """

    led_Config = []
    led_bus_run = []
    led_link_act = []
    led_link_act = []
    led_st = []
    led_power_ua = [0, 0]  # [green, red] at the moment led is off
    led_power_us = [0, 0]  # [green, red] at the moment led is off

    # led_power_us
    if 17.5 <= sensor_voltage <= 30:
        led_power_us = [1, 0]
    elif 12.5 <= sensor_voltage <= 17:
        led_power_us = [0, 1]

    elif 7.5 <= sensor_voltage <= 12:
        frequency = 1
        # Generate sine wave
        sine_wave = np.sin(2 * np.pi * frequency * current_time)
        # Convert to binary (0 and 1)
        if sine_wave > 0:
            led_power_us = [0, 1]
        else:
            led_power_us = [0, 0]
    elif sensor_voltage >= 30.5:
        frequency = 5
        # Generate sine wave
        sine_wave = np.sin(2 * np.pi * frequency * current_time)
        # Convert to binary (0 and 1)
        if sine_wave > 0:
            led_power_us = [0, 1]
        else:
            led_power_us = [0, 0]
    else:
        led_power_us = [0, 0]

    # led_power_ua
    if 17.5 <= actuator_voltage <= 30:
        led_power_ua = [1, 0]
    elif 12.5 <= actuator_voltage <= 17:
        led_power_ua = [0, 1]

    elif actuator_voltage <= 12:
        frequency = 1
        # Generate sine wave
        sine_wave = np.sin(2 * np.pi * frequency * current_time)
        # Convert to binary (0 and 1)
        if sine_wave > 0:
            led_power_ua = [0, 1]
        else:
            led_power_ua = [0, 0]
    elif actuator_voltage >= 30.5:
        frequency = 5
        # Generate sine wave
        sine_wave = np.sin(2 * np.pi * frequency * current_time)
        # Convert to binary (0 and 1)
        if sine_wave > 0:
            led_power_ua = [0, 1]
        else:
            led_power_ua = [0, 0]
    else:
        led_power_ua = [0, 0]

    leds = np.array([led_power_ua, led_power_us])
    return leds
