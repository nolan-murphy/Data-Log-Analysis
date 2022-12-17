import pandas as pd
import RoboRioMetrics as rrm
import PneumaticsHubMetrics as phm
import PowerDistributionHubMetrics as pdhm

""" TODO: The keys in this dictionary need to exactly match those used for logging the telemetry on the robot."""
ROBORIO_TELEMETRY_KEYS = {
    'RoboRio Browned Out':        {'pFunc': rrm.ProcessBrownedOut,        'cFunc': lambda x: x.replace({"true": 1, "false": 0})},
    'RoboRio CAN Utilization':    {'pFunc': rrm.ProcessCanUtilization,    'cFunc': pd.to_numeric},
    'RoboRio CAN Off Count':      {'pFunc': rrm.ProcessCanOffCount,       'cFunc': pd.to_numeric},
    'RoboRio CAN Rx Error Count': {'pFunc': rrm.ProcessCanRxErrorCount,   'cFunc': pd.to_numeric},
    'RoboRio CAN Tx Error Count': {'pFunc': rrm.ProcessCanTxErrorCount,   'cFunc': pd.to_numeric},
    'RoboRio CAN Tx Full Count':  {'pFunc': rrm.ProcessCanTxFullCount,    'cFunc': pd.to_numeric},
    'IMU Yaw Angle (deg)':        {'pFunc': rrm.ProcessImuYawAngle,       'cFunc': pd.to_numeric},
    'RoboRio Stale DS Data Count': {'pFunc': rrm.ProcessStaleDsData,       'cFunc': lambda x: x.replace({"true": 1, "false": 0})},
}

""" TODO: The keys in this dictionary need to exactly match those used for logging the telemetry on the robot."""
PH_TELEMETRY_KEYS = {
    'Pressure (psi)':             {'pFunc': phm.ProcessPressure,          'cFunc': pd.to_numeric},
    'Compressor Current (A)':     {'pFunc': phm.ProcessCompressorCurrent, 'cFunc': pd.to_numeric},
}

""" TODO: The keys in this dictionary need to exactly match those used for logging the telemetry on the robot."""
PDH_TELEMETRY_KEYS = {
    'PDH Input Voltage (V)':      {'pFunc': pdhm.ProcessInputVoltage,     'cFunc': pd.to_numeric},
    # 'PDH Total Current (A)':      {'pFunc': phm.ProcessTotalCurrent,      'cFunc': pd.to_numeric},
    # 'PDH Total Power (W)':        {'pFunc': phm.ProcessTotalPower,        'cFunc': pd.to_numeric},
}
