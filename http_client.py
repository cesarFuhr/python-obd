import requests
import json

pid_url = "http://localhost:5000/publish/pids"
dtc_url = "http://localhost:5000/publish/dtcs"
headers = {
    'Content-Type': 'application/json'
}


def sendPIDs(pids):
    try:
        payload = json.dumps(pids, indent=None)
        requests.post(pid_url, data=payload, headers=headers)
    except:
        print("error sending")
        return False
    return True


def sendDTCs(dtcs):
    try:
        payload = json.dumps(dtcs, indent=None)
        requests.post(pid_url, data=payload, headers=headers)
    except:
        print("error sending")
        return False
    return True
