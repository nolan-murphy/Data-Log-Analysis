from logging.config import stopListening
import pandas as pd
from pathlib import Path
import TelemetryKeys as tk


def GetStoplightMetricsAndCellEncodings(robotTelemetry: pd.DataFrame, telemetryKeys: dict):
    """ Process the device telemetry and generate the stoplight chart metrics.

    Args:
        robotTelemetry: Pandas dataframe of robot telemetry
        telemetryKeys:

    Returns:
        roboRioStoplightMetrics: List of strings which summarizes the stoplight metrics
        roboRioCellEncodings: List of stings which encode the cells for HTML styling

    Raises:
        TypeError: if the input isn't a pandas dataframe object

    """

    if not isinstance(robotTelemetry, pd.DataFrame):
        raise TypeError("expected a pandas dataframe input")

    stoplightMetrics = []
    cellEncodings = []
    deviceEncoding = 'device_ok'
    for key in telemetryKeys.keys():
        if telemetryKeys[key]['pFunc'] == None:
            stoplightMetrics.append(key)
            cellEncodings.append('metric_not_implemented')
        else:
            metrics, metricEncodings = telemetryKeys[key]['pFunc'](robotTelemetry, key, telemetryKeys[key]['cFunc'])
            stoplightMetrics.extend(metrics)
            cellEncodings.extend(metricEncodings)
            if 'metric_high_risk' in metricEncodings:
                deviceEncoding = 'device_high_risk'
            elif 'metric_low_risk' in metricEncodings and deviceEncoding == 'device_ok':
                deviceEncoding = 'device_low_risk'
    cellEncodings.insert(0, deviceEncoding)

    return stoplightMetrics, cellEncodings


def CreateStoplightSummary(telemetryFile: Path):
    """ Gather all of the device telemetry metrics and create a stoplight summary in HTML format.

    Args:
        telemetryFile: Absolute path to the robot telemetry file

    Returns:
        None

    Raises:
        TypeError: if the input isn't a pathlib Path object

    """

    if not isinstance(telemetryFile, Path):
        raise TypeError("expected a pathlib Path input")

    # Get the metrics from the varoious components
    robotTelemetry = pd.read_csv(str(telemetryFile))
    rrMetrics, rrCellEncodings = GetStoplightMetricsAndCellEncodings(robotTelemetry, tk.ROBORIO_TELEMETRY_KEYS)
    phMetrics, phCellEncodings = GetStoplightMetricsAndCellEncodings(robotTelemetry, tk.PH_TELEMETRY_KEYS)
    pdhMetrics, pdhCellEncodings = GetStoplightMetricsAndCellEncodings(robotTelemetry, tk.PDH_TELEMETRY_KEYS)

    # Build the stoplight summary and cell color dataframes
    rrMetrics.insert(0, r'<img src="..\resources\roborio.png">')
    phMetrics.insert(0, r'<img src="..\resources\pneumatics_hub.png">')
    pdhMetrics.insert(0, r'<img src="..\resources\power_distribution_hub.png">')
    stoplightSummary = pd.DataFrame({
        'RoboRIO': pd.Series(rrMetrics),
        'PH': pd.Series(phMetrics),
        'PDH': pd.Series(pdhMetrics)
    })

    # Style the cells based on their encodings
    s = stoplightSummary.style
    stoplightCellEncodings = pd.DataFrame({
        'RoboRIO': pd.Series(rrCellEncodings),
        'PH': pd.Series(phCellEncodings),
        'PDH': pd.Series(pdhCellEncodings)
    }, index=stoplightSummary.index, columns=stoplightSummary.columns[:len(stoplightSummary.columns)])

    stoplightSummary.fillna('', inplace=True)
    stoplightCellEncodings.fillna('metric_not_implemented', inplace=True)

    with open('..\..\output\stoplight.json', 'w') as f:
        f.write(stoplightSummary.to_json(orient='records', lines=True))

    s.set_table_styles([
        {'selector': 'thead', 'props': [('display', 'none')]},
        {'selector': '.device_ok', 'props': 'background-color: #00FF00;'},
        {'selector': '.device_high_risk', 'props': 'background-color: #FF0000;'},
        {'selector': '.device_low_risk', 'props': 'background-color: #FFFF00;'},
        {'selector': '.metric_not_implemented', 'props': 'text-align: right; color: #FFFFFF; background-color: #000000;'},
        {'selector': '.metric_ok', 'props': 'text-align: right; color: #00FF00; background-color: #000000;'},
        {'selector': '.metric_high_risk', 'props': 'text-align: right; color: #FF0000; background-color: #000000;'},
        {'selector': '.metric_low_risk', 'props': 'text-align: right; color: #FFFF00; background-color: #000000;'},
    ], overwrite=False)
    s.set_td_classes(stoplightCellEncodings)
    s.hide(axis="index")

    # Kludge to add a background color the HTML <body> tag
    html = s.to_html(escape=False)
    html_lines = html.splitlines()
    new_html_lines = html_lines[:1]
    new_html_lines.extend(['body {', '  background-color: #444444;', '}'])
    new_html_lines.extend(html_lines[1:])

    # Write the HTML to a file for viewing
    with open(r'..\..\output\stoplight_robot.html', 'w') as f:
        f.write("\n".join(new_html_lines))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("telemetryfile")
    args = parser.parse_args()
    telemetryFile = Path(args.telemetryfile)
    if not telemetryFile.is_file():
        raise OSError(2, 'File not found', telemetryFile)
    CreateStoplightSummary(telemetryFile)
