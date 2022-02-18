##Test Script from uldaq

from uldaq import (get_daq_device_inventory, DaqDevice, InterfaceType,
                   AiInputMode, Range, AInFlag)
import csv
file_header = ["c0","c1","c2","c3","c4","c5","c6","c7","c8","c9","c10","c11","c12","c13","c14","c15"]
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
    overall = []
    while True:
        x = input()
        if x != "":
            break
        
        info_row= []
        for channel in range(ai_info.get_num_chans()):
            data = ai_device.a_in(channel, AiInputMode.SINGLE_ENDED,
                              Range.BIP10VOLTS, AInFlag.DEFAULT)
            info_row.append(data)
            print('Channel', channel, 'Data:', data)
        overall.append(info_row)
        

    with open("./dataset.csv",'w') as file:
        writer = csv.writer(file)
        writer.writerow(file_header)
        writer.writerows(overall)

    daq_device.disconnect()
    daq_device.release()

except ULException as e:
    print('\n', e)  # Display any error messages