import psutil
import time

while True:

    print psutil.net_io_counters(pernic=True)
    time.sleep(2)