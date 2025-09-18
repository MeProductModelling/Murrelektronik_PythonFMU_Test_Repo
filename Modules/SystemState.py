import numpy as np


def System_State(
    qualifier_di_byte1,
    qualifier_di_byte2,
    qualifier_do_byte1,
    qualifier_do_byte2,
    no_actuator_supply,
    actuator_warning,
    sensor_voltage,
    actuator_voltage,
):

    # 4 System state bytes # This function is tested.
    """
    This method returns the state of the Simulation Module to PLC based on different parameters.

    :param qualifier_di_byte1: QualiferDI 1 are received form the other module in this section.
    :param qualifier_di_byte2: QualiferDI 2 are received form the other module in this section.
    :param qualifier_do_byte1: QualiferDO 1 are received form the other module in this section.
    :param qualifier_do_byte2: QualiferDO 2 are received form the other module in this section.
    :param no_actuator_supply: A bit that could be triggered from User Interface.
    :param actuator_warning: A bit that could be triggered from User Interface.
    :param sensor_voltage: Value that is triggered from User Interface.
    :param actuator_voltage: Value that is triggered from User Interface.
    :return: Returns the state of the Simulation Model to PLC.
    """
    # System state bytes 1, 2, 3, 4
    ss_byte_1 = 0
    ss_byte_2 = 0
    ss_byte_3 = 0
    ss_byte_4 = 0
    # Byte1 bits
    # bit0 = Sensor undervoltage
    ss_byte1_bit0 = 0
    # bit1 = Actuator undervoltage
    ss_byte1_bit1 = 0
    # bit2 = No actuator supply
    ss_byte1_bit2 = 0
    # bit3 = Reserved
    ss_byte1_bit3 = 0
    # bit4 = Sensor short circuit on at least one channel
    ss_byte1_bit4 = 0
    # bit5 = Actuator short circuit on at least one channel
    ss_byte1_bit5 = 0
    # bit6 = Actuator warning on at least one channel
    ss_byte1_bit6 = 0
    # bit7 = Reserved
    ss_byte1_bit7 = 0

    # Byte2 bits
    # bit0 = Internal communication error
    ss_byte2_bit0 = 0
    # bit1 = Reserved
    ss_byte2_bit1 = 0
    # bit2 = Sensor overvoltage
    ss_byte2_bit2 = 0
    # bit3 = Actuator overvoltage
    ss_byte2_bit3 = 0
    # bit4 = Reserved
    ss_byte2_bit4 = 0
    # bit5 = Reserved
    ss_byte2_bit5 = 0
    # bit6 = Reserved
    ss_byte2_bit6 = 0
    # bit7 = Reserved
    ss_byte2_bit7 = 0

    # The remaining bits in system state are Reserved.

    # Structure bits for System State byte 1
    # ss_byte1_bit0, ss_byte2_bit2 sensor over or under voltage building
    if sensor_voltage <= 23.5:
        ss_byte1_bit0 = 1
    elif sensor_voltage >= 24.5:
        ss_byte2_bit2 = 1
    else:
        ss_byte2_bit2 = 0
        ss_byte1_bit0 = 0

    # ss_byte1_bit1, ss_byte2_bit3 actuator over or under voltage building
    if actuator_voltage <= 23.5:
        ss_byte1_bit1 = 1
    elif actuator_voltage >= 24.5:
        ss_byte2_bit3 = 1
    else:
        ss_byte2_bit3 = 0
        ss_byte1_bit1 = 0

    # ss_byte1_bit4 Qualifer DIs
    if (
        (qualifier_di_byte1 == 15 and qualifier_di_byte2 == 15)
        or (qualifier_di_byte1 == 255 and qualifier_di_byte2 == 0)
        or (qualifier_di_byte1 == 0 and qualifier_di_byte2 == 255)
    ):
        ss_byte1_bit4 = 1
    else:
        ss_byte1_bit4 = 0

    # ss_byte1_bit5 Qualifer DOs
    if (
        (qualifier_do_byte1 == 240 and qualifier_do_byte2 == 240)
        or (qualifier_do_byte1 == 255 and qualifier_do_byte2 == 0)
        or (qualifier_do_byte1 == 0 and qualifier_do_byte2 == 255)
    ):
        ss_byte1_bit5 = 1
    else:
        ss_byte1_bit5 = 0

    # ss_byte1_bit2 no_actuator_supply
    if no_actuator_supply:
        ss_byte1_bit2 = 1
    else:
        ss_byte1_bit2 = 0

    # ss_byte1_bit6 actuator_warning
    if actuator_warning:
        ss_byte1_bit6 = 1
    else:
        ss_byte1_bit6 = 0

    # pack them in to an array as mentioned in manual
    ss_byte_1_bits = [
        ss_byte1_bit0,
        ss_byte1_bit1,
        ss_byte1_bit2,
        ss_byte1_bit3,
        ss_byte1_bit4,
        ss_byte1_bit5,
        ss_byte1_bit6,
        ss_byte1_bit7,
    ]

    ss_byte_2_bits = [
        ss_byte2_bit0,
        ss_byte2_bit1,
        ss_byte2_bit2,
        ss_byte2_bit3,
        ss_byte2_bit4,
        ss_byte2_bit5,
        ss_byte2_bit6,
        ss_byte2_bit7,
    ]

    # convert bits to bytes
    for i, bit in enumerate(ss_byte_1_bits):
        if bit not in (0, 1):
            raise ValueError("Each bit must be either 0 or 1.")
        ss_byte_1 |= bit << (7 - i)  # Shift the bit to its correct position

    for i, bit in enumerate(ss_byte_2_bits):
        if bit not in (0, 1):
            raise ValueError("Each bit must be either 0 or 1.")
        ss_byte_2 |= bit << (7 - i)  # Shift the bit to its correct position

    outBytes = np.array([ss_byte_1, ss_byte_2, ss_byte_3, ss_byte_4])

    return outBytes
