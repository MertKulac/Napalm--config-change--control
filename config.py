from napalm import get_network_driver
from multiprocessing.dummy import Pool as ThreadPool
import json

f_2 = open("multiple_device_list_napalm.txt","r")
multiple_device_list_napalm = f_2.readlines()

f_3 = open("Syslog_Unsuccess_Connection.txt","a")

with open("user_pass.txt", "r") as f5:
    user_pass = f5.readlines()

for list_user_pass in user_pass:
    if "username" in list_user_pass:
        username = list_user_pass.split(":")[1].strip()
    if "password" in list_user_pass:
        password = list_user_pass.split(":")[1].strip()

file1 = open("Syslog_Napalm.txt", "a")

driver = get_network_driver("ios")

def _ssh_(nodeip):
    try:
        device = driver(hostname= nodeip,
                        username='username',
                        password='password',
                        optional_args={'port': 22})
        print(nodeip.strip() + "  " + "is reachable")
    except Exception as e:
        print (e)
        f_3.write(nodeip.strip() + "\n")
        return

    device.open()

    print("Accesing device")
    device.load_merge_candidate(filename="syslog.txt")

    diffs = device.compare_config()
    if len(diffs) > 0:
        print(diffs)
        device.commit_config()
        file1.write(nodeip.strip() + "\n")
    else:
        print("no changes required")
        device.discard_config()

    device.close()

myPool = ThreadPool(1)
result = myPool.map(_ssh_,multiple_device_list_napalm)
