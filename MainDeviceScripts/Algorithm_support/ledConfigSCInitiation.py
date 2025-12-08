def led_SC_Initialisation(di_pins, do_pins, qualifier_dis, qualifier_dos):

    if len(di_pins) > 0 and len(do_pins) > 0:
        initialise_di_pins = "        _get_out_bytes()"
        initialise_do_pins = "        _get_out_bits()"
    elif len(di_pins) > 0 and len(do_pins) == 0:
        initialise_di_pins = "        _get_out_bytes()"
        initialise_do_pins = " "
    elif len(di_pins) == 0 and len(do_pins) > 0:
        initialise_di_pins = " "
        initialise_do_pins = "        _get_out_bits()"

    output = "\n\n" + initialise_di_pins + "\n" + initialise_do_pins + "\n"'''

        # LED Config behaviour
        (
            self.LED_Green,
            self.LED_Red,
            self.LED_Off,
        ) = led(self.Sensor_Voltage, current_time)

        # Short circuit bits for sensor and actuator
        short_circuit_result = short_circuit_trigger(
            self.sensor_short_circuit_trigger_value,
            self.actuator_short_circuit_trigger_value,
        )
        [
            short_circuit_actuator_trigger_as_bits,
            short_circuit_sensor_trigger_as_bits,
        ] = short_circuit_result''' + "\n" + "\n"

   # output = "\n\n" + initialise_di_pins + "\n" + initialise_do_pins + "\n"'''
#
   #     # LED Config behaviour
   #     (
   #         self.user_interface_os.LED_Green,
   #         self.user_interface_os.LED_Red,
   #         self.user_interface_os.LED_Off,
   #     ) = led(self.user_interface_is.Sensor_Voltage, current_time)
#
   #     # Short circuit bits for sensor and actuator
   #     short_circuit_result = short_circuit_trigger(
   #         self.user_interface_is.sensor_short_circuit_trigger_value,
   #         self.user_interface_is.actuator_short_circuit_trigger_value,
   #     )
   #     [
   #         short_circuit_actuator_trigger_as_bits,
   #         short_circuit_sensor_trigger_as_bits,
   #     ] = short_circuit_result''' + "\n" + "\n"

    if qualifier_dis and qualifier_dos:
        output += "        _get_qualifier_di_bytes()" + "\n"+ "\n" +"        _get_qualifier_do_bytes()"+ "\n"+ "\n"
    elif qualifier_dis:
        output += "        _get_qualifier_di_bytes()"+ "\n"+ "\n"
    elif qualifier_dos:
        output += "        _get_qualifier_do_bytes()"+ "\n"+ "\n"



    output +=  "        _get_system_state_bytes()"+ "\n"+ "\n"

    output +=  "        return True"

    return output