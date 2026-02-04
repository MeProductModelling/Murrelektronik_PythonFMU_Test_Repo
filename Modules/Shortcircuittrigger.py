import numpy as np


def short_circuit_trigger(Sensor_short_circuit_trigger, Actuator_short_circuit_trigger):
    """
    Short circuit trigger could be simulated both in Sensors and actuators.
    This module receives integers as inputs and split bits for sensor and actuators
    The inputs shall be between 255 - 0
    :param Sensor_short_circuit_trigger:  Trigger Value from User Interface
    :param Actuator_short_circuit_trigger: Trigger Values from User Interface
    :return: Converts bytes to bits.
    """

    actuator_bits = []
    sensor_bits = []

    if 0 <= Sensor_short_circuit_trigger <= 255:
        sensor_bits = [
            (Sensor_short_circuit_trigger >> i) & 1 for i in range(7, -1, -1)
        ]
    else:
        raise ValueError("### Error Code: MVK_27 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: Short circuit trigger Library ### "
                         "### Error Description: Sensor short circuit value should be between 0 - 255. ###     ")

    if 0 <= Actuator_short_circuit_trigger <= 255:
        actuator_bits = [
            (Actuator_short_circuit_trigger >> i) & 1 for i in range(7, -1, -1)
        ]
    else:
        raise ValueError("### Error Code: MVK_28 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: Short circuit trigger Library ### "
                         "### Error Description: Actuator short circuit value should be between 0 - 255. ###     ")

    bits_array = np.array([actuator_bits, sensor_bits])
    return bits_array
