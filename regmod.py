import pandas as pd
from datetime import datetime
import xgboost as xgb
import streamlit as st


def RegModel(available_carriers: list,
             city: str,
             weight: float,
             start_date: datetime
             ):

    df_avail = pd.DataFrame()
    df_avail['Carrier'] = available_carriers
    df_avail['City'] = city
    df_avail['Weight'] = weight
    df_avail['Year'] = start_date.year
    df_avail['Month'] = start_date.month
    df_avail['Day'] = start_date.day
    df_avail['DayOfWeek'] = start_date.weekday()

    df_avail['Carrier'] = df_avail['Carrier'].astype("category")
    df_avail['City'] = df_avail['City'].astype("category")

    df_avail['Year'] = df_avail['Year'].astype("category")
    df_avail['Month'] = df_avail['Month'].astype("category")
    df_avail['Day'] = df_avail['Day'].astype("category")
    df_avail['DayOfWeek'] = df_avail['DayOfWeek'].astype("category")

    model2 = xgb.XGBRegressor()
    model2.load_model("reg_model.json")

    df_avail['preds'] = model2.predict(df_avail)

    return df_avail['preds'].values
