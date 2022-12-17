import pandas as pd
import numpy as np
from typing import Callable
from scipy.stats import shapiro
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None


def ProcessBrownedOut(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the RoboRio browned out telemetry data.

    Get the count of brownouts.

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
    brownOut = robotTelemetry[robotTelemetry['Name'] == key]
    if brownOut.empty:
        return 'Brownout Count: 0', 'metric_not_implemented'
    brownOut[key] = cFunc(brownOut['Value'])

    metric = brownOut[key].sum()
    metricEncoding = 'metric_ok'
    if metric > 1:
        metricEncoding = 'metric_high_risk'
    elif metric > 0:
        metricEncoding = 'metric_low_risk'

    return [f'Brownout Count: {metric}'], [metricEncoding]


def ProcessCanUtilization(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the RoboRio CAN utilization telemetry data.

    Take the average of all CAN utilization data and spec that.

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
    canUtilization = robotTelemetry[robotTelemetry['Name'] == key]
    if canUtilization.empty:
        return 'CAN Utilization: 0.0', 'metric_not_implemented'
    canUtilization[key] = cFunc(canUtilization['Value'])

    metric = canUtilization[key].mean()
    metricEncoding = 'metric_ok'
    if metric > 80.0:
        metricEncoding = 'metric_high_risk'
    elif metric > 60.0:
        metricEncoding = 'metric_low_risk'

    return [f'CAN Utilization: {metric:.2f}'], [metricEncoding]


def ProcessCanOffCount(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the RoboRio CAN off count telemetry data.

    Filter this to grab the latest output. This will be used to spec the ending count and not used as an event to
    correlate to another metric.

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
    canOffCount = robotTelemetry[robotTelemetry['Name'] == key]
    canOffCount = canOffCount[canOffCount['Timestamp'] == canOffCount['Timestamp'].max()]
    if canOffCount.empty:
        return 'CAN Off Count: 0', 'metric_not_implemented'
    canOffCount[key] = cFunc(canOffCount['Value'])

    metric = canOffCount[key].values[0]
    metricEncoding = 'metric_ok'
    if metric > 5:
        metricEncoding = 'metric_high_risk'
    elif metric > 0:
        metricEncoding = 'metric_low_risk'

    return [f'CAN Off Count: {metric}'], [metricEncoding]


def ProcessCanRxErrorCount(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the RoboRio CAN receive error count telemetry data.

    Filter this to grab the latest output. This will be used to spec the ending count and not used as an event to
    correlate to another metric.

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
    canRxErrCount = robotTelemetry[robotTelemetry['Name'] == key]
    canRxErrCount = canRxErrCount[canRxErrCount['Timestamp'] == canRxErrCount['Timestamp'].max()]
    if canRxErrCount.empty:
        return 'CAN Rx Error Count: 0', 'metric_not_implemented'
    canRxErrCount[key] = cFunc(canRxErrCount['Value'])

    metric = canRxErrCount[key].values[0]
    metricEncoding = 'metric_ok'
    if metric > 5:
        metricEncoding = 'metric_high_risk'
    elif metric > 0:
        metricEncoding = 'metric_low_risk'

    return [f'CAN Rx Error Count: {metric}'], [metricEncoding]


def ProcessCanTxErrorCount(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the RoboRio CAN transmit error count telemetry data.

    Filter this to grab the latest output. This will be used to spec the ending count and not used as an event to
    correlate to another metric.

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
    canTxErrCount = robotTelemetry[robotTelemetry['Name'] == key]
    canTxErrCount = canTxErrCount[canTxErrCount['Timestamp'] == canTxErrCount['Timestamp'].max()]
    if canTxErrCount.empty:
        return 'CAN Tx Error Count: 0', 'metric_not_implemented'
    canTxErrCount[key] = cFunc(canTxErrCount['Value'])

    metric = canTxErrCount[key].values[0]
    metricEncoding = 'metric_ok'
    if metric > 5:
        metricEncoding = 'metric_high_risk'
    elif metric > 0:
        metricEncoding = 'metric_low_risk'

    return [f'CAN Tx Error Count: {metric}'], [metricEncoding]


def ProcessCanTxFullCount(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the RoboRio CAN transmit full count telemetry data.

    Filter this to grab the latest output. This will be used to spec the ending count and not used as an event to
    correlate to another metric.

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
    canTxFullCount = robotTelemetry[robotTelemetry['Name'] == key]
    canTxFullCount = canTxFullCount[canTxFullCount['Timestamp'] == canTxFullCount['Timestamp'].max()]
    if canTxFullCount.empty:
        return 'CAN Tx Full Count: 0', 'metric_not_implemented'
    canTxFullCount[key] = cFunc(canTxFullCount['Value'])

    metric = canTxFullCount[key].values[0]
    metricEncoding = 'metric_ok'
    if metric > 5:
        metricEncoding = 'metric_high_risk'
    elif metric > 0:
        metricEncoding = 'metric_low_risk'

    return [f'CAN Tx Full Count: {metric}'], [metricEncoding]


def ProcessStaleDsData(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the RoboRio stale drivers station telemetry data.

    Count the number of times there is stale data from the drivers station. TODO: this doesn't represent communication
    issues.

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
    staleDsData = robotTelemetry[robotTelemetry['Name'] == key]
    if staleDsData.empty:
        return 'Stale DS Data Count: 0', 'metric_not_implemented'
    staleDsData[key] = cFunc(staleDsData['Value'])

    metric = staleDsData[key].count()
    metricEncoding = 'metric_ok'
    if metric > 1:
        metricEncoding = 'metric_high_risk'
    elif metric > 0:
        metricEncoding = 'metric_low_risk'

    return [f'Stale DS Data Count: {metric}'], [metricEncoding]


def ProcessImuYawAngle(robotTelemetry: pd.DataFrame, key: str, cFunc: Callable):
    ''' Process the IMU yaw angle telemetry data.

    Filter the IMU data to only use the samples collected while the robot is not moving and in a known postion. This
    is determined by using the `FMS Mode` telemetry and using the samples from the first `Disabled` state and the
    minimum of the `Auto` and `Teleop` states.

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
    fmsMode = robotTelemetry[robotTelemetry['Name'] == 'FMS Mode']
    startTime = fmsMode[fmsMode['Value'] == 'Disabled']['Timestamp'].min()
    stopTime = fmsMode[fmsMode['Value'].isin(['Teleop', 'Auto'])]['Timestamp'].min()
    imuYawAngle = robotTelemetry[robotTelemetry['Name'] == key]
    imuYawAngle = imuYawAngle[(imuYawAngle['Timestamp'] <= stopTime) &
                              (imuYawAngle['Timestamp'] >= startTime)]
    imuYawAngle[key] = cFunc(imuYawAngle['Value'])

    # Test for gaussian (gaussian means there is no drift which is good)
    gaussianMetricEncoding = 'metric_ok'
    stat, p = shapiro(imuYawAngle[key].dropna())
    alpha = 0.05  # 95% confidence
    if p > alpha:
        txt = 'Gaussian (fail to reject H0), p = %.3f' % (p)
    else:
        gaussianMetricEncoding = 'metric_low_risk'
        txt = 'Not Gaussian (reject H0), p = %.3f' % (p)

    # Fit a linear model and spec the slope...which is the drift
    linearModel = np.polyfit(imuYawAngle['Timestamp'], imuYawAngle[key], 1)
    predictor = np.poly1d(linearModel)
    imuYawAngle['Linear Regression'] = predictor(imuYawAngle['Timestamp'])
    driftDegPerMinMetricEncoding = 'metric_ok'
    driftDegPerMin = abs(linearModel[0]*60.0)
    if driftDegPerMin > 1.0:
        driftDegPerMinMetricEncoding = 'metric_high_risk'
    elif driftDegPerMin > 0.5:
        driftDegPerMinMetricEncoding = 'metric_low_risk'

    # Create and save plots
    fig, ax = plt.subplot_mosaic("A;B")
    fig.suptitle('IMU Yaw Angle (deg) Analysis', fontsize=16)
    imuYawAngle.plot(ax=ax["A"], x='Timestamp', linestyle='--', marker='o')
    imuYawAngle[key].plot(kind='hist', ax=ax["B"], bins=10, legend=True)
    ax["B"].legend([txt])
    plt.savefig(r'..\..\output\IMU Yaw Angle.png', bbox_inches='tight')

    metrics = [f'IMU Yaw ?Norm Error? P-val: {p:.3f}', f'IMU Yaw DpM: {driftDegPerMin:.2f}']

    return metrics, [gaussianMetricEncoding, driftDegPerMinMetricEncoding]
