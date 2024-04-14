import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from catboost import CatBoostClassifier
from PIL import Image

from regmod import RegModel
from utils import limits


model = CatBoostClassifier()

model.load_model("model")

# open Logo file
img = Image.open("logo.png")
img = img.resize((70, 70))
ksa = Image.open('ksa.png').resize((100, 100))
# Set up the page configuration
st.set_page_config(
    page_title="Carr Co.",
    page_icon=img,
    layout="wide",
)


activities = ['Model Run', 'Model Constraints', 'Model Details']

option = st.sidebar.selectbox('Select The Activity Option', activities)

# Open Constraints File
df = pd.read_csv('constraints.csv')


if option == 'Model Run':
    # Page Header
    col_1, col_2 = st.columns([6, 1])
    with col_1:
        st.title(":coffee: Get The Perfect Carrier For The Shippments")
    with col_2:
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
    weight = st.number_input('Input Order Weight (gm)', value=1.) / 1000

    st.divider()

    # Initial Predictions button
    btn = st.button('Start',
                    type='primary', use_container_width=True)

    if btn:
        available_carriers = list(
            df[(df['Weight (kg)'] >= weight) & (df[city] == 1)]['carrier'].values)
        # st.write(available_carriers)
        # RegModel(available_carriers, city, weight, start_date)

        if len(available_carriers) > 0:
            data = pd.DataFrame()
            data['carriers'] = available_carriers

            prediction = model.predict([
                [i, city, weight, start_date.year, start_date.month, start_date.day, start_date.weekday()] for i in available_carriers
            ])
            data['class'] = prediction
            data = data[data['class'] == prediction.min(
            )].reset_index().drop('index', axis=1)

            data['expected time'] = RegModel(
                data['carriers'], city, weight, start_date)
            # data['upper limit'] = data['expected time'] + \
            #     limits(data['expected time'])
            # data['lower limit'] = data['expected time'] - \
            #     limits(data['expected time'])
            # data['lower limit'] = data['lower limit'].apply(
            #     lambda x: x if x > 0 else 0.)

            data = data.sort_values('expected time')
            data.columns = ['Carrier', 'class', 'Time (days)']

            st.success(
                f":dart: The Best Carrier for this Order is: ({data.iloc[0,0]})")
            st.dataframe(data.reset_index(),
                         use_container_width=True)
            st.snow()

        else:
            st.warning(
                f"We don't have a carrier for shipping from {city} with order weight {weight} kg So We released city Constraint"
            )

            available_carriers = list(
                df[(df['Weight (kg)'] >= weight)]['carrier'].values)
            if len(available_carriers) == 1:
                st.info(
                    f"We Only Have Carrier {available_carriers[0]} for This Weight")

            elif len(available_carriers) == 0:
                st.info(
                    "Even after releasing, We don't have Carrier for this special needs")

            else:
                st.info(
                    f"Available Carriers: {' - '.join(available_carriers)}")

                data = pd.DataFrame()
                data['carriers'] = available_carriers

                prediction = model.predict([
                    [i, city, weight, start_date.year, start_date.month, start_date.day, start_date.weekday()] for i in available_carriers
                ])

                data['class'] = prediction
                data = data[data['class'] == prediction.min(
                )].reset_index().drop('index', axis=1)

                data['expected time'] = RegModel(
                    data['carriers'], city, weight, start_date)

                # data['upper limit'] = data['expected time'] + \
                #     limits(data['expected time'])
                # data['lower limit'] = data['expected time'] - \
                #     limits(data['expected time'])
                # data['lower limit'] = data['lower limit'].apply(
                #     lambda x: x if x > 0 else 0.)

                data = data.sort_values('expected time')

                data.columns = ['Carrier', 'class', 'Time (days)']
                # st.write(data[data['preds'] == prediction.min()].reset_index())
                st.success(
                    f":dart: The Best Carrier for this Order is: ({data.iloc[0,0]})")
                st.dataframe(data)


elif option == 'Model Constraints':
    # Page Header

    st.title(":sparkles: Model Constraints")
    st.divider()
    df['Weight (kg)'] = np.ceil(df['Weight (kg)'])
    st.dataframe(df, use_container_width=True)


else:
    st.title(":ocean: Project Flowchart")
    st.divider()
    img = Image.open("Flowchart.png")
    st.image(img, use_column_width=True)
