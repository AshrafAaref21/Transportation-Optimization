import pandas as pd
import numpy as np
from catboost import CatBoostClassifier
from regmod import RegModel
import streamlit as st


df_error = pd.read_csv('error.csv', index_col=0)
df_orders = pd.read_csv('orders.csv')
df_constraints = pd.read_csv('constraints.csv', index_col='carrier')

df = pd.read_csv('constraints.csv')
model = CatBoostClassifier()

model.load_model("model")


def limits(expected_values: pd.Series = pd.Series()) -> pd.Series:
    """
    Get The Distance between expected values and its limits

    -------------------------------------------------------
    Args:

       expected_value: (pandas Series)

    -------------------------------------------------------
    Returns:

       Series of distances

    """

    ls = []
    # st.write(expected_values.values)
    if len(expected_values) > 0:
        for i in list(expected_values.values):
            distance = 2 * df_error.loc[np.ceil(i), 'stdv']
            ls.append(distance)

    return pd.Series(ls)


def get_orders_constraint(carriers):
    """
    Filter Function to get The list of carriers by its order constraints

    -------------------------------------------------------
    Args:

       carriers: (List)

    -------------------------------------------------------
    Returns:

       Filtered list of available Carriers

    """

    new_list_of_carriers = []
    for carrier in carriers:
        if len(df_orders[(df_orders['Delivered'] == False)
                         & (df_orders['Carrier'] == carrier)]) < df_constraints.loc[carrier, 'Num Orders']:
            new_list_of_carriers.append(carrier)
    return new_list_of_carriers


def place_order(order):
    """
    Place an order Method

    -------------------------------------------------------

    Args:

       order: (List)

    -------------------------------------------------------

    """
    headers = [
        'Id', 'City', 'Date', 'Weight', 'Carrier', 'Estimated Duration', 'Delivered', 'Actual Duration']
    df = pd.DataFrame(columns=headers)
    if order[0] == 'Select ID':
        pass
    else:
        df.loc[0] = [*order, False, np.nan]
        df.to_csv('orders.csv', mode='a', index=False, header=False)


def predict(display: bool = False, features: dict = {}) -> list[str, float]:
    """
    Predicition Cycle Function.

    -------------------------------------------------------
    Args:

       display: (Boolean) -> Display the out prediction in the UI, or not.
       features: (Dictionary) -> Order Features.

    -------------------------------------------------------
    Returns:

       Predicted Order Class and Delivery Duration.

    """
    available_carriers = list(
        df_constraints[(df_constraints['Weight (kg)'] >= features['weight']) & (df_constraints[features['city']] == 1)].index)

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
        data['carriers'] = data['carriers'].map(carrier_map(mapping=True))
        data.columns = ['Carrier', 'class', 'Estimated Duration (Days)']
        data.index = range(1, len(data)+1)

        if display:

            st.success(
                f":dart: The Best Carrier for this Order is: ({data.iloc[0,0]})")
            st.dataframe(data.drop('class', axis=1),
                         use_container_width=True)

        return data.iloc[0, 0], data.iloc[0, -1]

    else:
        st.warning(
            f"We don't have a carrier for shipping from {features['city']} with order weight {features['weight']} kg So We released city Constraint"
        )

        available_carriers = list(
            df_constraints[(df_constraints['Weight (kg)'] >= features['weight'])].index)

        if len(available_carriers) == 1:
            st.info(
                f"We Only Have Carrier {carrier_map(available_carriers[0])} for This Weight")

            return carrier_map(available_carriers[0]), RegModel(available_carriers, features['city'], features['weight'], features['start_date'])

        elif len(available_carriers) == 0:
            st.info(
                "Even after releasing, We don't have Carrier for this special needs")
            return None, None

        else:
            if display:
                st.info(
                    f"Available Carriers: {' - '.join([carrier_map(i) for i in available_carriers])}")

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

            data['carriers'] = data['carriers'].map(carrier_map(mapping=True))

            data.columns = ['Carrier', 'class', 'Estimated Duration (Days)']
            data.index = range(1, len(data)+1)

            # st.write(data[data['preds'] == prediction.min()].reset_index())
            if display:
                st.success(
                    f":dart: The Best Carrier for this Order is: ({data.iloc[0,0]})")

                st.dataframe(data.drop('class', axis=1))
            return carrier_map(data.iloc[0, 0]), data.iloc[0, -1]


def carrier_map(carrier: str = '', mapping=False):
    """
    Mapping Carrier Name to get the actual carrier name.

    -------------------------------------------------------
    Args:

       carrier: (str) -> Carrier Symbol.
       mapping: (Dictionary) -> Return the whole dictionary of Carriers name and its symbol or just the given carrier name.

    -------------------------------------------------------
    Returns:

       Mapped Carriers.

    """

    dic = {
        "A": "Aramex",
        "B":
            "LaBaih",
            "C":
            "Tamex",
            "D":
            "Aymakan",
            "E":
            "Smsa",
            "F":
            "FDA",
            "G":
            "Mkhdoom",
            "H":
            "Wadha",
            "I":
            "Kudhha",
            "J":
            "Mahmoul",
            "K":
            "Jones",
            "L":
            "Lastpoint",
            "M":
            "Naqel",
            "N":
            "MORA",
            "O":
            "UPS",
            "P":
            "Weenk",
            "Q":
            "Aja",
            "R":
            "IMile",
            "S":
            "JandT",
            "T":
            "Pick",
            "U":
            "BARQ",
            "V":
            "Onway",
            "W":
            "Flow",
            "X":
            "SPL",
            "Y":
            "R2",
            "Z":
            "Shipa",
            "AA":
            "Nashmi",
            "BB":
            "Roz",
            "CC":
            "SHL",
            "DD":
            "SMB",
    }

    if mapping:
        return dic

    return dic[carrier]


if __name__ == '__main__':
    print(carrier_map("A"))
