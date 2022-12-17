import pandas as pd
import matplotlib.pyplot as plt
from typing import Callable
pd.options.mode.chained_assignment = None


def ProcessPressure(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the pneumatics hub pressure telemetry data.

    Spec the pressure when the robot is first enabled. This will check that the pneumatics were charged up in the pit
    or queue.

    TODO: Check and spec the pressure at the beginning of auto. Check and spec an average pressure for teleop. Check
    and spec pressue at the beginning of the end game.


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
    pressure = robotTelemetry[robotTelemetry['Name'] == key]
    if pressure.empty:
        return 'Starting Pressure: 0.0', 'metric_not_implemented'
    pressure[key] = cFunc(pressure['Value'])

    metric = pressure[key].iloc[0]
    metricEncoding = 'metric_ok'
    if metric < 80.0:
        metricEncoding = 'metric_high_risk'
    elif metric < 100.0:
        metricEncoding = 'metric_low_risk'

    # Create and save plots
    fig, ax = plt.subplot_mosaic("A")
    fig.suptitle('Pressure Analysis', fontsize=16)
    pressure.plot(ax=ax["A"], x='Timestamp', linestyle='--', marker='o')
    plt.savefig(r'..\..\output\Pressure.png', bbox_inches='tight')

    return [f'Starting Pressure: {metric:.1f}'], [metricEncoding]


def ProcessCompressorCurrent(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the pneumatics hub compresoor current telemetry data.

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
    current = robotTelemetry[robotTelemetry['Name'] == key]
    if current.empty:
        return 'Max Compressor Current: 0.0', 'metric_not_implemented'
    current[key] = cFunc(current['Value'])

    metric = current[key].max()
    metricEncoding = 'metric_ok'
    if metric > 20.0:
        metricEncoding = 'metric_high_risk'
    elif metric > 16.0:
        metricEncoding = 'metric_low_risk'

    # Create and save plots
    fig, ax = plt.subplot_mosaic("A")
    fig.suptitle('Compressor Current Analysis', fontsize=16)
    current.plot(ax=ax["A"], x='Timestamp', linestyle='--', marker='o')
    plt.savefig(r'..\..\output\Current.png', bbox_inches='tight')

    return [f'Max Compressor Current: {metric:.1f}'], [metricEncoding]
