def get_System_State (qualifier_dis, qualifier_dos):

    output = ""

    if  qualifier_dis == True and qualifier_dos == True:
        output ='''
        def _get_system_state_bytes():
            # System State. These outputs from block are connected to PLC
            (
                self.system_state_byte_1,
                self.system_state_byte_2,
                self.system_state_byte_3,
                self.system_state_byte_4,
            ) = System_State(
                self.qualifier_di_8_byte1,
                self.qualifier_di_8_byte2,
                self.qualifier_do_8_byte1,
                self.qualifier_do_8_byte2,
                False,
                False,
                self.Sensor_Voltage,
                self.Actuator_Voltage,
            )'''

       # output = '''
       # def _get_system_state_bytes():
       #     # System State. These outputs from block are connected to PLC
       #     (
       #         self.system_state.system_state_byte_1,
       #         self.system_state.system_state_byte_2,
       #         self.system_state.system_state_byte_3,
       #         self.system_state.system_state_byte_4,
       #     ) = System_State(
       #         self.qualifier_dis.qualifier_di_8_byte1,
       #         self.qualifier_dis.qualifier_di_8_byte2,
       #         self.qualifier_dos.qualifier_do_8_byte1,
       #         self.qualifier_dos.qualifier_do_8_byte2,
       #         False,
       #         False,
       #         self.user_interface_is.Sensor_Voltage,
       #         self.user_interface_is.Actuator_Voltage,
       #     )'''

    elif qualifier_dis == True and qualifier_dos == False:
        output = '''
        def _get_system_state_bytes():
            # System State. These outputs from block are connected to PLC
            (
                self.system_state_byte_1,
                self.system_state_byte_2,
                self.system_state_byte_3,
                self.system_state_byte_4,
            ) = System_State(
                self.qualifier_di_8_byte1,
                self.qualifier_di_8_byte2,
                0,
                0,
                False,
                False,
                self.Sensor_Voltage,
                self.Actuator_Voltage,
            )'''

       # output = '''
       # def _get_system_state_bytes():
       #     # System State. These outputs from block are connected to PLC
       #     (
       #         self.system_state.system_state_byte_1,
       #         self.system_state.system_state_byte_2,
       #         self.system_state.system_state_byte_3,
       #         self.system_state.system_state_byte_4,
       #     ) = System_State(
       #         self.qualifier_dis.qualifier_di_8_byte1,
       #         self.qualifier_dis.qualifier_di_8_byte2,
       #         0,
       #         0,
       #         False,
       #         False,
       #         self.user_interface_is.Sensor_Voltage,
       #         self.user_interface_is.Actuator_Voltage,
       #     )'''

    elif qualifier_dis == False and qualifier_dos == True:

        output = '''
        def _get_system_state_bytes():
            # System State. These outputs from block are connected to PLC
            (
                self.system_state_byte_1,
                self.system_state_byte_2,
                self.system_state_byte_3,
                self.system_state_byte_4,
            ) = System_State(
                0,
                0,
                self.qualifier_do_8_byte1,
                self.qualifier_do_8_byte2,
                False,
                False,
                self.Sensor_Voltage,
                self.Actuator_Voltage,
            )'''

       # output = '''
       # def _get_system_state_bytes():
       #     # System State. These outputs from block are connected to PLC
       #     (
       #         self.system_state.system_state_byte_1,
       #         self.system_state.system_state_byte_2,
       #         self.system_state.system_state_byte_3,
       #         self.system_state.system_state_byte_4,
       #     ) = System_State(
       #         0,
       #         0,
       #         self.qualifier_dos.qualifier_do_8_byte1,
       #         self.qualifier_dos.qualifier_do_8_byte2,
       #         False,
       #         False,
       #         self.user_interface_is.Sensor_Voltage,
       #         self.user_interface_is.Actuator_Voltage,
       #     )'''

    return output