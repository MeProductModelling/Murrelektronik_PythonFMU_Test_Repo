def get_out_bits_to_PLC_from_SMBlock(outputs):

    output = ""

    if 8>= len(outputs) > 0:
        out_1 = '''
        def _get_out_bits():
            # The following section is to convert byte to bits....triggering the actuator values.
            # DO 8. These Outputs are connected to actuators in simulation tool.
            (''' + "\n"

        out_2 =""
        counter = 0
        for pins in outputs:
            counter += 1
            if pins != 0 and pins != "0" and counter != len(outputs):
                out_2 += "\t" + "\t" + "\t" + "self." + pins + "," + "\n"
            if pins != 0 and pins != "0" and counter == len(outputs):
                out_2 += "\t" + "\t" + "\t" + "self." + pins + "\n"

       # for pins in outputs:
       #     counter += 1
       #     if pins != 0 and pins != "0" and counter != len(outputs):
       #         out_2 +=   "\t" + "\t" + "\t" +"self.actuator_outputs."+ pins + "," + "\n"
       #     if pins != 0 and pins != "0" and counter == len(outputs):
       #         out_2 +=   "\t" + "\t" + "\t" +"self.actuator_outputs."+ pins + "\n"

        out_3 = '''
                  ) = digital_outputs(
                      self.inByte1,
                      self.inByte2,
                      self.PinBased,
                      self.PortBased,
                      self.Compact,
                  )
                  '''

       # out_3 = '''
       #     ) = digital_outputs(
       #         self.plc_is.inByte1,
       #         self.plc_is.inByte2,
       #         self.parameters.PinBased,
       #         self.parameters.PortBased,
       #         self.parameters.Compact,
       #     )
       #     '''
        output = out_1 + out_2 + out_3

    elif 16 >= len(outputs) > 8:
        out_1 = '''
        def _get_out_bits():
            # The following section is to convert byte to bits....triggering the actuator values.
            # DO 16. These Outputs are connected to actuators in simulation tool.
            (
        ''' + "\n"

        out_2 = ""
        counter = 0

        for pins in outputs:
            counter += 1
            if pins != 0 and pins != "0" and counter != len(outputs):
                out_2 += "\t" + "\t" + "\t" + "self." + pins + "," + "\n"
            if pins != 0 and pins != "0" and counter == len(outputs):
                out_2 += "\t" + "\t" + "\t" + "self." + pins + "\n"

       # for pins in outputs:
       #     counter += 1
       #     if pins != 0 and pins != "0" and counter != len(outputs):
       #         out_2 += "\t" + "\t" + "\t" + "self.actuator_outputs." + pins + "," + "\n"
       #     if pins != 0 and pins != "0" and counter == len(outputs):
       #         out_2 += "\t" + "\t" + "\t" + "self.actuator_outputs." + pins  + "\n"

        out_3 = '''
                   ) = digital_outputs_16(
                       self.inByte1,
                       self.inByte2,
                       self.PinBased,
                       self.PortBased,
                       self.Compact,
                   )
           '''

        #out_3 = '''
        #            ) = digital_outputs_16(
        #                self.plc_is.inByte1,
        #                self.plc_is.inByte2,
        #                self.parameters.PinBased,
        #                self.parameters.PortBased,
        #                self.parameters.Compact,
        #            )
        #    '''

        output = out_1 + out_2 + out_3

    return output