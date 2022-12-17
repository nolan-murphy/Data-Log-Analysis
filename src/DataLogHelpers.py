import pandas as pd


def GetStringColumn(df, base, telemetry):
    if base == '':
        col_df = df.loc[df['Name'] == telemetry].copy()
    else:
        col_df = df.loc[df['Name'] == base+' '+telemetry].copy()
    col_df[telemetry] = col_df["Value"]
    col_df = col_df.drop(["Name", "Value"], axis=1)
    return col_df


def GetBooleanColumn(df, base, telemetry, scaling=1.0):
    col_df = df.loc[df['Name'] == base+' '+telemetry].copy()
    col_df[telemetry] = col_df['Value'].replace(
        {"true": 1.0*scaling, "false": 0.0})
    col_df = col_df.drop(["Name", "Value"], axis=1)
    return col_df


def GetFloatColumn(df, base, telemetry):
    if base == '':
        col_df = df.loc[df['Name'] == telemetry].copy()
    else:
        col_df = df.loc[df['Name'] == base+' '+telemetry].copy()
    col_df[telemetry] = pd.to_numeric(col_df["Value"])
    col_df = col_df.drop(["Name", "Value"], axis=1)
    return col_df


def VerifyInput(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("expected a pandas dataframe input")
    if len(df.columns) != 3:
        raise AttributeError("expected exactly 3 columns")
    if "Timestamp" not in df.columns:
        raise AttributeError("missing column: Timestamp")
    if "Name" not in df.columns:
        raise AttributeError("missing column: Name")
    if "Value" not in df.columns:
        raise AttributeError("missing column: Value")
