import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from PIL import Image

from utils import place_order, predict
from visual import chart


# open Logo file
img = Image.open("logo.png").resize((100, 100))
ksa = Image.open('ksa.png').resize((70, 70))

# Set up the page configuration
st.set_page_config(
    page_title="Carr Co.",
    page_icon=img,
    layout="wide",
)


activities = ['Model Run', 'Model Constraints',
              'Model Details', 'Orders Dashboard']

option = st.sidebar.selectbox('Select The Activity Option', activities)

# Open Constraints File
df = pd.read_csv('constraints.csv')
df_orders = pd.read_csv('orders.csv')

if option == 'Model Run':
    # Page Header
    col_1, col_2 = st.columns([8, 1])
    with col_1:
        st.title(":coffee: Get The Perfect Carrier For The Shippments")
    with col_2:
        st.write('')
        st.image(ksa)

    # City Input
    city = st.selectbox('Choose Your City', [
        'Jeddah',
        'Riyadh',
        'Dammam',
        'Madinah',
        'Makkah'
    ])

    # Date Input
    start_date = st.date_input('Pickup Date',
                               value=datetime.today(),
                               )

    # Weight Input
    weight = st.number_input('Input Order Weight (gm)', value=0.) / 1000

    st.divider()
    disabled = weight == 0.
    col1, col2 = st.columns([1.5, 2])
    with col1:
        radio = st.radio(
            'Options', ['Show Prediction', 'Place Order'], index=0)
    # Initial Predictions button
    with col2:
    
        if radio == 'Show Prediction':
            st.write('')
            st.write('')
            text = 'Start'
            if disabled:
                text = 'Select Order Features'
            btn = st.button(text,
                            type='primary', use_container_width=True, disabled=disabled)

        else:
            text = 'Order'
            if disabled:
                text = 'Select Order Features'
            order_id = st.number_input('Input Order ID: ', value=1)
            btn = st.button(text,
                            type='primary', use_container_width=True, disabled=disabled)

    # st.write(get_orders_constraint('A'))

    if btn:
        st.divider()
        if radio == 'Show Prediction':
            if weight > 0:
                predict(display=True, features={
                    'city': city,
                    'weight': weight,
                    'start_date': start_date
                })

            else:
                st.error('Please Select a valid Weight :name_badge:')

        else:
            if weight == 0:
                st.error('Please Select a valid Weight :name_badge:')
            else:
                carrier, time = predict(features={
                    'city': city,
                    'weight': weight,
                    'start_date': start_date
                })
                if carrier != None:

                    df_orders['Id'] = df_orders['Id'].astype(int)
                    if int(order_id) in df_orders['Id'].unique():
                        st.error('This Order is already exists :name_badge:')

                    else:
                        place_order(
                            [order_id, city, start_date, weight, carrier, time])
                        st.success('The Order\'s added now 	:new:')
                        st.snow()


elif option == 'Model Constraints':
    # Page Header

    st.title(":sparkles: Model Constraints")
    st.divider()
    df['Weight (kg)'] = np.ceil(df['Weight (kg)'])

    st.dataframe(df, use_container_width=True)

elif option == 'Orders Dashboard':
    st.title(":anchor: Orders Dashboard")
    st.divider()
    df_orders = pd.read_csv('orders.csv', index_col='Id')

    x = st.empty()

    x.dataframe(df_orders, use_container_width=True)
    st.divider()

    if st.checkbox('Deliver Order'):
        st.write('')

        if len(df_orders[df_orders['Delivered'] == False].index) > 0:

            order_id = st.selectbox(
                'Select Order ID: ', ['Select ID', *df_orders[df_orders['Delivered'] == False].index])
            st.write('')
            btn = st.button('Order',
                            type='primary', use_container_width=True, disabled=order_id == 'Select ID')
            if btn:

                df_orders.loc[order_id, 'Delivered'] = True
                df_orders.to_csv('orders.csv')

                st.success(
                    f"Well Done..! Order #{order_id} is delivered by Carrier {df_orders.loc[order_id,'Carrier']} within {int(np.ceil(df_orders.loc[order_id,'Estimated Duration']))} days")

                df_orders = pd.read_csv('orders.csv', index_col='Id')
                x.dataframe(df_orders, use_container_width=True,)

        else:
            st.info('All The Orders has been delivered :white_check_mark:')

    st.write('')
    if st.checkbox('Visualize Orders'):

        chart(df_orders)

else:
    st.title(":ocean: Project Flowchart")
    st.divider()
    img = Image.open("Flowchart.png")
    st.image(img, use_column_width=True)
