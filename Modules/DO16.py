import numpy as np

def digital_outputs_16(byte1, byte2, pinBased, portBased, compact):
    """
    Converts two input bytes into 16 actuator control bits based on mapping configuration.

    :param byte1: First byte (0–255) from PLC
    :param byte2: Second byte (0–255) from PLC
    :param pinBased: Boolean flag for pin-based mapping
    :param portBased: Boolean flag for port-based mapping
    :param compact: Boolean flag for compact mapping
    :return: List of 16 actuator control bits (0 or 1)
    """

    if not (0 <= byte1 <= 255 and 0 <= byte2 <= 255):
        raise ValueError("### Error Code: 7 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Outputs Library ### "
                         "### Error Description: Inputs from PLC to FMU must be bytes in the range 0–255. ###     ")

    if sum([pinBased, portBased, compact]) != 1:
        raise ValueError("### Error Code: 8 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Outputs Library ### "
                         "### Error Description: Change one of the pinBased or portBased or compactBased Parameter to True and remaining value to False. ###     ")

    # Convert both bytes into bit arrays (MSB to LSB)
    bits1 = [(byte1 >> i) & 1 for i in range(7, -1, -1)]
    bits2 = [(byte2 >> i) & 1 for i in range(7, -1, -1)]

    bits = [0] * 16

    if pinBased:
        # Interleave bits2 and bits1
        # bits = [b2_0, b1_0, b2_1, b1_1, ..., b2_7, b1_7]
        for i in range(8):
            bits[2 * i] = bits2[i]
            bits[2 * i + 1] = bits1[i]

    elif portBased:
        # Concatenate bits1 and bits2, then swap pairs [1,0,3,2,...]
        combined = bits1 + bits2
        for i in range(0, 16, 2):
            bits[i], bits[i + 1] = combined[i + 1], combined[i]

    elif compact:
        # Same as portBased, but using only byte1 and byte2 as "compact data"
        combined = bits1 + bits2
        for i in range(0, 16, 2):
            bits[i], bits[i + 1] = combined[i + 1], combined[i]

    return bits
