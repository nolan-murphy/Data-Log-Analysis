import math
import DataLogHelpers as dlh
import pandas as pd
import matplotlib.pyplot as plt


def PlotSwerveModuleHoming(df):
    """Process the telemetry for swerve module homing analysis.

    This function will take the input pandas dataframe (constructed from the WPILib
    Data Log Tool) and filter out all of the telemetry unrelated to the swerve
    module homing routine.

    Args:
        df (:obj:`pd.DataFrame`): Pandas dataframe

    Returns:
        msg (str): Human readable string describing the exception.

    Raises:
        TypeError: if the input isn't a pandas dataframe
        AttributeError: if the dataframe columns aren't [Timestamp,Name,Value]
    """

    dlh.VerifyInput(df)

    baseKeys = ['FL', 'FR', 'RL', 'RR']

    telemetryKeys = {
        'Is Homed': 'boolean',
        'Turn Abs Enc (rad)': 'float',
        'Turn Position Error (rad)': 'float',
        'Turn Velocity Error (rad/s)': 'float',
        'Turn Feed-forward Output (V)': 'float',
        'Turn PID Output (V)': 'float',
    }

    dfs = {}
    for baseKey in baseKeys:
        dfs[baseKey] = pd.DataFrame(columns=["Timestamp"])
        for telemetryKey, telemetryType in telemetryKeys.items():
            if telemetryType == 'float':
                dfs[baseKey] = pd.merge(dfs[baseKey], dlh.GetFloatColumn(
                    df, baseKey, telemetryKey), how="outer", on=["Timestamp"])
            elif telemetryType == 'boolean':
                dfs[baseKey] = pd.merge(dfs[baseKey], dlh.GetBooleanColumn(
                    df, baseKey, telemetryKey), how="outer", on=["Timestamp"])

    fig, axes = plt.subplots(nrows=2, ncols=2, sharex=True)
    fig.suptitle('Swerve Modules - Homing', fontsize=18)
    plt.rc('legend', fontsize=6)
    dfs['FL'].plot(ax=axes[0, 0], x='Timestamp', linestyle='--',
                   ylim=(-0.1, 2*math.pi), marker='o', title='Front-Left')
    dfs['FR'].plot(ax=axes[0, 1], x='Timestamp', linestyle='--',
                   ylim=(-0.1, 2*math.pi), marker='o', title='Front-Right')
    dfs['RL'].plot(ax=axes[1, 0], x='Timestamp', linestyle='--',
                   ylim=(-0.1, 2*math.pi), marker='o', title='Rear-Left')
    dfs['RR'].plot(ax=axes[1, 1], x='Timestamp', linestyle='--',
                   ylim=(-0.1, 2*math.pi), marker='o', title='Rear-Right')
    plt.tight_layout()
    plt.show()
