import numpy as np


def digital_outputs(
    byte1, byte2, pinBased, portBased, compact
):  # This function is tested
    """
    This method returns actuator values by the Simulations models based on Input bytes from PLC, pin mapping parameters.

    :param byte1: Input byte 1 from PLC to control Actuators by the Simulation Module
    :param byte2: Input byte 2 from PLC to control Actuators by the Simulation Module
    :param pinBased:  Parameter of the Simulation Module basically describes the pin mapping.
    :param portBased: Parameter of the Simulation Module basically describes the port mapping.
    :param compact: Parameter of the Simulation Module basically describes the complex mapping.
    :return: This method returns Actuator values as an array of bits 0s and 1s.
    """
    # final bits
    bits = [0, 0, 0, 0, 0, 0, 0, 0]

    # The following section is to convert byte to bits....triggering the actuator values.
    if 0 <= byte1 and byte2 <= 255:

        if (
            pinBased == True and portBased == False and compact == False
        ):  # This loop is tested
            bits1 = [(byte1 >> i) & 1 for i in range(7, -1, -1)]
            bits2 = [(byte2 >> i) & 1 for i in range(7, -1, -1)]
            # Arrange bits according to manual
            bits[0], bits[1], bits[2], bits[3], bits[4], bits[5], bits[6], bits[7] = (
                bits2[0],
                bits1[0],
                bits2[1],
                bits1[1],
                bits2[2],
                bits1[2],
                bits2[3],
                bits1[3],
            )

        elif (
            pinBased == False and portBased == True and compact == False
        ):  # This loop is tested
            bits = [(byte1 >> i) & 1 for i in range(7, -1, -1)]
            # Arrange bits according to manual
            bits[0], bits[1], bits[2], bits[3], bits[4], bits[5], bits[6], bits[7] = (
                bits[1],
                bits[0],
                bits[3],
                bits[2],
                bits[5],
                bits[4],
                bits[7],
                bits[6],
            )

        elif (
            pinBased == False and portBased == False and compact == True
        ):  # This loop is tested
            bits = [(byte1 >> i) & 1 for i in range(7, -1, -1)]
            # Arrange bits according to manual
            bits[0], bits[1], bits[2], bits[3], bits[4], bits[5], bits[6], bits[7] = (
                bits[1],
                bits[0],
                bits[3],
                bits[2],
                bits[5],
                bits[4],
                bits[7],
                bits[6],
            )

        else:
            raise ValueError(
                "Two or more output mapping are selected or noone is selected"
            )

    else:
        raise ValueError("Input must be a single byte (0-255).")

    return bits
