#!/usr/bin/env python3
import datetime
from pystiebeleltron import pystiebeleltron as pyse
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from influxdb import InfluxDBClient

# INFLUXDB Parameters
INFLUX_DB_HOST = '192.168.178.22'
INFLUX_DB_PORT = 8086
INFLUX_DB_NAME = 'Tecalor'
INFLUX_DB_USER = 'admin'
INFLUX_DB_PASSWORD = '*****'

TECALOR_ISG_HOST = "192.168.178.87"
TECALOR_ISG_PORT = 502
TECALOR_ISG_SLAVE = 1

def write_to_db(client, time, key, value):
    
    json_body = [
        {
            "measurement": "tecalor_measurement",
            "time": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "fields": {key: value}
        }
    ]
    print(json_body)
    client.write_points(json_body)

def main():
    now = datetime.datetime.utcnow()

    print(now)

    with ModbusClient(host=TECALOR_ISG_HOST, port=TECALOR_ISG_PORT, timeout=2) as client:
        client.connect()
        unit = pyse.StiebelEltronAPI(client, TECALOR_ISG_SLAVE)

        attributes = [
            'OPERATING_MODE', 'AUSSENTEMPERATUR', 'ISTTEMPERATURWW', 'HEIZUNGSDRUCK', 'OPERATING_STATUS',
            'VD_WARMWASSER_TAG_WAERMEMENGE', 'VD_WARMWASSER_SUMME_WAERMEMENGE',
            'NHZ_HEIZEN_SUMME_WAERMEMENGE', 'NHZ_WARMWASSER_SUMME_WAERMEMENGE',
            'VD_WARMWASSER_TAG_LEISTUNG', 'VD_WARMWASSER_SUMME_LEISTUNG',
            'VD1_HEIZEN_LAUFZEIT', 'VD2_HEIZEN_LAUFZEIT', 'VD12_HEIZEN_LAUFZEIT',
            'VD1_WARMWASSER_LAUFZEIT', 'VD2_WARMWASSER_LAUFZEIT', 'VD12_WARMWASSER_LAUFZEIT',
            'VD_NHZ1_LAUFZEIT', 'VD_NHZ2_LAUFZEIT', 'VD_NHZ12_LAUFZEIT', 'FEHLER_STATUS'
        ]

        with InfluxDBClient(INFLUX_DB_HOST, INFLUX_DB_PORT, INFLUX_DB_USER, INFLUX_DB_PASSWORD, INFLUX_DB_NAME) as influx_client:
            for attribute in attributes:
                value = unit.get_conv_val(attribute)
                write_to_db(influx_client, now, attribute, value)

if __name__ == "__main__":
    main()
