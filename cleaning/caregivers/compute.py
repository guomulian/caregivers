import numpy as np
import pandas as pd


def los_hadm(df: pd.DataFrame) -> pd.DataFrame:
    df["LOS_HADM"] = df["DISCHTIME"].subtract(df["ADMITTIME"]) / np.timedelta64(1, "D")
    return df
    
    
def admission_age(df: pd.DataFrame) -> pd.DataFrame:
    df["ADMISSION_AGE"] = df["ADMITTIME"].subtract(df["DOB"]) / np.timedelta64(1, "Y")
    return df


def time_to_death(df: pd.DataFrame) -> pd.DataFrame:
    df["DAYS_TO_DEATH_HADM"] = df["DOD"].subtract(df["ADMITTIME"]) / np.timedelta64(1, "D")
    df["DAYS_TO_DEATH_ICU"] = df["DOD"].subtract(df["OUTTIME"]) / np.timedelta64(1, "D")
        
    # exclude rows with missing DOD info (so mortality values are NA rather than False)
    days_to_death_hadm = df[df["DAYS_TO_DEATH_HADM"].notna()]["DAYS_TO_DEATH_HADM"]
    days_to_death_icu = df[df["DAYS_TO_DEATH_ICU"].notna()]["DAYS_TO_DEATH_ICU"]    
    
    df["MORTALITY_3MO_FROM_HADM_ADMIT"] = days_to_death_hadm < 90
    df["MORTALITY_1Y_FROM_HADM_ADMIT"] = days_to_death_hadm < 365
    df["MORTALITY_6MO_FROM_ICU_OUT"] = days_to_death_icu < 180

    return df


def time_to_vent(df: pd.DataFrame) -> pd.DataFrame:
    df["VENT_TIME_FROM_HADM"] = df["STARTTIME"].subtract(df["ADMITTIME"]) / np.timedelta64(1, "h")
    df["VENT_TIME_FROM_ICU"] = df["STARTTIME"].subtract(df["INTIME"]) / np.timedelta64(1, "h")

    df["VENT_FIRST_48_HADM"] = df["VENT_TIME_FROM_HADM"] < 48
    df["VENT_FIRST_48_ICU"] = df["VENT_TIME_FROM_ICU"] < 48
    
    return df
