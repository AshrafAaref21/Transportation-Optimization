import pandas as pd
from datetime import datetime
import xgboost as xgb


city_map = {'Jeddah': 0, 'Madinah': 1,
            'Makkah': 2, 'Riyadh': 3, 'Dammam': 4}

carrier_map = {'A': 0,
               'B': 1,
               'C': 2,
               'D': 3,
               'E': 4,
               'F': 5,
               'G': 6,
               'H': 7,
               'I': 8,
               'J': 9,
               'K': 10,
               'L': 11,
               'M': 12,
               'N': 13,
               'O': 14,
               'P': 15,
               'Q': 16,
               'R': 17,
               'S': 18,
               'T': 19,
               'U': 20,
               'V': 21,
               'W': 22,
               'X': 23,
               'Y': 24,
               'Z': 25,
               'AA': 26,
               'BB': 27,
               'CC': 28,
               'DD': 29}


def treat(x):
    if x < 0:
        return 0.0015
    else:
        return x


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
    df_avail['Carrier'] = df_avail['Carrier'].map(carrier_map)
    df_avail['City'] = df_avail['City'].astype("category")
    df_avail['City'] = df_avail['City'].map(city_map)

    df_avail['Year'] = df_avail['Year'].astype("category")
    df_avail['Month'] = df_avail['Month'].astype("category")
    df_avail['Day'] = df_avail['Day'].astype("category")
    df_avail['DayOfWeek'] = df_avail['DayOfWeek'].astype("category")

    model2 = xgb.XGBRegressor()
    model2.load_model("reg_model.json")

    df_avail['preds'] = model2.predict(df_avail)
    df_avail['preds'] = df_avail['preds'].apply(treat)

    return df_avail['preds'].values
