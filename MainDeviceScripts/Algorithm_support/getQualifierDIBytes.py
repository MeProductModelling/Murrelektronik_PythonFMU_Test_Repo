def get_Qualifier_DI_Bytes ():
    output ='''
        def _get_qualifier_di_bytes():
            # Qualifier DI. These outputs from block are connected to PLC
            (self.qualifier_di_8_byte1, self.qualifier_di_8_byte2) = (
                qualifier_di_8(
                    short_circuit_sensor_trigger_as_bits,
                    self.PinBased,
                    self.PortBased,
                    self.Compact,
                )
            )'''

   # output = '''
   #     def _get_qualifier_di_bytes():
   #         # Qualifier DI. These outputs from block are connected to PLC
   #         (self.qualifier_dis.qualifier_di_8_byte1, self.qualifier_dis.qualifier_di_8_byte2) = (
   #             qualifier_di_8(
   #                 short_circuit_sensor_trigger_as_bits,
   #                 self.parameters.PinBased,
   #                 self.parameters.PortBased,
   #                 self.parameters.Compact,
   #             )
   #         )'''

    return output