To create python environment
    conda create -n py3.8 python=3.8
to Activate 
    conda activate py3.8


packages used
    https://pypi.org/project/uldaq/
        pip install uldaq
        - pre req https://github.com/mccdaq/uldaq
- for the motor control download package from ___
- go into the install folder for the dynamaxiel stuff
- go into python folder then do python setup.py install

to access the serial ports you first need to open access for read and write
sudo chmod 777 /dev/USBNAME
/dev/ttyUSB0

So looking at teh servo motor and talking with galagher, the motor might be too slow to use. i can see how fast i can get it but it might just not work for our prouposus
He didnt seem too mad at me but mad at himself for not checking my work but i do still feel fuly resposnable

    