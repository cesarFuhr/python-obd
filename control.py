import time
import datetime

from obd.decoders import dtc

import http_client
import reader
import obd


def formatDT(t: time.time):
    dt = datetime.datetime.utcfromtimestamp(t)
    print(dt.isoformat(timespec='milliseconds') + 'Z')
    return dt.isoformat(timespec='milliseconds') + 'Z'


def PIDFormatter(p: obd.OBDResponse):
    return {
        'at': formatDT(p.time),
        'pid': str(p.command.pid),
        'value': str(p.value.magnitude),
        'unit': p.unit,
        'description': p.command.name
    }


def DTCFormatter(d: obd.OBDResponse):
    at = formatDT(d.time)
    dtcs = d.value
    final = []
    for dtc in dtcs:
        final = final.append({
            'at': at,
            'dtc': dtc[0],
            'description': dtc[1]
        })
    return


def dtcHandler(r: obd.OBDResponse):
    http_client.sendDTCs(DTCFormatter(r))


def pidHandler(r: obd.OBDResponse):
    if not hasattr(r.value, 'magnitude'):
        obdReader.unwatch(r.command)
        return
    http_client.sendPIDs([PIDFormatter(r)])


def setupOBDReader():
    obdReader = reader.Reader()
    obdReader.connect()
    availablePIDs = obdReader.checkAvailable()

    if not obdReader.conn.is_connected():
        exit(1)

    obdReader.watch(availablePIDs, pidHandler, dtcHandler)

    return obdReader


def newCleanup(r):
    def cleanup():
        print("Bye...")
        r.stop()
        r.disconnect()
    return cleanup


count = 0
obdReader = reader.Reader()
try:
    obdReader = setupOBDReader()

    cleanup = newCleanup(obdReader)

    obdReader.start()
    while True:
        time.sleep(1)
        print(count)
        count += 1
finally:
    if obdReader.conn.is_connected():
        cleanup()
    print("Goodbye...")
