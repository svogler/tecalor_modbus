#!/usr/bin/env python3
import datetime
import tecalorapi as tecalorapi
import yaml
from argparse import ArgumentParser

# Important -> pymodbus 2.5.3. required, higher versions may need small rewrite
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

from influxdb import InfluxDBClient

def main():
    cmdline = ""
    parser = ArgumentParser()
    parser.add_argument("config", help="location of config file")
    args = parser.parse_args()
    
    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    json_values = {}


    influx_client = InfluxDBClient(host=config["influx_db"]["host"], port=config["influx_db"]["port"], username=config["influx_db"]["user"], password=config["influx_db"]["password"], database=config["influx_db"]["db_name"])

    with ModbusClient(host=config["modbus_isg"]["host"], port=config["modbus_isg"]["port"], timeout=2) as modbus_client:
        modbus_client.connect()
        unit = tecalorapi.TecalorAPI(modbus_client, config["modbus_isg"]["slave"])


        attributes = [
                    'OPERATING_MODE', 'AUSSENTEMPERATUR', 'ISTTEMPERATURWW', 'HEIZUNGSDRUCK', 'OPERATING_STATUS',
                    'VD_WARMWASSER_TAG_WAERMEMENGE', 'VD_WARMWASSER_SUMME_WAERMEMENGE', 'VD_WARMWASSER_SUMME_WAERMEMENGE_MWH',
                    'VD_HEIZEN_TAG_WAERMEMENGE','VD_HEIZEN_SUMME_WAERMEMENGE', 'VD_HEIZEN_SUMME_WAERMEMENGE_MWH',
                    'NHZ_HEIZEN_SUMME_WAERMEMENGE', 'NHZ_WARMWASSER_SUMME_WAERMEMENGE',
                    'VD_WARMWASSER_SUMME_LEISTUNG', 'VD_WARMWASSER_SUMME_LEISTUNG_MWH','VD_WARMWASSER_TAG_LEISTUNG', 
                    'ISTTEMPERATUR_HK1','SOLLTEMPERATUR_HK1',
                    'VD_HEIZEN_SUMME_LEISTUNG', 'VD_HEIZEN_SUMME_LEISTUNG_MWH', 'VD_HEIZEN_TAG_LEISTUNG',
                    'VD1_HEIZEN_LAUFZEIT', 'VD2_HEIZEN_LAUFZEIT', 'VD12_HEIZEN_LAUFZEIT',
                    'VD1_WARMWASSER_LAUFZEIT', 'VD2_WARMWASSER_LAUFZEIT', 'VD12_WARMWASSER_LAUFZEIT',
                    'VD_NHZ1_LAUFZEIT', 'VD_NHZ2_LAUFZEIT', 'VD_NHZ12_LAUFZEIT', 'FEHLER_STATUS','VD_WARMWASSER_LAUFZEIT','VD_HEIZEN_LAUFZEIT',
                    'VORLAUFTEMPERATUR', 'RUECKLAUFTEMPERATUR'
                ]

       
        for attribute in attributes:
            value = unit.get_conv_val(attribute)

            if value != None:
                #print(attribute + " " + str(value))
                json_values[attribute] = value

        # calculate data for leistung und waermemengen (KWH and MWH are stored in different fields, make 1 our of it)
        heizen_waermenge = json_values['VD_HEIZEN_SUMME_WAERMEMENGE'] + json_values['VD_HEIZEN_SUMME_WAERMEMENGE_MWH'] * 1000
        heizen_leistung = json_values['VD_HEIZEN_SUMME_LEISTUNG'] + json_values['VD_HEIZEN_SUMME_LEISTUNG_MWH'] * 1000
        ww_waermemenge = json_values['VD_WARMWASSER_SUMME_WAERMEMENGE'] + json_values['VD_WARMWASSER_SUMME_WAERMEMENGE_MWH'] * 1000
        ww_leistung = json_values['VD_WARMWASSER_SUMME_LEISTUNG'] + json_values['VD_WARMWASSER_SUMME_LEISTUNG_MWH'] * 1000

        json_values['VD_HEIZEN_SUMME_WAERMEMENGE'] = round(heizen_waermenge)
        json_values['VD_HEIZEN_SUMME_LEISTUNG'] = round(heizen_leistung)
        json_values['VD_WARMWASSER_SUMME_WAERMEMENGE'] = round(ww_waermemenge)
        json_values['VD_WARMWASSER_SUMME_LEISTUNG'] = round(ww_leistung)

        # remove values for MWH from the JSON
        json_values.pop('VD_HEIZEN_SUMME_WAERMEMENGE_MWH')
        json_values.pop('VD_HEIZEN_SUMME_LEISTUNG_MWH')
        json_values.pop('VD_WARMWASSER_SUMME_WAERMEMENGE_MWH')
        json_values.pop('VD_WARMWASSER_SUMME_LEISTUNG_MWH')

        # Calculate JAZ for WW and Heating
        json_values['VD_HEIZEN_SUMME_JAZ'] = round(heizen_waermenge / heizen_leistung,2)
        json_values['VD_WARMWASSER_SUMME_JAZ'] = round(ww_waermemenge/ ww_leistung,2)

        json_body = [
            {
                "measurement": "tecalor_measurement",
                "time": datetime.datetime.utcnow(),
                "fields": json_values
            }
        ]
        print(json_body) 
        influx_client.write_points(json_body)

if __name__ == "__main__":
    main()

