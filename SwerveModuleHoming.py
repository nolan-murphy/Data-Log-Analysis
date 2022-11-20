#import math
import DataLogHelpers as dlh
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import shapiro
#from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)


def PlotSwerveModuleHoming(df):
    """Process the telemetry for swerve module homing analysis.

    This function will take the input pandas dataframe (constructed from the WPILib
    Data Log Tool) and filter out all of the telemetry unrelated to the swerve
    module homing routine.

    The `baseKeys` and `telemetryKeys` members need to match the key's from the actual
    robot code. In other words, if the code changes these need to also change. TODO: is
    there a better way to manage this?? Perhaps link and scrape the actual robot code.

    The non-homing data is filtered out using the `Is Homed` and `Turn Position Setpoint
    (rad)` keys. It is assumed that the `Is Homed` key value is initialized to false. The
    `Turn Position Setpoint (rad)` key value of 0 is filtered out. This will only become
    an issue if true absolute postion of the sensor is 0.0 radians.

    Args:
        df (:obj:`pd.DataFrame`): Pandas dataframe

    Returns:
        none

    Raises:
        TypeError: if the input isn't a pandas dataframe
        AttributeError: if the dataframe columns aren't [Timestamp,Name,Value]
    """

    dlh.VerifyInput(df)

    baseKeys = ['FL', 'FR', 'RL', 'RR']

    telemetryKeys = {
        'Is Homed': 'boolean',
        'Turn Abs Enc (rad)': 'float',
        'Turn Position Setpoint (rad)': 'float',
        'Turn Position Error (rad)': 'float',
        'Turn Velocity Setpoint (rad/s)': 'float',
        'Turn Velocity Error (rad/s)': 'float',
        'Turn Feed-forward Output (V)': 'float',
        'Turn PID Output (V)': 'float',
        # 'Turn Rel Enc (rad)': 'float',
        # 'Drive Rel Enc (mps)': 'float',
    }

    dfs = {}
    filteredDfs = {}
    for baseKey in baseKeys:
        dfs[baseKey] = pd.DataFrame(columns=["Timestamp"])

        # Get all of the columns of the telemetry keys
        for telemetryKey, telemetryType in telemetryKeys.items():
            if telemetryType == 'float':
                dfs[baseKey] = pd.merge(dfs[baseKey], dlh.GetFloatColumn(
                    df, baseKey, telemetryKey), how="outer", on=["Timestamp"])
            elif telemetryType == 'boolean':
                dfs[baseKey] = pd.merge(dfs[baseKey], dlh.GetBooleanColumn(
                    df, baseKey, telemetryKey), how="outer", on=["Timestamp"])

        # Remove timestamp ranges where the module isn't actively homing
        filteredDfs[baseKey] = pd.DataFrame()
        diff = dfs[baseKey]['Is Homed'].diff()
        diff = diff[abs(diff) == 1.0]
        for diffIdx, dfsIdx in enumerate(diff.index):
            if diff.iloc[diffIdx] == 1.0:
                endTimestamp = dfs[baseKey].iloc[dfsIdx]["Timestamp"]
                if filteredDfs[baseKey].empty:
                    startTimestamp = dfs[baseKey].loc[
                        (dfs[baseKey]['Timestamp'] < endTimestamp) &
                        (dfs[baseKey]['Turn Position Setpoint (rad)'] == 0.0)
                    ].tail(1)["Timestamp"].item()
                    filteredDfs[baseKey] = dfs[baseKey].loc[
                        (dfs[baseKey]['Timestamp'] >= startTimestamp) &
                        (dfs[baseKey]['Timestamp'] < endTimestamp)
                    ]
                else:
                    filteredDfs[baseKey] = pd.concat([
                        filteredDfs[baseKey],
                        dfs[baseKey].loc[
                            (dfs[baseKey]['Timestamp'] >= startTimestamp) &
                            (dfs[baseKey]['Timestamp'] < endTimestamp)
                        ]
                    ])
            elif diff.iloc[diffIdx] == -1.0:
                startTimestamp = dfs[baseKey].iloc[dfsIdx]["Timestamp"]
            else:
                raise ValueError("Expected 1.0 or -1.0 for Is Homed")

        # Handle the case where the module never completes homing
        if filteredDfs[baseKey].empty:
            startTimestamp = dfs[baseKey].loc[
                (dfs[baseKey]['Timestamp'] < endTimestamp) &
                (dfs[baseKey]['Turn Position Setpoint (rad)'] == 0.0)
            ].tail(1)["Timestamp"].item()
            filteredDfs[baseKey] = dfs[baseKey].loc[
                (dfs[baseKey]['Timestamp'] >= startTimestamp)
            ]

        # Drop any remaining unwanted columns
        filteredDfs[baseKey] = filteredDfs[baseKey].drop(['Is Homed'], axis=1)

    # Plot the data
    fig1, axes1 = plt.subplots(nrows=2, ncols=2)
    fig1.suptitle('Swerve Modules - Homing Signals', fontsize=18)
    fig2, axes2 = plt.subplots(nrows=2, ncols=2)
    fig2.suptitle('Swerve Modules - Position Error Histograms', fontsize=18)
    fig3, axes3 = plt.subplots(nrows=2, ncols=2)
    fig3.suptitle('Swerve Modules - Velocity Error Histograms', fontsize=18)
    plt.rc('legend', fontsize=6)
    PlotSignals(filteredDfs['FL'], axes1[0, 0], 'Front-Left')
    PlotSignals(filteredDfs['FR'], axes1[0, 1], 'Front-Right')
    PlotSignals(filteredDfs['RL'], axes1[1, 0], 'Rear-Left')
    PlotSignals(filteredDfs['RR'], axes1[1, 1], 'Rear-Right')
    PlotHistograms(
        filteredDfs['FL']['Turn Position Error (rad)'], axes2[0, 0], 'Front-Left')
    PlotHistograms(
        filteredDfs['FR']['Turn Position Error (rad)'], axes2[0, 1], 'Front-Right')
    PlotHistograms(
        filteredDfs['RL']['Turn Position Error (rad)'], axes2[1, 0], 'Rear-Left')
    PlotHistograms(
        filteredDfs['RR']['Turn Position Error (rad)'], axes2[1, 1], 'Rear-Right')
    PlotHistograms(
        filteredDfs['FL']['Turn Velocity Error (rad/s)'], axes3[0, 0], 'Front-Left')
    PlotHistograms(
        filteredDfs['FR']['Turn Velocity Error (rad/s)'], axes3[0, 1], 'Front-Right')
    PlotHistograms(
        filteredDfs['RL']['Turn Velocity Error (rad/s)'], axes3[1, 0], 'Rear-Left')
    PlotHistograms(
        filteredDfs['RR']['Turn Velocity Error (rad/s)'], axes3[1, 1], 'Rear-Right')
    plt.tight_layout()
    plt.show()


def PlotSignals(module, axis, title):
    # module.plot(ax=axis, x='Timestamp', linestyle='--', secondary_y=[
    #             'Turn Velocity Setpoint (rad/s)', 'Turn Velocity Error (rad/s)',
    #             'Turn PID Output (V)', 'Turn Feed-forward Output (V)'], marker='o', title=title)
    module.plot(ax=axis, x='Timestamp', linestyle='--',
                marker='o', title=title)
    # axis.set_yticks(np.arange(0, 6.5, step=0.5))
    # axis.right_ax.set_yticks(np.arange(0, 13, step=1))

    # axis.yaxis.set_major_locator(MultipleLocator(1))
    # axis.yaxis.set_major_formatter('{x:.0f}')
    # axis.yaxis.set_minor_locator(AutoMinorLocator(5))
    axis.grid()


def PlotHistograms(module, axis, title):
    stat, p = shapiro(module.dropna())
    # print('Statistics=%.3f, p=%.3f' % (stat, p))
    alpha = 0.05
    if p > alpha:
        txt = 'Gaussian (fail to reject H0), p = %.3f' % (p)
        # print('Sample looks Gaussian (fail to reject H0)')
    else:
        txt = 'Not Gaussian (reject H0), p = %.3f' % (p)
        # print('Sample does not look Gaussian (reject H0)')
    module.plot(kind='hist', ax=axis, bins=10, title=title, legend=True)
    axis.legend([txt])


df = pd.read_csv(
    r"C:\Users\ejmcc\Documents\GIT Projects\Data-Log-Analysis\logs\FRC_20221116_013534.csv")
PlotSwerveModuleHoming(df)
