import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable
pd.options.mode.chained_assignment = None


def ProcessInputVoltage(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the power distribution hub pressure telemetry data.

    Args:
        robotTelemetry: Pandas dataframe of robot telemetry
        key: the telemetry key
        cFunc: the conversion function for the `Value` column

    Returns:
        metric: the string label used for displaying the metric in HTML
        metricEncoding: the string encoding used to style the metric in HTML

    Raises:
        None

    '''
    voltage = robotTelemetry[robotTelemetry['Name'] == key]
    if voltage.empty:
        return 'Ending Voltage: 0.0', 'metric_not_implemented'
    voltage[key] = cFunc(voltage['Value'])

    endVoltage = voltage[key].iloc[-1]
    endVoltageMetricEncoding = 'metric_ok'
    if endVoltage < 11.0:
        endVoltageMetricEncoding = 'metric_high_risk'
    elif endVoltage < 11.2:
        endVoltageMetricEncoding = 'metric_low_risk'

    startVoltage = voltage[key].iloc[0]
    startVoltageMetricEncoding = 'metric_ok'
    if startVoltage < 11.5:
        startVoltageMetricEncoding = 'metric_high_risk'
    elif startVoltage < 11.7:
        startVoltageMetricEncoding = 'metric_low_risk'

    # Create and save plots
    fig, ax = plt.subplot_mosaic("A")
    fig.suptitle('Voltage Analysis', fontsize=16)
    voltage.plot(ax=ax["A"], x='Timestamp', linestyle='--', marker='o')
    plt.savefig(r'..\..\output\Voltage.png', bbox_inches='tight')

    metrics = [f'Starting Voltage: {startVoltage:.2f}', f'Ending Voltage: {endVoltage:.2f}']

    return metrics, [endVoltageMetricEncoding, startVoltageMetricEncoding]
