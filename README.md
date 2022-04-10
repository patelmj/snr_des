# Setup
To create python environment:
- conda create -n py3.8 python=3.8
To Activate:  
- conda activate py3.8


packages used
- https://pypi.org/project/uldaq/
    - pip install uldaq
    - prerequisite is to install https://github.com/mccdaq/uldaq and follow any instructions there
- for the motor control download package from https://github.com/ROBOTIS-GIT/DynamixelSDK
- go into the install folder for the dynamaxiel stuff
- go into python folder then do python setup.py install

Make sure to access the serial ports you first need to open access for read and write
- sudo chmod 777 /dev/USBNAME
- For Example, on our linux machine, 
- sudo chmod 777 /dev/ttyUSB0

Other Python Packages
- pandas
    - conda install pandas
- Scipy
    - pip install scipy
- matplotlib
    - pip install matplotlib

# Usage
In each folder is a different set of scripts used throughout testing and design of this project
Folders
- Data  - In here there is all the data that we collected
- Data Collection
    - functs.py  - This is where functions for DAQ system are stored. These are used in the parallelization
    - toForces.py - This is a simple script that takes in straight signals from the DAQ and converts them to Force data. This is kept for sanity's sake
    - w_mass_calibration_step.py - This is a script used for seeing what the transducer sees with the mass of the device ontop of it accounted for. Essentially think of this as zeroing a scale with a beaker on top of it
    - zero_mass_calibration.py - This is a script where the mass of the device ontop of it is not accounted for. This means that you should be seeing the force of gravity on this device.
- Filtering
    - filtering.py - here we try to use a bandpass filter on different files in the data folder, then it will rectify the signal and provide average Torque Calculations
- Motor_control
    - example.py - FIXME
    - function_ns.py - FIXME
    - motor_control.py - FIXME
- Parallelization
    - motor_control.py - 
    - para.py - This is the culmination where the DAQ and motor control work is parallized. This is the main file used for data collection on our wing model system.

# Future Work
- Potentially change the servo to a DC motor to have increased speeds as current flapping is very slow
- 