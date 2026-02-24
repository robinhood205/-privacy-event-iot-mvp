import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, "MNLib"))

from apppal import AppPAL

# 串口初始化
PAL = AppPAL(port="COM4", baud=115200, tout=0.05, sformat="Ascii")

print("Serial test started...")

while True:
    try:
        if PAL.ReadSensorData():
            Data = PAL.GetDataDict()
            print("Received:", Data)

        time.sleep(0.1)

    except KeyboardInterrupt:
        break

print("Serial test stopped.")
