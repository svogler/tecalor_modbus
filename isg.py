#!/usr/bin/env python3
import time
import datetime
from pystiebeleltron import pystiebeleltron as pyse
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from influxdb import InfluxDBClient


#INFLUXDB Parameters
INFLUX_DB_HOST='192.168.178.22'
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

def write_to_db(key, value):
    client = InfluxDBClient(INFLUX_DB_HOST, INFLUX_DB_PORT, INFLUX_DB_USER, INFLUX_DB_PASSWORD, INFLUX_DB_NAME)
    now = datetime.datetime.utcnow()  # influx stores all data in UTC
    json_body = [
        {
            "measurement": "tecalor_measurement",
            "time": now.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "fields": { key : value}
        }
    ]
    print(json_body)
    client.write_points(json_body)
    client.close()


def main():
    print(datetime.datetime.today())

    client = ModbusClient(host=TECALOR_ISG_HOST,
                          port=TECALOR_ISG_PORT,
                          timeout=2)
    client.connect()

    unit = pyse.StiebelEltronAPI(client, TECALOR_ISG_SLAVE)

    AUSSENTEMPERATUR = unit.get_conv_val('AUSSENTEMPERATUR')
    write_to_db('AUSSENTEMPERATUR', AUSSENTEMPERATUR)

    ISTTEMPERATURWW = unit.get_conv_val('ISTTEMPERATURWW')
    write_to_db('ISTTEMPERATURWW', ISTTEMPERATURWW)


    druck = unit.get_conv_val('HEIZUNGSDRUCK')
    write_to_db('HEIZUNGSDRUCK', druck)

    mode =  unit.get_operation()
    write_to_db('WPMODUS', mode)

    status = unit.get_conv_val('OPERATING_STATUS')
    write_to_db('OPERATING_STATUS', status)

    status = unit.get_conv_val('OPERATING_STATUS')
    write_to_db('OPERATING_STATUS', status)

    value = unit.get_conv_val('VD_WARMWASSER_TAG_WAERMEMENGE')
    write_to_db('VD_WARMWASSER_TAG_WAERMEMENGE', value)

    value = unit.get_conv_val('VD_WARMWASSER_SUMME_WAERMEMENGE')
    write_to_db('VD_WARMWASSER_SUMME_WAERMEMENGE', value)

    value = unit.get_conv_val('NHZ_HEIZEN_SUMME_WAERMEMENGE')
    write_to_db('NHZ_HEIZEN_SUMME_WAERMEMENGE', value)

    value = unit.get_conv_val('NHZ_WARMWASSER_SUMME_WAERMEMENGE')
    write_to_db('NHZ_WARMWASSER_SUMME_WAERMEMENGE', value)

    value = unit.get_conv_val('VD_WARMWASSER_TAG_LEISTUNG')
    write_to_db('VD_WARMWASSER_TAG_LEISTUNG', value)

    value = unit.get_conv_val('VD_WARMWASSER_SUMME_LEISTUNG')
    write_to_db('VD_WARMWASSER_SUMME_LEISTUNG', value)

    value = unit.get_conv_val('VD1_HEIZEN_LAUFZEIT')
    write_to_db('VD1_HEIZEN_LAUFZEIT', value)

    value = unit.get_conv_val('VD2_HEIZEN_LAUFZEIT')
    write_to_db('VD2_HEIZEN_LAUFZEIT', value)

    value = unit.get_conv_val('VD12_HEIZEN_LAUFZEIT')
    write_to_db('VD12_HEIZEN_LAUFZEIT', value)

    value = unit.get_conv_val('VD1_WARMWASSER_LAUFZEIT')
    write_to_db('VD1_WARMWASSER_LAUFZEIT', value)

    value = unit.get_conv_val('VD2_WARMWASSER_LAUFZEIT')
    write_to_db('VD2_WARMWASSER_LAUFZEIT', value)

    value = unit.get_conv_val('VD12_WARMWASSER_LAUFZEIT')
    write_to_db('VD12_WARMWASSER_LAUFZEIT', value)

    value = unit.get_conv_val('VD_NHZ1_LAUFZEIT')
    write_to_db('VD_NHZ1_LAUFZEIT', value)

    value = unit.get_conv_val('VD_NHZ2_LAUFZEIT')
    write_to_db('VD_NHZ2_LAUFZEIT', value)

    value = unit.get_conv_val('VD_NHZ12_LAUFZEIT')
    write_to_db('VD_NHZ12_LAUFZEIT', value)

 
    client.close()

if __name__ == "__main__":
    main()
