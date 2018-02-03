#!/bin/bash

cd ~/sarah-new

pkill -f listen.py
pkill -f speak.py

#sudo kinect_upload_fw /lib/firmware/kinect/UACFirmware

sleep 10

nohup /usr/bin/python listen.py sarah.pmdl 192.168.254.220:1880 </dev/null > butler.log 2>&1 &
nohup /usr/bin/python speak.py 5555 </dev/null >> butler.log 2>&1 &
