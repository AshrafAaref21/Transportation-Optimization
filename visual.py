import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def chart(df: pd.DataFrame):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Date'] >= (datetime.now() - timedelta(30))]
    df = df[['Date', 'Carrier', 'Estimated Duration', 'Weight', 'Delivered']].groupby(['Date', 'Carrier', 'Delivered']).agg(
        num_orders=('Estimated Duration', len),
        total_duration=('Estimated Duration', sum),
        mean_order_weight=('Weight', np.mean),
    ).reset_index()

    # Plot!
    fig = px.bar(
        df,
        x='Date',
        y='num_orders',
        color='Carrier',
        pattern_shape='Delivered',
        pattern_shape_sequence=['.', ''],
        labels={'num_orders': 'Count Of Orders',
                # 'Carrier': '     Carrier',
                }
    )
    _, cl, _ = st.columns([2.5, 4, 2.5])

    with cl:
        st.subheader('The Carrier Orders in last 30 days')
    st.plotly_chart(fig,  use_container_width=True)
