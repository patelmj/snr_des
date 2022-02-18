##Test Script from uldaq

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   AiInputMode, Range, AInFlag)

try:
    # Get a list of available DAQ devices
    devices = get_daq_device_inventory(InterfaceType.USB)
    # Create a DaqDevice Object and connect to the device
    daq_device = DaqDevice(devices[0])
    daq_device.connect()
    # Get AiDevice and AiInfo objects for the analog input subsystem
    ai_device = daq_device.get_ai_device()
    ai_info = ai_device.get_info()

    # Read and display voltage values for all analog input channels
    while True:
        x = input('Anything')
        if x:
            break
        for channel in range(ai_info.get_num_chans()):
            data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED,
                              Range.BIP10VOLTS, AInFlag.DEFAULT)
            print('Channel', channel, 'Data:', data)

    daq_device.disconnect()
    daq_device.release()

except ULException as e:
    print('\n', e)  # Display any error messages