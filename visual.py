import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def chart(df: pd.DataFrame) -> st.plotly_chart:
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
        pattern_shape_sequence=['', '.'],
        labels={'num_orders': 'Count Of Orders',
                # 'Carrier': '     Carrier',
                }
    )
    _, cl, _ = st.columns([2.5, 4, 2.5])

    with cl:
        st.subheader('The Carrier Orders in last 30 days')
    st.plotly_chart(fig,  use_container_width=True)


def speed(df: pd.DataFrame) -> st.plotly_chart:

    tab1, tab2 = st.tabs(["Estimated Duration", "Actual Duration"])

    with tab1:
        df2 = df.copy()
        df2 = df2[['Carrier', 'Estimated Duration', 'City']
                  ].groupby(['Carrier', 'City']).mean().reset_index()

        fig = px.bar(
            df2,
            x='Carrier',
            y='Estimated Duration',
            color='City',
        )
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.write('')
        st.write('')
        df1 = df.copy()
        df1 = df1[df1['Delivered'] == True]
        df1 = df1[['Carrier', 'Actual Duration', 'City']
                  ].groupby(['Carrier', 'City']).mean().reset_index()

        fig = px.bar(
            df1,
            x='Carrier',
            y='Actual Duration',
            color='City',
        )
        st.plotly_chart(fig, use_container_width=True)


def scatter(df: pd.DataFrame) -> st.plotly_chart:
    # df['Delivered'] = df['Delivered'].replace({True: 1, False: 0})
    df = df[df['Delivered'] == True]
    fig = px.scatter(
        df,
        x='Weight',
        y='Actual Duration',
        color='Carrier',
    )
    st.plotly_chart(fig, use_container_width=True)


def performance(df: pd.DataFrame) -> st.plotly_chart:
    df = df[df['Delivered'] == True]
    df['Absolute Error'] = np.absolute(
        df['Estimated Duration'] - df['Actual Duration'])

    df = df[['Absolute Error', 'City', 'Carrier']].groupby(
        ['Carrier', 'City']).mean().reset_index()

    fig = px.bar(
        df,
        x='Carrier',
        y='Absolute Error',
        color='City',
    )

    _, cl, _ = st.columns([1, 4, 1])
    with cl:
        st.subheader('Model Mean Absolute Error For each Carrier in each City')
    st.plotly_chart(fig, use_container_width=True)
