#!/usr/bin/env python3
import datetime
import tecalorapi as tecalorapi
import yaml
from argparse import ArgumentParser

# Important -> pymodbus 2.5.3. required, higher versions may need small rewrite
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from influxdb import InfluxDBClient


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
    cmdline = ""
    parser = ArgumentParser()
    parser.add_argument("config", help="location of config file")
    args = parser.parse_args()
    print(args.config)
    
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    now = datetime.datetime.utcnow()

    influx_client = InfluxDBClient(host=config["influx_db"]["host"], port=config["influx_db"]["port"], username=config["influx_db"]["user"], password=config["influx_db"]["password"], database=config["influx_db"]["db_name"])

    with ModbusClient(host=config["modbus_isg"]["host"], port=config["modbus_isg"]["port"], timeout=2) as modbus_client:
        modbus_client.connect()
        unit = tecalorapi.TecalorAPI(modbus_client, config["modbus_isg"]["slave"])

        attributes = [
            'OPERATING_MODE', 'AUSSENTEMPERATUR', 'ISTTEMPERATURWW', 'HEIZUNGSDRUCK', 'OPERATING_STATUS',
            'VD_WARMWASSER_TAG_WAERMEMENGE', 'VD_WARMWASSER_SUMME_WAERMEMENGE',
            'NHZ_HEIZEN_SUMME_WAERMEMENGE', 'NHZ_WARMWASSER_SUMME_WAERMEMENGE',
            'VD_WARMWASSER_TAG_LEISTUNG', 'VD_WARMWASSER_SUMME_LEISTUNG',
            'VD1_HEIZEN_LAUFZEIT', 'VD2_HEIZEN_LAUFZEIT', 'VD12_HEIZEN_LAUFZEIT',
            'VD1_WARMWASSER_LAUFZEIT', 'VD2_WARMWASSER_LAUFZEIT', 'VD12_WARMWASSER_LAUFZEIT',
            'VD_NHZ1_LAUFZEIT', 'VD_NHZ2_LAUFZEIT', 'VD_NHZ12_LAUFZEIT', 'FEHLER_STATUS'
        ]

        for attribute in attributes:
            value = unit.get_conv_val(attribute)
            write_to_db(influx_client, now, attribute, value)

if __name__ == "__main__":
    main()

