from MainDeviceScripts.Algorithm_support.getOutBitsDef import get_out_bits_to_PLC_from_SMBlock
from MainDeviceScripts.Algorithm_support.getOutBytesDef import get_out_bytes_to_PLC_from_SMBlock
from MainDeviceScripts.Algorithm_support.getQualifierDIBytes import get_Qualifier_DI_Bytes
from MainDeviceScripts.Algorithm_support.getQualifierDOBytes import get_Qualifier_DO_Bytes
from MainDeviceScripts.Algorithm_support.getSystemState import get_System_State
from MainDeviceScripts.Algorithm_support.ledConfigSCInitiation import led_SC_Initialisation


def generate_algorithm(di_pins, do_pins, generate_qualifier_dis, generate_qualifier_dos):

    defstep = '''
    def do_step(self, current_time, step_size):
        """
        This is the function that is called at every simulation step.
        """
    '''

    # Get output bytes to PLC from Simulation block
    #This based on the number of inputs bits of the simulation block
    getOutBytes =  get_out_bytes_to_PLC_from_SMBlock(di_pins)

    # Get output bits to PLC from Simulation block
    # This based on the number of output bits of the PLC from block
    getOutBits = get_out_bits_to_PLC_from_SMBlock(do_pins)

    #  Get Qualifier DI bytes from the SM block
    getQualifierDI = ""
    if generate_qualifier_dis:
        getQualifierDI = get_Qualifier_DI_Bytes()

    #  Get Qualifier DO bytes from the SM block
    getQualifierDO =""
    if generate_qualifier_dos:
        getQualifierDO = get_Qualifier_DO_Bytes()

    # Get System State Bytes from SM Block to PLC
    getSystemState =""
    if generate_qualifier_dis and not generate_qualifier_dos:
        getSystemState = get_System_State(True, False)
    elif not generate_qualifier_dis and generate_qualifier_dos:
        getSystemState = get_System_State(False, True)
    elif  generate_qualifier_dis and generate_qualifier_dos:
        getSystemState = get_System_State(True, True)

    # Initialis the LED and Short-Circuit (SC) data
    getLEDandSCData = led_SC_Initialisation(di_pins, do_pins, generate_qualifier_dis, generate_qualifier_dos)

    output_code = defstep + "\n" + getOutBytes + "\n" + getOutBits + "\n" + getQualifierDI + "\n" + getQualifierDO + "\n" + getSystemState + "\n" + getLEDandSCData

    return output_code