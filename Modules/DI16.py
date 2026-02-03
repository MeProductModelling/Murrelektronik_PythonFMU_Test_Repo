import numpy as np

def digital_inputs_16(bits, pinBased, portBased, compact):
    """
    This module converts 16 sensor inputs into bytes based on the selected mapping configuration.

    :param bits: A list of 16 digital sensor values (0 or 1).
    :param pinBased: Boolean flag for pin-based mapping mode.
    :param portBased: Boolean flag for port-based mapping mode.
    :param compact: Boolean flag for compact mapping mode.
    :return: A numpy array of two bytes [byte1, byte2] to be connected to a PLC.
    """

    if len(bits) != 16:
        raise ValueError("### Error Code: 5 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Inputs Library ### "
                         "### Error Description: Input must be 16 bits (0s and 1s). ###     ")

    # Ensure only one mapping type is selected
    if sum([pinBased, portBased, compact]) != 1:
        raise ValueError("### Error Code: 3 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Inputs Library ### "
                         "### Error Description: Two or more types of IO mappings are selected or none are selected. ### "
                         "### Error Resolve: Change one of the pinBased or portBased or compactBased Parameter to True and remaining value to False ###")

    byte1 = 0
    byte2 = 0

    bits = np.array(bits).astype(int)  # Ensure it's a NumPy array of ints

    if pinBased:
        # Extract odd and even indexed bits
        # Example logic: byte1 gets bits[1,3,5,7,9,11,13,15], byte2 gets bits[0,2,4,6,8,10,12,14]
        bitsforbyte1 = bits[1::2]  # Odd indices
        bitsforbyte2 = bits[::2]   # Even indices

        for i, bit in enumerate(bitsforbyte1):
            if bit not in (0, 1):
                raise ValueError("### Error Code: 4 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Inputs Library ### "
                         "### Error Description: Input values must be either 0 or 1 ###     ")
            byte1 |= bit << (7 - i)

        for i, bit in enumerate(bitsforbyte2):
            if bit not in (0, 1):
                raise ValueError("### Error Code: 4 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Inputs Library ### "
                         "### Error Description: Input values must be either 0 or 1 ###     ")
            byte2 |= bit << (7 - i)

    elif portBased:
        # Swap pairs like original, now extended to 16 bits
        # Pair-wise swap: [1,0, 3,2, 5,4, ..., 15,14]
        bits_swapped = bits.copy()
        for i in range(0, 16, 2):
            bits_swapped[i], bits_swapped[i+1] = bits[i+1], bits[i]

        for i in range(8):
            bit = bits_swapped[i]
            if bit not in (0, 1):
                raise ValueError("### Error Code: 4 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Inputs Library ### "
                         "### Error Description: Input values must be either 0 or 1 ###     ")
            byte1 |= bit << (7 - i)

        for i in range(8, 16):
            bit = bits_swapped[i]
            if bit not in (0, 1):
                raise ValueError("### Error Code: 4 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Inputs Library ### "
                         "### Error Description: Input values must be either 0 or 1 ###     ")
            byte2 |= bit << (15 - i)

    elif compact:
        # Same shuffle logic as port-based
        bits_swapped = bits.copy()
        for i in range(0, 16, 2):
            bits_swapped[i], bits_swapped[i+1] = bits[i+1], bits[i]

        # Compact mode puts everything into byte1 and byte2 as-is
        for i in range(8):
            bit = bits_swapped[i]
            if bit not in (0, 1):
                raise ValueError("### Error Code: 4 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Inputs Library ### "
                         "### Error Description: Input values must be either 0 or 1 ###     ")
            byte1 |= bit << (7 - i)

        for i in range(8, 16):
            bit = bits_swapped[i]
            if bit not in (0, 1):
                raise ValueError("### Error Code: 4 ### "
                         "### Error Device: Murrelektronik_Module_MVK ### "
                         "### Error Location: 16 Digital Inputs Library ### "
                         "### Error Description: Input values must be either 0 or 1 ###     ")
            byte2 |= bit << (15 - i)

    return np.array([byte1, byte2])
