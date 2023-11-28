from pymodbus.pdu import ExceptionResponse

"""
Connection to Tecalor/Steibel Eltron Heatpump ModBus API, write data into an influx DB.

Modbus API :
https://www.stiebel-eltron.de/content/dam/ste/cdbassets/historic/bedienungs-_u_installationsanleitungen/ISG_Modbus__b89c1c53-6d34-4243-a630-b42cf0633361.pdf

Types of data:

Data | Value      | Multiplier  | Multiplier  | Signed | Step   | Step
type | range      | for reading | for writing |        | size 1 | size 5
-----|------------|-------------|-------------|--------|--------|-------
2    | -3276.8 to | 0.1         | 10          | Yes    | 0.1    | 0.5
     |  3276.7    |             |             |        |        |
6    | 0 to 65535 | 1           | 1           | No     | 1      | 5
7    | -327.68 to | 0.01        | 100         | Yes    | 0.01   | 0.05
     |  327.67    |             |             |        |        |
8    | 0 to 255   | 1           | 1           | No     | 1      | 5
"""

# Error - sensor lead is missing or disconnected.
ERROR_NOTAVAILABLE = -60
# Error - short circuit of the sensor lead.
ERROR_SHORTCUT = -50
# Error - object unavailable.
ERROR_OBJ_UNAVAILBLE = 0x8000

UNAVAILABLE_OBJECT = 32768

REGISTER_INPUT = 1
REGISTER_HOLDING = 2


REGMAP_INPUT = {
    'ISTTEMPERATUR_FE7':      {'addr':  500, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'SOLLTEMPERATUR_FE7':     {'addr':  501, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'ISTTEMPERATUR_FEK':      {'addr':  502, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'SOLLTEMPERATUR_FEK':     {'addr':  503, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'RAUMFEUCHTE':            {'addr':  504, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'TAUPUNKTTEMPERATUR':     {'addr':  505, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'AUSSENTEMPERATUR':       {'addr':  506, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'ISTTEMPERATUR_HK1':      {'addr':  507, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'SOLLTEMPERATUR_HK1':     {'addr':  508, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'ISTTEMPERATUR_HK2':      {'addr':  510, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'SOLLTEMPERATUR_HK2':     {'addr':  511, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'VORLAUFISTTEMPERATUR_WP':{'addr':  512, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'VORLAUFISTTEMPERATUR_NH':{'addr':  513, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'VORLAUFISTTEMPERATUR':   {'addr':  514, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'RUECKLAUISTTEMPERATUR':  {'addr':  515, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'HEIZUNGSDRUCK':          {'addr':  519, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'ISTTEMPERATURWW':        {'addr':  521, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'SOLLTEMPERATURWW':       {'addr':  522, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'EINSATZGRENZE_HZG':      {'addr':  532, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'EINSATZGRENZE_WW':       {'addr':  533, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'RUECKLAUFTEMPERATUR':    {'addr':  541, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'VORLAUFTEMPERATUR':      {'addr':  542, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'HEISSGASTEMPERATUR':     {'addr':  543, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'DRUCK_NIEDERDRUCK':      {'addr':  544, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'DRUCK_MITTELDRUCK':      {'addr':  545, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'DRUCK_HOCHDRUCK':        {'addr':  546, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},
    'WP_WASSERVOLUMENSTROM':  {'addr':  547, 'reg' : REGISTER_INPUT, 'type': 2, 'value': 0},

    'OPERATING_MODE':         {'addr': 1500, 'reg' : REGISTER_HOLDING, 'type': 8, 'value': 0},
    'KOMFORT_TEMPERATUR_HK1':      {'addr': 1501, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'ECO_TEMPERATUR_HK1':          {'addr': 1502, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'STEIGUNG_HEIZKURVE_HK1':      {'addr': 1503, 'reg' : REGISTER_HOLDING, 'type': 7, 'value': 0},
    'KOMFORT_TEMPERATUR_HK2':      {'addr': 1504, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'ECO_TEMPERATUR_HK2':          {'addr': 1505, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'STEIGUNG_HEIZKURVE_HK2':      {'addr': 1506, 'reg' : REGISTER_HOLDING, 'type': 7, 'value': 0},
    'FESTWERTBETRIEB':             {'addr': 1507, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'BIVALENZTEMPERATUR_HZG':      {'addr': 1508, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'KOMFORT_TEMPERATUR_WW':       {'addr': 1509, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'ECO_TEMPERATUR_WW':           {'addr': 1510, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'WARMWASSERSTUFEN':            {'addr': 1511, 'reg' : REGISTER_HOLDING, 'type': 2, 'value': 0},
    'OPERATING_STATUS':            {'addr': 2500, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'FEHLER_STATUS':               {'addr': 2503, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_HEIZEN_TAG_WAERMEMENGE':        {'addr': 3500, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_HEIZEN_SUMME_WAERMEMENGE':      {'addr': 3501, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_HEIZEN_SUMME_WAERMEMENGE_MWH':  {'addr': 3502, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_WARMWASSER_TAG_WAERMEMENGE':    {'addr': 3503, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_WARMWASSER_SUMME_WAERMEMENGE':  {'addr': 3504, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_WARMWASSER_SUMME_WAERMEMENGE_MWH':  {'addr': 3505, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'NHZ_HEIZEN_SUMME_WAERMEMENGE':     {'addr': 3506, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'NHZ_HEIZEN_SUMME_WAERMEMENGE_MWH': {'addr': 3507, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'NHZ_WARMWASSER_SUMME_WAERMEMENGE': {'addr': 3508, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'NHZ_WARMWASSER_SUMME_WAERMEMENGE_MWH': {'addr': 3509, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_HEIZEN_TAG_LEISTUNG':           {'addr': 3510, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_HEIZEN_SUMME_LEISTUNG':         {'addr': 3511, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_HEIZEN_SUMME_LEISTUNG_MWH':     {'addr': 3512, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_WARMWASSER_TAG_LEISTUNG':       {'addr': 3513, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_WARMWASSER_SUMME_LEISTUNG':     {'addr': 3514, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_WARMWASSER_SUMME_LEISTUNG_MWH': {'addr': 3515, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},


    'VD1_HEIZEN_LAUFZEIT':              {'addr': 3538, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD2_HEIZEN_LAUFZEIT':              {'addr': 3539, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD12_HEIZEN_LAUFZEIT':             {'addr': 3540, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD1_WARMWASSER_LAUFZEIT':          {'addr': 3541, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD2_WARMWASSER_LAUFZEIT':          {'addr': 3542, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD12_WARMWASSER_LAUFZEIT':         {'addr': 3543, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_KUEHLEN_LAUFZEIT':              {'addr': 3544, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_NHZ1_LAUFZEIT':                 {'addr': 3545, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_NHZ2_LAUFZEIT':                 {'addr': 3546, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_NHZ12_LAUFZEIT':                {'addr': 3547, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_HEIZEN_LAUFZEIT':               {'addr': 3643, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
    'VD_WARMWASSER_LAUFZEIT':           {'addr': 3644, 'reg' : REGISTER_INPUT, 'type': 6, 'value': 0},
}


OPERATING_MODE_READ = {
    1: 'BEREITSCHAFTSBETRIEB',
    2: 'PROGRAMMBETRIEB',
    3: 'KOMFORTBETRIEB',
    4: 'ECO-BETRIEB',
    5: 'WARMWASSERBETRIEB',
    0: 'NOTBETRIEB'
}

OPERATING_MODE_WRITE = {
    value: key for key, value in OPERATING_MODE_READ.items()
}

RESET = {
    'OFF': 0,
    'ON': 1
}

RESTART_ISG = {
    'OFF': 0,
    'RESET': 1,
    'MENU': 2
}


OPERATING_STATUS = {
    'HK_1_PUMPE': (1 << 0),
    'HK_2_PUMPE': (1 << 1),
    'AUFHEIZPROGRAMM': (1 << 2),
    'NHZ_STUFEN_IN_BETRIEB': (1 << 3),
    'WP_IM_HEIZBETRIEB': (1 << 4),
    'WP_IM_WARMWASSERBETRIEB': (1 << 5),
    'VERDICHTER_IN_BETRIEB': (1 << 6),
    'SOMMERBETRIEB_AKTIV': (1 << 7),
    'KUEHLBETRIEB_AKTIV': (1 << 8),
    'MIN_EINE_IWS_IM_ABTAUBETRIEB': (1 << 9),
    'SILENTMODE_1_AKTIV': (1 << 10),
    'SILENTMODE_1_AKTIV_WP_AUS': (1 << 11)
}

FAULT_STATUS = {
    'NO_FAULT': 0,
    'FAULT': 1
}

BUS_STATUS = {
    'STATUS OK': 0,
    'STATUS ERROR': -1,
    'ERROR-PASSIVE': -2,
    'BUS-OFF': -3,
    'PHYSICAL-ERROR': -4
}


class TecalorAPI():
    """Tecalor Modbus API."""

    def __init__(self, conn, slave, update_on_read=False):
        """Initialize  communication."""
        self._conn = conn
        self._registers_map = REGMAP_INPUT
        self._slave = slave

    def twos_comp(self, val, bits):
        """ Negative numbers are represented in 2's comp representation
            this function computes the 2's complement of int value val """
        if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
            val = val - (1 << bits)        # compute negative value
        return val                         # return positive value as is

    def get_conv_val(self, name):

        value_entry = self._registers_map.get(name)
        if value_entry is None:
            return None
        
        if value_entry['reg'] == REGISTER_INPUT:
            result_input = self._conn.read_input_registers(unit=self._slave, address = value_entry['addr'], count = 1)

        if value_entry['reg'] == REGISTER_HOLDING:
            result_input = self._conn.read_holding_registers(unit=self._slave, address = value_entry['addr'], count = 1)
        
        if type(result_input) == ExceptionResponse:
            print("Illegal Address " + name + " " + str(value_entry['addr']))
            return None
        
        value = result_input.registers[0]

        if value == UNAVAILABLE_OBJECT:
            return None

        # convert negative values read from Modbus
        value = self.twos_comp(int(value), 16)

        # conversation based on type
        if value_entry['type'] == 2:
            value = round(value * 0.1,1)
        if value_entry['type'] == 7:
            value = round(value  * 0.01,1)
        
        return value




#    def get_raw_input_register(self, name):
#        """Get raw register value by name."""
#        if self._update_on_read:
#            self.update()
#        return self._block_1_input_regs[name]

#    def get_raw_holding_register(self, name):
#        """Get raw register value by name."""
#        if self._update_on_read:
#            self.update()
#        return self._block_2_holding_regs[name]

#    def set_raw_holding_register(self, name, value):
#        """Write to register by name."""
#        self._conn.write_register(
#            unit=self._slave,
#            address=(self._holding_regs[name]['addr']),
#            value=value)

    # Handle room temperature & humidity

    def get_current_temp(self):
        """Get the current room temperature."""
        return self.get_conv_val('ACTUAL_ROOM_TEMPERATURE_HC1')

    def get_target_temp(self):
        """Get the target room temperature."""
        return self.get_conv_val('ROOM_TEMP_HEAT_DAY_HC1')

    def set_target_temp(self, temp):
        """Set the target room temperature (day)(HC1)."""
        self._conn.write_register(
            unit=self._slave,
            address=(
                self._block_2_holding_regs['ROOM_TEMP_HEAT_DAY_HC1']['addr']),
            value=round(temp * 10.0))

    # Handle operation mode

    def get_operation(self):
        op_mode = self.get_conv_val('OPERATING_MODE')
        return OPERATING_MODE_READ.get(op_mode, 'UNKNOWN')

    def set_operation(self, mode):
        """Set the operation mode."""
        self._conn.write_register(
            unit=self._slave,
            address=(self._block_2_holding_regs['OPERATING_MODE']['addr']),
            value=OPERATING_MODE_WRITE.get(mode))

    # Handle device status

    def error_detected(self, fault_code):
        return bool(fault_code & FAULT_STATUS['FAULT'])

    def get_heating_status(self):
        return bool(self.get_conv_val('OPERATING_STATUS') &
                    OPERATING_STATUS['HEATING'])

    def get_cooling_status(self):
        return bool(self.get_conv_val('OPERATING_STATUS') &
                    OPERATING_STATUS['COOLING'])


