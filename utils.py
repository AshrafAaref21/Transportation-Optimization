import pandas as pd
import numpy as np
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
