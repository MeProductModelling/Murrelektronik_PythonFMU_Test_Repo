import numpy as np


def qualifier_di_8(
    short_circuit_sensor_trigger_as_bits, pinBased, portBased, compact
):  # This function is tested
    """

    :param short_circuit_sensor_trigger_as_bits: These bits are from User Interface of the Simulation Module to trigger errors and check the behaviour of the model.
    :param pinBased: Parameter of the Simulation Module basically describes the pin mapping.
    :param portBased: Parameter of the Simulation Module basically describes the port mapping.
    :param compact: Parameter of the Simulation Module basically describes the complex mapping
    :return: Returns the QualifierDI values and shows where exactly the error is coming from.
    """

    qualifier_di_byte1 = 0
    qualifier_di_byte2 = 0

    # This folowing section is to convert bits to bytes...i.e sensor values to a bit..
    if len(short_circuit_sensor_trigger_as_bits) == 8:
        # Combine the bits into a single byte using bitwise operations

        if (
            pinBased == True and portBased == False and compact == False
        ):  # This loop is tested
            dummyarray = [0, 0, 0, 0]
            bitsforbyte1 = np.concatenate(
                (dummyarray, short_circuit_sensor_trigger_as_bits[1::2])
            )  # odd bits from position[7,5,3,1]
            bitsforbyte2 = np.concatenate(
                (dummyarray, short_circuit_sensor_trigger_as_bits[::2])
            )  # even bits from position[6,4,2,0]
            for i, bit in enumerate(bitsforbyte1):
                if bit not in (0, 1):
                    raise ValueError("### Error Code: MVK_17 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: Qualifier DI Library ### "
                         "### Error Description: Internal error of Qualifier DIs Each bit must be either 0 or 1. ### "
                         "### Error Resolve: Contact FMU supplier for resolving the problem ###     ")
                qualifier_di_byte1 |= bit << (
                    7 - i
                )  # Shift the bit to its correct position

            for i, bit in enumerate(bitsforbyte2):
                if bit not in (0, 1):
                    raise ValueError("### Error Code: MVK_18 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: Qualifier DI Library ### "
                         "### Error Description: Internal error of Qualifier DIs Each bit must be either 0 or 1. ### "
                         "### Error Resolve: Contact FMU supplier for resolving the problem ###     ")
                qualifier_di_byte2 |= bit << (
                    7 - i
                )  # Shift the bit to its correct position

        elif (
            pinBased == False and portBased == True and compact == False
        ):  # This loop is tested

            bits = short_circuit_sensor_trigger_as_bits
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
            for j, bit in enumerate(bits):
                if bit not in (0, 1):
                    raise ValueError("### Error Code: MVK_19 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: Qualifier DI Library ### "
                         "### Error Description: Internal error of Qualifier DIs Each bit must be either 0 or 1. ### "
                         "### Error Resolve: Contact FMU supplier for resolving the problem ###     ")
                qualifier_di_byte2 |= bit << (
                    7 - j
                )  # Shift the bit to its correct position

        elif (
            pinBased == False and portBased == False and compact == True
        ):  # This loop is also tested

            bits = short_circuit_sensor_trigger_as_bits
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
            for k, bit in enumerate(bits):
                if bit not in (0, 1):
                    raise ValueError("### Error Code: MVK_20 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: Qualifier DI Library ### "
                         "### Error Description: Internal error of Qualifier DIs Each bit must be either 0 or 1. ### "
                         "### Error Resolve: Contact FMU supplier for resolving the problem ###     ")
                qualifier_di_byte1 |= bit << (
                    7 - k
                )  # Shift the bit to its correct position

        else:
            raise ValueError("### Error Code: MVK_21 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: Qualifier DI Library ### "
                         "### Error Description: Change one of the pinBased or portBased or compactBased Parameter to True and remaining value to False. ###     "
               )

    else:
        raise ValueError("### Error Code: MVK_22 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: Qualifier DI Library ### "
                         "### Error Description: Sensor short circuit value shall be between 0 -255. ###     ")

    bytes = np.array([qualifier_di_byte1, qualifier_di_byte2])

    return bytes
