#!/usr/bin/python3
import obd

ports = obd.scan_serial()
print(ports)

obd.logger.setLevel(obd.logging.DEBUG)
connection = obd.OBD()  # auto-connects to USB or RF port

cmd = obd.commands.O2_B1S1

response = connection.query(cmd)  # send the command, and parse the response

print(response)  # returns unit-bearing values thanks to Pint
