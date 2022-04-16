from napalm import get_network_driver
import json

driver = get_network_driver("ios")

device = driver(hostname='192.168.0.X',
                username='admin',
                password='admin',
                optional_args={'port': 22})

device.open()

print("Accesing device")
device.load_merge_candidate(filename="syslog.txt")

diffs = device.compare_config()
if len(diffs) > 0 :
    print(diffs)
    device.commit_config()
else:
    print("no changes required")
    device.discard_config()

device.close()

