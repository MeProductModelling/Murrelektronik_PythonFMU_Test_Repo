def get_out_bytes_to_PLC_from_SMBlock (inputs):


    output_code= ""

    #inputs = di_pins
    if 8>= len(inputs) > 0:
        out_1 = '''
        def _get_out_bytes():
            # This following section is to convert bits to bytes...i.e sensor values to a bit.
            # DI 8. These Inputs are from Sensor which are usually connected in simulation tool.
            self.plc_ios.outByte1, self.plc_ios.outByte2 = digital_inputs(
                np.array(
                    [
                    '''+ "\n"
        out_2 = ""
        counter = 0
        for pins in inputs:
            counter += 1
            if pins != 0 and pins != "0" and counter != len(inputs):
                out_2 += "\t" +"\t"+"\t"+"\t"+ "\t"+"self.sensor_inputs." + pins + "," + "\n"

            if pins != 0 and pins != "0" and counter == len(inputs):
                out_2 += "\t" + "\t" + "\t" + "\t" + "\t" + "self.sensor_inputs." + pins + "\n"

        out_3 = '''
                ]
            ),
            self.parameters.PinBased,
            self.parameters.PortBased,
            self.parameters.Compact,
        )
        '''

        output_code = out_1+out_2+out_3
    elif 16 >= len(inputs) > 8:
        out_1 = '''
        def _get_out_bytes():
            # This following section is to convert bits to bytes...i.e sensor values to a bit.
            # DI 16. These Inputs are from Sensor which are usually connected in simulation tool.
            self.plc_ios.outByte1, self.plc_ios.outByte2 = digital_inputs_16(
                np.array(
                    [
                    ''' + "\n"
        out_2 = ""
        counter = 0
        for pins in inputs:
            counter += 1
            if pins != 0 and pins != "0" and counter != len(inputs):
                out_2 +=  "\t" + "\t" + "\t" + "\t" + "\t" + "self.sensor_inputs."  + pins +  "," +"\n"
            if pins != 0 and pins != "0" and counter == len(inputs):
                out_2 += "\t" + "\t" + "\t" + "\t" + "\t" + "self.sensor_inputs." + pins + "\n"

        out_3 = '''
                ]
            ),
            self.parameters.PinBased,
            self.parameters.PortBased,
            self.parameters.Compact,
        )
        '''

        output_code = out_1 + out_2 + out_3


    return output_code
