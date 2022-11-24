import DataLogHelpers as dlh
import pandas as pd
import numpy as np
from scipy.stats import shapiro
import matplotlib.pyplot as plt


def Test(df):
    """Process the telemetry for swerve module homing analysis.

    Args:
        df (:obj:`pd.DataFrame`): Pandas dataframe

    Returns:
        none

    Raises:
        TypeError: if the input isn't a pandas dataframe
        AttributeError: if the dataframe columns aren't [Timestamp,Name,Value]
    """

    dlh.VerifyInput(df)

    telemetryKeys = {
        'IMU Yaw Angle (deg)': 'float',
        ' Pressure (psi)': 'float',
        'Compressor Current (A)': 'float',
        # 'Drivetrain State'
        # 'systemTime'
        'FMS Mode': 'string',
    }

    # Get all of the columns of the telemetry keys
    sensorsDf = pd.DataFrame(columns=["Timestamp"])
    for telemetryKey, telemetryType in telemetryKeys.items():
        if telemetryType == 'float':
            sensorsDf = pd.merge(sensorsDf, dlh.GetFloatColumn(
                df, '', telemetryKey), how="outer", on=["Timestamp"])
        elif telemetryType == 'boolean':
            sensorsDf = pd.merge(sensorsDf, dlh.GetBooleanColumn(
                df, '', telemetryKey), how="outer", on=["Timestamp"])
        elif telemetryType == 'string':
            sensorsDf = pd.merge(sensorsDf, dlh.GetStringColumn(
                df, '', telemetryKey), how="outer", on=["Timestamp"])

    # Plot the data
    # fig1, ax1 = plt.subplot_mosaic("A;B;C;D", sharex=True)
    fig2, ax2 = plt.subplots()
    plt.rc('legend', fontsize=6)
    # __PlotSignals(sensorsDf[['Timestamp', ' Pressure (psi)']],
    #               ax1["A"], 'Pressure (psi)')
    # __PlotSignals(sensorsDf[['Timestamp', 'Compressor Current (A)']],
    #               ax1["B"], 'Compressor Current (amps)')
    # __PlotSignals(sensorsDf[['Timestamp', 'IMU Yaw Angle (deg)']],
    #               ax1["C"], 'IMU Yaw Angle (deg)')
    # __PlotSignals(sensorsDf[['Timestamp', 'FMS Mode']],
    #               ax1["D"], 'FMS Mode')

    loopTime = sensorsDf[['Timestamp', 'IMU Yaw Angle (deg)']].dropna()
    loopTime = loopTime.loc[loopTime['Timestamp'] >= 10.0]['Timestamp']
    loopTime = 1000 * (loopTime - loopTime.shift(-1))
    __PlotHistogram(loopTime, ax2, 'Loop Time (ms)')
    plt.tight_layout()
    plt.show()


def __PlotSignals(module, axis, title):
    module.plot(ax=axis, x='Timestamp', linestyle='--',
                marker='o', title=title)
    axis.grid()


def __PlotHistogram(module, axis, title):
    stat, p = shapiro(module.dropna())
    garbage = module.loc[abs(module) >= 21.0]
    garbageTime = 100 * garbage.size / module.size

    #print('Statistics=%.3f, p=%.5f' % (stat, p))
    alpha = 0.05  # 95% confidence
    if p > alpha:
        txt = 'Gaussian (fail to reject H0), p = %.3f\n %.1f%% loops > 5%% error' % (
            p, garbageTime)
    else:
        txt = 'Not Gaussian (reject H0), p = %.3f\n %.1f%% loops > 5%% error' % (
            p, garbageTime)

    module.plot(kind='hist', ax=axis, bins=range(
        int(np.floor(module.min())), int(np.ceil(module.max())) + 1, 1),
        title=title, legend=True)
    axis.legend([txt])


df = pd.read_csv(
    r"C:\Users\ejmcc\Documents\GIT Projects\Data-Log-Analysis\logs\FRC_20221116_013534.csv")
# r"C:\Users\ejmcc\Documents\GIT Projects\Data-Log-Analysis\logs\FRC_20221116_013024.csv")
# r"C:\Users\ejmcc\Documents\GIT Projects\Data-Log-Analysis\logs\FRC_20221116_012513.csv")
# r"C:\Users\ejmcc\Documents\GIT Projects\Data-Log-Analysis\logs\FRC_20221116_012152.csv")
# r"C:\Users\ejmcc\Documents\GIT Projects\Data-Log-Analysis\logs\FRC_20221116_011927.csv")
# r"C:\Users\ejmcc\Documents\GIT Projects\Data-Log-Analysis\logs\FRC_20221116_011621.csv")
# r"C:\Users\ejmcc\Documents\GIT Projects\Data-Log-Analysis\logs\FRC_20221116_011206.csv")


Test(df)
