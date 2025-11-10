def get_Qualifier_DO_Bytes ():
    output ='''
        def _get_qualifier_do_bytes():
            # Qualifier DO.  These outputs from block are connected to PLC
            (self.qualifier_do_8_byte1, self.qualifier_do_8_byte2) = (
                qualifier_do_8(
                    self.inByte1,
                    self.inByte2,
                    short_circuit_actuator_trigger_as_bits,
                    self.PinBased,
                    self.PortBased,
                    self.Compact,
                )
            )'''

   # output = '''
   #     def _get_qualifier_do_bytes():
   #         # Qualifier DO.  These outputs from block are connected to PLC
   #         (self.qualifier_dos.qualifier_do_8_byte1, self.qualifier_dos.qualifier_do_8_byte2) = (
   #             qualifier_do_8(
   #                 self.plc_is.inByte1,
   #                 self.plc_is.inByte2,
   #                 short_circuit_actuator_trigger_as_bits,
   #                 self.parameters.PinBased,
   #                 self.parameters.PortBased,
   #                 self.parameters.Compact,
   #             )
   #         )'''

    return output