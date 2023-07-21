#!/usr/bin/env python3
import time
import datetime
from pystiebeleltron import pystiebeleltron as pyse
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from influxdb import InfluxDBClient


#INFLUXDB Parameters
INFLUX_DB_HOST='localhost'
INFLUX_DB_PORT=8086
INFLUX_DB_NAME='Tecalor'
INFLUX_DB_USER='admin'
INFLUX_DB_PASSWORD='influx'

TECALOR_ISG_HOST = "192.168.178.87"
TECALOR_ISG_PORT = 502
TECALOR_ISG_SLAVE = 1

def test_function(mod, fun):
    """Executes the given function on the Stiebel Heatpump and prints the result."""
    result = getattr(mod, fun) # Executes function directly, instead of giving back the function reference
    print("{}: {}".format(str(fun), str(result)))


def execute_tests(unit):
    """Execute the provided tests."""
    test_function(unit, "get_current_temp")
    test_function(unit, "get_current_humidity")
    test_function(unit, "get_target_temp")
    test_function(unit, "get_operation")
    test_function(unit, "get_filter_alarm_status")
    test_function(unit, "get_heating_status")
    test_function(unit, "get_cooling_status")

def write_to_db(aussentemperatur):
    client = InfluxDBClient(INFLUX_DB_HOST, INFLUX_DB_PORT, INFLUX_DB_USER, INFLUX_DB_PASSWORD, INFLUX_DB_NAME)
    now = datetime.datetime.utcnow()  # influx stores all data in UTC
    json_body = [
        {
            "measurement": "tecalor_measurement",
            "time": now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "fields": { "aussentemperatur" : aussentemperatur}
        }
    ]
    client.write_points(json_body)
    client.close()


def main():
    client = ModbusClient(host=TECALOR_ISG_HOST,
                          port=TECALOR_ISG_PORT,
                          timeout=2)
    client.connect()

    unit = pyse.StiebelEltronAPI(client, TECALOR_ISG_SLAVE)

    temperatur = unit.get_conv_val('AUSSENTEMPERATUR')
    write_to_db(temperatur)

    print(unit.get_operation())
    print(temperatur)
    print(unit.get_conv_val('ECO_TEMPERATUR_HK1'))
    print(unit.get_conv_val('OPERATING_STATUS'))

    


    #execute_tests(unit)

    client.close()

if __name__ == "__main__":
    main()
