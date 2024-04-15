import pandas as pd
import numpy as np
from csv import DictWriter
from catboost import CatBoostClassifier
from regmod import RegModel
import streamlit as st


df_error = pd.read_csv('error.csv', index_col=0)


def limits(expected_values: pd.Series = pd.Series()) -> pd.Series:
    """
    Get The Distance between expected values and its limits
    -------------------------------------------------------
    -------------------------------------------------------
    Args:
    -----
       expected_value: (pandas Series)

    -------------------------------------------------------
    Returns:
    --------
       Series of distances

    """

    ls = []
    # st.write(expected_values.values)
    if len(expected_values) > 0:
        for i in list(expected_values.values):
            distance = 2 * df_error.loc[np.ceil(i), 'stdv']
            ls.append(distance)

    return pd.Series(ls)


def place_order(order):
    headers = [
        'Id', 'City', 'Date', 'Weight', 'Carrier', 'Estimated Duration', 'Delivered']
    df = pd.DataFrame(columns=headers)
    df.loc[0] = [*order, False]
    df.to_csv('orders.csv', mode='a', index=False, header=False)


df = pd.read_csv('constraints.csv')
model = CatBoostClassifier()

model.load_model("model")


def predict(display=False, features: dict = {}):

    available_carriers = list(
        df[(df['Weight (kg)'] >= features['weight']) & (df[features['city']] == 1)]['carrier'].values)

    if len(available_carriers) > 0:
        data = pd.DataFrame()
        data['carriers'] = available_carriers

        prediction = model.predict([
            [i, features['city'], features['weight'], features['start_date'].year, features['start_date'].month, features['start_date'].day, features['start_date'].weekday()] for i in available_carriers
        ])
        data['class'] = prediction
        data = data[data['class'] == prediction.min(
        )].reset_index().drop('index', axis=1)

        data['expected time'] = RegModel(
            data['carriers'], features['city'], features['weight'], features['start_date'])

        data = data.sort_values('expected time')
        data.columns = ['Carrier', 'class', 'Time (days)']

        if display:

            st.success(
                f":dart: The Best Carrier for this Order is: ({data.iloc[0,0]})")
            st.dataframe(data,
                         use_container_width=True)
            st.snow()
        return data.iloc[0, 0], data.iloc[0, -1]

    else:
        st.warning(
            f"We don't have a carrier for shipping from {features['city']} with order weight {features['weight']} kg So We released city Constraint"
        )

        available_carriers = list(
            df[(df['Weight (kg)'] >= features['weight'])]['carrier'].values)
        if len(available_carriers) == 1:
            st.info(
                f"We Only Have Carrier {available_carriers[0]} for This Weight")

            return available_carriers[0], RegModel(available_carriers, features['city'], features['weight'], features['start_date'])

        elif len(available_carriers) == 0:
            st.info(
                "Even after releasing, We don't have Carrier for this special needs")
            return None, None

        else:
            if display:
                st.info(
                    f"Available Carriers: {' - '.join(available_carriers)}")

            data = pd.DataFrame()
            data['carriers'] = available_carriers

            prediction = model.predict([
                [i, features['city'], features['weight'], features['start_date'].year, features['start_date'].month, features['start_date'].day, features['start_date'].weekday()] for i in available_carriers
            ])

            data['class'] = prediction
            data = data[data['class'] == prediction.min(
            )].reset_index().drop('index', axis=1)

            data['expected time'] = RegModel(
                data['carriers'], features['city'], features['weight'], features['start_date'])

            data = data.sort_values('expected time')

            data.columns = ['Carrier', 'class', 'Time (days)']
            # st.write(data[data['preds'] == prediction.min()].reset_index())
            if display:
                st.success(
                    f":dart: The Best Carrier for this Order is: ({data.iloc[0,0]})")

                st.dataframe(data)
            return data.iloc[0, 0], data.iloc[0, -1]
